# Tickets for Sprints 7–12

Этот документ детализирует вторую половину MVP roadmap: спринты **7–12**. Формат рассчитан на командную разработку: у каждого спринта есть цель, инженерный scope, список тикетов, demo-сценарий и критерии `go / no-go`.

---

# Sprint 7 — Digests, Quotes, Evidence Profile

## Цель
Сделать научное ядро статьи:
- digest pack
- quote pack
- evidence profile
- research design without forcing dataset in every case

## Ожидаемый результат спринта
Проект может получить:
- дайджесты по core sources;
- цитатный пакет;
- выбранный evidence profile;
- research design, который допускает обзорную статью, концептуальную статью или прикладной сценарий.

## Тикеты

### T7.1 — Implement source digests CRUD
**Что сделать**
- backend CRUD для `evidence.source_digests`
- endpoints:
  - `POST /sources/{id}/digests`
  - `GET /sources/{id}/digests`
  - `PATCH /digests/{digest_id}`

**Definition of Done**
- digest можно создать, прочитать, обновить;
- digest связан с конкретным source;
- digest хранит `digest_type`, `short_digest`, `methods_digest`, `findings_digest`, `limitations_digest`.

---

### T7.2 — Implement source quotes CRUD and quote validation entrypoints
**Что сделать**
- backend CRUD для `evidence.source_quotes`
- endpoints:
  - `POST /sources/{id}/quotes`
  - `GET /sources/{id}/quotes`
  - `PATCH /quotes/{quote_id}`
  - `POST /quotes/{quote_id}/verify`

**Definition of Done**
- цитата создаётся и хранится с `quote_mode`;
- есть флаг `verified`;
- direct verified quote запрещён для источника без нужного статуса.

---

### T7.3 — Add policy guard for direct quotes
**Что сделать**
- реализовать policy/service-level guard:
  - direct verified quote only if `source.validation_mode = fulltext_verified`
  - and `source.direct_quote_allowed = true`

**Definition of Done**
- нарушение даёт deterministic 4xx ошибку;
- покрыто тестами.

---

### T7.4 — Implement evidence profile selection
**Что сделать**
- CRUD/read endpoints для `core.evidence_profiles`
- endpoint выбора профиля проекту:
  - `POST /projects/{id}/evidence-profile`
  - `GET /projects/{id}/evidence-profile`

**Definition of Done**
- проект может выбрать profile;
- profile пишется в `project_evidence_profiles`;
- journal tier/work type учитываются в response metadata.

---

### T7.5 — Implement research design CRUD
**Что сделать**
- CRUD for `evidence.research_designs`
- endpoint:
  - `POST /projects/{id}/research-design`
  - `GET /projects/{id}/research-design`

**Definition of Done**
- research design сохраняет method, research question, object/subject, AI tools, reproducibility plan;
- design можно создать без dataset, если profile допускает.

---

### T7.6 — Seed initial evidence profiles
**Что сделать**
Добавить baseline profiles:
- `literature_review`
- `bibliometric_study`
- `conceptual_paper`
- `applied_ai_research`
- `rinc_theoretical`

**Definition of Done**
- profiles появляются в bootstrap/seed;
- доступны через API.

---

## Demo sprint 7
1. В проекте есть active bibliography snapshot.
2. Для 5 источников созданы digests.
3. Для 3 источников добавлены quotes.
4. Проекту назначен profile `literature_review`.
5. Создан research design без dataset.

## Go / No-Go
**Go**, если:
- digest/quote/evidence profile реально используются как связанные сущности;
- review-only статья не блокируется из-за отсутствия dataset.

**No-Go**, если:
- profiles декоративны;
- quotes не проверяются policy guard;
- research design не влияет на pipeline.

---

# Sprint 8 — Outline and Article Versions

## Цель
Сделать controlled article assembly.

## Ожидаемый результат
Из проекта с locked bibliography можно построить:
- outline
- section scaffolding
- первую article version

## Тикеты

### T8.1 — Implement article outline CRUD
**Что сделать**
- CRUD for `article.article_outlines`
- endpoints:
  - `POST /projects/{id}/outlines`
  - `GET /projects/{id}/outlines`
  - `GET /outlines/{outline_id}`

**Definition of Done**
- outline хранит `outline_json`, `argument_chain_json`, `required_sections_json`, `evidence_map_json`.

---

### T8.2 — Implement article sections CRUD
**Что сделать**
- CRUD for `article.article_sections`
- endpoints:
  - `POST /outlines/{outline_id}/sections`
  - `PATCH /sections/{section_id}`
  - `GET /projects/{id}/sections`

**Definition of Done**
- section связан с outline и project;
- section может хранить `source_links_json` и `quote_links_json`.

---

### T8.3 — Implement article version creation
**Что сделать**
- endpoint `POST /projects/{id}/article-versions`
- versioning logic by `version_no`

**Definition of Done**
- статья сохраняется как versioned object;
- можно получить список версий по проекту.

---

### T8.4 — Controlled writing guard
**Что сделать**
- article version creation only if:
  - project has active bibliography snapshot;
  - evidence profile selected;
  - no blocking gate reports.

**Definition of Done**
- создать draft без snapshot нельзя;
- guard покрыт тестами.

---

### T8.5 — Outline builder placeholder service
**Что сделать**
- service-layer placeholder, который собирает skeleton outline из:
  - evidence profile
  - digests
  - quotes
  - journal target if exists

**Definition of Done**
- outline может быть создан полуавтоматически;
- логика не хардкодится в router.

---

## Demo sprint 8
1. Проект имеет active bibliography snapshot.
2. Создаётся outline.
3. Создаются sections.
4. Создаётся article version v1.
5. Нельзя создать version для проекта без snapshot.

## Go / No-Go
**Go**, если:
- article version действительно зависит от project state;
- controlled writing guard работает.

**No-Go**, если:
- outline/versions не привязаны к evidence layer;
- можно писать статью в обход snapshot.

---

# Sprint 9 — Journal Layer and Compliance

## Цель
Сделать journal-aware article pipeline.

## Ожидаемый результат
Проект может выбрать журнал и получить compliance report.

## Тикеты

### T9.1 — Implement journal catalog API
**Что сделать**
- endpoints:
  - `GET /journals`
  - `GET /journals/{journal_id}`
  - `GET /journals/{journal_id}/requirements`

**Definition of Done**
- journal catalog читается из БД;
- требования versioned.

---

### T9.2 — Implement project journal target
**Что сделать**
- endpoints:
  - `POST /projects/{id}/journal-target`
  - `GET /projects/{id}/journal-target`
- writes to `core.project_journal_targets`

**Definition of Done**
- project может выбрать journal or journal tier;
- target может быть locked later.

---

### T9.3 — Implement journal fit check service
**Что сделать**
- endpoint `POST /projects/{id}/journal-fit-check`
- service that compares:
  - work type
  - evidence profile
  - draft structure
  - bibliography characteristics
  - journal requirements

**Definition of Done**
- fit check returns structured report;
- report сохраняется в gate reports or article reports.

---

### T9.4 — Add article formatting endpoint
**Что сделать**
- endpoint `POST /article-versions/{id}/format`
- output writes `formatted_text`

**Definition of Done**
- formatting запускается отдельно от raw version creation;
- report of formatting issues is returned.

---

### T9.5 — Implement citation compliance report
**Что сделать**
- article compliance service computes:
  - citations inside snapshot only
  - quote validity
  - bibliography fit
  - basic journal structure fit

**Definition of Done**
- result stored in `citation_check_report` and `requirement_check_report`;
- response is machine-readable.

---

## Demo sprint 9
1. Журнал выбран и привязан к проекту.
2. Draft проходит journal fit check.
3. Article version получает compliance report.
4. Форматированный текст сохраняется отдельно.

## Go / No-Go
**Go**, если:
- journal layer реально влияет на article pipeline;
- есть работающий compliance report.

**No-Go**, если:
- journal requirements хранятся, но не используются;
- formatting неотделима от version logic.

---

# Sprint 10 — Workflow and Approvals

## Цель
Сделать проектный pipeline процессным.

## Ожидаемый результат
Критические переходы идут только через workflow + approval.

## Тикеты

### T10.1 — Implement workflow state CRUD/service
**Что сделать**
- endpoints:
  - `GET /projects/{id}/workflow`
  - `GET /programs/{id}/workflow`
  - `POST /workflow/transition`

**Definition of Done**
- workflow state хранится централизованно;
- есть history of transitions.

---

### T10.2 — Implement project state machine guards
**Что сделать**
Ввести guards для ключевых переходов:
- `specialty_framing -> hypothesis_discovery`
- `source_verification -> bibliography_lock`
- `compliance_check -> submission_ready`

**Definition of Done**
- переходы валидируются централизованно;
- direct DB write не считается valid transition path.

---

### T10.3 — Implement approval requests API
**Что сделать**
- endpoints:
  - `GET /approvals`
  - `GET /approvals/{id}`
  - `POST /approvals`
  - `POST /approvals/{id}/approve`
  - `POST /approvals/{id}/reject`

**Definition of Done**
- approval request создаётся и меняет статус;
- human review action логируется.

---

### T10.4 — Wire approval-required transitions
**Что сделать**
Сделать обязательным approval для:
- specialities lock
- hypothesis lock
- bibliography lock
- evidence profile lock
- final submission_ready release

**Definition of Done**
- без approval state transition не коммитится.

---

### T10.5 — Add gate report integration
**Что сделать**
- transition guard должен читать `project_gate_reports`
- blocking issues stop transition

**Definition of Done**
- нельзя пройти в следующий state при active blocking issues.

---

## Demo sprint 10
1. Проект переводится между состояниями.
2. bibliography lock создаёт approval request.
3. Без approve state не двигается.
4. После approve transition commit проходит.

## Go / No-Go
**Go**, если:
- workflow нельзя обойти обычным CRUD;
- approval реально управляет критическими переходами.

**No-Go**, если:
- transitions разбросаны по разным роутам без общего ядра.

---

# Sprint 11 — Agent Runtime and RAG Metadata

## Цель
Поднять минимально рабочий агентный слой.

## Ожидаемый результат
Есть единый runtime для задач агентов, retrieval profiles и RAG metadata.

## Тикеты

### T11.1 — Implement RAG collections/documents/chunks CRUD
**Что сделать**
- endpoints:
  - `GET /rag/collections`
  - `POST /rag/collections`
  - `POST /rag/collections/{id}/documents`
  - `POST /rag/documents/{id}/chunks`

**Definition of Done**
- RAG metadata хранится централизованно;
- можно наполнить collections для personal corpus / verified sources / project memory.

---

### T11.2 — Implement retrieval profiles API
**Что сделать**
- endpoints:
  - `GET /retrieval-profiles`
  - `POST /retrieval-profiles`

**Definition of Done**
- retrieval profile хранит collection list, filters, top_k, rerank strategy.

---

### T11.3 — Implement agent tasks and agent runs API
**Что сделать**
- endpoints:
  - `POST /agent-tasks`
  - `GET /agent-tasks`
  - `GET /agent-tasks/{id}`
  - `POST /agent-tasks/{id}/run`
  - `GET /agent-runs/{id}`

**Definition of Done**
- task and run lifecycle сохраняются в БД;
- run log воспроизводим.

---

### T11.4 — Implement orchestrator next-step endpoint
**Что сделать**
- endpoints:
  - `POST /projects/{id}/orchestrate/next`
  - `POST /programs/{id}/orchestrate/next`

**Definition of Done**
- orchestrator возвращает next recommended action based on workflow state + policy.

---

### T11.5 — Add first 3 working agents through unified runtime
**Что сделать**
Поднять как минимум:
- Specialty Boundary Agent
- Bibliography Architect Agent
- Citation Compliance Agent

**Definition of Done**
- агент стартует через runtime;
- читает retrieval profile;
- пишет run output;
- создаёт effect through service layer or proposal object.

---

## Demo sprint 11
1. Создаётся retrieval profile.
2. Создаётся agent task.
3. Агент запускается.
4. Создаётся agent run.
5. Orchestrator выдаёт next step для проекта.

## Go / No-Go
**Go**, если:
- минимум 3 агента реально работают через единый runtime;
- RAG metadata используется, а не просто лежит в БД.

**No-Go**, если:
- agent layer остаётся только логом без поведения.

---

# Sprint 12 — Big Path Orchestration and Portfolio

## Цель
Сделать длинную академическую траекторию реально работающей.

## Ожидаемый результат
Program layer не просто хранит требования, а реально считает прогресс, дефициты и рекомендует следующие шаги.

## Тикеты

### T12.1 — Implement program tracks and project links APIs
**Что сделать**
- CRUD/read for:
  - `program_theme_tracks`
  - `program_project_links`

**Definition of Done**
- project can be linked to program with role and theme track.

---

### T12.2 — Implement portfolio entries CRUD/service
**Что сделать**
- endpoints:
  - `GET /programs/{id}/portfolio`
  - `POST /programs/{id}/portfolio`
  - `PATCH /portfolio/{entry_id}`

**Definition of Done**
- portfolio item can point to project and/or article version;
- publication status is tracked.

---

### T12.3 — Implement progress recalculation service
**Что сделать**
- endpoint `POST /programs/{id}/recalculate-progress`
- creates `program_progress_snapshots`

**Definition of Done**
- progress snapshot counts:
  - total required/completed articles
  - fresh article deficit
  - high-tier deficit
  - active project count
  - risk score

---

### T12.4 — Implement portfolio gap analysis endpoint
**Что сделать**
- endpoint `GET /programs/{id}/portfolio/gaps`

**Definition of Done**
- system returns structured gap analysis:
  - missing article count
  - missing high-tier items
  - missing recent publications
  - thematic imbalance

---

### T12.5 — Wire program-level agents
**Что сделать**
Поднять через unified runtime:
- Program Strategist Agent
- Portfolio Gap Agent
- Career Compliance Agent

**Definition of Done**
- program-level agents can run through same runtime as project-level agents.

---

### T12.6 — Implement program orchestrator next-step logic
**Что сделать**
- `POST /programs/{id}/orchestrate/next`
returns next strategic action:
- create project
- rebalance tracks
- increase recent publications
- push article to target journal tier

**Definition of Done**
- output is actionable and based on actual portfolio state.

---

## Demo sprint 12
1. Создаётся программа `Профессор 2029`.
2. В неё привязаны 3 проекта.
3. Одна article version попадает в portfolio.
4. Пересчитывается progress snapshot.
5. Gap analysis показывает дефициты.
6. Program orchestrator рекомендует следующий проект или действие.

## Go / No-Go
**Go**, если:
- Big Path даёт реальный strategic output;
- program layer связан с project/article data.

**No-Go**, если:
- Big Path остаётся просто красивым dashboard без управляющей логики.

---

# Финальный acceptance check после Sprint 12

Система считается прошедшей MVP wave 2, если одновременно выполняются все условия:

1. Есть active bibliography snapshot.
2. Evidence profile реально влияет на pipeline.
3. Article version строится на controlled data.
4. Workflow and approvals enforce critical transitions.
5. Минимум 3 project-level и 3 program-level agents работают через единый runtime.
6. Big Path считает дефициты и выдаёт next strategic action.

---

# Рекомендуемая очередность внутри wave 2

1. Sprint 7 — evidence layer
2. Sprint 8 — controlled drafting
3. Sprint 9 — journal fit & compliance
4. Sprint 10 — workflow & approvals
5. Sprint 11 — agent runtime & RAG metadata
6. Sprint 12 — Big Path orchestration

Такой порядок минимизирует риск: сначала доказываем научную управляемость статьи, потом включаем агентность и стратегический слой.
