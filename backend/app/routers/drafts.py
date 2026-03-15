from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Draft, User
from app.schemas import DraftGenerateIn, DraftOut
from app.services.llm import PolicyError, generate_safe_draft
from app.services.subscription import has_active_subscription

router = APIRouter(prefix='/drafts', tags=['drafts'])


@router.post('/generate', response_model=DraftOut)
def generate_draft(payload: DraftGenerateIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not has_active_subscription(user):
        raise HTTPException(status_code=403, detail='Active subscription required')

    try:
        content = generate_safe_draft(payload.topic, payload.title, payload.draft_type)
    except PolicyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    draft = Draft(user_id=user.id, draft_type=payload.draft_type, title=payload.title, content=content)
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft
