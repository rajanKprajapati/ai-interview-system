import { useState } from "react";
import Interview from "./Interview";

function App() {

  const [started, setStarted] = useState(false);

  const [config, setConfig] = useState({
    type: "technical",
    questionCount: 5,
  });


  if (started) {

    return (
      <Interview
        config={config}
      />
    );
  }


  return (
    <div className="home-page">

      <div className="home-card">

        <h1>
          AI Interview Preparation
          & Evaluation System
        </h1>

        <p>
          Practice technical, HR and
          behavioral interviews using AI.
        </p>


        <label>
          Interview Type
        </label>

        <select
          value={config.type}
          onChange={(e) =>
            setConfig({
              ...config,
              type: e.target.value,
            })
          }
        >

          <option value="technical">
            Technical
          </option>

          <option value="hr">
            HR
          </option>

          <option value="behavioral">
            Behavioral
          </option>

        </select>


        <label>
          Number of Questions
        </label>

        <select
          value={config.questionCount}
          onChange={(e) =>
            setConfig({
              ...config,
              questionCount:
                Number(e.target.value),
            })
          }
        >

          <option value="3">3 Questions</option>
          <option value="5">5 Questions</option>
          <option value="7">7 Questions</option>
          <option value="10">10 Questions</option>

        </select>


        <button
          onClick={() => setStarted(true)}
        >
          Start AI Interview
        </button>

      </div>

    </div>
  );
}

export default App;