from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ExpertiseRequest, User
from app.schemas import ExpertiseRequestIn

router = APIRouter(prefix='/expertise', tags=['expertise'])


@router.post('')
def create_expertise_request(payload: ExpertiseRequestIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    req = ExpertiseRequest(
        user_id=payload.user_id,
        request_type=payload.request_type,
        request_text=payload.request_text,
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return {'id': req.id, 'status': req.status}
