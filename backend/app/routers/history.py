from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/moods", response_model=list[schemas.HistoryMoodOut])
def mood_history(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
    limit: int = 50,
):
    rows = (
        db.query(models.MoodLog)
        .filter(models.MoodLog.user_id == user.id)
        .order_by(models.MoodLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return rows


@router.get("/playlists", response_model=list[schemas.HistoryPlaylistOut])
def playlist_history(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
    limit: int = 50,
):
    rows = (
        db.query(models.PlaylistHistory)
        .filter(models.PlaylistHistory.user_id == user.id)
        .order_by(models.PlaylistHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return rows
