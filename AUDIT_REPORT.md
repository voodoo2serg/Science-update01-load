# Audit report for `voodoo2serg/Science`

## What was reviewed
- repository structure visible on GitHub
- backend raw files
- bot raw files
- Docker and compose files

## Main issues found
1. Source files are stored in one-line Python format, which makes maintenance and review fragile.
2. Database schema is created at app startup with `create_all`, without migrations.
3. Backend is published directly on port 8000 without reverse proxy.
4. PostgreSQL is not exposed in compose, which is good, but there is no separation of prod/staging and no backup flow.
5. File upload had no type or size validation.
6. LLM safety relied only on prompt wording and had no explicit policy gate.
7. Containers ran as root in both backend and bot.
8. n8n was exposed without auth in the original compose file.
9. Demo payment endpoint existed, but request body validation was weak.
10. No one-command server bootstrap script for Debian 13.

## Integrity notes
I could inspect the public repository tree and raw files, but I could not push directly to the remote GitHub repository from this environment. The branch attached in this package is prepared locally and can be pushed by you.

## Security posture after hardening
- upload validation: added
- LLM policy layer: added
- non-root containers: added
- nginx reverse proxy: added
- n8n basic auth: added
- stronger settings validation: added
- compose healthchecks: added

## Remaining gaps before full production
- Alembic migrations
- real payment provider integration
- S3/MinIO instead of local volume
- RBAC/auth for web layer
- backup/restore automation
- HTTPS termination with Let's Encrypt
