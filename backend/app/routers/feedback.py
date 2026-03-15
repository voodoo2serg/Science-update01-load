from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import ChatHistory
from app.schemas import FeedbackIn

router = APIRouter(prefix='/feedback', tags=['feedback'])


@router.post('')
def set_feedback(payload: FeedbackIn, db: Session = Depends(get_db)):
    item = db.query(ChatHistory).filter(ChatHistory.id == payload.chat_id).first()
    if not item:
        raise HTTPException(status_code=404, detail='Chat record not found')
    item.rating = payload.rating
    db.add(item)
    db.commit()
    return {'status': 'updated'}
