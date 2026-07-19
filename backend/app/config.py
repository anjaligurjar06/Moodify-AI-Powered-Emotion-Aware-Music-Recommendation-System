"""
Central configuration for the Moodify backend.
All values can be overridden with environment variables (see .env.example).
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "Moodify API"
    ENV: str = "development"

    # --- Security ---
    SECRET_KEY: str = "change-this-secret-in-production-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # --- Database ---
    DATABASE_URL: str = "sqlite:///./moodify.db"

    # --- CORS ---
    FRONTEND_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # --- Spotify (optional — app works with a curated fallback catalog if unset) ---
    SPOTIFY_CLIENT_ID: str = ""
    SPOTIFY_CLIENT_SECRET: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.FRONTEND_ORIGINS.split(",") if o.strip()]


settings = Settings()
