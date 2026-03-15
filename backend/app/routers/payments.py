from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Payment, SubscriptionPlan, User
from app.schemas import PaymentActivateIn
from app.services.subscription import activate_plan

router = APIRouter(prefix='/payments', tags=['payments'])


@router.post('/activate-demo')
def activate_demo_subscription(payload: PaymentActivateIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.name == payload.plan_name).first()
    if not plan:
        raise HTTPException(status_code=404, detail='Plan not found')

    activate_plan(db, user, plan)
    payment = Payment(
        user_id=user.id,
        amount=plan.price_rub,
        status='succeeded',
        transaction_id='demo',
        provider='demo',
    )
    db.add(payment)
    db.commit()
    return {'status': 'ok', 'subscription_status': user.subscription_status}
