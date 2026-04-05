from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db

from . import schemas, service_layer

router = APIRouter(prefix="/academic-os-v2", tags=["academic-os-v2"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "module": "academic_os_v2"}


@router.get("/programs", response_model=list[schemas.ProgramOut])
def list_programs(db: Session = Depends(get_db)):
    return service_layer.list_programs(db)


@router.post("/programs", response_model=schemas.ProgramOut)
def create_program(payload: schemas.ProgramCreate, db: Session = Depends(get_db)):
    return service_layer.create_program(db, payload, owner_user_id="bootstrap-user")


@router.post("/programs/{program_id}/requirements")
def add_program_requirement(program_id: str, payload: schemas.ProgramRequirementCreate, db: Session = Depends(get_db)):
    program = service_layer.get_program(db, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    item = service_layer.create_program_requirement(db, program_id, payload)
    return {"id": item.id, "program_id": program_id}


@router.get("/projects", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return service_layer.list_projects(db)


@router.post("/projects", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return service_layer.create_project(db, payload, owner_user_id="bootstrap-user")


@router.patch("/projects/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: str, payload: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = service_layer.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return service_layer.update_project(db, project, payload)


@router.get("/sources", response_model=list[schemas.SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return service_layer.list_sources(db)


@router.post("/sources", response_model=schemas.SourceOut)
def create_source(payload: schemas.SourceCreate, db: Session = Depends(get_db)):
    return service_layer.create_source(db, payload)


@router.post("/projects/{project_id}/sources", response_model=schemas.ProjectSourceOut)
def attach_source_to_project(project_id: str, payload: schemas.ProjectSourceCreate, db: Session = Depends(get_db)):
    project = service_layer.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    source = service_layer.get_source(db, payload.source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return service_layer.attach_source_to_project(db, project_id, payload)


@router.post("/projects/{project_id}/bibliography-snapshots", response_model=schemas.BibliographySnapshotOut)
def create_snapshot(project_id: str, payload: schemas.BibliographySnapshotCreate, db: Session = Depends(get_db)):
    project = service_layer.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return service_layer.create_snapshot(db, project_id, payload)


@router.post("/bibliography-snapshots/{snapshot_id}/activate", response_model=schemas.BibliographySnapshotOut)
def activate_snapshot(snapshot_id: str, db: Session = Depends(get_db)):
    snapshot = service_layer.get_snapshot(db, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return service_layer.activate_snapshot(db, snapshot)
