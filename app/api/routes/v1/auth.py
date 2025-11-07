from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models import User
from app.schemas.auth import LoginRequest
from app.utils.security import verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


# -----------------------
# POST /api/v1/auth/login
# -----------------------
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "id": user.id,
        "username": user.username,
    }
