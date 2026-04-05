from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.academic_os import models as academic_os_models  # noqa: F401
from app.academic_os.bootstrap import ensure_bootstrap_data
from app.academic_os.router_service_layer import router as academic_os_v2_router
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
                        name="candidate_5m",
                        description="Кандидатский минимум, 5 месяцев",
                        duration_months=5,
                        price_rub=49000,
                    ),
                    SubscriptionPlan(
                        name="full_9m",
                        description="Полный цикл, 9 месяцев",
                        duration_months=9,
                        price_rub=99000,
                    ),
                ]
            )
            db.commit()

        ensure_bootstrap_data(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Science Concierge + Academic Research OS v2", version="0.3.0", lifespan=lifespan)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(drafts.router)
app.include_router(documents.router)
app.include_router(expertise.router)
app.include_router(feedback.router)
app.include_router(payments.router)
app.include_router(academic_os_v2_router)
