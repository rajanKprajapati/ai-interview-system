import { useEffect, useState } from "react";
import { fetchInterviewDetail } from "./services/api";

function ReportDetail({ interviewId, onBack, onStartNew }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (interviewId) {
      loadReport();
    }
  }, [interviewId]);

  const loadReport = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await fetchInterviewDetail(interviewId);
      setReport(data);
    } catch (err) {
      console.error("Error loading interview detail:", err);
      setError(err.message || "Failed to load interview report.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="center-view">
        <div className="spinner" />
        <p>Loading full interview report...</p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="center-view">
        <div className="error-icon">!</div>
        <h2>Report Not Found</h2>
        <p>{error || "Could not retrieve the specified interview session."}</p>
        <button className="primary-btn" onClick={onBack}>← Back to History</button>
      </div>
    );
  }

  const overallScore = Number(report.overall_score || 0);
  const cat = report.category_scores || {};
  const comm = report.communication_metrics || {};
  const feedback = report.personalized_feedback || {};
  const questions = report.evaluations || [];

  const getVerdict = (s) => {
    if (s >= 8.5) return "Excellent Performance";
    if (s >= 7.0) return "Good Interview";
    if (s >= 5.5) return "Average / Passing";
    return "Needs Improvement";
  };

  const getScoreBadgeClass = (s) => {
    if (s >= 8) return "score-high";
    if (s >= 6) return "score-mid";
    return "score-low";
  };

  return (
    <div className="results-container">
      {/* Top Navigation */}
      <div className="report-nav-bar">
        <button className="back-link" onClick={onBack}>
          ← Back to History
        </button>
        <button className="primary-btn" onClick={onStartNew}>
          + Practice Another Session
        </button>
      </div>

      {/* Header */}
      <div className="results-header">
        <div>
          <span className="eyebrow">
            SESSION #{report.interview_id} • {report.interview_type?.toUpperCase()} INTERVIEW
          </span>
          <h1>Interview Performance Report</h1>
          <p>Recorded on {report.created_at ? new Date(report.created_at).toLocaleString() : "Recently"}</p>
        </div>
      </div>

      {/* Overall Score Card */}
      <div className="overall-card">
        <div className="overall-score">
          <div className="score-number">{overallScore.toFixed(1)}</div>
          <div className="score-out-of">/ 10</div>
        </div>

        <div className="overall-info">
          <span className="eyebrow">OVERALL VERDICT</span>
          <h2>{getVerdict(overallScore)}</h2>
          <p>
            Evaluated across <strong>{questions.length}</strong> questions with verified AI scoring and communication metrics.
          </p>
        </div>
      </div>

      {/* Score Breakdown Grid */}
      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">EVALUATION METRICS</span>
            <h2>Core Competency Scores</h2>
          </div>
        </div>

        <div className="score-grid">
          <div className="score-card">
            <div className="score-card-top">
              <span>Relevance</span>
              <strong>{Number(cat.relevance || 0).toFixed(1)}</strong>
            </div>
            <div className="score-progress"><div style={{ width: `${(cat.relevance || 0) * 10}%` }} /></div>
            <small>/ 10</small>
          </div>

          <div className="score-card">
            <div className="score-card-top">
              <span>Technical Accuracy</span>
              <strong>{Number(cat.technical_accuracy || 0).toFixed(1)}</strong>
            </div>
            <div className="score-progress"><div style={{ width: `${(cat.technical_accuracy || 0) * 10}%` }} /></div>
            <small>/ 10</small>
          </div>

          <div className="score-card">
            <div className="score-card-top">
              <span>Communication</span>
              <strong>{Number(cat.communication || 0).toFixed(1)}</strong>
            </div>
            <div className="score-progress"><div style={{ width: `${(cat.communication || 0) * 10}%` }} /></div>
            <small>/ 10</small>
          </div>

          <div className="score-card">
            <div className="score-card-top">
              <span>Observable Confidence</span>
              <strong>{Number(cat.confidence || 0).toFixed(1)}</strong>
            </div>
            <div className="score-progress"><div style={{ width: `${(cat.confidence || 0) * 10}%` }} /></div>
            <small>/ 10</small>
          </div>
        </div>
      </section>

      {/* Observable Communication Indicators */}
      {comm && (
        <section className="section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">DELIVERY & COMMUNICATION</span>
              <h2>Observable Delivery Indicators</h2>
            </div>
          </div>

          <div className="comm-metrics-grid">
            <div className="comm-card">
              <span className="comm-label">Speaking Pace</span>
              <strong className="comm-val">
                {comm.speaking_pace_wpm ? `${comm.speaking_pace_wpm} WPM` : "Not measured"}
              </strong>
              <span className="comm-desc">
                Pace Rating: <strong>{comm.speaking_pace_label || "Normal"}</strong> (Target: 120–160 WPM)
              </span>
            </div>

            <div className="comm-card">
              <span className="comm-label">Filler Words</span>
              <strong className="comm-val">
                {comm.filler_word_count !== undefined ? `${comm.filler_word_count}` : "0"} detected
              </strong>
              <span className="comm-desc">
                Filler Density: <strong>{comm.filler_label || "Low"}</strong> ({comm.filler_rate_percent ?? 0}%)
              </span>
            </div>

            <div className="comm-card">
              <span className="comm-label">Total Duration</span>
              <strong className="comm-val">
                {comm.duration_seconds ? `${Math.round(comm.duration_seconds)}s` : "Calculated per answer"}
              </strong>
              <span className="comm-desc">Active speaking and audio capture</span>
            </div>

            <div className="comm-card">
              <span className="comm-label">Visual Engagement</span>
              <strong className="comm-val">
                {comm.face_present ? "Face Detected" : "Camera Active"}
              </strong>
              <span className="comm-desc">Continuous webcam preview engaged</span>
            </div>
          </div>

          <p className="metric-disclaimer">
            ℹ️ {comm.interpretation || "These are observable communication metrics and delivery signals, not psychological assessments."}
          </p>
        </section>
      )}

      {/* Personalized Feedback */}
      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">SYNTHESIS</span>
            <h2>Personalized Feedback & Action Plan</h2>
          </div>
        </div>

        <div className="feedback-split">
          <div className="feedback-box strengths-box">
            <h3>✓ Key Strengths</h3>
            <ul>
              {(feedback.strengths || ["Demonstrated solid technical understanding."]).map((s, idx) => (
                <li key={idx}>{s}</li>
              ))}
            </ul>
          </div>

          <div className="feedback-box weaknesses-box">
            <h3>! Areas for Growth</h3>
            <ul>
              {(feedback.weaknesses || ["No major low-scoring area was flagged."]).map((w, idx) => (
                <li key={idx}>{w}</li>
              ))}
            </ul>
          </div>
        </div>

        {feedback.recommended_practice && feedback.recommended_practice.length > 0 && (
          <div className="practice-box">
            <h3>🎯 Recommended Practice Topics</h3>
            <ol>
              {feedback.recommended_practice.map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ol>
          </div>
        )}
      </section>

      {/* Question by Question Detailed Breakdown */}
      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">DETAILED BREAKDOWN</span>
            <h2>Question & Answer Analysis</h2>
          </div>
        </div>

        <div className="evaluation-list">
          {questions.map((q, idx) => {
            const qScore = Number(q.overall_score || 0);
            return (
              <div key={idx} className="evaluation-card">
                <div className="evaluation-top">
                  <div>
                    <span className="question-number">QUESTION {q.question_number || idx + 1}</span>
                    <h3>{q.question}</h3>
                  </div>
                  <div className={`question-score ${getScoreBadgeClass(qScore)}`}>
                    {qScore.toFixed(1)} / 10
                  </div>
                </div>

                <div className="answer-box">
                  <span className="answer-label">CANDIDATE TRANSCRIPT:</span>
                  <p>{q.answer || "No response recorded."}</p>
                </div>

                <div className="mini-score-grid">
                  <div className="mini-score">
                    <span>Relevance</span>
                    <strong>{Number(q.relevance || 0).toFixed(1)}</strong>
                  </div>
                  <div className="mini-score">
                    <span>Technical</span>
                    <strong>{Number(q.technical_accuracy || 0).toFixed(1)}</strong>
                  </div>
                  <div className="mini-score">
                    <span>Communication</span>
                    <strong>{Number(q.communication || 0).toFixed(1)}</strong>
                  </div>
                  <div className="mini-score">
                    <span>Confidence</span>
                    <strong>{Number(q.confidence || 0).toFixed(1)}</strong>
                  </div>
                </div>

                <div className="qa-feedback-grid">
                  {q.strengths && q.strengths.length > 0 && (
                    <div className="qa-strengths">
                      <strong>Strengths:</strong>
                      <ul>
                        {q.strengths.map((st, i) => (
                          <li key={i}>{st}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {q.weaknesses && q.weaknesses.length > 0 && (
                    <div className="qa-weaknesses">
                      <strong>Weaknesses:</strong>
                      <ul>
                        {q.weaknesses.map((wk, i) => (
                          <li key={i}>{wk}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {q.improvement_feedback && (
                  <div className="improvement-note">
                    <strong>Suggestion:</strong> {q.improvement_feedback}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}

export default ReportDetail;
