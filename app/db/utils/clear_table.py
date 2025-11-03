import sys
from sqlalchemy import text
from app.db.session import SessionLocal
from app.models.models import Base


def clear_table(table_name: str):
    """Truncate a single table and reset its primary key."""
    db = SessionLocal()
    try:
        print(f"🧹 Clearing table: {table_name}")

        all_tables = list(Base.metadata.tables.keys())
        if table_name not in all_tables:
            print(f"❌ Table '{table_name}' not found. Available tables:")
            for t in all_tables:
                print(f" - {t}")
            return

        query = text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
        db.execute(query)
        db.commit()

        print(f"✅ Successfully cleared table: {table_name}")
        print("✅ Primary keys reset and related data cascaded.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error while clearing table '{table_name}': {e}")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/clear_table.py <table_name>")
        sys.exit(1)

    table_name = sys.argv[1]
    clear_table(table_name)
