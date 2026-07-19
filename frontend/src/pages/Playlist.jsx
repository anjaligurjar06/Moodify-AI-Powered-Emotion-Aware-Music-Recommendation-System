import { useCallback, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import AppNavbar from "../components/AppNavbar.jsx";
import { EMOTION_META } from "../components/ScoreBars.jsx";
import { api } from "../api/client.js";
import "../styles/app.css";

const EMOTIONS = ["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"];

export default function Playlist() {
  const [params, setParams] = useSearchParams();
  const emotion = params.get("emotion") || "neutral";
  const [uplift, setUplift] = useState(false);
  const [playlist, setPlaylist] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);

  const load = useCallback(async (em, up) => {
    setLoading(true);
    setError("");
    setSaved(false);
    try {
      const data = await api.generatePlaylist(em, up, 10);
      setPlaylist(data);
    } catch (err) {
      setError(err.message || "Couldn't build a playlist right now.");
      setPlaylist(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load(emotion, uplift);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [emotion, uplift]);

  async function handleSave() {
    if (!playlist) return;
    try {
      await api.savePlaylist({
        emotion: playlist.emotion,
        uplift_mode: playlist.uplift_mode,
        tracks: playlist.tracks,
      });
      setSaved(true);
    } catch {
      setError("Couldn't save this playlist to your history.");
    }
  }

  const meta = EMOTION_META[emotion] || { label: emotion, color: "var(--violet)" };

  return (
    <div className="app-shell">
      <AppNavbar />

      <main className="wrap playlist-page">
        <div className="section-head left">
          <span className="eyebrow">Step 2</span>
          <h2>
            Your <span style={{ color: meta.color }}>{meta.label.toLowerCase()}</span> playlist
          </h2>
          <p>Tuned to Spotify audio-feature targets for this mood — valence, energy, and tempo.</p>
        </div>

        <div className="playlist-controls">
          <div className="emotion-picker">
            {EMOTIONS.map((e) => (
              <button
                key={e}
                className={`chip ${e === emotion ? "active" : ""}`}
                onClick={() => setParams({ emotion: e })}
              >
                {EMOTION_META[e]?.label}
              </button>
            ))}
          </div>

          <label className="uplift-toggle">
            <input type="checkbox" checked={uplift} onChange={(e) => setUplift(e.target.checked)} />
            Uplift mode — nudge toward a brighter energy
          </label>
        </div>

        {playlist && (
          <div className="audio-targets-strip">
            <span>VALENCE {playlist.audio_targets.valence}</span>
            <span>ENERGY {playlist.audio_targets.energy}</span>
            <span>TEMPO {playlist.audio_targets.tempo} BPM</span>
            <span className={`source-badge ${playlist.source}`}>
              {playlist.source === "spotify" ? "Live Spotify data" : "Curated catalog"}
            </span>
          </div>
        )}

        {error && <p className="error-msg">{error}</p>}

        {loading ? (
          <div className="loading-block">
            <div className="spinner" />
            <p>Building your playlist…</p>
          </div>
        ) : (
          <div className="track-list">
            {playlist?.tracks.map((t, i) => (
              <a
                key={t.id}
                className="track-row"
                href={t.external_url || "#"}
                target="_blank"
                rel="noreferrer"
              >
                <span className="track-num">{String(i + 1).padStart(2, "0")}</span>
                <div className="track-art">
                  {t.image ? <img src={t.image} alt="" /> : <span className="art-fallback">♪</span>}
                </div>
                <div className="track-meta">
                  <span className="track-title">{t.title}</span>
                  <span className="track-artist">{t.artist}</span>
                </div>
                <span className="track-open">Open ↗</span>
              </a>
            ))}
          </div>
        )}

        {playlist && (
          <div className="playlist-actions">
            <button className="btn btn-primary" onClick={handleSave} disabled={saved}>
              {saved ? "Saved to history ✓" : "Save this playlist"}
            </button>
            <button className="btn btn-ghost" onClick={() => load(emotion, uplift)}>Regenerate</button>
          </div>
        )}
      </main>
    </div>
  );
}
