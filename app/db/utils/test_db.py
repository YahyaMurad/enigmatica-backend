from app.db.session import SessionLocal
from app.models.models import User

# create a session
db = SessionLocal()

# create a dummy user
dummy_user = User(username="testuser", email="test@example.com")

# add and commit
db.add(dummy_user)
db.commit()

# refresh to get the generated ID
db.refresh(dummy_user)

print("✅ User created with ID:", dummy_user.id)

db.close()
