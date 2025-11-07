from datetime import datetime, timedelta
from pprint import pprint

from sqlalchemy.orm import Session

from app.models import Heartbeat


class ActivityAggregator:
    def __init__(self):
        pass

    def aggregate_daily_activity(self, db: Session, target_date: datetime):
        start = datetime(target_date.year, target_date.month, target_date.day)
        end = start + timedelta(days=1)

        heartbeats = (
            db.query(Heartbeat)
            .filter(Heartbeat.time >= start, Heartbeat.time < end)
            .order_by(Heartbeat.user_id, Heartbeat.alternate_project, Heartbeat.time)
            .all()
        )

        results = {}

        for hb in heartbeats:
            key = (hb.user_id, hb.alternate_project, hb.language, hb.entity)
            results.setdefault(key, []).append(hb.time)

        user_daily_data = {}

        for (user_id, project, language, entity), timestamps in results.items():
            timestamps.sort()
            total_seconds = sum(
                (t2 - t1).total_seconds()
                for t1, t2 in zip(timestamps, timestamps[1:])
                if (t2 - t1).total_seconds() < 120
            )

            user_data = user_daily_data.setdefault(
                user_id, {"total_active_seconds": 0, "projects": {}}
            )

            project_data = user_data["projects"].setdefault(
                project, {"total_seconds": 0, "languages": {}, "files": {}}
            )

            user_data["total_active_seconds"] += total_seconds
            project_data["total_seconds"] += total_seconds

            project_data["languages"][language] = (
                project_data["languages"].get(language, 0) + total_seconds
            )

            project_data["files"][entity] = (
                project_data["files"].get(entity, 0) + total_seconds
            )

        return user_daily_data


if __name__ == "__main__":
    agg = ActivityAggregator()

    from app.core.dependencies import get_db

    db_gen = get_db()

    db = next(db_gen)
    try:
        result = agg.aggregate_daily_activity(db, datetime(2025, 11, 5))
        pprint(result)
    finally:
        db_gen.close()
