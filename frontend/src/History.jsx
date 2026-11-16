import { useEffect, useState } from "react";
import { fetchInterviews, deleteInterviewSession } from "./services/api";

function History({ onViewDetail, onStartNew }) {
  const [interviews, setInterviews] = useState([]);
  const [filterType, setFilterType] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    loadInterviews();
  }, [filterType]);

  const loadInterviews = async () => {
    try {
      setLoading(true);
      setError("");
      const typeParam = filterType === "all" ? null : filterType;
      const data = await fetchInterviews(typeParam);
      setInterviews(data.interviews || []);
    } catch (err) {
      console.error("Error loading interview history:", err);
      setError(err.message || "Could not load interview history.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm(`Are you sure you want to delete Interview Session #${id}?`)) {
      return;
    }

    try {
      setDeletingId(id);
      await deleteInterviewSession(id);
      setInterviews((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      alert("Failed to delete interview: " + err.message);
    } finally {
      setDeletingId(null);
    }
  };

  const formatDate = (isoStr) => {
    if (!isoStr) return "Recently";
    try {
      const d = new Date(isoStr);
      return d.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return isoStr;
    }
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <div>
          <span className="setup-badge">SESSION LOGS</span>
          <h1>Interview History</h1>
          <p>Review past answers, AI evaluations, strengths, weaknesses, and improvement advice.</p>
        </div>
        <button className="primary-btn" onClick={onStartNew}>
          + New Interview
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="history-filters">
        {["all", "technical", "hr", "behavioral"].map((f) => (
          <button
            key={f}
            className={`filter-tab ${filterType === f ? "active" : ""}`}
            onClick={() => setFilterType(f)}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="center-view">
          <div className="spinner" />
          <p>Loading past interviews...</p>
        </div>
      ) : error ? (
        <div className="center-view">
          <div className="error-icon">!</div>
          <p>{error}</p>
          <button className="primary-btn" onClick={loadInterviews}>Retry</button>
        </div>
      ) : interviews.length === 0 ? (
        <div className="empty-card">
          <div className="empty-icon">📁</div>
          <h2>No Interviews Found</h2>
          <p>
            {filterType === "all"
              ? "You haven't completed any mock interviews yet."
              : `No ${filterType} interviews found in your history.`}
          </p>
          <button className="primary-btn" onClick={onStartNew}>
            Start An Interview
          </button>
        </div>
      ) : (
        <div className="history-list">
          {interviews.map((item) => {
            const score = Number(item.overall_score || 0);
            return (
              <div
                key={item.id}
                className="history-card"
                onClick={() => onViewDetail(item.id)}
              >
                <div className="history-card-left">
                  <div className="session-number">#{item.id}</div>
                  <div>
                    <div className="history-card-title">
                      <span className={`badge-type ${item.interview_type}`}>
                        {item.interview_type.toUpperCase()}
                      </span>
                      <span className="history-date">{formatDate(item.created_at)}</span>
                    </div>
                    <div className="history-sub">
                      {item.question_count} questions completed
                    </div>
                  </div>
                </div>

                <div className="history-card-right">
                  <div className="history-score-box">
                    <span className="score-val">{score.toFixed(1)}</span>
                    <span className="score-denom">/10</span>
                  </div>

                  <div className="history-actions">
                    <button
                      className="view-btn"
                      onClick={() => onViewDetail(item.id)}
                    >
                      View Report
                    </button>
                    <button
                      className="delete-btn"
                      disabled={deletingId === item.id}
                      onClick={(e) => handleDelete(item.id, e)}
                      title="Delete interview session"
                    >
                      {deletingId === item.id ? "..." : "🗑️"}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default History;
