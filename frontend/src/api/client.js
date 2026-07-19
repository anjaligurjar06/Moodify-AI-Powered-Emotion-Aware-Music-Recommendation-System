const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const TOKEN_KEY = "moodify_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function request(path, { method = "GET", body, auth = true, params } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  let url = `${API_URL}${path}`;
  if (params) {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== null)
    ).toString();
    if (qs) url += `?${qs}`;
  }

  const res = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    // no JSON body
  }

  if (!res.ok) {
    const message = data?.detail || res.statusText || "Something went wrong.";
    throw new ApiError(typeof message === "string" ? message : JSON.stringify(message), res.status);
  }

  return data;
}

export const api = {
  register: (payload) => request("/api/auth/register", { method: "POST", body: payload, auth: false }),
  login: (payload) => request("/api/auth/login", { method: "POST", body: payload, auth: false }),
  me: () => request("/api/auth/me"),

  detectText: (text) => request("/api/detect/text", { method: "POST", body: { text } }),
  detectFace: (image) => request("/api/detect/face", { method: "POST", body: { image } }),
  detectFusion: (payload) => request("/api/detect/fusion", { method: "POST", body: payload }),

  generatePlaylist: (emotion, uplift, limit = 10) =>
    request("/api/playlist/generate", { params: { emotion, uplift, limit } }),
  savePlaylist: (payload) => request("/api/playlist/save", { method: "POST", body: payload }),

  moodHistory: () => request("/api/history/moods"),
  playlistHistory: () => request("/api/history/playlists"),

  health: () => request("/health", { auth: false }),
};

export { ApiError };
