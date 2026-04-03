# Academic Research OS v1.0

Этот документ переводит исходный MVP `Science Concierge` в целевую архитектуру платформы для управляемого научного производства.

## Цель

Система должна уметь:
- вести долгую академическую траекторию (`Big Path`): кандидатская, докторская, доцент, профессор, PhD, grant;
- запускать и сопровождать отдельные research-проекты;
- собирать и фиксировать управляемую библиографию;
- хранить полные тексты локально только для верификации, дайджеста, проверки цитат и антиплагиатной сверки;
- поддерживать канонические источники даже при отсутствии полного текста;
- использовать multi-RAG и субагентов по этапам;
- собирать статью под журнал или ГОСТ с контролем ссылок и доказательности.

## Архитектурная формула

`Big Path -> Research Project -> Source Intelligence -> Policy -> Agents -> RAG -> Article -> Portfolio`

## Главные слои

### 1. Big Path Layer
Стратегический уровень длинной цели.

Сущности:
- `big_path_programs`
- `big_path_templates`
- `program_requirements`
- `program_theme_tracks`
- `publication_portfolio_entries`
- `program_progress_snapshots`

### 2. Research Project Layer
Единица исследования и будущей статьи.

Сущности:
- `research_projects`
- `project_specialties`
- `research_hypotheses`
- `project_evidence_profiles`
- `project_artifacts`
- `project_gate_reports`

### 3. Source Intelligence Layer
Единая база научных источников.

Сущности:
- `sources`
- `project_sources`
- `source_fulltexts`
- `source_verification_reports`
- `source_evidence_chain`
- `source_digests`
- `source_quotes`
- `bibliography_snapshots`

### 4. Fulltext Verification Layer
Полные тексты хранятся **только локально** и используются только для:
- верификации существования статьи;
- проверки цитат;
- качественного дайджеста;
- поиска ложных ссылок;
- антиплагиатной сверки.

### 5. Multi-Collection RAG Layer
Коллекции:
- personal corpus;
- verified sources;
- canonical sources;
- quotes;
- digests;
- specialty passports;
- journal requirements;
- methods library;
- project memory;
- program memory;
- style memory.

### 6. Agent Layer
Project-level:
- Project Intake Agent
- Specialty Boundary Agent
- Hypothesis Discovery Agent
- Bibliography Architect Agent
- Source Verification Agent
- Canonical Trace Agent
- Digest & Quote Agent
- Research Design Agent
- Analysis Execution Agent
- Outline Architect Agent
- Journal Fit Agent
- Draft Composer Agent
- Style Alignment Agent
- Citation Compliance Agent
- Revision Agent

Program-level:
- Program Strategist Agent
- Portfolio Gap Agent
- Publication Planning Agent
- Deadline Control Agent
- Career Compliance Agent

### 7. Policy + Approval Layer
Критические переходы не происходят автоматически без policy-check и, где нужно, без human approval.

Approval-required точки:
- specialties lock;
- hypothesis lock;
- bibliography lock;
- canonical exception;
- evidence profile lock;
- journal target lock;
- final submission-ready release.

## Workflow

### Program states
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

### Project states
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

## Принципы реализации

1. PostgreSQL — source of truth.
2. RAG не заменяет БД, а работает как retrieval/memory слой.
3. Full text — только локально.
4. Один table owner = один service owner.
5. Controlled writing всегда идёт только на основе `active bibliography snapshot`.
6. Канонические источники без полного текста допускаются, но не могут использоваться для неподтверждённых прямых цитат.

## Структура документации

- `ARCHITECTURE.md` — этот документ
- `docs/DB_DDL_V1.sql` — PostgreSQL DDL v1.0
- `docs/API_SERVICE_CATALOG_V1.md` — каталог сервисов и API
- `docs/AGENTS_AND_WORKFLOWS_V1.md` — state machine + контракты субагентов
- `docs/MVP_ROADMAP_12_SPRINTS.md` — roadmap на 12 спринтов

## Рекомендуемый следующий шаг для команды

1. Стабилизировать текущий backend под modular monolith.
2. Поднять DDL и Alembic миграции на отдельной ветке инфраструктуры.
3. Реализовать первые домены в таком порядке:
   - projects
   - sources
   - fulltexts
   - verification
   - bibliography snapshots
   - article versions
   - workflow / approvals
4. После этого включать agent runtime и Big Path orchestration.
