import datetime as dt

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    spotify_connected = Column(Boolean, default=False)
    preferred_genres = Column(JSON, default=list)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    mood_logs = relationship("MoodLog", back_populates="user", cascade="all, delete-orphan")
    playlists = relationship("PlaylistHistory", back_populates="user", cascade="all, delete-orphan")


class MoodLog(Base):
    __tablename__ = "mood_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source = Column(String(20))  # face | text | audio | fusion
    dominant_emotion = Column(String(20))
    scores = Column(JSON)  # {happy: 0.8, sad: 0.1, ...}
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    user = relationship("User", back_populates="mood_logs")


class PlaylistHistory(Base):
    __tablename__ = "playlist_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    emotion = Column(String(20))
    uplift_mode = Column(Boolean, default=False)
    tracks = Column(JSON)  # list of track dicts
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    user = relationship("User", back_populates="playlists")
