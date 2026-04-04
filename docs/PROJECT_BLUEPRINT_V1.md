# Project Blueprint v1.0

Этот документ собирает в одном месте всю целевую трансформацию репозитория `Science-update01-load` из MVP `Science Concierge` в **Academic Research OS** — платформу управляемого научного производства.

## 1. Что было

Исходный репозиторий — это MVP сервиса сопровождения исследователя:
- FastAPI backend
- PostgreSQL
- Telegram bot
- n8n
- загрузка файлов
- генерация безопасного черновика
- запросы на экспертизу
- подписка и платежный слой

Это хорошая SaaS-основа, но не полноценная research platform.

## 2. Во что превращается проект

Целевое состояние — **Academic Research OS**:
- управление длинной академической траекторией (`Big Path`)
- управление research-проектами
- единая база научных источников
- локальное хранилище полных текстов только для верификации
- управляемая bibliography snapshot
- канонические источники без полного текста
- multi-collection RAG
- субагенты по этапам
- controlled article assembly
- journal compliance
- publication portfolio

## 3. Главная архитектурная формула

`Big Path -> Research Project -> Source Intelligence -> Policy -> Agents -> RAG -> Article -> Portfolio`

## 4. Главные сущности

### Big Path
- программа длинной цели: кандидатская, докторская, доцент, профессор, PhD, grant
- хранит требования, milestones, thematic tracks, publication targets, portfolio

### Research Project
- единица научной работы
- тема, проблема, гипотеза, gap, specialities, evidence profile, journal target

### Source Intelligence
- единая база источников
- metadata, роли в проекте, fulltext status, verification status, digests, quotes, canonical exception logic

### Article Production
- outline
- sections
- versions
- submissions
- revisions

## 5. Почему здесь нужен ИИ

ИИ в этой системе не декоративен и не является единственным центром принятия решений.

Он присутствует в трёх режимах:

### 1. Reasoning layer
Формирует гипотезы, structure of argument, digests, draft text.

### 2. Memory layer
Через RAG работает с:
- personal corpus
- verified sources
- canonical sources
- quotes
- digests
- specialty passports
- journal requirements
- methods library
- project memory
- program memory
- style memory

### 3. Execution layer
Субагенты двигают проект между стадиями.

## 6. Субагенты

### Program-level
- Program Strategist Agent
- Portfolio Gap Agent
- Publication Planning Agent
- Deadline Control Agent
- Career Compliance Agent

### Project-level
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

## 7. Workflow

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

## 8. Полные тексты и научная корректность

Полные тексты хранятся только локально и используются только для:
- верификации существования статьи
- извлечения фрагментов
- подготовки качественного дайджеста
- проверки цитат
- поиска ложных ссылок
- антиплагиатной сверки

Система не является библиотекой для внешнего распространения full text.

## 9. Канонические источники

Система поддерживает случай, когда:
- источник методологически фундаментален
- оригинальный текст отсутствует в локальном архиве
- существование подтверждается вторичным корпусом, каталогами, архивными следами

В этом случае источник может использоваться как:
- canonical foundation
- methodological foundation
- bibliography item

Но не может использоваться для неподтверждённой прямой цитаты.

## 10. Управляемая библиография

Библиография в системе — это не просто список источников, а **snapshot**:
- плановое число источников
- +20% расширенный пул
- квоты RU/foreign
- квоты свежести
- системные источники
- core idea sources
- partner/self citation layer

После `lock` активный snapshot становится контрактом для writing pipeline.

## 11. Сервисная декомпозиция

Ключевые backend-модули:
- auth-service
- program-service
- portfolio-service
- project-service
- specialty-service
- hypothesis-service
- reference-service
- fulltext-service
- verification-service
- bibliography-service
- digest-service
- quote-service
- research-service
- journal-service
- article-service
- rag-service
- style-memory-service
- workflow-service
- agent-runtime-service
- policy-service
- approval-service
- audit-service

## 12. DDL и модель данных

База проектируется как PostgreSQL source of truth со schema namespace:
- `core`
- `program`
- `source`
- `verify`
- `evidence`
- `article`
- `agent`
- `policy`
- `rag`

Полный baseline DDL см. в `docs/DB_DDL_V1.sql`.

## 13. Каталог API

Полный service/API catalog см. в `docs/API_SERVICE_CATALOG_V1.md`.

Он фиксирует:
- ownership границы сервисов
- REST endpoints
- события и фоновые задачи
- write ownership по таблицам

## 14. Agent contracts и workflow

Подробная спецификация state machine и контрактов субагентов находится в `docs/AGENTS_AND_WORKFLOWS_V1.md`.

## 15. Реализация по спринтам

План поставки MVP на 12 спринтов с чёткой проверкой реализуемости после каждого спринта — в `docs/MVP_ROADMAP_12_SPRINTS.md`.

## 16. Практический план для команды

### Шаг 1
Сохранить текущий продукт как legacy MVP и не ломать его ad-hoc правками.

### Шаг 2
Поднять DDL baseline и Alembic migration scaffold.

### Шаг 3
Сделать новые домены в таком порядке:
1. projects
2. sources
3. fulltexts
4. verification
5. bibliography snapshots
6. evidence profiles
7. article versions
8. workflow + approvals
9. agent runtime
10. portfolio + Big Path

### Шаг 4
После устойчивости data layer начинать включать агентов и orchestration.

## 17. Главный инженерный принцип

**Сначала источник истины и управляемость, потом writing, потом агентность, потом длинная академическая стратегия.**

То есть:
- сначала база данных и контуры истины;
- потом verification и bibliography governance;
- потом controlled article assembly;
- потом subagents;
- потом Big Path orchestration.

## 18. Карта документов в репозитории

- `ARCHITECTURE.md` — целевая архитектура уровня системы
- `docs/PROJECT_BLUEPRINT_V1.md` — этот обзорный документ
- `docs/DB_DDL_V1.sql` — PostgreSQL baseline
- `docs/API_SERVICE_CATALOG_V1.md` — каталог API и сервисов
- `docs/AGENTS_AND_WORKFLOWS_V1.md` — state machine и агенты
- `docs/MVP_ROADMAP_12_SPRINTS.md` — реализация по спринтам

Этот набор делает репозиторий самодостаточной проектной базой для запуска следующей инженерной фазы.
