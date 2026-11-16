const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function readJson(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || `Request failed (${response.status})`);
  }
  return data;
}

export async function analyzeConfidence(transcript, durationSeconds) {
  const response = await fetch(`${API_BASE_URL}/api/confidence/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      transcript,
      duration_seconds: durationSeconds || null,
    }),
  });
  return readJson(response);
}

export async function analyzeResumeAndJob(resumeFile, jobDescription) {
  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("job_description", jobDescription);

  const response = await fetch(`${API_BASE_URL}/api/resume/profile`, {
    method: "POST",
    body: formData,
  });
  return readJson(response);
}

export async function getPersonalizedFeedback(evaluations, communicationMetrics = null) {
  const response = await fetch(`${API_BASE_URL}/api/feedback/personalized`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      evaluations,
      communication_metrics: communicationMetrics,
    }),
  });
  return readJson(response);
}
