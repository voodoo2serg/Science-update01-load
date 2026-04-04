from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class ProgramTemplate(Base):
    __tablename__ = "ao_program_templates"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), unique=True)
    program_type: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, default="")
    rules_json: Mapped[str] = mapped_column(Text, default="{}")
    default_time_horizon_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Program(Base):
    __tablename__ = "ao_programs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_user_id: Mapped[str] = mapped_column(String(255))
    template_id: Mapped[str | None] = mapped_column(ForeignKey("ao_program_templates.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255))
    program_type: Mapped[str] = mapped_column(String(100))
    target_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    template: Mapped[ProgramTemplate | None] = relationship()
    requirements: Mapped[list[ProgramRequirement]] = relationship(back_populates="program", cascade="all, delete-orphan")


class ProgramRequirement(Base):
    __tablename__ = "ao_program_requirements"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    program_id: Mapped[str] = mapped_column(ForeignKey("ao_programs.id"))
    requirement_code: Mapped[str] = mapped_column(String(100))
    requirement_type: Mapped[str] = mapped_column(String(100))
    condition_json: Mapped[str] = mapped_column(Text, default="{}")
    priority: Mapped[int] = mapped_column(Integer, default=100)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)

    program: Mapped[Program] = relationship(back_populates="requirements")


class WorkType(Base):
    __tablename__ = "ao_work_types"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")


class ResearchProject(Base):
    __tablename__ = "ao_research_projects"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_user_id: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    topic_description: Mapped[str] = mapped_column(Text, default="")
    problem_statement: Mapped[str] = mapped_column(Text, default="")
    hypothesis: Mapped[str] = mapped_column(Text, default="")
    gap_statement: Mapped[str] = mapped_column(Text, default="")
    novelty_claim: Mapped[str] = mapped_column(Text, default="")
    work_type_id: Mapped[str | None] = mapped_column(ForeignKey("ao_work_types.id"), nullable=True)
    journal_target_mode: Mapped[str] = mapped_column(String(50), default="generic_gost")
    status: Mapped[str] = mapped_column(String(50), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    work_type: Mapped[WorkType | None] = relationship()
    sources: Mapped[list[ProjectSource]] = relationship(back_populates="project", cascade="all, delete-orphan")
    snapshots: Mapped[list[BibliographySnapshot]] = relationship(back_populates="project", cascade="all, delete-orphan")


class SpecialtyPassport(Base):
    __tablename__ = "ao_specialty_passports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    scope_text: Mapped[str] = mapped_column(Text, default="")
    boundaries_text: Mapped[str] = mapped_column(Text, default="")


class Source(Base):
    __tablename__ = "ao_sources"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(500))
    authors_raw: Mapped[str] = mapped_column(Text, default="")
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    journal_name: Mapped[str] = mapped_column(String(255), default="")
    doi: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    url: Mapped[str] = mapped_column(String(1000), default="")
    language: Mapped[str] = mapped_column(String(50), default="")
    country_type: Mapped[str] = mapped_column(String(50), default="MIXED")
    gost_reference: Mapped[str] = mapped_column(Text, default="")
    source_type: Mapped[str] = mapped_column(String(100), default="article")
    is_systemic: Mapped[bool] = mapped_column(Boolean, default=False)
    is_self_citation: Mapped[bool] = mapped_column(Boolean, default=False)
    is_partner_source: Mapped[bool] = mapped_column(Boolean, default=False)
    is_canonical: Mapped[bool] = mapped_column(Boolean, default=False)
    has_fulltext: Mapped[bool] = mapped_column(Boolean, default=False)
    validation_mode: Mapped[str] = mapped_column(String(100), default="unverified")
    access_class: Mapped[str] = mapped_column(String(100), default="metadata_only")
    usage_level: Mapped[str] = mapped_column(String(100), default="for_background_only")
    direct_quote_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    reliability_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProjectSource(Base):
    __tablename__ = "ao_project_sources"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(ForeignKey("ao_research_projects.id"))
    source_id: Mapped[str] = mapped_column(ForeignKey("ao_sources.id"))
    role: Mapped[str] = mapped_column(String(100), default="reserve_source")
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    selection_reason: Mapped[str] = mapped_column(Text, default="")
    selected_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    inclusion_mode: Mapped[str] = mapped_column(String(100), default="verified_secondary")

    project: Mapped[ResearchProject] = relationship(back_populates="sources")
    source: Mapped[Source] = relationship()


class SourceFulltext(Base):
    __tablename__ = "ao_source_fulltexts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id: Mapped[str] = mapped_column(ForeignKey("ao_sources.id"), unique=True)
    storage_path: Mapped[str] = mapped_column(String(1000))
    file_type: Mapped[str] = mapped_column(String(50))
    origin_type: Mapped[str] = mapped_column(String(100), default="manual_upload")
    checksum: Mapped[str] = mapped_column(String(255), default="")
    pages_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    text_extracted: Mapped[bool] = mapped_column(Boolean, default=False)
    parse_status: Mapped[str] = mapped_column(String(50), default="pending")
    access_scope: Mapped[str] = mapped_column(String(100), default="internal_validation_only")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    source: Mapped[Source] = relationship()


class SourceVerificationReport(Base):
    __tablename__ = "ao_source_verification_reports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id: Mapped[str] = mapped_column(ForeignKey("ao_sources.id"))
    exists_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata_consistent: Mapped[bool] = mapped_column(Boolean, default=False)
    suspected_fake_reference: Mapped[bool] = mapped_column(Boolean, default=False)
    quote_extraction_quality: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    digest_quality_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    source: Mapped[Source] = relationship()


class BibliographySnapshot(Base):
    __tablename__ = "ao_bibliography_snapshots"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(ForeignKey("ao_research_projects.id"))
    planned_count: Mapped[int] = mapped_column(Integer)
    expanded_count: Mapped[int] = mapped_column(Integer)
    ru_share: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    foreign_share: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    fresh_2024_plus_share: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    systemic_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    core_idea_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    project: Mapped[ResearchProject] = relationship(back_populates="snapshots")
    items: Mapped[list[BibliographySnapshotItem]] = relationship(back_populates="snapshot", cascade="all, delete-orphan")


class BibliographySnapshotItem(Base):
    __tablename__ = "ao_bibliography_snapshot_items"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("ao_bibliography_snapshots.id"))
    project_source_id: Mapped[str] = mapped_column(ForeignKey("ao_project_sources.id"))
    position_no: Mapped[int] = mapped_column(Integer)

    snapshot: Mapped[BibliographySnapshot] = relationship(back_populates="items")
    project_source: Mapped[ProjectSource] = relationship()


class ArticleVersion(Base):
    __tablename__ = "ao_article_versions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(ForeignKey("ao_research_projects.id"))
    version_no: Mapped[int] = mapped_column(Integer, default=1)
    full_text: Mapped[str] = mapped_column(Text, default="")
    formatted_text: Mapped[str] = mapped_column(Text, default="")
    citation_check_report: Mapped[str] = mapped_column(Text, default="{}")
    requirement_check_report: Mapped[str] = mapped_column(Text, default="{}")
    readiness_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    project: Mapped[ResearchProject] = relationship()


class WorkflowState(Base):
    __tablename__ = "ao_workflow_states"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_type: Mapped[str] = mapped_column(String(50))
    entity_id: Mapped[str] = mapped_column(String(255))
    stage_code: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(50))
    entered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    exited_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class AgentTask(Base):
    __tablename__ = "ao_agent_tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_type: Mapped[str] = mapped_column(String(50))
    entity_id: Mapped[str] = mapped_column(String(255))
    agent_name: Mapped[str] = mapped_column(String(255))
    task_type: Mapped[str] = mapped_column(String(100))
    priority: Mapped[int] = mapped_column(Integer, default=100)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    approval_required: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
