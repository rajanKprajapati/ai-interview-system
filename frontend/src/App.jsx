import { useState } from "react";
import InterviewSetup from "./InterviewSetup";
import Interview from "./Interview";
import Dashboard from "./Dashboard";
import History from "./History";
import ReportDetail from "./ReportDetail";

function App() {
  const [currentTab, setCurrentTab] = useState("interview"); // 'interview', 'dashboard', 'history', 'report'
  const [interviewStarted, setInterviewStarted] = useState(false);
  const [interviewConfig, setInterviewConfig] = useState({
    type: "technical",
    questionCount: 5,
    difficulty: "intermediate",
    role: "Software Engineer",
    subject: "",
    resumeSkills: [],
    skillGaps: [],
    jobDescription: "",
    resumeFilename: null,
  });
  const [selectedReportId, setSelectedReportId] = useState(null);

  const handleStartInterview = (config) => {
    setInterviewConfig(config);
    setInterviewStarted(true);
    setCurrentTab("interview");
  };

  const handleRestartSetup = () => {
    setInterviewStarted(false);
    setCurrentTab("interview");
  };

  const handleViewReport = (id) => {
    setSelectedReportId(id);
    setCurrentTab("report");
  };

  const handleNavClick = (tab) => {
    if (interviewStarted && currentTab === "interview" && tab !== "interview") {
      if (!window.confirm("An interview is currently in progress. Navigating away will cancel this active session. Proceed?")) {
        return;
      }
      setInterviewStarted(false);
    }
    setCurrentTab(tab);
  };

  return (
    <div className="app-shell">
      {/* Top Application Navbar */}
      <header className="navbar">
        <div className="navbar-brand" onClick={() => handleNavClick("interview")}>
          <span className="brand-logo">🤖</span>
          <div className="brand-text">
            <span className="brand-name">AI Interview Prep</span>
            <span className="brand-tagline">Campus Placement & Technical Readiness</span>
          </div>
        </div>

        <nav className="nav-links">
          <button
            className={`nav-btn ${currentTab === "interview" ? "active" : ""}`}
            onClick={() => handleNavClick("interview")}
          >
            🎙️ Practice Interview
          </button>
          <button
            className={`nav-btn ${currentTab === "dashboard" ? "active" : ""}`}
            onClick={() => handleNavClick("dashboard")}
          >
            📊 Dashboard
          </button>
          <button
            className={`nav-btn ${currentTab === "history" || currentTab === "report" ? "active" : ""}`}
            onClick={() => handleNavClick("history")}
          >
            📁 Session History
          </button>
        </nav>
      </header>

      {/* Main Content Viewport */}
      <main className="main-viewport">
        {currentTab === "interview" && (
          !interviewStarted ? (
            <InterviewSetup onStart={handleStartInterview} />
          ) : (
            <Interview
              config={interviewConfig}
              onNavigate={(tab) => handleNavClick(tab)}
              onRestart={handleRestartSetup}
            />
          )
        )}

        {currentTab === "dashboard" && (
          <Dashboard
            onStartNew={() => {
              setInterviewStarted(false);
              setCurrentTab("interview");
            }}
            onViewDetail={(id) => handleViewReport(id)}
          />
        )}

        {currentTab === "history" && (
          <History
            onViewDetail={(id) => handleViewReport(id)}
            onStartNew={() => {
              setInterviewStarted(false);
              setCurrentTab("interview");
            }}
          />
        )}

        {currentTab === "report" && (
          <ReportDetail
            interviewId={selectedReportId}
            onBack={() => setCurrentTab("history")}
            onStartNew={() => {
              setInterviewStarted(false);
              setCurrentTab("interview");
            }}
          />
        )}
      </main>

      {/* Application Footer */}
      <footer className="app-footer">
        <p>AI Interview Preparation & Evaluation System • Powered by FastAPI, PostgreSQL, Whisper & Gemini</p>
      </footer>
    </div>
  );
}

export default App;
