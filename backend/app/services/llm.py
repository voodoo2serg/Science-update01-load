from app.config import settings

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


DISCLAIMER = (
    '\n\nВажно: это только черновой каркас и методическая заготовка. '
    'Ее нельзя использовать как готовую научную работу без глубокой самостоятельной переработки.'
)


def _fallback(topic: str, title: str, draft_type: str) -> str:
    return (
        f'Название: {title}\n'
        f'Тип: {draft_type}\n'
        f'Тема: {topic}\n\n'
        '1. Проблема исследования\n'
        '2. Цель и 3-5 задач\n'
        '3. Гипотеза или научное предположение\n'
        '4. Предварительная структура\n'
        '5. Набор ключевых источников\n'
        '6. Риски для защиты и что проверить заранее\n'
        '7. План самостоятельной доработки материала автором'
        + DISCLAIMER
    )


def generate_safe_draft(topic: str, title: str, draft_type: str) -> str:
    if not settings.openai_api_key or OpenAI is None:
        return _fallback(topic, title, draft_type)

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f'''
Ты — академический консультант.
Нельзя писать готовую диссертацию, статью или раздел под ключ.
Нужно выдать только безопасный черновой каркас: структура, тезисы, вопросы для самопроверки,
рекомендации по литературе и логике аргументации.

Сформируй результат на русском языке.
Тип материала: {draft_type}
Заголовок: {title}
Тема: {topic}

Обязательно:
- не писать завершенный научный текст;
- не имитировать итоговую публикацию;
- дать 5-10 опорных источников по типам, без вымышленных DOI;
- завершить блоком "Что автор должен дописать сам".
'''
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.4,
    )
    content = response.choices[0].message.content or ''
    return content + DISCLAIMER
