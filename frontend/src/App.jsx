import { Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing.jsx";
import Auth from "./pages/Auth.jsx";
import Detect from "./pages/Detect.jsx";
import Playlist from "./pages/Playlist.jsx";
import History from "./pages/History.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/auth" element={<Auth />} />
      <Route
        path="/detect"
        element={
          <ProtectedRoute>
            <Detect />
          </ProtectedRoute>
        }
      />
      <Route
        path="/playlist"
        element={
          <ProtectedRoute>
            <Playlist />
          </ProtectedRoute>
        }
      />
      <Route
        path="/history"
        element={
          <ProtectedRoute>
            <History />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}
