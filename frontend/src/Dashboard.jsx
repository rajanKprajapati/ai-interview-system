import { useEffect, useState } from "react";
import { fetchDashboardStats } from "./services/api";

function Dashboard({ onStartNew, onViewDetail }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await fetchDashboardStats();
      setStats(data);
    } catch (err) {
      console.error("Dashboard stats load error:", err);
      setError(err.message || "Failed to load performance statistics.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="center-view">
        <div className="spinner" />
        <h2>Loading Performance Dashboard...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="center-view">
        <div className="error-icon">!</div>
        <h2>Could Not Load Dashboard</h2>
        <p>{error}</p>
        <button className="primary-btn" onClick={loadStats}>Retry</button>
      </div>
    );
  }

  const total = stats?.total_interviews || 0;
  const avg = Number(stats?.average_score || 0);
  const cats = stats?.category_scores || {};
  const recent = stats?.recent_interviews || [];
  const trend = stats?.score_trend || [];
  const types = stats?.type_breakdown || {};
  const comm = stats?.communication_summary || {};

  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="dashboard-header">
        <div>
          <span className="setup-badge">PERFORMANCE ANALYTICS</span>
          <h1>Candidate Dashboard</h1>
          <p>Track your interview preparation trends, score improvements, and delivery analytics.</p>
        </div>
        <button className="primary-btn" onClick={onStartNew}>
          + Start New Interview
        </button>
      </div>

      {total === 0 ? (
        <div className="empty-card">
          <div className="empty-icon">🎯</div>
          <h2>No Interviews Completed Yet</h2>
          <p>Complete your first AI mock interview to generate performance analytics, score trends, and personalized feedback.</p>
          <button className="primary-btn" onClick={onStartNew}>
            Take Your First Interview
          </button>
        </div>
      ) : (
        <>
          {/* KPI Grid */}
          <div className="kpi-grid">
            <div className="kpi-card highlight">
              <span className="kpi-label">OVERALL AVERAGE</span>
              <div className="kpi-val-group">
                <span className="kpi-num">{avg.toFixed(1)}</span>
                <span className="kpi-denom">/ 10</span>
              </div>
              <span className="kpi-note">{total} completed session{total === 1 ? "" : "s"}</span>
            </div>

            <div className="kpi-card">
              <span className="kpi-label">TECHNICAL ACCURACY</span>
              <div className="kpi-val-group">
                <span className="kpi-num">{Number(cats.technical_accuracy || 0).toFixed(1)}</span>
                <span className="kpi-denom">/ 10</span>
              </div>
              <div className="mini-progress">
                <div style={{ width: `${(cats.technical_accuracy || 0) * 10}%` }} />
              </div>
            </div>

            <div className="kpi-card">
              <span className="kpi-label">COMMUNICATION</span>
              <div className="kpi-val-group">
                <span className="kpi-num">{Number(cats.communication || 0).toFixed(1)}</span>
                <span className="kpi-denom">/ 10</span>
              </div>
              <div className="mini-progress">
                <div style={{ width: `${(cats.communication || 0) * 10}%` }} />
              </div>
            </div>

            <div className="kpi-card">
              <span className="kpi-label">SPEAKING PACE</span>
              <div className="kpi-val-group">
                <span className="kpi-num">{comm.average_wpm ? `${comm.average_wpm}` : "—"}</span>
                {comm.average_wpm && <span className="kpi-denom">WPM</span>}
              </div>
              <span className="kpi-note">
                {comm.average_wpm ? "Target: 120–160 WPM" : "Calculated from recording"}
              </span>
            </div>
          </div>

          {/* Progress Chart & Breakdown */}
          <div className="analytics-row">
            {/* Score Trend Card */}
            <div className="card flex-2">
              <div className="card-top">
                <h3>Score Trend (Recent Sessions)</h3>
                <span className="card-hint">Scores out of 10</span>
              </div>
              {trend.length > 0 ? (
                <div className="chart-container">
                  <div className="bar-chart">
                    {trend.map((point, index) => {
                      const heightPercent = Math.min(100, Math.max(15, (point.score / 10) * 100));
                      const isGood = point.score >= 7.5;
                      return (
                        <div key={index} className="bar-col" onClick={() => onViewDetail(point.id)}>
                          <span className="bar-val">{Number(point.score).toFixed(1)}</span>
                          <div
                            className={`chart-bar ${isGood ? "bar-green" : "bar-blue"}`}
                            style={{ height: `${heightPercent}%` }}
                            title={`Session #${point.id} (${point.type}): ${point.score}/10`}
                          />
                          <span className="bar-label">{point.date}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ) : (
                <p className="muted">Complete more sessions to build a score trend.</p>
              )}
            </div>

            {/* Category Breakdown */}
            <div className="card flex-1">
              <div className="card-top">
                <h3>Competency Breakdown</h3>
              </div>
              <div className="competency-list">
                <div className="comp-item">
                  <div className="comp-info">
                    <span>Relevance</span>
                    <strong>{Number(cats.relevance || 0).toFixed(1)} / 10</strong>
                  </div>
                  <div className="comp-bar"><div style={{ width: `${(cats.relevance || 0) * 10}%` }} /></div>
                </div>

                <div className="comp-item">
                  <div className="comp-info">
                    <span>Technical Accuracy</span>
                    <strong>{Number(cats.technical_accuracy || 0).toFixed(1)} / 10</strong>
                  </div>
                  <div className="comp-bar"><div style={{ width: `${(cats.technical_accuracy || 0) * 10}%` }} /></div>
                </div>

                <div className="comp-item">
                  <div className="comp-info">
                    <span>Communication</span>
                    <strong>{Number(cats.communication || 0).toFixed(1)} / 10</strong>
                  </div>
                  <div className="comp-bar"><div style={{ width: `${(cats.communication || 0) * 10}%` }} /></div>
                </div>

                <div className="comp-item">
                  <div className="comp-info">
                    <span>Confidence Signals</span>
                    <strong>{Number(cats.confidence || 0).toFixed(1)} / 10</strong>
                  </div>
                  <div className="comp-bar"><div style={{ width: `${(cats.confidence || 0) * 10}%` }} /></div>
                </div>
              </div>

              <div className="type-pills">
                <span className="type-pill">Technical: <strong>{types.technical || 0}</strong></span>
                <span className="type-pill">HR: <strong>{types.hr || 0}</strong></span>
                <span className="type-pill">Behavioral: <strong>{types.behavioral || 0}</strong></span>
              </div>
            </div>
          </div>

          {/* Recent Interviews Table */}
          <div className="card">
            <div className="card-top">
              <h3>Recent Interview Sessions</h3>
              <span className="card-hint">Total: {total}</span>
            </div>

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Questions</th>
                    <th>Score</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {recent.map((item) => (
                    <tr key={item.id}>
                      <td><strong>{item.date}</strong></td>
                      <td>
                        <span className={`badge-type ${item.interview_type}`}>
                          {item.interview_type}
                        </span>
                      </td>
                      <td>{item.question_count} questions</td>
                      <td>
                        <span className={`badge-score ${item.overall_score >= 8 ? "high" : item.overall_score >= 6 ? "mid" : "low"}`}>
                          {Number(item.overall_score).toFixed(1)} / 10
                        </span>
                      </td>
                      <td>
                        <button
                          className="link-btn"
                          onClick={() => onViewDetail(item.id)}
                        >
                          View Report →
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard;
