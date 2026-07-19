"""
Emotion -> Spotify audio-feature mapping + playlist assembly, matching the
table on p.5 of the project blueprint.
"""
from __future__ import annotations

from app.services import spotify_service, catalog

AUDIO_FEATURE_MAP = {
    "happy":    {"valence": 0.9, "energy": 0.8, "tempo": 130, "danceability": 0.8, "genres": ["pop", "dance", "funk"]},
    "sad":      {"valence": 0.15, "energy": 0.25, "tempo": 75, "danceability": 0.3, "genres": ["acoustic", "indie", "blues"]},
    "angry":    {"valence": 0.35, "energy": 0.9, "tempo": 145, "danceability": 0.6, "genres": ["metal", "rock", "hip-hop"]},
    "neutral":  {"valence": 0.5, "energy": 0.5, "tempo": 105, "danceability": 0.5, "genres": ["pop", "indie", "chill"]},
    "fear":     {"valence": 0.2, "energy": 0.7, "tempo": 115, "danceability": 0.4, "genres": ["ambient", "electronic"]},
    "surprise": {"valence": 0.75, "energy": 0.8, "tempo": 135, "danceability": 0.7, "genres": ["edm", "pop", "latin"]},
    "disgust":  {"valence": 0.25, "energy": 0.65, "tempo": 105, "danceability": 0.4, "genres": ["punk", "alternative"]},
}


def uplift_targets(targets: dict) -> dict:
    """Shift valence/energy upward for 'uplift mode' (sad/angry -> happier)."""
    shifted = dict(targets)
    shifted["valence"] = round(min(1.0, targets["valence"] + 0.25), 2)
    shifted["energy"] = round(min(1.0, targets["energy"] + 0.15), 2)
    shifted["genres"] = AUDIO_FEATURE_MAP["happy"]["genres"][:2] + targets["genres"][:1]
    return shifted


def build_playlist(emotion: str, uplift: bool = False, limit: int = 10) -> dict:
    emotion = emotion if emotion in AUDIO_FEATURE_MAP else "neutral"
    targets = AUDIO_FEATURE_MAP[emotion]
    if uplift and emotion in {"sad", "angry", "fear", "disgust"}:
        targets = uplift_targets(targets)

    genre_seeds = targets["genres"]

    tracks = spotify_service.search_tracks_by_genre(genre_seeds, limit=limit)
    source = "spotify"
    if not tracks:
        tracks = catalog.get_catalog_tracks(emotion, limit=limit)
        source = "catalog"

    return {
        "emotion": emotion,
        "uplift_mode": uplift,
        "audio_targets": {k: v for k, v in targets.items() if k != "genres"},
        "genre_seeds": genre_seeds,
        "tracks": tracks,
        "source": source,
    }
