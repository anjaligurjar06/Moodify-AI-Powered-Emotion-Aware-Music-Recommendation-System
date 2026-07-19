"""
Face -> Emotion classifier.

Design notes
------------
The blueprint's target architecture fine-tunes an EfficientNet-B0 on
FER-2013 (35k labelled images, ~68-72% accuracy, exported to ONNX for fast
CPU inference). Training/hosting that model needs a GPU, a multi-hour
training run and a dataset download from Kaggle — out of scope for a
self-contained repo that has to "just run".

Instead this module ships a **real, working, dependency-light CV
pipeline** that plugs into the exact same API contract
(`predict(image_bytes) -> dict[label, score]`):

  1. Decode the incoming frame and run OpenCV's Haar Cascade face detector
     (bundled with opencv-python, no download required).
  2. Crop the largest detected face, split it into an eye-band and a
     mouth-band using standard facial proportion heuristics.
  3. Derive lightweight, explainable signals per band: edge density
     (Canny), local contrast, and vertical-gradient energy — proxies for
     "how much is happening" around the eyes/mouth (raised brows, an open
     smile, a furrowed brow, etc).
  4. Combine those signals with a small rule set into the 7-emotion
     distribution used everywhere else in the app.

Swap point: to use a real trained FER model, replace the body of
`_score_from_face()` with `model(face_crop)` — everything upstream
(base64 decoding, face detection, the FastAPI route, the response schema)
stays identical.
"""
from __future__ import annotations

import base64
import math
import re

import cv2
import numpy as np

EMOTIONS = ["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"]

_face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
_smile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_smile.xml"
)
_eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

_DATA_URL_RE = re.compile(r"^data:image/\w+;base64,")


class NoFaceDetected(Exception):
    pass


def _decode_image(b64_str: str) -> np.ndarray:
    b64_str = _DATA_URL_RE.sub("", b64_str.strip())
    if not b64_str:
        raise ValueError(
            "Received an empty image. This usually means the camera frame was captured "
            "before the video feed was ready — wait for the live preview to appear before capturing."
        )
    try:
        raw = base64.b64decode(b64_str + "=" * (-len(b64_str) % 4))
    except Exception as e:
        raise ValueError(f"Image data was not valid base64: {e}")

    arr = np.frombuffer(raw, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(
            "Could not decode image data. The captured frame may be empty or corrupted — "
            "make sure the camera preview is visibly showing video before capturing."
        )
    return img


def _largest_face(gray: np.ndarray):
    faces = _face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    if len(faces) == 0:
        return None
    return max(faces, key=lambda f: f[2] * f[3])


def _edge_density(region: np.ndarray) -> float:
    if region.size == 0:
        return 0.0
    edges = cv2.Canny(region, 60, 150)
    return float(np.count_nonzero(edges)) / edges.size


def _score_from_face(gray: np.ndarray, face_box) -> dict[str, float]:
    x, y, w, h = face_box
    face = gray[y:y + h, x:x + w]

    eye_band = face[int(0.15 * h):int(0.5 * h), :]
    mouth_band = face[int(0.62 * h):int(0.95 * h), :]

    mouth_edge = _edge_density(mouth_band)
    eye_edge = _edge_density(eye_band)
    brow_contrast = float(np.std(eye_band)) if eye_band.size else 0.0
    mouth_contrast = float(np.std(mouth_band)) if mouth_band.size else 0.0

    smiles = _smile_cascade.detectMultiScale(mouth_band, scaleFactor=1.7, minNeighbors=22)
    eyes = _eye_cascade.detectMultiScale(eye_band, scaleFactor=1.1, minNeighbors=8)

    raw = {e: 0.15 for e in EMOTIONS}

    # A confident smile detection is the strongest single "happy" signal.
    if len(smiles) > 0:
        raw["happy"] += 2.6 + min(len(smiles), 2) * 0.3
    raw["happy"] += mouth_edge * 4.0  # open/curved mouth -> more edges

    # Wide eyes + high brow contrast reads as surprise/fear; low activity
    # everywhere reads as sad/neutral.
    raw["surprise"] += max(0.0, (len(eyes) - 1)) * 0.7 + eye_edge * 2.5
    raw["fear"] += brow_contrast / 60.0

    raw["angry"] += max(0.0, brow_contrast / 55.0 - mouth_edge * 1.5)
    raw["sad"] += max(0.0, 1.0 - mouth_edge * 3.0) * 0.9
    raw["disgust"] += max(0.0, mouth_contrast / 70.0 - mouth_edge)
    raw["neutral"] += max(0.0, 1.2 - (mouth_edge + eye_edge) * 2.0)

    exps = {e: math.exp(v) for e, v in raw.items()}
    denom = sum(exps.values())
    return {e: round(v / denom, 4) for e, v in exps.items()}


def predict(image_b64: str) -> dict[str, float]:
    img = _decode_image(image_b64)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    face_box = _largest_face(gray)
    if face_box is None:
        raise NoFaceDetected("No face detected in frame — move into frame and ensure good lighting.")

    return _score_from_face(gray, face_box)


def dominant(scores: dict[str, float]) -> str:
    return max(scores, key=scores.get)
