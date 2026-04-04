from __future__ import annotations

from sqlalchemy.orm import Session

from . import models


def get_program_or_404(db: Session, program_id: str) -> models.Program | None:
    return db.query(models.Program).filter(models.Program.id == program_id).first()


def get_project_or_404(db: Session, project_id: str) -> models.ResearchProject | None:
    return db.query(models.ResearchProject).filter(models.ResearchProject.id == project_id).first()


def get_source_or_404(db: Session, source_id: str) -> models.Source | None:
    return db.query(models.Source).filter(models.Source.id == source_id).first()


def get_snapshot_or_404(db: Session, snapshot_id: str) -> models.BibliographySnapshot | None:
    return db.query(models.BibliographySnapshot).filter(models.BibliographySnapshot.id == snapshot_id).first()


def list_programs(db: Session) -> list[models.Program]:
    return db.query(models.Program).order_by(models.Program.created_at.desc()).all()


def list_projects(db: Session) -> list[models.ResearchProject]:
    return db.query(models.ResearchProject).order_by(models.ResearchProject.created_at.desc()).all()


def list_sources(db: Session) -> list[models.Source]:
    return db.query(models.Source).order_by(models.Source.created_at.desc()).all()
