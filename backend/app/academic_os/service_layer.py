from __future__ import annotations

from sqlalchemy.orm import Session

from . import models, schemas


def list_programs(db: Session) -> list[models.Program]:
    return db.query(models.Program).order_by(models.Program.created_at.desc()).all()


def get_program(db: Session, program_id: str) -> models.Program | None:
    return db.query(models.Program).filter(models.Program.id == program_id).first()


def create_program(db: Session, payload: schemas.ProgramCreate, owner_user_id: str) -> models.Program:
    obj = models.Program(
        owner_user_id=owner_user_id,
        template_id=payload.template_id,
        name=payload.name,
        program_type=payload.program_type,
        description=payload.description,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_program_requirement(db: Session, program_id: str, payload: schemas.ProgramRequirementCreate) -> models.ProgramRequirement:
    obj = models.ProgramRequirement(
        program_id=program_id,
        requirement_code=payload.requirement_code,
        requirement_type=payload.requirement_type,
        condition_json=str(payload.condition_json),
        priority=payload.priority,
        is_mandatory=payload.is_mandatory,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_projects(db: Session) -> list[models.ResearchProject]:
    return db.query(models.ResearchProject).order_by(models.ResearchProject.created_at.desc()).all()


def get_project(db: Session, project_id: str) -> models.ResearchProject | None:
    return db.query(models.ResearchProject).filter(models.ResearchProject.id == project_id).first()


def create_project(db: Session, payload: schemas.ProjectCreate, owner_user_id: str) -> models.ResearchProject:
    obj = models.ResearchProject(
        owner_user_id=owner_user_id,
        title=payload.title,
        topic_description=payload.topic_description,
        problem_statement=payload.problem_statement,
        work_type_id=payload.work_type_id,
        journal_target_mode=payload.journal_target_mode,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_project(db: Session, obj: models.ResearchProject, payload: schemas.ProjectUpdate) -> models.ResearchProject:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_sources(db: Session) -> list[models.Source]:
    return db.query(models.Source).order_by(models.Source.created_at.desc()).all()


def get_source(db: Session, source_id: str) -> models.Source | None:
    return db.query(models.Source).filter(models.Source.id == source_id).first()


def create_source(db: Session, payload: schemas.SourceCreate) -> models.Source:
    obj = models.Source(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def attach_source_to_project(db: Session, project_id: str, payload: schemas.ProjectSourceCreate) -> models.ProjectSource:
    obj = models.ProjectSource(
        project_id=project_id,
        source_id=payload.source_id,
        role=payload.role,
        selection_reason=payload.selection_reason,
        inclusion_mode=payload.inclusion_mode,
        is_mandatory=payload.is_mandatory,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_snapshot(db: Session, project_id: str, payload: schemas.BibliographySnapshotCreate) -> models.BibliographySnapshot:
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

    for idx, project_source_id in enumerate(payload.item_ids, start=1):
        db.add(
            models.BibliographySnapshotItem(
                snapshot_id=snapshot.id,
                project_source_id=project_source_id,
                position_no=idx,
            )
        )
    db.commit()
    db.refresh(snapshot)
    return snapshot


def get_snapshot(db: Session, snapshot_id: str) -> models.BibliographySnapshot | None:
    return db.query(models.BibliographySnapshot).filter(models.BibliographySnapshot.id == snapshot_id).first()


def activate_snapshot(db: Session, snapshot: models.BibliographySnapshot) -> models.BibliographySnapshot:
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
