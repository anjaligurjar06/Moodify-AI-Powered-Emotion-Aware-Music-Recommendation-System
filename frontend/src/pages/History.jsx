import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AppNavbar from "../components/AppNavbar.jsx";
import { EMOTION_META } from "../components/ScoreBars.jsx";
import { api } from "../api/client.js";
import "../styles/app.css";

function timeAgo(iso) {
  const diffMs = Date.now() - new Date(iso + "Z").getTime();
  const mins = Math.round(diffMs / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.round(hrs / 24)}d ago`;
}

export default function History() {
  const [moods, setMoods] = useState([]);
  const [playlists, setPlaylists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const [m, p] = await Promise.all([api.moodHistory(), api.playlistHistory()]);
        setMoods(m);
        setPlaylists(p);
      } catch (err) {
        setError(err.message || "Couldn't load your history.");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="app-shell">
      <AppNavbar />

      <main className="wrap history-page">
        <div className="section-head left">
          <span className="eyebrow">Your timeline</span>
          <h2>Mood & playlist history</h2>
          <p>Every scan and every playlist you've saved, most recent first.</p>
        </div>

        {error && <p className="error-msg">{error}</p>}

        {loading ? (
          <div className="loading-block">
            <div className="spinner" />
            <p>Loading your history…</p>
          </div>
        ) : (
          <div className="history-grid">
            <div className="card history-col">
              <h3>Mood scans</h3>
              {moods.length === 0 && (
                <p className="empty-state">
                  No scans yet. <Link to="/detect">Run your first detection →</Link>
                </p>
              )}
              <ul className="history-list">
                {moods.map((m) => {
                  const meta = EMOTION_META[m.dominant_emotion] || { label: m.dominant_emotion, color: "var(--violet)" };
                  return (
                    <li key={m.id}>
                      <span className="history-swatch" style={{ background: meta.color }} />
                      <div className="history-line">
                        <span className="history-title">{meta.label}</span>
                        <span className="history-sub">via {m.source}</span>
                      </div>
                      <span className="history-time">{timeAgo(m.created_at)}</span>
                    </li>
                  );
                })}
              </ul>
            </div>

            <div className="card history-col">
              <h3>Saved playlists</h3>
              {playlists.length === 0 && (
                <p className="empty-state">
                  No playlists saved yet. <Link to="/playlist">Generate one →</Link>
                </p>
              )}
              <ul className="history-list">
                {playlists.map((p) => {
                  const meta = EMOTION_META[p.emotion] || { label: p.emotion, color: "var(--violet)" };
                  return (
                    <li key={p.id}>
                      <span className="history-swatch" style={{ background: meta.color }} />
                      <div className="history-line">
                        <span className="history-title">{meta.label} playlist</span>
                        <span className="history-sub">{p.tracks.length} tracks{p.uplift_mode ? " · uplift mode" : ""}</span>
                      </div>
                      <span className="history-time">{timeAgo(p.created_at)}</span>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
