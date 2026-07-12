import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="nav">
      <div className="wrap">
        <Link to="/" className="logo">
          <span className="dot"></span>Moodify
        </Link>
        <ul className="nav-links">
          <li><a href="#features">Detection</a></li>
          <li><a href="#how">How it works</a></li>
          <li><a href="#mapping">Mood mapping</a></li>
        </ul>
        <div className="nav-cta">
          <Link to="/auth?mode=login" className="btn btn-ghost nav-only">Log in</Link>
          <Link to="/auth?mode=register" className="btn btn-primary">Get started</Link>
        </div>
      </div>
    </nav>
  );
}
