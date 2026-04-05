from __future__ import annotations

from sqlalchemy.orm import Session

from . import models, schemas


BOOTSTRAP_USER_ID = "bootstrap-user"


def create_program(db: Session, payload: schemas.ProgramCreate, owner_user_id: str = BOOTSTRAP_USER_ID) -> models.Program:
    program = models.Program(
        owner_user_id=owner_user_id,
        template_id=payload.template_id,
        name=payload.name,
        program_type=payload.program_type,
        description=payload.description,
    )
    db.add(program)
    db.commit()
    db.refresh(program)
    return program


def create_program_requirement(db: Session, program_id: str, payload: schemas.ProgramRequirementCreate) -> models.ProgramRequirement:
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
    return requirement


def create_project(db: Session, payload: schemas.ProjectCreate, owner_user_id: str = BOOTSTRAP_USER_ID) -> models.ResearchProject:
    project = models.ResearchProject(
        owner_user_id=owner_user_id,
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


def update_project(db: Session, project: models.ResearchProject, payload: schemas.ProjectUpdate) -> models.ResearchProject:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def create_source(db: Session, payload: schemas.SourceCreate) -> models.Source:
    source = models.Source(**payload.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def attach_source_to_project(db: Session, project_id: str, payload: schemas.ProjectSourceCreate) -> models.ProjectSource:
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

    for idx, item_id in enumerate(payload.item_ids, start=1):
        db.add(models.BibliographySnapshotItem(snapshot_id=snapshot.id, project_source_id=item_id, position_no=idx))
    db.commit()
    db.refresh(snapshot)
    return snapshot


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


def register_fulltext(db: Session, source: models.Source, payload: schemas.FulltextRegister) -> models.SourceFulltext:
    fulltext = models.SourceFulltext(source_id=source.id, **payload.model_dump())
    db.add(fulltext)
    source.has_fulltext = True
    db.add(source)
    db.commit()
    db.refresh(fulltext)
    return fulltext


def create_verification_report(db: Session, source_id: str, payload: schemas.VerificationCreate) -> models.SourceVerificationReport:
    report = models.SourceVerificationReport(source_id=source_id, **payload.model_dump())
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def create_article_version(db: Session, payload: schemas.ArticleVersionCreate) -> models.ArticleVersion:
    version = models.ArticleVersion(**payload.model_dump())
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


def create_agent_task(db: Session, payload: schemas.AgentTaskCreate) -> models.AgentTask:
    task = models.AgentTask(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
