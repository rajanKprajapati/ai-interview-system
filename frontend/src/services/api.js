const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function handleResponse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const errorMsg = data.detail || `Request failed with status ${response.status}`;
    throw new Error(errorMsg);
  }
  return data;
}

export async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  return handleResponse(response);
}

export async function fetchQuestions({
  type = "technical",
  questionCount = 5,
  difficulty = "intermediate",
  role = "Software Engineer",
  subject = "",
  resumeSkills = null,
  skillGaps = null,
  jobDescription = null,
}) {
  const response = await fetch(`${API_BASE_URL}/api/questions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      interview_type: type,
      question_count: Number(questionCount),
      difficulty,
      role: role || undefined,
      subject: subject || undefined,
      resume_skills: resumeSkills && resumeSkills.length ? resumeSkills : undefined,
      skill_gaps: skillGaps && skillGaps.length ? skillGaps : undefined,
      job_description: jobDescription || undefined,
    }),
  });
  return handleResponse(response);
}

export async function transcribeAudioBlob(audioBlob) {
  const formData = new FormData();
  formData.append("file", audioBlob, "answer.webm");

  const response = await fetch(`${API_BASE_URL}/api/transcribe`, {
    method: "POST",
    body: formData,
  });
  return handleResponse(response);
}

export async function submitEvaluation({
  answers,
  interviewType = "technical",
  difficulty = "intermediate",
  role = "Software Engineer",
  totalDurationSeconds = null,
  developmentMode = false,
  evaluations = null,
  resumeSkills = null,
  resumeFilename = null,
  jobDescription = null,
  visualMetrics = null,
}) {
  const response = await fetch(`${API_BASE_URL}/api/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      answers,
      interview_type: interviewType,
      difficulty,
      role,
      total_duration_seconds: totalDurationSeconds,
      development_mode: developmentMode,
      evaluations,
      resume_skills: resumeSkills,
      resume_filename: resumeFilename,
      job_description: jobDescription,
      visual_metrics: visualMetrics,
    }),
  });
  return handleResponse(response);
}

export async function parseResumeAndJob(resumeFile, jobDescription = "") {
  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("job_description", jobDescription || "General software engineer role");

  const response = await fetch(`${API_BASE_URL}/api/resume/profile`, {
    method: "POST",
    body: formData,
  });
  return handleResponse(response);
}

export async function fetchDashboardStats() {
  const response = await fetch(`${API_BASE_URL}/api/dashboard/stats`);
  return handleResponse(response);
}

export async function fetchInterviews(interviewType = null) {
  const url = interviewType
    ? `${API_BASE_URL}/api/interviews?interview_type=${encodeURIComponent(interviewType)}`
    : `${API_BASE_URL}/api/interviews`;
  const response = await fetch(url);
  return handleResponse(response);
}

export async function fetchInterviewDetail(id) {
  const response = await fetch(`${API_BASE_URL}/api/interviews/${id}`);
  return handleResponse(response);
}

export async function deleteInterviewSession(id) {
  const response = await fetch(`${API_BASE_URL}/api/interviews/${id}`, {
    method: "DELETE",
  });
  return handleResponse(response);
}
