from pathlib import Path
from fastapi import UploadFile
from app.config import settings
import uuid


def save_upload(file: UploadFile) -> tuple[str, str]:
    Path(settings.storage_dir).mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename or '').suffix
    generated = f'{uuid.uuid4()}{ext}'
    path = Path(settings.storage_dir) / generated
    with path.open('wb') as f:
        f.write(file.file.read())
    return generated, str(path)
