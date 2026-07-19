"""
Thin wrapper around the Spotify Web API using the Client Credentials flow
(app-only auth — good enough for search/recommendations, no user login
required). If SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET aren't set, every
call safely returns None and the caller falls back to the curated catalog.
"""
from __future__ import annotations

import time

import requests

from app.config import settings

_TOKEN_URL = "https://accounts.spotify.com/api/token"
_SEARCH_URL = "https://api.spotify.com/v1/search"

_token_cache = {"access_token": None, "expires_at": 0}


def _configured() -> bool:
    return bool(settings.SPOTIFY_CLIENT_ID and settings.SPOTIFY_CLIENT_SECRET)


def _get_token() -> str | None:
    if not _configured():
        return None

    if _token_cache["access_token"] and time.time() < _token_cache["expires_at"] - 30:
        return _token_cache["access_token"]

    try:
        resp = requests.post(
            _TOKEN_URL,
            data={"grant_type": "client_credentials"},
            auth=(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET),
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
        _token_cache["access_token"] = data["access_token"]
        _token_cache["expires_at"] = time.time() + data.get("expires_in", 3600)
        return _token_cache["access_token"]
    except requests.RequestException:
        return None


def search_tracks_by_genre(genre_seeds: list[str], limit: int = 10) -> list[dict] | None:
    """Search Spotify for tracks matching the given genre seeds.

    Uses the /search endpoint (genre-scoped query) rather than the
    recommendations endpoint, which Spotify has restricted on newer app
    grants — this keeps the integration working for any registered app.
    Returns None on any failure so the caller can fall back to the catalog.
    """
    token = _get_token()
    if not token:
        return None

    try:
        query = " OR ".join(f'genre:"{g}"' for g in genre_seeds[:3])
        resp = requests.get(
            _SEARCH_URL,
            headers={"Authorization": f"Bearer {token}"},
            params={"q": query, "type": "track", "limit": limit},
            timeout=8,
        )
        resp.raise_for_status()
        items = resp.json().get("tracks", {}).get("items", [])
        tracks = []
        for t in items:
            images = t.get("album", {}).get("images", [])
            tracks.append({
                "id": t["id"],
                "title": t["name"],
                "artist": ", ".join(a["name"] for a in t.get("artists", [])),
                "album": t.get("album", {}).get("name"),
                "image": images[0]["url"] if images else None,
                "preview_url": t.get("preview_url"),
                "external_url": t.get("external_urls", {}).get("spotify"),
            })
        return tracks or None
    except requests.RequestException:
        return None


def is_configured() -> bool:
    return _configured()
