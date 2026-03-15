from pathlib import Path
import uuid

from fastapi import HTTPException, UploadFile

from app.config import settings


def save_upload(file: UploadFile) -> tuple[str, str, int]:
    ext = Path(file.filename or '').suffix.lower()
    if ext not in settings.allowed_extensions_set:
        raise HTTPException(status_code=400, detail='Unsupported file type')

    Path(settings.storage_dir).mkdir(parents=True, exist_ok=True)
    payload = file.file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(payload) > max_bytes:
        raise HTTPException(status_code=400, detail='File is too large')

    generated = f'{uuid.uuid4()}{ext}'
    path = Path(settings.storage_dir) / generated
    path.write_bytes(payload)
    return generated, str(path), len(payload)
