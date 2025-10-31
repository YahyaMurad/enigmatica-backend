import datetime
import uuid

import bcrypt
from sqlalchemy.orm import Session

from app.db.session import Base, engine
from app.db.utils.clear_db import clear_database
from app.models.models import APIKey, User


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def generate_api_key() -> str:
    # You can later replace this with more secure HMAC-based keys if desired
    return uuid.uuid4().hex


def seed_user():
    Base.metadata.create_all(bind=engine)  # ensure tables exist

    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    db: Session = SessionLocal()

    try:
        # Create dummy user
        username = "yahyamurad"
        email = "yahya@gmail.com"
        password = "yahya"

        password_hash = hash_password(password)

        user = User(username=username, email=email, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)

        api_key = APIKey(
            user_id=user.id,
            key=generate_api_key(),
            created_at=datetime.datetime.now(datetime.UTC).date(),
            is_active=True,
        )
        db.add(api_key)
        db.commit()

        print(f"✅ User created: {user.username} (ID: {user.id})")
        print(f"🔑 API Key: {api_key.key}")

    finally:
        db.close()


if __name__ == "__main__":
    clear_database()
    seed_user()
