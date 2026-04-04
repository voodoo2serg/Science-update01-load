-- Academic Research OS v1.0
-- PostgreSQL DDL baseline for Science-update01-load evolution

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS program;
CREATE SCHEMA IF NOT EXISTS source;
CREATE SCHEMA IF NOT EXISTS verify;
CREATE SCHEMA IF NOT EXISTS evidence;
CREATE SCHEMA IF NOT EXISTS article;
CREATE SCHEMA IF NOT EXISTS agent;
CREATE SCHEMA IF NOT EXISTS policy;
CREATE SCHEMA IF NOT EXISTS rag;

CREATE TABLE core.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'researcher',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE core.work_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE core.specialty_passports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    scope_text TEXT,
    keywords_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    methods_allowed_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    objects_of_study_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    boundaries_text TEXT
);

CREATE TABLE core.method_catalog (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    requires_dataset BOOLEAN NOT NULL DEFAULT FALSE,
    requires_code BOOLEAN NOT NULL DEFAULT FALSE,
    requires_open_repository BOOLEAN NOT NULL DEFAULT FALSE,
    allowed_for_ai_only_workflow BOOLEAN NOT NULL DEFAULT TRUE,
    description TEXT
);

CREATE TABLE core.journals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    publisher TEXT,
    quartile TEXT,
    index_type TEXT,
    language TEXT,
    specialty_codes_supported_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    template_type TEXT,
    requirements_file_ref TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE core.journal_requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journal_id UUID NOT NULL REFERENCES core.journals(id) ON DELETE CASCADE,
    format_rules_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    citation_style TEXT,
    max_words INTEGER,
    min_words INTEGER,
    abstract_rules TEXT,
    keywords_rules TEXT,
    structure_rules TEXT,
    table_figure_rules TEXT,
    bibliography_rules TEXT,
    version_no INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE program.big_path_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    program_type TEXT NOT NULL,
    description TEXT,
    rules_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    default_time_horizon_months INTEGER,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE program.big_path_programs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_user_id UUID NOT NULL REFERENCES core.users(id) ON DELETE RESTRICT,
    template_id UUID REFERENCES program.big_path_templates(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    program_type TEXT NOT NULL,
    target_date DATE,
    status TEXT NOT NULL DEFAULT 'draft',
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE core.research_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_user_id UUID NOT NULL REFERENCES core.users(id) ON DELETE RESTRICT,
    title TEXT NOT NULL,
    topic_description TEXT,
    problem_statement TEXT,
    hypothesis TEXT,
    gap_statement TEXT,
    novelty_claim TEXT,
    work_type_id UUID REFERENCES core.work_types(id) ON DELETE SET NULL,
    journal_target_mode TEXT NOT NULL DEFAULT 'generic_gost',
    status TEXT NOT NULL DEFAULT 'draft',
    row_version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE core.project_specialties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    specialty_id UUID NOT NULL REFERENCES core.specialty_passports(id) ON DELETE RESTRICT,
    role TEXT NOT NULL,
    justification TEXT,
    is_locked BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (project_id, specialty_id)
);

CREATE TABLE source.sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    authors_raw TEXT,
    year INTEGER,
    journal_name TEXT,
    publisher TEXT,
    doi TEXT,
    url TEXT,
    language TEXT,
    country_type TEXT,
    institution_tags_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    gost_reference TEXT,
    source_type TEXT NOT NULL,
    is_systemic BOOLEAN NOT NULL DEFAULT FALSE,
    is_self_citation BOOLEAN NOT NULL DEFAULT FALSE,
    is_partner_source BOOLEAN NOT NULL DEFAULT FALSE,
    is_core_idea_source BOOLEAN NOT NULL DEFAULT FALSE,
    is_canonical BOOLEAN NOT NULL DEFAULT FALSE,
    is_historical_foundation BOOLEAN NOT NULL DEFAULT FALSE,
    freshness_bucket TEXT,
    has_fulltext BOOLEAN NOT NULL DEFAULT FALSE,
    has_partial_text BOOLEAN NOT NULL DEFAULT FALSE,
    validation_mode TEXT NOT NULL DEFAULT 'unverified',
    access_class TEXT NOT NULL DEFAULT 'metadata_only',
    usage_level TEXT NOT NULL DEFAULT 'for_background_only',
    digest_type TEXT,
    direct_quote_allowed BOOLEAN NOT NULL DEFAULT FALSE,
    needs_trace_research BOOLEAN NOT NULL DEFAULT FALSE,
    trace_research_status TEXT,
    reliability_score NUMERIC(5,2),
    interpretation_risk_score NUMERIC(5,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX source_sources_doi_uidx ON source.sources (doi) WHERE doi IS NOT NULL;

CREATE TABLE evidence.project_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES source.sources(id) ON DELETE RESTRICT,
    role TEXT NOT NULL,
    is_mandatory BOOLEAN NOT NULL DEFAULT FALSE,
    is_locked BOOLEAN NOT NULL DEFAULT FALSE,
    selection_reason TEXT,
    selected_order INTEGER,
    inclusion_mode TEXT NOT NULL,
    UNIQUE (project_id, source_id)
);

CREATE TABLE verify.source_fulltexts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL UNIQUE REFERENCES source.sources(id) ON DELETE CASCADE,
    storage_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    origin_type TEXT NOT NULL,
    checksum TEXT,
    pages_count INTEGER,
    text_extracted BOOLEAN NOT NULL DEFAULT FALSE,
    ocr_status TEXT,
    parse_status TEXT,
    access_scope TEXT NOT NULL DEFAULT 'internal_validation_only',
    retention_policy TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE verify.source_fulltext_fragments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES source.sources(id) ON DELETE CASCADE,
    fulltext_id UUID NOT NULL REFERENCES verify.source_fulltexts(id) ON DELETE CASCADE,
    fragment_type TEXT NOT NULL,
    page_from INTEGER,
    page_to INTEGER,
    text_fragment TEXT NOT NULL,
    embedding_ref TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE verify.source_verification_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES source.sources(id) ON DELETE CASCADE,
    exists_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    metadata_consistent BOOLEAN NOT NULL DEFAULT FALSE,
    reference_list_consistent BOOLEAN NOT NULL DEFAULT FALSE,
    quote_extraction_quality NUMERIC(5,2),
    digest_quality_score NUMERIC(5,2),
    suspected_fake_reference BOOLEAN NOT NULL DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE verify.source_evidence_chain (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES source.sources(id) ON DELETE CASCADE,
    evidence_type TEXT NOT NULL,
    evidence_text TEXT,
    evidence_url TEXT,
    evidence_source_id UUID REFERENCES source.sources(id) ON DELETE SET NULL,
    confidence_score NUMERIC(5,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE verify.canonical_source_trace_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES source.sources(id) ON DELETE CASCADE,
    task_status TEXT NOT NULL DEFAULT 'pending',
    goal TEXT,
    search_notes TEXT,
    search_spaces_checked_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    best_candidate_location TEXT,
    access_barrier_type TEXT,
    resolution_status TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE evidence.bibliography_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    planned_count INTEGER NOT NULL,
    expanded_count INTEGER NOT NULL,
    ru_share NUMERIC(5,2),
    foreign_share NUMERIC(5,2),
    fresh_2024_plus_share NUMERIC(5,2),
    systemic_count INTEGER,
    core_idea_count INTEGER,
    locked_at TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE evidence.bibliography_snapshot_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_id UUID NOT NULL REFERENCES evidence.bibliography_snapshots(id) ON DELETE CASCADE,
    project_source_id UUID NOT NULL REFERENCES evidence.project_sources(id) ON DELETE CASCADE,
    position_no INTEGER NOT NULL,
    UNIQUE (snapshot_id, project_source_id),
    UNIQUE (snapshot_id, position_no)
);

CREATE TABLE evidence.source_digests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES source.sources(id) ON DELETE CASCADE,
    digest_type TEXT NOT NULL,
    short_digest TEXT,
    methods_digest TEXT,
    findings_digest TEXT,
    limitations_digest TEXT,
    relevance_to_project TEXT,
    supports_idea_score NUMERIC(5,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE evidence.source_quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES source.sources(id) ON DELETE CASCADE,
    quote_text TEXT NOT NULL,
    page_info TEXT,
    quote_type TEXT NOT NULL,
    quote_mode TEXT NOT NULL,
    verified BOOLEAN NOT NULL DEFAULT FALSE,
    gost_inline_hint TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE core.evidence_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    work_type_id UUID NOT NULL REFERENCES core.work_types(id) ON DELETE CASCADE,
    journal_tier TEXT,
    profile_name TEXT NOT NULL,
    required_artifacts_json JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE core.project_evidence_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    evidence_profile_id UUID NOT NULL REFERENCES core.evidence_profiles(id) ON DELETE RESTRICT,
    selected_reason TEXT,
    locked_at TIMESTAMPTZ
);

CREATE TABLE evidence.research_designs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    method_id UUID REFERENCES core.method_catalog(id) ON DELETE SET NULL,
    research_question TEXT,
    object_of_study TEXT,
    subject_of_study TEXT,
    dataset_description TEXT,
    ai_tools_used_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    reproducibility_plan TEXT,
    github_repo_url TEXT,
    open_science_status TEXT
);

CREATE TABLE evidence.datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    origin TEXT,
    schema_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    storage_path TEXT,
    license TEXT,
    is_open BOOLEAN NOT NULL DEFAULT FALSE,
    version_tag TEXT
);

CREATE TABLE evidence.analysis_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    run_type TEXT NOT NULL,
    parameters_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    result_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    artifact_path TEXT,
    reproducible_script_path TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE article.article_outlines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    journal_id UUID REFERENCES core.journals(id) ON DELETE SET NULL,
    outline_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    argument_chain_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    required_sections_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    evidence_map_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'draft'
);

CREATE TABLE article.article_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    journal_id UUID REFERENCES core.journals(id) ON DELETE SET NULL,
    version_no INTEGER NOT NULL,
    full_text TEXT,
    formatted_text TEXT,
    citation_check_report JSONB NOT NULL DEFAULT '{}'::jsonb,
    requirement_check_report JSONB NOT NULL DEFAULT '{}'::jsonb,
    readiness_score NUMERIC(5,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (project_id, version_no)
);

CREATE TABLE article.article_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES core.research_projects(id) ON DELETE CASCADE,
    article_version_id UUID NOT NULL REFERENCES article.article_versions(id) ON DELETE RESTRICT,
    journal_id UUID NOT NULL REFERENCES core.journals(id) ON DELETE RESTRICT,
    submission_date DATE,
    status TEXT NOT NULL,
    decision_date DATE,
    notes TEXT
);

CREATE TABLE program.publication_portfolio_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_id UUID NOT NULL REFERENCES program.big_path_programs(id) ON DELETE CASCADE,
    project_id UUID REFERENCES core.research_projects(id) ON DELETE SET NULL,
    article_version_id UUID REFERENCES article.article_versions(id) ON DELETE SET NULL,
    publication_status TEXT NOT NULL,
    journal_id UUID REFERENCES core.journals(id) ON DELETE SET NULL,
    journal_tier TEXT,
    publication_date DATE,
    freshness_bucket TEXT,
    specialty_code TEXT,
    counts_toward_program BOOLEAN NOT NULL DEFAULT TRUE,
    notes TEXT
);

CREATE TABLE program.program_progress_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_id UUID NOT NULL REFERENCES program.big_path_programs(id) ON DELETE CASCADE,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    total_required_articles INTEGER,
    total_completed_articles INTEGER,
    fresh_articles_required INTEGER,
    fresh_articles_completed INTEGER,
    required_high_tier_articles INTEGER,
    completed_high_tier_articles INTEGER,
    active_projects_count INTEGER,
    risk_score NUMERIC(5,2),
    summary_json JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE agent.workflow_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    stage_code TEXT NOT NULL,
    state TEXT NOT NULL,
    entered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    exited_at TIMESTAMPTZ
);

CREATE TABLE agent.workflow_transitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    from_stage TEXT,
    to_stage TEXT NOT NULL,
    trigger_type TEXT NOT NULL,
    agent_name TEXT,
    requires_approval BOOLEAN NOT NULL DEFAULT FALSE,
    policy_check_required BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE agent.agent_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    agent_name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 100,
    status TEXT NOT NULL DEFAULT 'pending',
    approval_required BOOLEAN NOT NULL DEFAULT FALSE,
    approved_by_user_id UUID REFERENCES core.users(id) ON DELETE SET NULL,
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE agent.agent_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES agent.agent_tasks(id) ON DELETE SET NULL,
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    agent_name TEXT NOT NULL,
    stage_code TEXT,
    input_context_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'running',
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at TIMESTAMPTZ
);

CREATE TABLE agent.retrieval_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    agent_name TEXT NOT NULL,
    collections_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    filters_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    top_k INTEGER NOT NULL DEFAULT 10,
    rerank_strategy TEXT,
    notes TEXT
);

CREATE TABLE policy.policy_sets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    scope TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE policy.policy_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_set_id UUID REFERENCES policy.policy_sets(id) ON DELETE SET NULL,
    rule_code TEXT NOT NULL,
    scope TEXT NOT NULL,
    condition_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    action_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    severity TEXT NOT NULL DEFAULT 'error',
    message_template TEXT,
    UNIQUE (scope, rule_code)
);

CREATE TABLE policy.approval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    approval_type TEXT NOT NULL,
    target_table TEXT NOT NULL,
    target_record_id UUID NOT NULL,
    requested_by_agent TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE policy.human_review_actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    approval_request_id UUID REFERENCES policy.approval_requests(id) ON DELETE SET NULL,
    user_id UUID NOT NULL REFERENCES core.users(id) ON DELETE RESTRICT,
    action_type TEXT NOT NULL,
    target_entity_type TEXT NOT NULL,
    target_entity_id UUID NOT NULL,
    decision TEXT NOT NULL,
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE policy.audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    event_type TEXT NOT NULL,
    actor_type TEXT NOT NULL,
    actor_ref TEXT,
    payload_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rag.rag_collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    collection_type TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE rag.rag_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collection_id UUID NOT NULL REFERENCES rag.rag_collections(id) ON DELETE CASCADE,
    source_table TEXT NOT NULL,
    source_record_id UUID NOT NULL,
    title TEXT,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rag.rag_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rag_document_id UUID NOT NULL REFERENCES rag.rag_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding_ref TEXT,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (rag_document_id, chunk_index)
);
