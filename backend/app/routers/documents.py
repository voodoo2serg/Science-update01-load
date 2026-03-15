from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Document, User
from app.services.storage import save_upload

router = APIRouter(prefix='/documents', tags=['documents'])


@router.post('/upload')
def upload_document(
    user_id: str = Form(...),
    doc_type: str = Form('other'),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    generated_name, file_path, size_bytes = save_upload(file)
    doc = Document(
        user_id=user_id,
        filename=file.filename or generated_name,
        file_path=file_path,
        mime_type=file.content_type or 'application/octet-stream',
        size_bytes=size_bytes,
        doc_type=doc_type,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {'id': doc.id, 'filename': doc.filename, 'size_bytes': doc.size_bytes}
