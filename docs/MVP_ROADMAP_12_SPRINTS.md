# MVP Roadmap — 12 спринтов

Ниже — реалистичный roadmap для сборки MVP v1.0 как **Academic Research OS**. Каждый спринт должен заканчиваться демонстрацией, acceptance checklist и явным решением `go / no-go`.

Предполагаемая длительность спринта: **2 недели**.

---

## Sprint 1 — Platform skeleton

### Цель
Поднять инженерный каркас платформы.

### Scope
- FastAPI skeleton
- PostgreSQL connection
- Alembic migrations
- schema namespaces
- базовый auth
- healthcheck
- базовый audit middleware

### Проверка реализуемости
**Demo:**
- backend запускается в docker
- миграции применяются с нуля
- пользователь создаётся и читается
- audit event пишется

**Go, если:**
- миграции стабильны
- API доступен через Swagger
- есть smoke tests

---

## Sprint 2 — Program + Project core

### Цель
Сделать рабочие сущности Program и Research Project.

### Scope
- `big_path_templates`
- `big_path_programs`
- `program_requirements`
- `research_projects`
- `work_types`
- API `/programs`, `/projects`

### Проверка реализуемости
**Demo:**
- создаётся программа `Профессор 2029`
- добавляются требования
- создаётся исследовательский проект

**Go, если:**
- CRUD работает стабильно
- связи program/project не конфликтуют

---

## Sprint 3 — Source registry

### Цель
Собрать единый реестр источников.

### Scope
- `sources`
- `source_authors`
- `institutions`
- `project_sources`
- базовый поиск источников
- привязка источников к проектам

### Проверка реализуемости
**Demo:**
- в проект добавляются 20 источников
- фильтрация по году/валидации/каноничности работает
- один источник участвует в двух проектах

**Go, если:**
- нет хаотичного дублирования
- `project_sources` работает как M:N

---

## Sprint 4 — Fulltext ingestion

### Цель
Поднять локальный контур хранения full text.

### Scope
- `source_fulltexts`
- `source_fulltext_fragments`
- upload PDF/DOCX/MD
- parse job
- fragment storage

### Проверка реализуемости
**Demo:**
- загружается PDF
- full text сохраняется локально
- фрагменты извлекаются
- API отдаёт только metadata и fragments

**Go, если:**
- минимум 10 файлов проходят ingestion
- fulltext не экспонируется наружу целиком

---

## Sprint 5 — Verification + canonical logic

### Цель
Сделать верификацию источников и canonical exception flow.

### Scope
- `source_verification_reports`
- `source_evidence_chain`
- `canonical_source_trace_tasks`
- `source_interpretation_links`
- статусные поля источника

### Проверка реализуемости
**Demo:**
- один источник = fulltext verified
- один = metadata verified
- один = canonical unresolved
- для canonical строится evidence chain

**Go, если:**
- статусы реально влияют на дальнейшее использование
- canonical logic не ломает основную модель

---

## Sprint 6 — Bibliography governance

### Цель
Сделать управляемый bibliography snapshot.

### Scope
- `bibliography_snapshots`
- `bibliography_snapshot_items`
- active snapshot rule
- lock flow
- расчёт базовых квот

### Проверка реализуемости
**Demo:**
- создаётся snapshot на 30 источников
- snapshot lock проходит через API
- второй active snapshot невозможен без деактивации первого

**Go, если:**
- bibliography snapshot реально становится контрактом для writing pipeline

---

## Sprint 7 — Digests, quotes, evidence profile

### Цель
Сделать digest/quote/evidence ядро статьи.

### Scope
- `source_digests`
- `source_quotes`
- `evidence_profiles`
- `project_evidence_profiles`
- `research_designs`

### Проверка реализуемости
**Demo:**
- для core sources созданы digests
- извлечены quotes
- выбран evidence profile `literature_review`
- проект может двигаться без dataset, если это допустимо

**Go, если:**
- минимум 3 evidence profiles реально поддерживаются
- review-only profile проходит pipeline

---

## Sprint 8 — Outline + article versions

### Цель
Собрать первый controlled drafting pipeline.

### Scope
- `article_outlines`
- `article_sections`
- `article_versions`
- outline builder
- draft persistence

### Проверка реализуемости
**Demo:**
- из locked bibliography создаётся outline
- sections собираются
- появляется `article version v1`

**Go, если:**
- статья собирается только из project state и active snapshot
- нельзя незаметно подмешать внешние источники

---

## Sprint 9 — Journal layer + compliance

### Цель
Сделать статью валидируемой под журнал.

### Scope
- `journals`
- `journal_requirements`
- `project_journal_targets`
- citation check
- requirement check
- formatting

### Проверка реализуемости
**Demo:**
- журнал выбран и зафиксирован
- article version проверяется на требования журнала
- формируется compliance report

**Go, если:**
- journal layer реально влияет на pipeline
- статья может дойти до `submission_ready`

---

## Sprint 10 — Workflow + approvals

### Цель
Сделать систему процессной, а не CRUD-овой.

### Scope
- `workflow_states`
- `workflow_transitions`
- `approval_requests`
- `human_review_actions`
- `project_gate_reports`
- project state machine

### Проверка реализуемости
**Demo:**
- проект проходит state transitions
- bibliography lock требует approval
- без approval state не меняется

**Go, если:**
- workflow нельзя обойти прямыми CRUD вызовами
- approvals реально блокируют критические переходы

---

## Sprint 11 — Agent runtime + RAG metadata

### Цель
Поднять минимально рабочий agent layer.

### Scope
- `agent_tasks`
- `agent_runs`
- `retrieval_profiles`
- `rag_collections`
- `rag_documents`
- `rag_chunks`
- `project_memory_entries`
- 3 рабочих агента:
  - Specialty Boundary Agent
  - Bibliography Architect Agent
  - Citation Compliance Agent

### Проверка реализуемости
**Demo:**
- создаётся agent task
- агент стартует через runtime
- пишется agent run log
- orchestrator предлагает next step

**Go, если:**
- минимум 3 агента работают через единый runtime
- есть воспроизводимый run log

---

## Sprint 12 — Big Path orchestration + portfolio

### Цель
Сделать долгую академическую траекторию реально работающей.

### Scope
- `program_theme_tracks`
- `program_project_links`
- `publication_portfolio_entries`
- `program_progress_snapshots`
- `program_milestones`
- `publication_batches`
- Program agents:
  - Program Strategist Agent
  - Portfolio Gap Agent
  - Career Compliance Agent

### Проверка реализуемости
**Demo:**
- создаётся программа `Профессор 2029`
- привязаны 3 проекта
- хотя бы 1 статья попадает в portfolio
- progress snapshot показывает дефициты и прогресс
- program orchestrator рекомендует следующий проект

**Go, если:**
- Big Path даёт actionable planning output
- portfolio связан с project/article data

---

## End-to-end acceptance scenario после Sprint 12

### Должно уметь работать вместе:
1. создать программу;
2. создать проект;
3. задать специальности;
4. сформировать гипотезу;
5. загрузить full texts;
6. верифицировать источники;
7. собрать bibliography snapshot;
8. выбрать evidence profile;
9. построить outline;
10. собрать draft;
11. пройти compliance;
12. добавить статью в portfolio;
13. обновить progress snapshot по программе.

---

## Общие критерии жизнеспособности MVP v1.0

### 1. Controlled writing works
Draft собирается только из locked project state.

### 2. Verification logic works
Источник может быть verified / secondary / canonical exception, и это реально влияет на использование.

### 3. Workflow is enforceable
Нельзя перескочить критические стадии без approval/policy.

### 4. Agents are real
Есть минимум 3–5 работающих субагентов с run log.

### 5. Big Path is actionable
Система показывает дефициты и рекомендует следующие шаги по большой цели.

---

## Что резать первым при перегрузе

Можно урезать:
1. advanced style memory
2. сложные journal heuristics
3. глубокие multi-agent сценарии
4. grant-specific advanced logic
5. сложные scientometric runs

Нельзя резать:
1. source registry
2. local fulltext storage
3. verification statuses
4. bibliography snapshots
5. workflow + approvals
6. article versions
7. portfolio core

---

## Обязательные артефакты завершения каждого спринта

1. demo script
2. acceptance checklist
3. regression smoke tests
4. architecture delta note

Это обязательная дисциплина, иначе проект быстро расползётся по смыслу.
