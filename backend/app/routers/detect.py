from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.deps import get_current_user
from app.ml import text_emotion, face_emotion, fusion

router = APIRouter(prefix="/api/detect", tags=["detect"])


def _log_mood(db: Session, user: models.User, source: str, scores: dict, dominant_label: str):
    entry = models.MoodLog(
        user_id=user.id, source=source, dominant_emotion=dominant_label, scores=scores
    )
    db.add(entry)
    db.commit()


@router.post("/text", response_model=schemas.EmotionResult)
def detect_text(
    payload: schemas.TextInput,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    scores = text_emotion.predict(payload.text)
    label = text_emotion.dominant(scores)
    _log_mood(db, user, "text", scores, label)
    return schemas.EmotionResult(dominant_emotion=label, scores=scores, source="text")


@router.post("/face", response_model=schemas.EmotionResult)
def detect_face(
    payload: schemas.FaceInput,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    try:
        scores = face_emotion.predict(payload.image)
    except face_emotion.NoFaceDetected as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    label = face_emotion.dominant(scores)
    _log_mood(db, user, "face", scores, label)
    return schemas.EmotionResult(dominant_emotion=label, scores=scores, source="face")


@router.post("/fusion", response_model=schemas.EmotionResult)
def detect_fusion(
    payload: schemas.FusionInput,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    scores = fusion.fuse({"face": payload.face, "text": payload.text, "audio": payload.audio})
    label = fusion.dominant(scores)
    _log_mood(db, user, "fusion", scores, label)
    return schemas.EmotionResult(dominant_emotion=label, scores=scores, source="fusion")
