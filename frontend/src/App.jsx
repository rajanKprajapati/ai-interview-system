import { useState } from "react";
import "./App.css";
import Interview from "./Interview";

function App() {
  const [page, setPage] = useState("home");

  if (page === "interview") {
    return <Interview />;
  }

  return (
    <div className="app">
      <div className="hero">
        <h1>AI Interview Preparation & Evaluation System</h1>

        <p>
          Practice realistic camera-based interviews and receive
          AI-powered feedback on your answers and communication.
        </p>

        <button onClick={() => setPage("interview")}>
          Start Interview
        </button>
      </div>
    </div>
  );
}

export default App;