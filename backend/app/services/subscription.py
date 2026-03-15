from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import SubscriptionPlan, User


def has_active_subscription(user: User) -> bool:
    return bool(
        user.subscription_status == 'active'
        and user.subscription_end is not None
        and user.subscription_end > datetime.utcnow()
    )


def activate_plan(db: Session, user: User, plan: SubscriptionPlan) -> User:
    user.subscription_plan_id = plan.id
    user.subscription_status = 'active'
    user.subscription_end = datetime.utcnow() + timedelta(days=30 * plan.duration_months)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
