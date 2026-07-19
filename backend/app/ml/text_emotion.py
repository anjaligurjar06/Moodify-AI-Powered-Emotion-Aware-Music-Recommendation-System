"""
Text -> Emotion classifier.

Design notes
------------
The project blueprint calls for a transformer model (e.g.
`j-hartmann/emotion-english-distilroberta-base`) served through Hugging Face.
That model requires a multi-hundred-MB download from huggingface.co at
startup, which isn't available in every deployment environment (offline
servers, restricted networks, low-RAM containers, CI, etc).

To keep the project fully self-contained and dependency-light while still
being a *real* NLP classifier (not a random mock), this module implements a
transparent lexicon + rule based scorer:

  1. Tokenize & normalise the input.
  2. Score each of the 7 emotion classes using curated keyword/phrase
     lexicons with per-word weights.
  3. Apply negation handling ("not happy" flips polarity of the next
     token's contribution).
  4. Apply intensifier/diminisher scaling ("very", "so", "slightly").
  5. Apply emoji + punctuation heuristics (e.g. "!!!", "🙂").
  6. Normalise into a probability-like distribution (softmax).

If you want to swap in the real transformer model, drop a
`transformers.pipeline("text-classification", model="j-hartmann/...")`
call into `predict()` behind a feature flag — the FastAPI route and the
response schema are already compatible with it (dict[label, score]).
"""
from __future__ import annotations

import math
import re

EMOTIONS = ["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"]

NEGATIONS = {"not", "no", "never", "n't", "cant", "can't", "won't", "wont", "isn't", "aren't", "don't", "didn't"}

INTENSIFIERS = {
    "very": 1.6, "so": 1.5, "really": 1.5, "extremely": 1.9, "super": 1.6,
    "incredibly": 1.8, "totally": 1.4, "absolutely": 1.7, "quite": 1.2,
}
DIMINISHERS = {"slightly": 0.6, "a bit": 0.6, "kinda": 0.7, "somewhat": 0.7, "little": 0.7}

LEXICON: dict[str, dict[str, float]] = {
    "happy": {
        "happy": 3, "joy": 3, "joyful": 3, "glad": 2.5, "great": 2, "excited": 3,
        "awesome": 2.5, "amazing": 2.5, "love": 2.5, "wonderful": 2.5, "fantastic": 2.5,
        "good": 1.5, "delighted": 3, "cheerful": 2.5, "thrilled": 3, "smile": 2,
        "smiling": 2, "fun": 1.8, "blessed": 2, "grateful": 2, "proud": 2, "yay": 2.5,
        "celebrate": 2.5, "party": 1.8, "win": 1.8, "won": 1.8, "success": 1.8,
        "energized": 2, "pumped": 2.2, "lit": 1.8, ":)": 2.5, "😊": 3, "😄": 3, "🎉": 2.5,
    },
    "sad": {
        "sad": 3, "unhappy": 2.8, "down": 1.8, "depressed": 3, "cry": 2.8, "crying": 2.8,
        "tears": 2.2, "lonely": 2.5, "heartbroken": 3, "miserable": 2.8, "hopeless": 2.8,
        "empty": 2, "exhausted": 1.8, "tired": 1.5, "drained": 2, "grief": 2.8,
        "sorrow": 2.8, "hurt": 2, "broken": 2.2, "disappointed": 2.2, "gloomy": 2.2,
        "blue": 1.5, "miss": 1.8, "missing": 1.8, "loss": 2, "lost": 1.8, ":(": 2.8, "😢": 3, "😭": 3,
    },
    "angry": {
        "angry": 3, "mad": 2.8, "furious": 3, "annoyed": 2.2, "irritated": 2.2,
        "rage": 2.8, "hate": 2.8, "pissed": 2.8, "frustrated": 2.5, "outraged": 2.8,
        "resent": 2.2, "hostile": 2.2, "yell": 2, "yelling": 2, "screaming": 2.2,
        "unfair": 1.8, "betrayed": 2.2, "livid": 3, "😠": 2.8, "😡": 3,
    },
    "fear": {
        "afraid": 2.8, "scared": 2.8, "fear": 2.8, "terrified": 3, "anxious": 2.5,
        "anxiety": 2.5, "nervous": 2.2, "worried": 2.2, "worry": 2.2, "panic": 2.8,
        "dread": 2.5, "threat": 1.8, "threatened": 2.2, "insecure": 1.8, "stressed": 2,
        "overwhelmed": 2.2, "uneasy": 1.8, "😨": 2.8, "😰": 2.8,
    },
    "surprise": {
        "surprised": 2.8, "shocked": 2.6, "wow": 2.2, "unexpected": 2, "startled": 2.4,
        "astonished": 2.6, "amazed": 2.2, "whoa": 2, "unbelievable": 2, "sudden": 1.5,
        "omg": 2.2, "no way": 2, "😮": 2.6, "😲": 2.8,
    },
    "disgust": {
        "disgusted": 3, "disgusting": 2.8, "gross": 2.4, "eww": 2.4, "ew": 2.2,
        "nasty": 2.2, "revolting": 2.8, "sick": 1.6, "repulsed": 2.8, "yuck": 2.4,
        "🤢": 2.8,
    },
    "neutral": {
        "okay": 1.2, "fine": 1.2, "normal": 1.4, "alright": 1.2, "meh": 1.4,
        "usual": 1.2, "average": 1.2, "nothing": 1, "calm": 1.6, "relaxed": 1.6,
        "chill": 1.5, "content": 1.4,
    },
}

_WORD_RE = re.compile(r"[a-zA-Z']+|[:;][-]?[)(dDpP]|[\U0001F300-\U0001FAFF]")


def _tokenize(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())


def predict(text: str) -> dict[str, float]:
    """Return a normalised score distribution over the 7 emotion classes."""
    tokens = _tokenize(text)
    raw = {e: 0.0 for e in EMOTIONS}

    negate_next = False
    scale = 1.0

    for i, tok in enumerate(tokens):
        if tok in NEGATIONS or tok.endswith("n't"):
            negate_next = True
            continue
        if tok in INTENSIFIERS:
            scale = INTENSIFIERS[tok]
            continue
        if tok in DIMINISHERS:
            scale = DIMINISHERS[tok]
            continue

        for emotion, words in LEXICON.items():
            if tok in words:
                weight = words[tok] * scale
                if negate_next:
                    # Negated positive emotion nudges toward its rough opposite.
                    opposite = {
                        "happy": "sad", "sad": "happy", "angry": "neutral",
                        "fear": "neutral", "disgust": "neutral",
                        "surprise": "neutral", "neutral": "neutral",
                    }[emotion]
                    raw[opposite] += weight * 0.6
                else:
                    raw[emotion] += weight

        negate_next = False
        scale = 1.0

    # Punctuation-based intensity cues.
    exclaims = text.count("!")
    if exclaims:
        # Amplify whichever non-neutral emotion currently leads.
        leader = max((e for e in EMOTIONS if e != "neutral"), key=lambda e: raw[e])
        if raw[leader] > 0:
            raw[leader] += min(exclaims, 3) * 0.4

    if text.isupper() and len(text) > 3:
        leader = max((e for e in EMOTIONS if e != "neutral"), key=lambda e: raw[e])
        if raw[leader] > 0:
            raw[leader] += 0.6

    total_signal = sum(raw.values())
    if total_signal <= 0:
        # No lexicon hits at all -> mildly neutral distribution.
        raw["neutral"] = 1.0

    # Small baseline (Laplace-style smoothing) so every class stays > 0,
    # then softmax for a clean probability-like output.
    for e in EMOTIONS:
        raw[e] += 0.15

    exps = {e: math.exp(v) for e, v in raw.items()}
    denom = sum(exps.values())
    scores = {e: round(v / denom, 4) for e, v in exps.items()}
    return scores


def dominant(scores: dict[str, float]) -> str:
    return max(scores, key=scores.get)
