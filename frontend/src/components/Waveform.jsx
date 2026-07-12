import { useEffect, useMemo, useState } from "react";

const MOODS = [
  "Focused, easing into calm",
  "Upbeat, energy climbing",
  "Steady, low arousal",
  "Reflective, valence dipping",
];

const BAR_COUNT = 28;

export default function Waveform() {
  const [moodIndex, setMoodIndex] = useState(0);
  const [visible, setVisible] = useState(true);

  // Randomised timing per bar so the equalizer feels alive rather
  // than mechanically uniform, computed once on mount.
  const bars = useMemo(
    () =>
      Array.from({ length: BAR_COUNT }, () => ({
        duration: (1.2 + Math.random() * 1.4).toFixed(2),
        delay: (Math.random() * 1.2).toFixed(2),
      })),
    []
  );

  useEffect(() => {
    const cycle = setInterval(() => {
      setVisible(false);
      const swap = setTimeout(() => {
        setMoodIndex((i) => (i + 1) % MOODS.length);
        setVisible(true);
      }, 250);
      return () => clearTimeout(swap);
    }, 4200);
    return () => clearInterval(cycle);
  }, []);

  return (
    <div className="waveform-card">
      <div className="waveform-head">
        <div>
          <div className="mood-label">Current read</div>
          <div className="mood-value" style={{ opacity: visible ? 1 : 0 }}>
            {MOODS[moodIndex]}
          </div>
        </div>
        <div className="live-badge">
          <span className="ping"></span>LIVE
        </div>
      </div>

      <div className="bars" aria-hidden="true">
        {bars.map((bar, i) => (
          <span
            key={i}
            style={{ animationDuration: `${bar.duration}s`, animationDelay: `${bar.delay}s` }}
          />
        ))}
      </div>

      <div className="waveform-foot">
        <span>VALENCE 0.62</span>
        <span>ENERGY 0.48</span>
        <span>TEMPO 104 BPM</span>
      </div>
    </div>
  );
}
