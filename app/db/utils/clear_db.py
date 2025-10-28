from sqlalchemy import text

from app.db.session import SessionLocal


def clear_database():
    db = SessionLocal()
    try:
        print("Clearing database...")

        db.execute(
            text(
                "TRUNCATE TABLE "
                "heartbeats, machines, daily_activity, users "
                "RESTART IDENTITY CASCADE;"
            )
        )

        db.commit()
        print("[SUCCESS] Tables cleared and primary keys reset.")

    except Exception as e:
        db.rollback()
        print("Error while clearing DB:", e)
    finally:
        db.close()


if __name__ == "__main__":
    clear_database()
