from __future__ import annotations

from sqlalchemy.orm import Session

from .models import ProgramTemplate, WorkType


def ensure_bootstrap_data(db: Session) -> None:
    if not db.query(WorkType).count():
        db.add_all(
            [
                WorkType(name="literature_review", description="Narrative or systematic literature review"),
                WorkType(name="bibliometric_study", description="Bibliometric or scientometric study"),
                WorkType(name="conceptual_paper", description="Conceptual or theoretical article"),
                WorkType(name="applied_ai_research", description="Applied AI-assisted research"),
                WorkType(name="rinc_theoretical", description="Theoretical article for RINC-like target"),
            ]
        )

    if not db.query(ProgramTemplate).count():
        db.add_all(
            [
                ProgramTemplate(
                    name="professor_default",
                    program_type="professor",
                    description="Default publication path template for professor track",
                    rules_json='{"articles_total": 20, "recent_articles_min": 5, "recent_years": 3}',
                    default_time_horizon_months=36,
                ),
                ProgramTemplate(
                    name="grant_default",
                    program_type="grant",
                    description="Grant delivery template",
                    rules_json='{"articles_total": 10}',
                    default_time_horizon_months=12,
                ),
            ]
        )

    db.commit()
