from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, SessionLocal, engine
from app.models import SubscriptionPlan
from app.routers import documents, drafts, expertise, feedback, health, payments, users


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(SubscriptionPlan).count():
            db.add_all(
                [
                    SubscriptionPlan(
                        name='candidate_5m',
                        description='Кандидатский минимум, 5 месяцев',
                        duration_months=5,
                        price_rub=49000,
                    ),
                    SubscriptionPlan(
                        name='full_9m',
                        description='Полный цикл, 9 месяцев',
                        duration_months=9,
                        price_rub=99000,
                    ),
                ]
            )
            db.commit()
    finally:
        db.close()
    yield


app = FastAPI(title=settings.app_name, version='0.2.0', lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(health.router)
app.include_router(users.router)
app.include_router(drafts.router)
app.include_router(documents.router)
app.include_router(expertise.router)
app.include_router(feedback.router)
app.include_router(payments.router)
