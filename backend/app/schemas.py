import datetime as dt
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- Auth ----------
class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    spotify_connected: bool
    preferred_genres: list[str] = []

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Detection ----------
class TextInput(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class EmotionResult(BaseModel):
    dominant_emotion: str
    scores: dict[str, float]
    source: str


class FaceInput(BaseModel):
    image: str  # base64 data-url or raw base64 JPEG/PNG


class FusionInput(BaseModel):
    face: Optional[dict[str, float]] = None
    text: Optional[dict[str, float]] = None
    audio: Optional[dict[str, float]] = None


# ---------- Playlist ----------
class Track(BaseModel):
    id: str
    title: str
    artist: str
    album: Optional[str] = None
    image: Optional[str] = None
    preview_url: Optional[str] = None
    external_url: Optional[str] = None
    valence: Optional[float] = None
    energy: Optional[float] = None
    tempo: Optional[float] = None


class PlaylistOut(BaseModel):
    emotion: str
    uplift_mode: bool
    audio_targets: dict[str, float]
    genre_seeds: list[str]
    tracks: list[Track]
    source: str  # "spotify" | "catalog"


class SavePlaylistIn(BaseModel):
    emotion: str
    uplift_mode: bool = False
    tracks: list[Track]


class HistoryMoodOut(BaseModel):
    id: int
    source: str
    dominant_emotion: str
    scores: dict[str, float]
    created_at: dt.datetime

    class Config:
        from_attributes = True


class HistoryPlaylistOut(BaseModel):
    id: int
    emotion: str
    uplift_mode: bool
    tracks: list[Track]
    created_at: dt.datetime

    class Config:
        from_attributes = True
