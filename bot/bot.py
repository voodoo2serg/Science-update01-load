import asyncio
import logging

import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Профиль'), KeyboardButton(text='Запрос экспертизы')],
        [KeyboardButton(text='Сгенерировать черновик')],
    ],
    resize_keyboard=True,
)


async def ensure_user(message: Message):
    async with httpx.AsyncClient(timeout=20) as client:
        await client.post(
            f'{settings.backend_url}/users',
            json={
                'telegram_id': message.from_user.id,
                'full_name': message.from_user.full_name,
            },
        )


@dp.message(CommandStart())
async def start(message: Message):
    await ensure_user(message)
    await message.answer(
        'Добро пожаловать в Science Concierge. '
        'Это консультационный сервис сопровождения соискателя, а не генератор готовых научных работ.',
        reply_markup=menu,
    )


@dp.message(F.text == 'Профиль')
async def profile(message: Message):
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(f'{settings.backend_url}/users/by-telegram/{message.from_user.id}')
        if resp.status_code != 200:
            await message.answer('Профиль пока не найден.')
            return
        data = resp.json()
    await message.answer(
        f"ID: {data['id']}\n"
        f"ФИО: {data.get('full_name')}\n"
        f"Статус подписки: {data.get('subscription_status')}"
    )


@dp.message(F.text == 'Запрос экспертизы')
async def expertise_hint(message: Message):
    await message.answer('Отправьте сообщение в формате:\nэкспертиза: ваш вопрос')


@dp.message(F.text == 'Сгенерировать черновик')
async def draft_hint(message: Message):
    await message.answer('Отправьте сообщение в формате:\nчерновик: название | тема')


@dp.message(F.text.startswith('экспертиза:'))
async def expertise_create(message: Message):
    async with httpx.AsyncClient(timeout=20) as client:
        user = await client.get(f'{settings.backend_url}/users/by-telegram/{message.from_user.id}')
        if user.status_code != 200:
            await message.answer('Не удалось найти профиль.')
            return
        user_id = user.json()['id']
        text = message.text.split(':', 1)[1].strip()
        resp = await client.post(
            f'{settings.backend_url}/expertise',
            json={'user_id': user_id, 'request_type': 'generic', 'request_text': text},
        )
    await message.answer(f'Запрос на экспертизу создан: {resp.json()["id"]}')


@dp.message(F.text.startswith('черновик:'))
async def draft_create(message: Message):
    try:
        payload = message.text.split(':', 1)[1].strip()
        title, topic = [x.strip() for x in payload.split('|', 1)]
    except Exception:
        await message.answer('Неверный формат. Используйте: черновик: название | тема')
        return

    async with httpx.AsyncClient(timeout=60) as client:
        user = await client.get(f'{settings.backend_url}/users/by-telegram/{message.from_user.id}')
        if user.status_code != 200:
            await message.answer('Не удалось найти профиль.')
            return
        user_id = user.json()['id']
        resp = await client.post(
            f'{settings.backend_url}/payments/activate-demo',
            json={'user_id': user_id, 'plan_name': 'candidate_5m'},
        )
        if resp.status_code not in {200, 201}:
            logger.warning('Demo activation failed: %s', resp.text)
        resp = await client.post(
            f'{settings.backend_url}/drafts/generate',
            json={'user_id': user_id, 'title': title, 'topic': topic, 'draft_type': 'article_plan'},
        )
    if resp.status_code != 200:
        await message.answer(f'Ошибка: {resp.text}')
        return
    await message.answer(resp.json()['content'][:4000])


@dp.message()
async def fallback(message: Message):
    await message.answer(
        'Доступные команды:\n'
        '- Профиль\n'
        '- Запрос экспертизы\n'
        '- Сгенерировать черновик\n\n'
        'Или используйте форматы:\n'
        'экспертиза: ваш вопрос\n'
        'черновик: название | тема'
    )


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
