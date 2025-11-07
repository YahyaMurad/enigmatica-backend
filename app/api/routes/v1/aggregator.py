from datetime import date as date_type
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.aggregator.activity_aggregator import ActivityAggregator
from app.core.dependencies import get_db
from app.models import (
    DailyActivity,
    DailyFileActivity,
    DailyLanguageActivity,
    DailyProjectActivity,
)

router = APIRouter(prefix="/api/v1/aggregator", tags=["aggregator"])


# ---------------------------------------
# POST /api/v1/aggregator/aggregate_daily
# ---------------------------------------
@router.post("/aggregate_daily")
def aggregate_daily(
    date: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if date:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        target_date = datetime.utcnow().date()

    aggregator = ActivityAggregator()
    result = aggregator.aggregate_daily_activity(db, target_date)

    for user_id, user_data in result.items():
        total_active_seconds = user_data.get("total_active_seconds", 0)
        projects = user_data.get("projects", {})

        total_projects = len(projects)
        total_files = sum(len(p["files"]) for p in projects.values())
        total_languages = len(
            {lang for p in projects.values() for lang in p.get("languages", {}).keys()}
        )

        daily_activity = DailyActivity(
            user_id=user_id,
            date=target_date,
            total_active_seconds=total_active_seconds,
            total_projects=total_projects,
            total_files_edited=total_files,
            total_languages=total_languages,
        )

        db.add(daily_activity)
        db.flush()

        for project_name, project_data in projects.items():
            project_total_seconds = project_data.get("total_seconds", 0)
            project_files = project_data.get("files", {})

            db.add(
                DailyProjectActivity(
                    daily_activity_id=daily_activity.id,
                    project_name=project_name,
                    total_seconds=project_total_seconds,
                    files_edited=len(project_files),
                )
            )

            for language, seconds in project_data.get("languages", {}).items():
                db.add(
                    DailyLanguageActivity(
                        daily_activity_id=daily_activity.id,
                        language=language or "Unknown",
                        total_seconds=seconds,
                    )
                )

            for entity, seconds in project_files.items():
                db.add(
                    DailyFileActivity(
                        daily_activity_id=daily_activity.id,
                        entity=entity,
                        project=project_name,
                        total_seconds=seconds,
                        total_line_changes=0,
                    )
                )

    db.commit()
    return {"date": str(target_date), "status": "aggregation complete"}
