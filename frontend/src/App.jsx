import { Routes, Route } from "react-router-dom";
import Landing from "./pages/Landing.jsx";
import Auth from "./pages/Auth.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/auth" element={<Auth />} />
    </Routes>
  );
}
