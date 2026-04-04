from app.academic_os.schemas import (
    AgentTaskCreate,
    BibliographySnapshotCreate,
    ProgramCreate,
    ProjectCreate,
    SourceCreate,
)


def test_program_create_schema() -> None:
    payload = ProgramCreate(name="Professor 2029", program_type="professor")
    assert payload.name == "Professor 2029"
    assert payload.program_type == "professor"


def test_project_create_schema_defaults() -> None:
    payload = ProjectCreate(title="AI and communication")
    assert payload.journal_target_mode == "generic_gost"
    assert payload.problem_statement == ""


def test_source_create_schema_defaults() -> None:
    payload = SourceCreate(title="Example source")
    assert payload.source_type == "article"
    assert payload.country_type == "MIXED"
    assert payload.is_canonical is False


def test_bibliography_snapshot_create_schema() -> None:
    payload = BibliographySnapshotCreate(planned_count=20, expanded_count=24, item_ids=["a", "b"])
    assert payload.planned_count == 20
    assert payload.expanded_count == 24
    assert payload.item_ids == ["a", "b"]


def test_agent_task_schema() -> None:
    payload = AgentTaskCreate(
        entity_type="project",
        entity_id="project-1",
        agent_name="Bibliography Architect Agent",
        task_type="build_snapshot",
    )
    assert payload.priority == 100
    assert payload.approval_required is False
