from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import RegisterUserIn, UserOut

router = APIRouter(prefix='/users', tags=['users'])


@router.post('', response_model=UserOut)
def register_user(payload: RegisterUserIn, db: Session = Depends(get_db)):
    if payload.telegram_id:
        existing = db.query(User).filter(User.telegram_id == payload.telegram_id).first()
        if existing:
            return existing
    if payload.email:
        existing = db.query(User).filter(User.email == payload.email).first()
        if existing:
            return existing
    user = User(
        telegram_id=payload.telegram_id,
        email=payload.email,
        full_name=payload.full_name,
        scientific_field=payload.scientific_field,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/by-telegram/{telegram_id}', response_model=UserOut)
def get_by_telegram(telegram_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
