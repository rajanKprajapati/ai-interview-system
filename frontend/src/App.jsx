import { useState } from "react";
import "./App.css";

import InterviewSetup from "./InterviewSetup";
import Interview from "./Interview";

function App() {
  const [page, setPage] = useState("home");
  const [interviewConfig, setInterviewConfig] = useState(null);

  const handleStartInterview = (config) => {
    setInterviewConfig(config);
    setPage("interview");
  };

  if (page === "setup") {
    return (
      <InterviewSetup
        onStart={handleStartInterview}
      />
    );
  }

  if (page === "interview") {
    return (
      <Interview
        config={interviewConfig}
      />
    );
  }

  return (
    <div className="app">
      <div className="hero">

        <h1>
          AI Interview Preparation & Evaluation System
        </h1>

        <p>
          Practice realistic camera-based interviews
          and receive AI-powered feedback.
        </p>

        <button onClick={() => setPage("setup")}>
          Start Interview
        </button>

      </div>
    </div>
  );
}

export default App;