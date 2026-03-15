from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import ExpertiseRequest
from app.schemas import ExpertiseRequestIn

router = APIRouter(prefix='/expertise', tags=['expertise'])


@router.post('')
def create_expertise_request(payload: ExpertiseRequestIn, db: Session = Depends(get_db)):
    req = ExpertiseRequest(
        user_id=payload.user_id,
        request_type=payload.request_type,
        request_text=payload.request_text,
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return {'id': req.id, 'status': req.status}
