"""
Mood Fusion Layer — combines face / text / audio emotion score dicts into a
single weighted distribution, matching the blueprint's `mood_fusion.py`.

Text is weighted highest by default since typed input is the most explicit
signal a user gives; face is a close second; audio (phase 2) lowest.
"""
from __future__ import annotations

EMOTIONS = ["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"]

DEFAULT_WEIGHTS = {"text": 0.45, "face": 0.4, "audio": 0.15}


def fuse(signals: dict[str, dict[str, float] | None], weights: dict[str, float] | None = None) -> dict[str, float]:
    weights = weights or DEFAULT_WEIGHTS
    present = {k: v for k, v in signals.items() if v}
    if not present:
        return {e: (1.0 if e == "neutral" else 0.0) for e in EMOTIONS}

    # Re-normalise weights over the sources that are actually present.
    total_w = sum(weights.get(k, 0.0) for k in present) or 1.0
    fused = {e: 0.0 for e in EMOTIONS}
    for source, scores in present.items():
        w = weights.get(source, 0.0) / total_w
        for e in EMOTIONS:
            fused[e] += w * scores.get(e, 0.0)

    return {e: round(v, 4) for e, v in fused.items()}


def dominant(scores: dict[str, float]) -> str:
    return max(scores, key=scores.get)
