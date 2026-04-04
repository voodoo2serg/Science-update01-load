from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db

from . import models, queries, schemas

api_router = APIRouter(prefix="/academic-os", tags=["academic-os"])


@api_router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "module": "academic_os"}


@api_router.get("/programs", response_model=list[schemas.ProgramOut])
def list_programs(db: Session = Depends(get_db)):
    return queries.list_programs(db)


@api_router.post("/programs", response_model=schemas.ProgramOut)
def create_program(payload: schemas.ProgramCreate, db: Session = Depends(get_db)):
    program = models.Program(
        owner_user_id="bootstrap-user",
        template_id=payload.template_id,
        name=payload.name,
        program_type=payload.program_type,
        description=payload.description,
    )
    db.add(program)
    db.commit()
    db.refresh(program)
    return program


@api_router.post("/programs/{program_id}/requirements")
def add_program_requirement(
    program_id: str,
    payload: schemas.ProgramRequirementCreate,
    db: Session = Depends(get_db),
):
    program = queries.get_program_or_404(db, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    requirement = models.ProgramRequirement(
        program_id=program_id,
        requirement_code=payload.requirement_code,
        requirement_type=payload.requirement_type,
        condition_json=str(payload.condition_json),
        priority=payload.priority,
        is_mandatory=payload.is_mandatory,
    )
    db.add(requirement)
    db.commit()
    db.refresh(requirement)
    return {"id": requirement.id, "program_id": program_id}


@api_router.get("/projects", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return queries.list_projects(db)


@api_router.post("/projects", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    project = models.ResearchProject(
        owner_user_id="bootstrap-user",
        title=payload.title,
        topic_description=payload.topic_description,
        problem_statement=payload.problem_statement,
        work_type_id=payload.work_type_id,
        journal_target_mode=payload.journal_target_mode,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@api_router.patch("/projects/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: str, payload: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    project = queries.get_project_or_404(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@api_router.get("/sources", response_model=list[schemas.SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return queries.list_sources(db)


@api_router.post("/sources", response_model=schemas.SourceOut)
def create_source(payload: schemas.SourceCreate, db: Session = Depends(get_db)):
    source = models.Source(**payload.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@api_router.post("/projects/{project_id}/sources", response_model=schemas.ProjectSourceOut)
def attach_source_to_project(
    project_id: str,
    payload: schemas.ProjectSourceCreate,
    db: Session = Depends(get_db),
):
    project = queries.get_project_or_404(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    source = queries.get_source_or_404(db, payload.source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    project_source = models.ProjectSource(
        project_id=project_id,
        source_id=payload.source_id,
        role=payload.role,
        selection_reason=payload.selection_reason,
        inclusion_mode=payload.inclusion_mode,
        is_mandatory=payload.is_mandatory,
    )
    db.add(project_source)
    db.commit()
    db.refresh(project_source)
    return project_source


@api_router.post("/projects/{project_id}/bibliography-snapshots", response_model=schemas.BibliographySnapshotOut)
def create_snapshot(
    project_id: str,
    payload: schemas.BibliographySnapshotCreate,
    db: Session = Depends(get_db),
):
    project = queries.get_project_or_404(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    snapshot = models.BibliographySnapshot(
        project_id=project_id,
        planned_count=payload.planned_count,
        expanded_count=payload.expanded_count,
        ru_share=payload.ru_share,
        foreign_share=payload.foreign_share,
        fresh_2024_plus_share=payload.fresh_2024_plus_share,
        systemic_count=payload.systemic_count,
        core_idea_count=payload.core_idea_count,
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    for idx, item_id in enumerate(payload.item_ids, start=1):
        item = models.BibliographySnapshotItem(
            snapshot_id=snapshot.id,
            project_source_id=item_id,
            position_no=idx,
        )
        db.add(item)
    db.commit()
    db.refresh(snapshot)
    return snapshot


@api_router.post("/bibliography-snapshots/{snapshot_id}/activate", response_model=schemas.BibliographySnapshotOut)
def activate_snapshot(snapshot_id: str, db: Session = Depends(get_db)):
    snapshot = queries.get_snapshot_or_404(db, snapshot_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    db.query(models.BibliographySnapshot).filter(
        models.BibliographySnapshot.project_id == snapshot.project_id,
        models.BibliographySnapshot.is_active.is_(True),
        models.BibliographySnapshot.id != snapshot.id,
    ).update({models.BibliographySnapshot.is_active: False})
    snapshot.is_active = True
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


@api_router.post("/sources/{source_id}/fulltext")
def register_fulltext(source_id: str, payload: schemas.FulltextRegister, db: Session = Depends(get_db)):
    source = queries.get_source_or_404(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    fulltext = models.SourceFulltext(source_id=source_id, **payload.model_dump())
    db.add(fulltext)
    source.has_fulltext = True
    db.add(source)
    db.commit()
    db.refresh(fulltext)
    return {"id": fulltext.id, "source_id": source_id}


@api_router.post("/sources/{source_id}/verification", response_model=schemas.VerificationOut)
def create_verification(source_id: str, payload: schemas.VerificationCreate, db: Session = Depends(get_db)):
    source = queries.get_source_or_404(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    report = models.SourceVerificationReport(source_id=source_id, **payload.model_dump())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@api_router.post("/article-versions", response_model=schemas.ArticleVersionOut)
def create_article_version(payload: schemas.ArticleVersionCreate, db: Session = Depends(get_db)):
    project = queries.get_project_or_404(db, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    article_version = models.ArticleVersion(**payload.model_dump())
    db.add(article_version)
    db.commit()
    db.refresh(article_version)
    return article_version


@api_router.post("/agent-tasks", response_model=schemas.AgentTaskOut)
def create_agent_task(payload: schemas.AgentTaskCreate, db: Session = Depends(get_db)):
    task = models.AgentTask(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
