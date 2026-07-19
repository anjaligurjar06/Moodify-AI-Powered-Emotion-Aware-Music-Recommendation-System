import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function AppNavbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="nav app-nav">
      <div className="wrap">
        <Link to="/" className="logo">
          <span className="dot"></span>Moodify
        </Link>
        <ul className="nav-links">
          <li><NavLink to="/detect" className={({ isActive }) => (isActive ? "active" : "")}>Detect</NavLink></li>
          <li><NavLink to="/playlist" className={({ isActive }) => (isActive ? "active" : "")}>Playlist</NavLink></li>
          <li><NavLink to="/history" className={({ isActive }) => (isActive ? "active" : "")}>History</NavLink></li>
        </ul>
        <div className="nav-cta">
          <span className="hello-user nav-only">Hi, {user?.name?.split(" ")[0]}</span>
          <button type="button" className="btn btn-ghost" onClick={logout}>Log out</button>
        </div>
      </div>
    </nav>
  );
}
