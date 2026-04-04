from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProgramCreate(BaseModel):
    name: str
    program_type: str
    target_date: str | None = None
    description: str = ""
    template_id: str | None = None


class ProgramRequirementCreate(BaseModel):
    requirement_code: str
    requirement_type: str
    condition_json: dict[str, Any] = Field(default_factory=dict)
    priority: int = 100
    is_mandatory: bool = True


class ProgramOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    program_type: str
    status: str
    description: str


class WorkTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str


class ProjectCreate(BaseModel):
    title: str
    topic_description: str = ""
    problem_statement: str = ""
    work_type_id: str | None = None
    journal_target_mode: str = "generic_gost"


class ProjectUpdate(BaseModel):
    title: str | None = None
    topic_description: str | None = None
    problem_statement: str | None = None
    hypothesis: str | None = None
    gap_statement: str | None = None
    novelty_claim: str | None = None
    status: str | None = None


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    topic_description: str
    problem_statement: str
    hypothesis: str
    gap_statement: str
    novelty_claim: str
    journal_target_mode: str
    status: str


class SourceCreate(BaseModel):
    title: str
    authors_raw: str = ""
    year: int | None = None
    journal_name: str = ""
    doi: str | None = None
    url: str = ""
    language: str = ""
    country_type: str = "MIXED"
    gost_reference: str = ""
    source_type: str = "article"
    is_systemic: bool = False
    is_self_citation: bool = False
    is_partner_source: bool = False
    is_canonical: bool = False


class SourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    authors_raw: str
    year: int | None
    journal_name: str
    doi: str | None
    url: str
    language: str
    country_type: str
    source_type: str
    validation_mode: str
    access_class: str
    usage_level: str
    is_canonical: bool
    has_fulltext: bool


class ProjectSourceCreate(BaseModel):
    source_id: str
    role: str = "reserve_source"
    selection_reason: str = ""
    inclusion_mode: str = "verified_secondary"
    is_mandatory: bool = False


class ProjectSourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    source_id: str
    role: str
    is_mandatory: bool
    is_locked: bool
    selection_reason: str
    selected_order: int | None
    inclusion_mode: str


class BibliographySnapshotCreate(BaseModel):
    planned_count: int
    expanded_count: int
    ru_share: float | None = None
    foreign_share: float | None = None
    fresh_2024_plus_share: float | None = None
    systemic_count: int | None = None
    core_idea_count: int | None = None
    item_ids: list[str] = Field(default_factory=list)


class BibliographySnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    planned_count: int
    expanded_count: int
    is_active: bool


class FulltextRegister(BaseModel):
    storage_path: str
    file_type: str
    origin_type: str = "manual_upload"
    checksum: str = ""
    pages_count: int | None = None


class VerificationCreate(BaseModel):
    exists_confirmed: bool = False
    metadata_consistent: bool = False
    suspected_fake_reference: bool = False
    quote_extraction_quality: float | None = None
    digest_quality_score: float | None = None
    notes: str = ""


class VerificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source_id: str
    exists_confirmed: bool
    metadata_consistent: bool
    suspected_fake_reference: bool
    notes: str


class ArticleVersionCreate(BaseModel):
    project_id: str
    version_no: int = 1
    full_text: str = ""
    formatted_text: str = ""


class ArticleVersionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    version_no: int
    full_text: str
    formatted_text: str


class AgentTaskCreate(BaseModel):
    entity_type: str
    entity_id: str
    agent_name: str
    task_type: str
    priority: int = 100
    approval_required: bool = False


class AgentTaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    entity_type: str
    entity_id: str
    agent_name: str
    task_type: str
    priority: int
    status: str
    approval_required: bool
