import { useState } from "react";

function InterviewSetup({ onStart }) {
  const [type, setType] = useState("technical");
  const [questionCount, setQuestionCount] = useState(5);

  const startInterview = () => {
    onStart({
      type,
      questionCount: Number(questionCount),
    });
  };

  return (
    <div className="setup-page">
      <h1>AI Interview</h1>

      <p>
        Configure your interview before starting.
      </p>

      <div className="setup-section">
        <h2>Interview Type</h2>

        <div className="option-group">
          <button
            className={type === "technical" ? "selected" : ""}
            onClick={() => setType("technical")}
          >
            Technical
          </button>

          <button
            className={type === "hr" ? "selected" : ""}
            onClick={() => setType("hr")}
          >
            HR
          </button>

          <button
            className={type === "behavioral" ? "selected" : ""}
            onClick={() => setType("behavioral")}
          >
            Behavioral
          </button>
        </div>
      </div>

      <div className="setup-section">
        <h2>Number of Questions</h2>

        <select
          value={questionCount}
          onChange={(e) => setQuestionCount(e.target.value)}
        >
          <option value="3">3 Questions</option>
          <option value="5">5 Questions</option>
          <option value="10">10 Questions</option>
        </select>
      </div>

      <button
        className="start-interview-button"
        onClick={startInterview}
      >
        Start Interview
      </button>
    </div>
  );
}

export default InterviewSetup;