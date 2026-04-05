"""academic_os baseline

Revision ID: 20260405_000001
Revises:
Create Date: 2026-04-05
"""

from alembic import op
import sqlalchemy as sa


revision = "20260405_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ao_program_templates",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("program_type", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("rules_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("default_time_horizon_months", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ao_work_types",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
    )

    op.create_table(
        "ao_specialty_passports",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("scope_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("boundaries_text", sa.Text(), nullable=False, server_default=""),
    )

    op.create_table(
        "ao_programs",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("owner_user_id", sa.String(length=255), nullable=False),
        sa.Column("template_id", sa.String(), sa.ForeignKey("ao_program_templates.id"), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("program_type", sa.String(length=100), nullable=False),
        sa.Column("target_date", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ao_program_requirements",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("program_id", sa.String(), sa.ForeignKey("ao_programs.id"), nullable=False),
        sa.Column("requirement_code", sa.String(length=100), nullable=False),
        sa.Column("requirement_type", sa.String(length=100), nullable=False),
        sa.Column("condition_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("is_mandatory", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )

    op.create_table(
        "ao_research_projects",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("owner_user_id", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("topic_description", sa.Text(), nullable=False, server_default=""),
        sa.Column("problem_statement", sa.Text(), nullable=False, server_default=""),
        sa.Column("hypothesis", sa.Text(), nullable=False, server_default=""),
        sa.Column("gap_statement", sa.Text(), nullable=False, server_default=""),
        sa.Column("novelty_claim", sa.Text(), nullable=False, server_default=""),
        sa.Column("work_type_id", sa.String(), sa.ForeignKey("ao_work_types.id"), nullable=True),
        sa.Column("journal_target_mode", sa.String(length=50), nullable=False, server_default="generic_gost"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ao_sources",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("authors_raw", sa.Text(), nullable=False, server_default=""),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("journal_name", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("doi", sa.String(length=255), nullable=True),
        sa.Column("url", sa.String(length=1000), nullable=False, server_default=""),
        sa.Column("language", sa.String(length=50), nullable=False, server_default=""),
        sa.Column("country_type", sa.String(length=50), nullable=False, server_default="MIXED"),
        sa.Column("gost_reference", sa.Text(), nullable=False, server_default=""),
        sa.Column("source_type", sa.String(length=100), nullable=False, server_default="article"),
        sa.Column("is_systemic", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_self_citation", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_partner_source", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_canonical", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("has_fulltext", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("validation_mode", sa.String(length=100), nullable=False, server_default="unverified"),
        sa.Column("access_class", sa.String(length=100), nullable=False, server_default="metadata_only"),
        sa.Column("usage_level", sa.String(length=100), nullable=False, server_default="for_background_only"),
        sa.Column("direct_quote_allowed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("reliability_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("doi", name="uq_ao_sources_doi"),
    )

    op.create_table(
        "ao_project_sources",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("project_id", sa.String(), sa.ForeignKey("ao_research_projects.id"), nullable=False),
        sa.Column("source_id", sa.String(), sa.ForeignKey("ao_sources.id"), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False, server_default="reserve_source"),
        sa.Column("is_mandatory", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("selection_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("selected_order", sa.Integer(), nullable=True),
        sa.Column("inclusion_mode", sa.String(length=100), nullable=False, server_default="verified_secondary"),
    )
    op.create_index("ix_ao_project_sources_project", "ao_project_sources", ["project_id"])

    op.create_table(
        "ao_source_fulltexts",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("source_id", sa.String(), sa.ForeignKey("ao_sources.id"), nullable=False, unique=True),
        sa.Column("storage_path", sa.String(length=1000), nullable=False),
        sa.Column("file_type", sa.String(length=50), nullable=False),
        sa.Column("origin_type", sa.String(length=100), nullable=False, server_default="manual_upload"),
        sa.Column("checksum", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("pages_count", sa.Integer(), nullable=True),
        sa.Column("text_extracted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("parse_status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("access_scope", sa.String(length=100), nullable=False, server_default="internal_validation_only"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ao_source_verification_reports",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("source_id", sa.String(), sa.ForeignKey("ao_sources.id"), nullable=False),
        sa.Column("exists_confirmed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("metadata_consistent", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("suspected_fake_reference", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("quote_extraction_quality", sa.Numeric(5, 2), nullable=True),
        sa.Column("digest_quality_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("notes", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ao_bibliography_snapshots",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("project_id", sa.String(), sa.ForeignKey("ao_research_projects.id"), nullable=False),
        sa.Column("planned_count", sa.Integer(), nullable=False),
        sa.Column("expanded_count", sa.Integer(), nullable=False),
        sa.Column("ru_share", sa.Numeric(5, 2), nullable=True),
        sa.Column("foreign_share", sa.Numeric(5, 2), nullable=True),
        sa.Column("fresh_2024_plus_share", sa.Numeric(5, 2), nullable=True),
        sa.Column("systemic_count", sa.Integer(), nullable=True),
        sa.Column("core_idea_count", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ao_bibliography_snapshot_items",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("snapshot_id", sa.String(), sa.ForeignKey("ao_bibliography_snapshots.id"), nullable=False),
        sa.Column("project_source_id", sa.String(), sa.ForeignKey("ao_project_sources.id"), nullable=False),
        sa.Column("position_no", sa.Integer(), nullable=False),
    )

    op.create_table(
        "ao_article_versions",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("project_id", sa.String(), sa.ForeignKey("ao_research_projects.id"), nullable=False),
        sa.Column("version_no", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("full_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("formatted_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("citation_check_report", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("requirement_check_report", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("readiness_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ao_workflow_states",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.String(length=255), nullable=False),
        sa.Column("stage_code", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=50), nullable=False),
        sa.Column("entered_at", sa.DateTime(), nullable=False),
        sa.Column("exited_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_ao_workflow_states_entity", "ao_workflow_states", ["entity_type", "entity_id"])

    op.create_table(
        "ao_agent_tasks",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.String(length=255), nullable=False),
        sa.Column("agent_name", sa.String(length=255), nullable=False),
        sa.Column("task_type", sa.String(length=100), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("approval_required", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ao_agent_tasks")
    op.drop_index("ix_ao_workflow_states_entity", table_name="ao_workflow_states")
    op.drop_table("ao_workflow_states")
    op.drop_table("ao_article_versions")
    op.drop_table("ao_bibliography_snapshot_items")
    op.drop_table("ao_bibliography_snapshots")
    op.drop_table("ao_source_verification_reports")
    op.drop_table("ao_source_fulltexts")
    op.drop_index("ix_ao_project_sources_project", table_name="ao_project_sources")
    op.drop_table("ao_project_sources")
    op.drop_table("ao_sources")
    op.drop_table("ao_research_projects")
    op.drop_table("ao_program_requirements")
    op.drop_table("ao_programs")
    op.drop_table("ao_specialty_passports")
    op.drop_table("ao_work_types")
    op.drop_table("ao_program_templates")
