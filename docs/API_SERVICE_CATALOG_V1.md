# API и сервисный каталог v1.0

Ниже — целевая backend-декомпозиция для **Academic Research OS**. Предполагается modular monolith на FastAPI с чёткими bounded contexts.

## Главный принцип

- один service owner на группу таблиц;
- один table owner — один write-path;
- критические переходы идут через `workflow-service + policy-service + approval-service`;
- агенты пишут в систему через сервисный слой, а не напрямую в БД.

---

## 1. Auth service

### Назначение
Аутентификация и профиль пользователя.

### Таблицы
- `core.users`

### API
- `POST /auth/login`
- `GET /auth/me`
- `PATCH /auth/me`

---

## 2. Program service

### Назначение
Управление Big Path Program.

### Таблицы
- `program.big_path_templates`
- `program.big_path_programs`
- `program.program_requirements`
- `program.program_milestones`
- `program.program_theme_tracks`
- `program.program_project_links`
- `program.program_publication_targets`
- `program.publication_batches`

### API
- `POST /programs`
- `GET /programs`
- `GET /programs/{program_id}`
- `PATCH /programs/{program_id}`
- `POST /programs/{program_id}/apply-template`
- `GET /programs/{program_id}/requirements`
- `POST /programs/{program_id}/requirements`
- `GET /programs/{program_id}/tracks`
- `POST /programs/{program_id}/tracks`
- `GET /programs/{program_id}/milestones`
- `POST /programs/{program_id}/milestones`
- `POST /programs/{program_id}/projects/{project_id}`

---

## 3. Portfolio service

### Назначение
Публикационный портфель и прогресс по программе.

### Таблицы
- `program.publication_portfolio_entries`
- `program.program_progress_snapshots`

### API
- `GET /programs/{program_id}/portfolio`
- `POST /programs/{program_id}/portfolio`
- `PATCH /portfolio/{entry_id}`
- `GET /programs/{program_id}/portfolio/gaps`
- `POST /programs/{program_id}/recalculate-progress`

---

## 4. Project service

### Назначение
Research Project как единица работы.

### Таблицы
- `core.research_projects`
- `core.project_memory_entries`
- `core.project_artifacts`
- `core.project_gate_reports`
- `core.project_journal_targets`

### API
- `POST /projects`
- `GET /projects`
- `GET /projects/{project_id}`
- `PATCH /projects/{project_id}`
- `GET /projects/{project_id}/memory`
- `POST /projects/{project_id}/memory`
- `GET /projects/{project_id}/artifacts`
- `POST /projects/{project_id}/artifacts`
- `GET /projects/{project_id}/gate-reports`

---

## 5. Specialty service

### Таблицы
- `core.specialty_passports`
- `core.project_specialties`

### API
- `GET /specialties`
- `GET /specialties/{specialty_id}`
- `POST /projects/{project_id}/specialties`
- `PATCH /project-specialties/{id}`
- `POST /projects/{project_id}/specialties/lock`

---

## 6. Hypothesis service

### Таблицы
- `core.research_hypotheses`
- `core.gap_evidence`

### API
- `GET /projects/{project_id}/hypotheses`
- `POST /projects/{project_id}/hypotheses`
- `PATCH /hypotheses/{hypothesis_id}`
- `POST /hypotheses/{hypothesis_id}/lock`
- `GET /hypotheses/{hypothesis_id}/gap-evidence`
- `POST /hypotheses/{hypothesis_id}/gap-evidence`

---

## 7. Reference service

### Таблицы
- `source.sources`
- `source.source_authors`
- `source.institutions`
- `source.source_ingestion_jobs`
- `source.source_raw_records`

### API
- `POST /sources`
- `GET /sources`
- `GET /sources/{source_id}`
- `PATCH /sources/{source_id}`
- `POST /sources/{source_id}/authors`
- `POST /sources/ingestion-jobs`
- `GET /ingestion-jobs/{job_id}`
- `POST /ingestion-jobs/{job_id}/raw-records/normalize`

---

## 8. Fulltext service

### Таблицы
- `verify.source_fulltexts`
- `verify.source_fulltext_fragments`

### API
- `POST /sources/{source_id}/fulltext`
- `GET /sources/{source_id}/fulltext`
- `POST /sources/{source_id}/fulltext/parse`
- `GET /sources/{source_id}/fragments`
- `POST /sources/{source_id}/fragments/reindex`

Принцип: полный текст не отдаётся наружу целиком, только metadata и fragments.

---

## 9. Verification service

### Таблицы
- `verify.source_verification_reports`
- `verify.source_evidence_chain`
- `verify.canonical_source_trace_tasks`
- `verify.source_interpretation_links`

### API
- `POST /sources/{source_id}/verify`
- `GET /sources/{source_id}/verification`
- `POST /sources/{source_id}/evidence-chain`
- `GET /sources/{source_id}/evidence-chain`
- `POST /sources/{source_id}/canonical-trace`
- `GET /canonical-trace-tasks/{task_id}`
- `PATCH /canonical-trace-tasks/{task_id}`
- `POST /sources/{source_id}/interpretations`

---

## 10. Bibliography service

### Таблицы
- `evidence.project_sources`
- `evidence.bibliography_snapshots`
- `evidence.bibliography_snapshot_items`

### API
- `POST /projects/{project_id}/sources`
- `GET /projects/{project_id}/sources`
- `PATCH /project-sources/{id}`
- `POST /projects/{project_id}/bibliography-snapshots`
- `GET /projects/{project_id}/bibliography-snapshots`
- `GET /bibliography-snapshots/{snapshot_id}`
- `POST /bibliography-snapshots/{snapshot_id}/lock`
- `POST /bibliography-snapshots/{snapshot_id}/activate`

Ключевое правило: draft assembly допускается только с `active bibliography snapshot`.

---

## 11. Digest service

### Таблицы
- `evidence.source_digests`

### API
- `POST /sources/{source_id}/digests`
- `GET /sources/{source_id}/digests`
- `PATCH /digests/{digest_id}`

---

## 12. Quote service

### Таблицы
- `evidence.source_quotes`

### API
- `POST /sources/{source_id}/quotes`
- `GET /sources/{source_id}/quotes`
- `PATCH /quotes/{quote_id}`
- `POST /sources/{source_id}/quotes/extract`
- `POST /quotes/{quote_id}/verify`

Rule: `direct_verified` допустим только для источников с `validation_mode=fulltext_verified` и `direct_quote_allowed=true`.

---

## 13. Research service

### Таблицы
- `core.evidence_profiles`
- `core.project_evidence_profiles`
- `evidence.research_designs`
- `evidence.datasets`
- `evidence.analysis_runs`
- `core.method_catalog`

### API
- `GET /work-types`
- `GET /evidence-profiles`
- `POST /projects/{project_id}/evidence-profile`
- `GET /projects/{project_id}/evidence-profile`
- `POST /projects/{project_id}/research-design`
- `GET /projects/{project_id}/research-design`
- `POST /projects/{project_id}/datasets`
- `GET /projects/{project_id}/datasets`
- `POST /projects/{project_id}/analysis-runs`
- `GET /projects/{project_id}/analysis-runs`

---

## 14. Journal service

### Таблицы
- `core.journals`
- `core.journal_requirements`
- `core.project_journal_targets`

### API
- `GET /journals`
- `GET /journals/{journal_id}`
- `GET /journals/{journal_id}/requirements`
- `POST /projects/{project_id}/journal-target`
- `GET /projects/{project_id}/journal-target`
- `POST /projects/{project_id}/journal-fit-check`

---

## 15. Article service

### Таблицы
- `article.article_outlines`
- `article.article_sections`
- `article.article_versions`
- `article.article_submissions`
- `article.article_revision_cycles`

### API
- `POST /projects/{project_id}/outlines`
- `GET /projects/{project_id}/outlines`
- `GET /outlines/{outline_id}`
- `POST /outlines/{outline_id}/sections`
- `PATCH /sections/{section_id}`
- `POST /projects/{project_id}/article-versions`
- `GET /projects/{project_id}/article-versions`
- `GET /article-versions/{version_id}`
- `POST /article-versions/{version_id}/format`
- `POST /projects/{project_id}/submissions`
- `GET /projects/{project_id}/submissions`
- `PATCH /submissions/{submission_id}`
- `POST /submissions/{submission_id}/revision-cycles`

---

## 16. RAG service

### Таблицы
- `rag.rag_collections`
- `rag.rag_documents`
- `rag.rag_chunks`
- `agent.retrieval_profiles`

### API
- `GET /rag/collections`
- `POST /rag/collections`
- `POST /rag/collections/{collection_id}/documents`
- `POST /rag/documents/{document_id}/chunks`
- `POST /rag/retrieve`
- `GET /retrieval-profiles`
- `POST /retrieval-profiles`

---

## 17. Style memory service

### Таблицы
- `core.author_profiles`
- `core.author_corpus_documents`
- `core.style_profiles`
- `core.style_constraints`

### API
- `POST /author-profiles`
- `GET /author-profiles/{id}`
- `POST /author-profiles/{id}/corpus-documents`
- `POST /author-profiles/{id}/style-profiles/extract`
- `GET /author-profiles/{id}/style-profiles`
- `POST /projects/{project_id}/style-constraints`

---

## 18. Workflow service

### Таблицы
- `agent.workflow_states`
- `agent.workflow_transitions`
- `core.project_gate_reports`

### API
- `GET /projects/{project_id}/workflow`
- `GET /programs/{program_id}/workflow`
- `POST /workflow/transition`
- `GET /workflow/history`

---

## 19. Agent runtime service

### Таблицы
- `agent.agent_tasks`
- `agent.agent_runs`
- `agent.retrieval_profiles`
- `core.project_memory_entries`

### API
- `POST /agent-tasks`
- `GET /agent-tasks`
- `GET /agent-tasks/{task_id}`
- `POST /agent-tasks/{task_id}/run`
- `GET /agent-runs/{run_id}`
- `POST /projects/{project_id}/orchestrate/next`
- `POST /programs/{program_id}/orchestrate/next`

---

## 20. Policy service

### Таблицы
- `policy.policy_sets`
- `policy.policy_rules`
- `policy.policy_overrides`

### API
- `GET /policy-sets`
- `GET /policy-rules`
- `POST /policy/evaluate`
- `POST /policy-overrides`
- `GET /policy-overrides`

---

## 21. Approval service

### Таблицы
- `policy.approval_requests`
- `policy.human_review_actions`

### API
- `GET /approvals`
- `GET /approvals/{approval_id}`
- `POST /approvals`
- `POST /approvals/{approval_id}/approve`
- `POST /approvals/{approval_id}/reject`
- `POST /approvals/{approval_id}/comment`

---

## 22. Audit service

### Таблицы
- `policy.audit_events`

### API
- `GET /audit`
- `GET /audit/{event_id}`

---

## 23. Сервисные ownership boundaries

### Program service
owner of:
- `big_path_*`
- `program_*`
- `publication_batches`

### Portfolio service
owner of:
- `publication_portfolio_entries`
- `program_progress_snapshots`

### Project service
owner of:
- `research_projects`
- `project_memory_entries`
- `project_artifacts`
- `project_gate_reports`
- `project_journal_targets`

### Reference service
owner of:
- `sources`
- `source_authors`
- `institutions`
- `source_ingestion_jobs`
- `source_raw_records`

### Fulltext service
owner of:
- `source_fulltexts`
- `source_fulltext_fragments`

### Verification service
owner of:
- `source_verification_reports`
- `source_evidence_chain`
- `canonical_source_trace_tasks`
- `source_interpretation_links`

### Bibliography service
owner of:
- `project_sources`
- `bibliography_snapshots`
- `bibliography_snapshot_items`

### Article service
owner of:
- `article_outlines`
- `article_sections`
- `article_versions`
- `article_submissions`
- `article_revision_cycles`

### Agent runtime service
owner of:
- `agent_tasks`
- `agent_runs`
- `retrieval_profiles`

### Policy service
owner of:
- `policy_sets`
- `policy_rules`
- `policy_overrides`

### Approval service
owner of:
- `approval_requests`
- `human_review_actions`

### RAG service
owner of:
- `rag_collections`
- `rag_documents`
- `rag_chunks`

---

## 24. Domain events

### Project events
- `project.created`
- `project.specialties.locked`
- `project.hypothesis.locked`
- `project.bibliography.locked`
- `project.evidence_profile.selected`
- `project.outline.created`
- `project.article_version.created`

### Source events
- `source.created`
- `source.fulltext.uploaded`
- `source.fulltext.parsed`
- `source.verified`
- `source.canonical_trace.created`
- `source.digest.created`
- `source.quote.created`

### Program events
- `program.created`
- `program.template.applied`
- `program.progress.recalculated`
- `program.portfolio.updated`

### Approval events
- `approval.requested`
- `approval.approved`
- `approval.rejected`

---

## 25. Internal-only mechanics

Не стоит открывать как публичный API:
- low-level policy evaluation internals;
- direct RAG chunk low-level writes;
- auto-lock transitions;
- internal agent step execution internals;
- style extraction internals;
- compliance internal heuristics.

---

## 26. Итоговая backend формула

`FastAPI modular monolith + PostgreSQL + local object storage + vector index + workers + policy/approval/workflow layer`

Это даёт управляемый backend, где БД и API стыкуются без зазоров.
