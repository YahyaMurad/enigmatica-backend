from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_user_id,
    get_current_user_id_from_api_key,
    get_db,
)
from app.models.models import Heartbeat
from app.schemas.heartbeats import HeartbeatCreate, HeartbeatOut

router = APIRouter(prefix="/api/v1/heartbeats", tags=["heartbeats"])


# ----------------------
# GET /api/v1/heartbeats
# ----------------------
@router.get("/", response_model=List[HeartbeatOut])
async def get_heartbeats(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    heartbeats = db.query(Heartbeat).filter(Heartbeat.user_id == current_user_id).all()
    return heartbeats


# -----------------------
# POST /api/v1/heartbeats
# -----------------------
@router.post("/", response_model=List[HeartbeatOut])
async def create_heartbeats(
    heartbeats: List[HeartbeatCreate],
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id_from_api_key),
):
    new_heartbeats = [
        Heartbeat(**hb.model_dump(), user_id=current_user_id) for hb in heartbeats
    ]

    db.add_all(new_heartbeats)
    db.commit()

    for hb in new_heartbeats:
        db.refresh(hb)

    return new_heartbeats
