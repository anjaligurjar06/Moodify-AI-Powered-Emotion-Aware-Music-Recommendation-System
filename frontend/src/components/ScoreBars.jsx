const EMOTION_META = {
  happy: { label: "Happy", color: "var(--amber)" },
  sad: { label: "Sad", color: "var(--cyan)" },
  angry: { label: "Angry", color: "var(--rose)" },
  neutral: { label: "Neutral", color: "var(--violet)" },
  fear: { label: "Fear", color: "#7c8cff" },
  surprise: { label: "Surprise", color: "#ff9f6b" },
  disgust: { label: "Disgust", color: "#6bff9d" },
};

export default function ScoreBars({ scores }) {
  const entries = Object.entries(scores || {}).sort((a, b) => b[1] - a[1]);

  return (
    <div className="score-bars">
      {entries.map(([key, value]) => {
        const meta = EMOTION_META[key] || { label: key, color: "var(--violet)" };
        const pct = Math.round(value * 100);
        return (
          <div className="score-row" key={key}>
            <span className="score-label">{meta.label}</span>
            <div className="score-track">
              <div className="score-fill" style={{ width: `${pct}%`, background: meta.color }} />
            </div>
            <span className="score-pct">{pct}%</span>
          </div>
        );
      })}
    </div>
  );
}

export { EMOTION_META };
