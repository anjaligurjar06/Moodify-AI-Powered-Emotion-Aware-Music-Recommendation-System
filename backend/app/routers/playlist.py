from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.deps import get_current_user
from app.services.playlist_builder import build_playlist

router = APIRouter(prefix="/api/playlist", tags=["playlist"])


@router.get("/generate", response_model=schemas.PlaylistOut)
def generate_playlist(
    emotion: str = Query(..., description="One of: happy, sad, angry, neutral, fear, surprise, disgust"),
    uplift: bool = Query(False, description="Uplift mode — nudge sad/angry moods toward higher valence"),
    limit: int = Query(10, ge=1, le=25),
    user: models.User = Depends(get_current_user),
):
    return build_playlist(emotion=emotion, uplift=uplift, limit=limit)


@router.post("/save", status_code=201)
def save_playlist(
    payload: schemas.SavePlaylistIn,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    entry = models.PlaylistHistory(
        user_id=user.id,
        emotion=payload.emotion,
        uplift_mode=payload.uplift_mode,
        tracks=[t.model_dump() for t in payload.tracks],
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"id": entry.id, "saved": True}
