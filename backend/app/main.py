from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import Base, engine, SessionLocal
from app.models import SubscriptionPlan
from app.routers import health, users, drafts, documents, expertise, feedback, payments


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(SubscriptionPlan).count():
            db.add_all([
                SubscriptionPlan(name='candidate_5m', description='Кандидатский минимум, 5 месяцев', duration_months=5, price_rub=49000),
                SubscriptionPlan(name='full_9m', description='Полный цикл, 9 месяцев', duration_months=9, price_rub=99000),
            ])
            db.commit()
    finally:
        db.close()
    yield


app = FastAPI(title='Science Concierge MVP', version='0.1.0', lifespan=lifespan)
app.include_router(health.router)
app.include_router(users.router)
app.include_router(drafts.router)
app.include_router(documents.router)
app.include_router(expertise.router)
app.include_router(feedback.router)
app.include_router(payments.router)
