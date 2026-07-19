from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app import models  # noqa: F401  (ensures models are registered before create_all)
from app.routers import auth, detect, playlist, history
from app.services import spotify_service

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Emotion-aware music playlist generator API — face, text & fusion emotion "
                "detection, Spotify-mapped playlist generation, and mood history.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(detect.router)
app.include_router(playlist.router)
app.include_router(history.router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "spotify_configured": spotify_service.is_configured(),
    }


@app.get("/")
def root():
    return {"message": "Moodify API is running. See /docs for interactive API docs."}
