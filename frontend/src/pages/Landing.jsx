import { Link } from "react-router-dom";
import Navbar from "../components/Navbar.jsx";
import Footer from "../components/Footer.jsx";
import Waveform from "../components/Waveform.jsx";
import "../styles/landing.css";

const MOOD_ROWS = [
  { emotion: "Happy", color: "var(--amber)", valence: "0.8 – 1.0", energy: "0.7 – 0.9", genres: "pop, dance, funk" },
  { emotion: "Sad", color: "var(--cyan)", valence: "0.0 – 0.3", energy: "0.1 – 0.4", genres: "acoustic, indie, blues" },
  { emotion: "Angry", color: "var(--rose)", valence: "0.2 – 0.5", energy: "0.8 – 1.0", genres: "metal, rock, hip-hop" },
  { emotion: "Neutral", color: "var(--violet)", valence: "0.4 – 0.6", energy: "0.4 – 0.6", genres: "pop, indie, chill" },
];

const FEATURES = [
  { key: "face", icon: "◐", title: "Facial expression", tag: "~50ms per frame", body: "Your camera reads micro-expressions in real time and classifies your mood across seven emotional states." },
  { key: "text", icon: "✎", title: "Type it out", tag: "Works in plain language", body: "Describe your day in a sentence. Moodify's language model picks up the emotional undertone, even if you don't name it." },
  { key: "voice", icon: "◈", title: "Say it out loud", tag: "Phase 2 · optional", body: "Speak for a few seconds. Tone, pace, and pitch are enough to place your mood — no words required." },
];

const STEPS = [
  { num: "01", title: "Read", body: "Face, text, or voice signals are captured and sent for inference." },
  { num: "02", title: "Fuse", body: "Signals are weighted and combined into a single emotional read." },
  { num: "03", title: "Map", body: "Your mood is translated into audio targets — valence, energy, tempo." },
  { num: "04", title: "Play", body: "A ranked playlist streams straight from Spotify, ready to go." },
];

export default function Landing() {
  return (
    <>
      <Navbar />

      <header className="hero">
        <div className="wrap hero-grid">
          <div>
            <span className="eyebrow">Emotion-aware listening</span>
            <h1>
              Music that meets you<br />
              where your <span className="accent">mood</span> is.
            </h1>
            <p className="sub">
              Moodify reads your expression, your words, or your voice — then builds a playlist tuned to how you
              actually feel right now, not a genre you picked last year.
            </p>
            <div className="hero-actions">
              <Link to="/auth?mode=register" className="btn btn-primary">Start listening →</Link>
              <a href="#how" className="btn btn-ghost">See how it works</a>
            </div>
            <div className="emotion-strip" aria-label="Detected emotions">
              <span className="emotion-tag happy">Happy</span>
              <span className="emotion-tag sad">Sad</span>
              <span className="emotion-tag angry">Angry</span>
              <span className="emotion-tag calm">Neutral</span>
              <span className="emotion-tag happy">Surprise</span>
              <span className="emotion-tag sad">Fear</span>
            </div>
          </div>

          <Waveform />
        </div>
      </header>

      <div className="trust">
        <div className="wrap">
          <span>FACE · TEXT · VOICE INPUT</span>
          <span>SPOTIFY-POWERED RECOMMENDATIONS</span>
          <span>7-EMOTION MODEL</span>
          <span>REAL-TIME FUSION</span>
        </div>
      </div>

      <section className="section" id="features">
        <div className="wrap">
          <div className="section-head">
            <span className="eyebrow">Three ways in</span>
            <h2>Tell Moodify how you feel, however that's easiest.</h2>
            <p>Every signal feeds the same mood engine — use one, or combine them for a sharper read.</p>
          </div>
          <div className="feature-grid">
            {FEATURES.map((f) => (
              <div className={`feature-card ${f.key}`} key={f.key}>
                <div className="icon">{f.icon}</div>
                <h3>{f.title}</h3>
                <p>{f.body}</p>
                <span className="tag">{f.tag}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="how section" id="how">
        <div className="wrap">
          <div className="section-head">
            <span className="eyebrow">From feeling to playlist</span>
            <h2>Four steps, no manual searching.</h2>
          </div>
          <div className="steps">
            {STEPS.map((s) => (
              <div className="step" key={s.num}>
                <span className="num">{s.num}</span>
                <h4>{s.title}</h4>
                <p>{s.body}</p>
              </div>
            ))}
          </div>

          <div className="mood-table" id="mapping" aria-label="Emotion to audio feature mapping">
            <div className="mood-row head">
              <span>Emotion</span><span>Valence</span><span>Energy</span><span>Genre seeds</span>
            </div>
            {MOOD_ROWS.map((row) => (
              <div className="mood-row" key={row.emotion}>
                <span><i className="swatch" style={{ background: row.color }}></i>{row.emotion}</span>
                <span>{row.valence}</span>
                <span>{row.energy}</span>
                <span className="genres">{row.genres}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="cta-final">
        <div className="wrap">
          <span className="eyebrow" style={{ justifyContent: "center" }}>Ready when you are</span>
          <h2>Your next playlist already<br />knows how you feel.</h2>
          <p>Free to start. Connect Spotify in under a minute.</p>
          <Link to="/auth?mode=register" className="btn btn-primary">Create your account</Link>
        </div>
      </section>

      <Footer />
    </>
  );
}
