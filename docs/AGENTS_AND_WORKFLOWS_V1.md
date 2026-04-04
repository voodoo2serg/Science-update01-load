# Subagents and Workflow Specification v1.0

Документ фиксирует state machine и контракты субагентов для Academic Research OS.

## 1. Program state machine

### States
- `program_created`
- `requirements_loaded`
- `portfolio_baselined`
- `theme_tracks_defined`
- `portfolio_planned`
- `project_pipeline_active`
- `milestone_review`
- `program_on_track`
- `program_at_risk`
- `program_goal_achieved`

### Critical transitions

#### `program_created -> requirements_loaded`
Инициатор: пользователь или `Program Strategist Agent`

#### `requirements_loaded -> portfolio_baselined`
Инициатор: `Portfolio Gap Agent`

#### `portfolio_baselined -> theme_tracks_defined`
Инициатор: `Program Strategist Agent`

#### `theme_tracks_defined -> portfolio_planned`
Инициатор: `Publication Planning Agent`

#### `portfolio_planned -> project_pipeline_active`
Инициатор: `Master Orchestrator`

#### `milestone_review -> program_on_track | program_at_risk`
Инициатор: `Career Compliance Agent`

#### `program_on_track -> program_goal_achieved`
Инициатор: `Career Compliance Agent`
Approval: рекомендуется финальное подтверждение человеком.

---

## 2. Project state machine

### States
- `intake`
- `specialty_framing`
- `hypothesis_discovery`
- `source_collection`
- `source_verification`
- `bibliography_lock`
- `evidence_profile_selection`
- `digest_and_quotes`
- `research_design`
- `analysis_if_needed`
- `outline_ready`
- `draft_assembly`
- `style_alignment`
- `compliance_check`
- `submission_ready`
- `submitted`
- `accepted`
- `published`

### Critical transitions

#### `intake -> specialty_framing`
Инициатор: `Project Intake Agent`

#### `specialty_framing -> hypothesis_discovery`
Инициатор: `Specialty Boundary Agent`
Approval: lock specialities required.

#### `hypothesis_discovery -> source_collection`
Инициатор: `Hypothesis Discovery Agent`
Approval: lock hypothesis recommended.

#### `source_collection -> source_verification`
Инициатор: `Bibliography Architect Agent`

#### `source_verification -> bibliography_lock`
Инициатор: `Source Verification Agent`
Approval: bibliography snapshot lock required.

#### `bibliography_lock -> evidence_profile_selection`
Инициатор: `Research Design Agent`

#### `evidence_profile_selection -> digest_and_quotes`
Инициатор: `Digest & Quote Agent`

#### `digest_and_quotes -> research_design`
Инициатор: `Research Design Agent`

#### `research_design -> analysis_if_needed | outline_ready`
Инициатор: `Research Design Agent`

#### `analysis_if_needed -> outline_ready`
Инициатор: `Analysis Execution Agent`

#### `outline_ready -> draft_assembly`
Инициатор: `Draft Composer Agent`

#### `draft_assembly -> style_alignment`
Инициатор: `Style Alignment Agent`

#### `style_alignment -> compliance_check`
Инициатор: `Citation Compliance Agent` + `Journal Fit Agent`

#### `compliance_check -> submission_ready`
Инициатор: `Citation Compliance Agent`
Approval: recommended.

#### `submission_ready -> submitted`
Инициатор: пользователь/оператор.

---

## 3. Approval-required locks

Следующие действия считаются критическими:
- specialties lock
- hypothesis lock
- bibliography lock
- canonical exception approval
- evidence profile lock
- journal target lock
- final article release

---

## 4. Agent contracts

Ниже — рабочий minimum set contracts.

### 4.1. Program Strategist Agent
**Role:** строит publication strategy для Big Path.

**Inputs:**
- big path program
- program requirements
- current portfolio
- program memory

**Retrieval profile:**
- `program_memory`
- `personal_corpus`
- `journal_requirements`
- `methods_library`

**Allowed writes:**
- `program.program_theme_tracks`
- `program.program_milestones`
- `program.program_publication_targets`
- `policy.audit_events`

**Approval mode:** `approval_required`

**Output:**
- strategy summary
- theme tracks
- article mix plan
- milestones

---

### 4.2. Portfolio Gap Agent
**Role:** считает дефициты публикационного портфеля.

**Inputs:**
- program requirements
- publication portfolio
- progress snapshots

**Retrieval profile:**
- `program_memory`

**Allowed writes:**
- `program.program_progress_snapshots`
- `policy.audit_events`

**Approval mode:** `auto`

**Output:**
- gap report
- risk score
- missing article types

---

### 4.3. Publication Planning Agent
**Role:** превращает publication strategy в очередь проектов.

**Inputs:**
- gap report
- theme tracks
- existing projects

**Retrieval profile:**
- `program_memory`
- `personal_corpus`
- `verified_sources`

**Allowed writes:**
- `program.program_project_links`
- `policy.audit_events`

**Approval mode:** `approval_required`

---

### 4.4. Deadline Control Agent
**Role:** следит за дедлайнами и окнами свежести.

**Allowed writes:**
- `program.program_progress_snapshots`
- `agent.agent_tasks`
- `policy.audit_events`

**Approval mode:** `auto`

---

### 4.5. Career Compliance Agent
**Role:** проверяет достижение формальной цели программы.

**Allowed writes:**
- `program.program_progress_snapshots`
- `agent.workflow_transitions`
- `policy.audit_events`

**Approval mode:** финальное достижение цели требует подтверждения.

---

### 4.6. Project Intake Agent
**Role:** переводит тему в рабочий scope проекта.

**Allowed writes:**
- `core.research_projects`
- `core.project_memory_entries`
- `agent.workflow_transitions`

**Approval mode:** `auto`

---

### 4.7. Specialty Boundary Agent
**Role:** подбирает 1–3 специальности и пишет boundary statement.

**Retrieval profile:**
- `specialty_passports`
- `project_memory`

**Allowed writes:**
- `core.project_specialties`
- `core.project_memory_entries`
- `policy.audit_events`

**Approval mode:** `approval_required`

---

### 4.8. Hypothesis Discovery Agent
**Role:** находит scientific gap и формулирует гипотезу.

**Retrieval profile:**
- `verified_sources`
- `specialty_passports`
- `project_memory`
- `methods_library`

**Allowed writes:**
- `core.research_hypotheses`
- `core.gap_evidence`
- `core.project_memory_entries`

**Approval mode:** `approval_required`

---

### 4.9. Bibliography Architect Agent
**Role:** собирает фиксируемую bibliography snapshot.

**Retrieval profile:**
- `verified_sources`
- `canonical_sources`
- `project_memory`
- `program_memory`
- `personal_corpus`

**Allowed writes:**
- `evidence.project_sources`
- `evidence.bibliography_snapshots`
- `evidence.bibliography_snapshot_items`
- `policy.audit_events`

**Approval mode:** `approval_required`

---

### 4.10. Source Verification Agent
**Role:** верифицирует источники.

**Allowed writes:**
- `verify.source_verification_reports`
- updates to `source.sources.validation_mode`
- updates to `source.sources.usage_level`
- `policy.audit_events`

**Approval mode:** `auto`, кроме спорных случаев.

---

### 4.11. Canonical Trace Agent
**Role:** работает со сложными каноническими источниками.

**Allowed writes:**
- `verify.canonical_source_trace_tasks`
- `verify.source_evidence_chain`
- updates to `source.sources`
- `policy.audit_events`

**Approval mode:** mixed / often approval required.

---

### 4.12. Digest & Quote Agent
**Role:** формирует digest pack и quote pack.

**Allowed writes:**
- `evidence.source_digests`
- `evidence.source_quotes`
- `core.project_artifacts`

**Approval mode:** `auto`, кроме high-risk цитат.

---

### 4.13. Research Design Agent
**Role:** выбирает evidence profile и оформляет research design.

**Allowed writes:**
- `core.project_evidence_profiles`
- `evidence.research_designs`
- `core.project_gate_reports`

**Approval mode:** `approval_required`

---

### 4.14. Analysis Execution Agent
**Role:** проводит analysis runs, если профиль требует.

**Allowed writes:**
- `evidence.analysis_runs`
- `core.project_artifacts`
- `core.project_gate_reports`

**Approval mode:** `auto`

---

### 4.15. Outline Architect Agent
**Role:** строит outline и evidence map.

**Allowed writes:**
- `article.article_outlines`
- `article.article_sections`
- `core.project_artifacts`

**Approval mode:** usually `auto`

---

### 4.16. Journal Fit Agent
**Role:** проверяет совместимость проекта со journal target.

**Allowed writes:**
- `core.project_journal_targets`
- `core.project_gate_reports`
- `policy.audit_events`

**Approval mode:** `approval_required`

---

### 4.17. Draft Composer Agent
**Role:** собирает controlled draft статьи.

**Retrieval profile:**
- `digests`
- `quotes`
- `journal_requirements`
- `project_memory`
- `style_memory`

**Allowed writes:**
- `article.article_versions`
- `article.article_sections`
- `policy.audit_events`

**Approval mode:** `auto` for intermediate drafts.

---

### 4.18. Style Alignment Agent
**Role:** выравнивает текст под авторский научный стиль.

**Allowed writes:**
- new `article.article_versions`
- `policy.audit_events`

**Approval mode:** mixed.

---

### 4.19. Citation Compliance Agent
**Role:** проверяет ссылки, цитаты и bibliography constraints.

**Allowed writes:**
- update `article.article_versions.citation_check_report`
- `core.project_gate_reports`
- `policy.audit_events`

**Approval mode:** `auto`, кроме override.

---

### 4.20. Revision Agent
**Role:** ведёт цикл доработки по reviewer comments.

**Allowed writes:**
- `article.article_revision_cycles`
- new `article.article_versions`
- `policy.audit_events`

**Approval mode:** `approval_required` for final revision submission.

---

## 5. Agent execution modes

### `auto`
Агент сам выполняет задачу и фиксирует результат.

### `approval_required`
Агент подготавливает результат, но final write/transition допускается только после approval.

### `manual_assist`
Агент ничего не фиксирует без прямой команды.

---

## 6. Execution pipeline

1. создаётся `agent_task`
2. оркестратор формирует `input_context`
3. стартует `agent_run`
4. агент делает вывод
5. policy engine валидирует выход
6. при необходимости создаётся `approval_request`
7. после approve `workflow-service` фиксирует transition
8. `audit-service` записывает событие

---

## 7. Главный принцип

**Агент не является источником истины.**
Источники истины:
- PostgreSQL
- policy rules
- approvals
- active bibliography snapshot
- locked project state

Агенты делают систему умной и продуктивной, но не снимают научную управляемость.
