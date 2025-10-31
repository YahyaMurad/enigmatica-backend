from sqlalchemy import text

from app.db.session import SessionLocal
from app.models.models import Base


def clear_database():
    db = SessionLocal()
    try:
        print("Clearing database dynamically...")

        table_names = Base.metadata.tables.keys()
        if not table_names:
            print(
                "No tables found in metadata. Ensure models are imported before Base.metadata is populated."
            )
            return
        tables = ", ".join(table_names)

        query = text(f"TRUNCATE TABLE {tables} RESTART IDENTITY CASCADE;")

        db.execute(query)
        db.commit()

        print(f"[SUCCESS] Cleared tables: {tables}")
        print("[SUCCESS] Primary keys reset and relations cascaded.")
    except Exception as e:
        db.rollback()
        print("Error while clearing DB:", e)
    finally:
        db.close()


if __name__ == "__main__":
    clear_database()
