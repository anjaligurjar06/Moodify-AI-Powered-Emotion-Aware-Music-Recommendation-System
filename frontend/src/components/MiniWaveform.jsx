import { useMemo } from "react";

const BAR_COUNT = 22;

export default function MiniWaveform() {
  const bars = useMemo(
    () =>
      Array.from({ length: BAR_COUNT }, () => ({
        duration: (1.4 + Math.random() * 1.6).toFixed(2),
        delay: (Math.random() * 1.2).toFixed(2),
      })),
    []
  );

  return (
    <div className="mini-bars" aria-hidden="true">
      {bars.map((bar, i) => (
        <span
          key={i}
          style={{ animationDuration: `${bar.duration}s`, animationDelay: `${bar.delay}s` }}
        />
      ))}
    </div>
  );
}
