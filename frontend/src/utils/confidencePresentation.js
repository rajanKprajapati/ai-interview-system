/**
 * Maps measured metrics to presentation labels.
 * These are communication indicators, NOT a definitive confidence score.
 */
export function confidenceIndicatorRows(metrics) {
  if (!metrics) return [];

  const rows = [
    {
      label: "Speaking pace",
      value: metrics.speaking_pace_label || "Not measured",
      detail: metrics.speaking_pace_wpm == null
        ? "Recording duration was not supplied."
        : `${metrics.speaking_pace_wpm} words/minute`,
    },
    {
      label: "Filler words",
      value: metrics.filler_label || "Not measured",
      detail: `${metrics.filler_word_count ?? 0} detected`,
    },
    {
      label: "Long pauses",
      value: metrics.long_pauses?.status === "measured"
        ? metrics.long_pauses.label
        : "Not measured",
      detail: metrics.long_pauses?.message || "",
    },
    {
      label: "Camera engagement",
      value: metrics.camera_engagement?.status === "measured"
        ? metrics.camera_engagement.label
        : "Not measured",
      detail: metrics.camera_engagement?.message || "",
    },
  ];

  return rows;
}
