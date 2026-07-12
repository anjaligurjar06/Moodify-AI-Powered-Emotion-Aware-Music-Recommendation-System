import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import MiniWaveform from "../components/MiniWaveform.jsx";
import "../styles/auth.css";

function PasswordField({ id, label, value, onChange, error, placeholder, hint }) {
  const [visible, setVisible] = useState(false);

  return (
    <div className={`field ${error ? "has-error" : ""}`}>
      <label htmlFor={id}>{label}</label>
      <div className="input-wrap">
        <input
          type={visible ? "text" : "password"}
          id={id}
          name={id}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          required
          minLength={8}
        />
        <button type="button" className="toggle-visibility" onClick={() => setVisible((v) => !v)}>
          {visible ? "HIDE" : "SHOW"}
        </button>
      </div>
      {hint && <p className="hint">{hint}</p>}
      {error && <p className="error-msg">{error}</p>}
    </div>
  );
}

function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    const nextErrors = {};
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) nextErrors.email = "Enter a valid email address.";
    if (password.length < 8) nextErrors.password = "Password must be at least 8 characters.";
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;

    setSubmitting(true);
    // Replace with: await fetch("/api/auth/login", { method: "POST", body: JSON.stringify({ email, password }) })
    setTimeout(() => {
      setSubmitting(false);
      alert("Logged in — connect this to your FastAPI /api/auth/login endpoint.");
    }, 700);
  }

  return (
    <>
      <h2>Welcome back</h2>
      <p className="lede">Log in to pick up your playlist where your mood left off.</p>

      <form onSubmit={handleSubmit} noValidate>
        <div className={`field ${errors.email ? "has-error" : ""}`}>
          <label htmlFor="loginEmail">Email</label>
          <input
            type="email"
            id="loginEmail"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          {errors.email && <p className="error-msg">{errors.email}</p>}
        </div>

        <PasswordField
          id="loginPassword"
          label="Password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          error={errors.password}
        />

        <div className="row-between">
          <label className="checkbox-row">
            <input type="checkbox" name="remember" /> Remember me
          </label>
          <a href="#" className="link-muted">Forgot password?</a>
        </div>

        <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
          {submitting ? "Please wait…" : "Log in"}
        </button>
      </form>

      <div className="divider">or</div>
      <button type="button" className="btn btn-spotify">
        <span className="dot-spotify"></span>Continue with Spotify
      </button>
    </>
  );
}

function RegisterForm() {
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" });
  const [terms, setTerms] = useState(false);
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }));
  }

  function handleSubmit(e) {
    e.preventDefault();
    const nextErrors = {};
    if (form.name.trim().length < 2) nextErrors.name = "Enter your name.";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) nextErrors.email = "Enter a valid email address.";
    if (form.password.length < 8) nextErrors.password = "Password must be at least 8 characters.";
    if (form.confirm !== form.password || !form.confirm) nextErrors.confirm = "Passwords don't match.";
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length || !terms) return;

    setSubmitting(true);
    // Replace with: await fetch("/api/auth/register", { method: "POST", body: JSON.stringify(form) })
    setTimeout(() => {
      setSubmitting(false);
      alert("Account created — connect this to your FastAPI /api/auth/register endpoint.");
    }, 700);
  }

  return (
    <>
      <h2>Create your account</h2>
      <p className="lede">Takes under a minute. Connect Spotify after.</p>

      <form onSubmit={handleSubmit} noValidate>
        <div className={`field ${errors.name ? "has-error" : ""}`}>
          <label htmlFor="regName">Full name</label>
          <input type="text" id="regName" placeholder="Your name" value={form.name} onChange={update("name")} required />
          {errors.name && <p className="error-msg">{errors.name}</p>}
        </div>

        <div className={`field ${errors.email ? "has-error" : ""}`}>
          <label htmlFor="regEmail">Email</label>
          <input type="email" id="regEmail" placeholder="you@example.com" value={form.email} onChange={update("email")} required />
          {errors.email && <p className="error-msg">{errors.email}</p>}
        </div>

        <PasswordField
          id="regPassword"
          label="Password"
          placeholder="At least 8 characters"
          value={form.password}
          onChange={update("password")}
          error={errors.password}
          hint="Use 8+ characters. Mix letters and numbers for a stronger password."
        />

        <PasswordField
          id="regConfirm"
          label="Confirm password"
          placeholder="Re-enter your password"
          value={form.confirm}
          onChange={update("confirm")}
          error={errors.confirm}
        />

        <div className="row-between" style={{ justifyContent: "flex-start", gap: 8 }}>
          <label className="checkbox-row">
            <input type="checkbox" checked={terms} onChange={(e) => setTerms(e.target.checked)} required />
            I agree to the Terms and Privacy Policy
          </label>
        </div>

        <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
          {submitting ? "Please wait…" : "Create account"}
        </button>
      </form>

      <div className="divider">or</div>
      <button type="button" className="btn btn-spotify">
        <span className="dot-spotify"></span>Sign up with Spotify
      </button>
    </>
  );
}

export default function Auth() {
  const [params, setParams] = useSearchParams();
  const mode = params.get("mode") === "register" ? "register" : "login";

  function setMode(next) {
    setParams({ mode: next });
  }

  return (
    <div className="auth-shell">
      <aside className="auth-brand">
        <Link to="/" className="logo">
          <span className="dot"></span>Moodify
        </Link>

        <div className="pitch">
          <h1>Your mood is the playlist.</h1>
          <p>Every session starts with a read of how you feel, then Moodify builds around it — no scrolling, no guessing what to play.</p>
          <MiniWaveform />
        </div>

        <span className="footnote">FACE · TEXT · VOICE → SPOTIFY</span>
      </aside>

      <main className="auth-panel">
        <div className="auth-card">
          <Link to="/" className="back">← Back to Moodify</Link>

          <div className="tabs" role="tablist">
            <button
              className={`tab ${mode === "login" ? "active" : ""}`}
              role="tab"
              aria-selected={mode === "login"}
              onClick={() => setMode("login")}
            >
              Log in
            </button>
            <button
              className={`tab ${mode === "register" ? "active" : ""}`}
              role="tab"
              aria-selected={mode === "register"}
              onClick={() => setMode("register")}
            >
              Create account
            </button>
          </div>

          {mode === "login" ? <LoginForm /> : <RegisterForm />}

          <p className="switch-line">
            {mode === "login" ? (
              <>Don't have an account? <button type="button" onClick={() => setMode("register")}>Sign up</button></>
            ) : (
              <>Already have an account? <button type="button" onClick={() => setMode("login")}>Log in</button></>
            )}
          </p>
        </div>
      </main>
    </div>
  );
}
