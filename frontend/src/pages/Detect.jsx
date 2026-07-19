import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import AppNavbar from "../components/AppNavbar.jsx";
import ScoreBars, { EMOTION_META } from "../components/ScoreBars.jsx";
import { api, ApiError } from "../api/client.js";
import "../styles/app.css";

export default function Detect() {
  const navigate = useNavigate();
  const [tab, setTab] = useState("face");

  // --- Face detection state ---
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const [camOn, setCamOn] = useState(false);
  const [camError, setCamError] = useState("");
  const [faceScores, setFaceScores] = useState(null);
  const [faceBusy, setFaceBusy] = useState(false);
  const [faceStatus, setFaceStatus] = useState("");

  // --- Text detection state ---
  const [text, setText] = useState("");
  const [textScores, setTextScores] = useState(null);
  const [textBusy, setTextBusy] = useState(false);
  const [textError, setTextError] = useState("");

  const dominantFace = faceScores ? Object.entries(faceScores).sort((a, b) => b[1] - a[1])[0][0] : null;
  const dominantText = textScores ? Object.entries(textScores).sort((a, b) => b[1] - a[1])[0][0] : null;
  const finalEmotion = dominantText || dominantFace;

  const stopCamera = useCallback(() => {
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
    setCamOn(false);
  }, []);

  useEffect(() => () => stopCamera(), [stopCamera]);

  async function startCamera() {
    setCamError("");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 480, height: 360 } });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }
      setCamOn(true);
    } catch {
      setCamError("Couldn't access your webcam. Check browser permissions and try again.");
    }
  }

  async function captureAndDetect() {
    if (!videoRef.current || !canvasRef.current) return;
    setFaceBusy(true);
    setFaceStatus("");
    try {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataUrl = canvas.toDataURL("image/jpeg", 0.85);

      const result = await api.detectFace(dataUrl);
      setFaceScores(result.scores);
    } catch (err) {
      if (err instanceof ApiError && err.status === 422) {
        setFaceStatus("No face detected — center your face in the frame with good lighting, then try again.");
      } else {
        setFaceStatus(err.message || "Something went wrong reading that frame.");
      }
      setFaceScores(null);
    } finally {
      setFaceBusy(false);
    }
  }

  async function handleTextSubmit(e) {
    e.preventDefault();
    if (!text.trim()) return;
    setTextBusy(true);
    setTextError("");
    try {
      const result = await api.detectText(text.trim());
      setTextScores(result.scores);
    } catch (err) {
      setTextError(err.message || "Couldn't read that mood — try again.");
    } finally {
      setTextBusy(false);
    }
  }

  function goToPlaylist() {
    if (!finalEmotion) return;
    navigate(`/playlist?emotion=${finalEmotion}`);
  }

  return (
    <div className="app-shell">
      <AppNavbar />

      <main className="wrap detect-page">
        <div className="section-head left">
          <span className="eyebrow">Step 1</span>
          <h2>How are you feeling right now?</h2>
          <p>Use your camera, describe it in words, or both — Moodify combines every signal you give it.</p>
        </div>

        <div className="detect-tabs">
          <button className={tab === "face" ? "active" : ""} onClick={() => setTab("face")}>◐ Facial expression</button>
          <button className={tab === "text" ? "active" : ""} onClick={() => setTab("text")}>✎ Type it out</button>
        </div>

        <div className="detect-grid">
          <div className="detect-panel card">
            {tab === "face" ? (
              <>
                <div className="cam-frame">
                  {camOn ? (
                    <video ref={videoRef} muted playsInline />
                  ) : (
                    <div className="cam-placeholder">
                      <span>◐</span>
                      <p>Camera is off</p>
                    </div>
                  )}
                  <canvas ref={canvasRef} style={{ display: "none" }} />
                </div>

                {camError && <p className="error-msg">{camError}</p>}
                {faceStatus && <p className="hint">{faceStatus}</p>}

                <div className="detect-actions">
                  {!camOn ? (
                    <button className="btn btn-primary" onClick={startCamera}>Enable camera</button>
                  ) : (
                    <>
                      <button className="btn btn-primary" onClick={captureAndDetect} disabled={faceBusy}>
                        {faceBusy ? "Reading expression…" : "Capture & analyse"}
                      </button>
                      <button className="btn btn-ghost" onClick={stopCamera}>Turn off</button>
                    </>
                  )}
                </div>
              </>
            ) : (
              <form onSubmit={handleTextSubmit} className="text-detect-form">
                <label htmlFor="moodText">Describe how you feel</label>
                <textarea
                  id="moodText"
                  rows={6}
                  placeholder="e.g. I'm exhausted after work but relieved the week is finally over…"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                />
                {textError && <p className="error-msg">{textError}</p>}
                <div className="detect-actions">
                  <button type="submit" className="btn btn-primary" disabled={textBusy || !text.trim()}>
                    {textBusy ? "Reading mood…" : "Analyse text"}
                  </button>
                </div>
              </form>
            )}
          </div>

          <div className="detect-panel card results-panel">
            <h3>Detected mood</h3>

            {!faceScores && !textScores && (
              <p className="empty-state">Run a scan on the left to see your emotion breakdown here.</p>
            )}

            {faceScores && (
              <div className="result-block">
                <div className="result-head">
                  <span className="tag">From your face</span>
                  {dominantFace && (
                    <span className="dominant-pill" style={{ borderColor: EMOTION_META[dominantFace]?.color }}>
                      {EMOTION_META[dominantFace]?.label}
                    </span>
                  )}
                </div>
                <ScoreBars scores={faceScores} />
              </div>
            )}

            {textScores && (
              <div className="result-block">
                <div className="result-head">
                  <span className="tag">From your words</span>
                  {dominantText && (
                    <span className="dominant-pill" style={{ borderColor: EMOTION_META[dominantText]?.color }}>
                      {EMOTION_META[dominantText]?.label}
                    </span>
                  )}
                </div>
                <ScoreBars scores={textScores} />
              </div>
            )}

            {finalEmotion && (
              <button className="btn btn-primary btn-block go-playlist" onClick={goToPlaylist}>
                Build my {EMOTION_META[finalEmotion]?.label.toLowerCase()} playlist →
              </button>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
