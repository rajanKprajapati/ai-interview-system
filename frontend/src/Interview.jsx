import { useEffect, useRef, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

const DEVELOPMENT_MODE = true;
const SAMPLE_QUESTIONS = [
  "What is Object-Oriented Programming and what are its main principles?",
  "What is the difference between a stack and a queue?",
  "Explain the difference between a process and a thread.",
  "What is a primary key in a database?",
  "Tell me about a technical project you have worked on."
];



const SAMPLE_EVALUATIONS = [
  {
    question_number: 1,
    relevance: 8,
    technical_accuracy: 8,
    communication: 8,
    confidence: 7,
    overall_score: 8,
    strengths: [
      "Good understanding of the concept",
      "Explained the main principles clearly"
    ],
    weaknesses: [
      "Could provide more practical examples"
    ],
    improvement_feedback:
      "Try to support theoretical explanations with a simple real-world or programming example."
  },
  {
    question_number: 2,
    relevance: 8,
    technical_accuracy: 7,
    communication: 8,
    confidence: 8,
    overall_score: 7.8,
    strengths: [
      "Correctly explained the basic concepts",
      "Answer was easy to understand"
    ],
    weaknesses: [
      "Could explain use cases in more detail"
    ],
    improvement_feedback:
      "Practice explaining when each data structure should be preferred."
  },
  {
    question_number: 3,
    relevance: 8,
    technical_accuracy: 8,
    communication: 7,
    confidence: 7,
    overall_score: 7.5,
    strengths: [
      "Good conceptual understanding"
    ],
    weaknesses: [
      "Answer could be more structured"
    ],
    improvement_feedback:
      "Use a simple comparison structure when explaining similar technical concepts."
  },
  {
    question_number: 4,
    relevance: 9,
    technical_accuracy: 8,
    communication: 8,
    confidence: 8,
    overall_score: 8.2,
    strengths: [
      "Correct database terminology",
      "Clear explanation"
    ],
    weaknesses: [
      "Could include a practical example"
    ],
    improvement_feedback:
      "Practice explaining database concepts using small example tables."
  },
  {
    question_number: 5,
    relevance: 9,
    technical_accuracy: 8,
    communication: 9,
    confidence: 8,
    overall_score: 8.5,
    strengths: [
      "Good project explanation",
      "Clear communication"
    ],
    weaknesses: [
      "Could explain personal contribution in greater detail"
    ],
    improvement_feedback:
      "During project questions, clearly describe your individual role, technologies used, and challenges solved."
  }
];

function Interview() {
  const [interviewType, setInterviewType] = useState("technical");
  const [questionCount, setQuestionCount] = useState(5);

  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [answers, setAnswers] = useState([]);
  const [currentAnswer, setCurrentAnswer] = useState("");

  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");

  const [cameraEnabled, setCameraEnabled] = useState(false);
  const [micEnabled, setMicEnabled] = useState(false);
  const [recording, setRecording] = useState(false);

  const [transcribing, setTranscribing] = useState(false);
  const [evaluating, setEvaluating] = useState(false);

  const [evaluations, setEvaluations] = useState([]);

  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

useEffect(() => {
  generateQuestions();

  return () => {
    stopMediaStream();
  };
}, []);

useEffect(() => {
  if (
    cameraEnabled &&
    videoRef.current &&
    streamRef.current
  ) {
    videoRef.current.srcObject = streamRef.current;

    videoRef.current.play().catch((err) => {
      console.error("Camera video playback error:", err);
    });
  }
}, [cameraEnabled]);

  async function generateQuestions() {
  setStatus("loading");
  setError("");
  setQuestions([]);
  setAnswers([]);
  setCurrentQuestion(0);
  setCurrentAnswer("");
  setEvaluations([]);

  if (DEVELOPMENT_MODE) {
    setTimeout(() => {
      setQuestions(
        SAMPLE_QUESTIONS.slice(0, questionCount)
      );

      setStatus("interview");
    }, 300);

    return;
  }

  try {
    const response = await fetch(
      `${API_URL}/api/questions`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          interview_type: interviewType,
          question_count: questionCount,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
          "Failed to generate interview questions."
      );
    }

    if (!data.questions || data.questions.length === 0) {
      throw new Error(
        "No interview questions were generated."
      );
    }

    setQuestions(data.questions);
    setStatus("interview");
  } catch (err) {
    console.error(err);
    setError(err.message || "Something went wrong.");
    setStatus("error");
  }
}

async function enableCameraAndMic() {
  try {
    setError("");

    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });

    streamRef.current = stream;

    if (videoRef.current) {
      videoRef.current.srcObject = stream;

      try {
        await videoRef.current.play();
      } catch (err) {
        console.error("Video playback error:", err);
      }
    }

    setCameraEnabled(true);
    setMicEnabled(true);
  } catch (err) {
    console.error(err);

    setError(
      "Camera or microphone permission was denied. Please allow access in your browser."
    );
  }
}

  function stopMediaStream() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        track.stop();
      });

      streamRef.current = null;
    }
  }

  function startRecording() {
    if (!streamRef.current) {
      setError("Please enable the camera and microphone first.");
      return;
    }

    try {
      setError("");
      audioChunksRef.current = [];

      const audioTracks = streamRef.current.getAudioTracks();

      if (audioTracks.length === 0) {
        setError("Microphone is not available.");
        return;
      }

      const audioStream = new MediaStream(audioTracks);

      let options = {};

      if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
        options = {
          mimeType: "audio/webm;codecs=opus",
        };
      } else if (MediaRecorder.isTypeSupported("audio/webm")) {
        options = {
          mimeType: "audio/webm",
        };
      }

      const recorder = new MediaRecorder(audioStream, options);

      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: recorder.mimeType || "audio/webm",
        });

        await transcribeAudio(audioBlob);
      };

      recorder.start();

      setRecording(true);
    } catch (err) {
      console.error(err);
      setError("Unable to start recording.");
    }
  }

  function stopRecording() {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !== "inactive"
    ) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  }

  async function transcribeAudio(audioBlob) {
    try {
      setTranscribing(true);
      setError("");

      const formData = new FormData();

      formData.append(
        "file",
        audioBlob,
        "interview-answer.webm"
      );

      const response = await fetch(
        `${API_URL}/api/transcribe`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Speech-to-text failed."
        );
      }

      const transcript = (data.transcript || "").trim();

      if (!transcript) {
        throw new Error(
          "No speech was detected. Please try recording again."
        );
      }

      setCurrentAnswer(transcript);
    } catch (err) {
      console.error(err);
      setError(err.message || "Transcription failed.");
    } finally {
      setTranscribing(false);
    }
  }

    function saveCurrentAnswer() {
    const answer = currentAnswer.trim();

    if (!answer) {
      setError("Please provide an answer before continuing.");
      return;
    }

    const question = questions[currentQuestion];

    const updatedAnswers = [
      ...answers,
      {
        question,
        answer,
      },
    ];

    setAnswers(updatedAnswers);
    setCurrentAnswer("");
    setError("");

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((previous) => previous + 1);
    } else {
      finishInterview(updatedAnswers);
    }
  }

  async function finishInterview(finalAnswers) {
    try {
      setEvaluating(true);
      setStatus("evaluating");
      setError("");

      const sampleEvaluations = SAMPLE_EVALUATIONS.slice(
        0,
        finalAnswers.length
      );

      const requestBody = DEVELOPMENT_MODE
        ? {
            answers: finalAnswers,
            development_mode: true,
            evaluations: sampleEvaluations,
          }
        : {
            answers: finalAnswers,
          };

      const response = await fetch(
        `${API_URL}/api/evaluate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Interview evaluation failed."
        );
      }

      if (
        !data.evaluations ||
        data.evaluations.length === 0
      ) {
        throw new Error(
          "No evaluation was returned."
        );
      }

      setEvaluations(data.evaluations);
      setStatus("results");

      stopMediaStream();
      setCameraEnabled(false);
      setMicEnabled(false);
      setRecording(false);

    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Unable to evaluate the interview."
      );

      setStatus("error");

    } finally {
      setEvaluating(false);
    }
  }

  function restartInterview() {
    stopMediaStream();

    setQuestions([]);
    setAnswers([]);
    setCurrentAnswer("");
    setCurrentQuestion(0);
    setEvaluations([]);
    setError("");
    setCameraEnabled(false);
    setMicEnabled(false);
    setRecording(false);

    generateQuestions();
  }

  function calculateOverallScore() {
    if (evaluations.length === 0) {
      return 0;
    }

    const total = evaluations.reduce(
      (sum, item) =>
        sum + Number(item.overall_score || 0),
      0
    );

    return total / evaluations.length;
  }

  function calculateCategoryScore(category) {
    if (evaluations.length === 0) {
      return 0;
    }

    const total = evaluations.reduce(
      (sum, item) =>
        sum + Number(item[category] || 0),
      0
    );

    return total / evaluations.length;
  }

  function getPerformanceLabel(score) {
    if (score >= 8.5) {
      return "Excellent";
    }

    if (score >= 7) {
      return "Good";
    }

    if (score >= 5) {
      return "Average";
    }

    return "Needs Improvement";
  }

  function getScoreClass(score) {
    if (score >= 8) {
      return "score-good";
    }

    if (score >= 5) {
      return "score-average";
    }

    return "score-low";
  }

  if (status === "loading") {
    return (
      <Page>
        <div className="center-card">
          <div className="spinner" />

          <h2>Preparing Your Interview</h2>

          <p>
            AI is generating your interview questions...
          </p>
        </div>
      </Page>
    );
  }

  if (status === "evaluating") {
    return (
      <Page>
        <div className="center-card">
          <div className="spinner" />

          <h2>Evaluating Your Interview</h2>

          <p>
            AI is analyzing all your answers.
          </p>

          <p className="muted">
            This may take a few moments...
          </p>
        </div>
      </Page>
    );
  }

  if (status === "error") {
    return (
      <Page>
        <div className="center-card error-card">
          <div className="error-icon">!</div>

          <h2>Something Went Wrong</h2>

          <p>{error}</p>

          <button
            className="primary-button"
            onClick={restartInterview}
          >
            Try Again
          </button>
        </div>
      </Page>
    );
  }

  if (status === "results") {
    const overallScore = calculateOverallScore();

    const relevance = calculateCategoryScore(
      "relevance"
    );

    const technicalAccuracy =
      calculateCategoryScore(
        "technical_accuracy"
      );

    const communication =
      calculateCategoryScore("communication");

    const confidence =
      calculateCategoryScore("confidence");

    const allStrengths = evaluations.flatMap(
      (item) => item.strengths || []
    );

    const allWeaknesses = evaluations.flatMap(
      (item) => item.weaknesses || []
    );

    return (
      <Page>
        <div className="results-container">
          <div className="results-header">
            <div>
              <span className="eyebrow">
                INTERVIEW COMPLETED
              </span>

              <h1>Interview Results</h1>

              <p>
                Here is your AI-powered interview
                performance report.
              </p>
            </div>

            <button
              className="secondary-button"
              onClick={restartInterview}
            >
              Start New Interview
            </button>
          </div>

          <div className="overall-card">
            <div className="overall-score">
              <div className="score-number">
                {overallScore.toFixed(1)}
              </div>

              <div className="score-out-of">
                / 10
              </div>
            </div>

            <div className="overall-info">
              <span className="eyebrow">
                OVERALL PERFORMANCE
              </span>

              <h2>
                {getPerformanceLabel(overallScore)}
              </h2>

              <p>
                You completed{" "}
                <strong>{answers.length}</strong>{" "}
                interview questions.
              </p>
            </div>
          </div>

          <section className="section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">
                  PERFORMANCE
                </span>

                <h2>Score Breakdown</h2>
              </div>
            </div>

            <div className="score-grid">
              <ScoreCard
                title="Relevance"
                score={relevance}
              />

              <ScoreCard
                title="Technical Accuracy"
                score={technicalAccuracy}
              />

              <ScoreCard
                title="Communication"
                score={communication}
              />

              <ScoreCard
                title="Confidence"
                score={confidence}
              />
            </div>
          </section>

          <section className="section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">
                  AI ANALYSIS
                </span>

                <h2>Overall Strengths</h2>
              </div>
            </div>

            <div className="feedback-card">
              {allStrengths.length > 0 ? (
                <ul className="feedback-list">
                  {[
                    ...new Set(allStrengths),
                  ].map((strength, index) => (
                    <li key={index}>
                      <span className="check">
                        ✓
                      </span>

                      <span>{strength}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>
                  No specific strengths were returned.
                </p>
              )}
            </div>
          </section>

          <section className="section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">
                  AI ANALYSIS
                </span>

                <h2>Areas to Improve</h2>
              </div>
            </div>

            <div className="feedback-card">
              {allWeaknesses.length > 0 ? (
                <ul className="feedback-list">
                  {[
                    ...new Set(allWeaknesses),
                  ].map((weakness, index) => (
                    <li key={index}>
                      <span className="warning">
                        !
                      </span>

                      <span>{weakness}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>
                  No major weaknesses were identified.
                </p>
              )}
            </div>
          </section>

          <section className="section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">
                  QUESTION-BY-QUESTION
                </span>

                <h2>Detailed Evaluation</h2>
              </div>
            </div>

            <div className="evaluation-list">
              {evaluations.map(
                (evaluation, index) => {
                  const answer =
                    answers[index];

                  return (
                    <div
                      className="evaluation-card"
                      key={index}
                    >
                      <div className="evaluation-top">
                        <div>
                          <span className="question-number">
                            QUESTION{" "}
                            {index + 1}
                          </span>

                          <h3>
                            {answer?.question ||
                              `Question ${
                                index + 1
                              }`}
                          </h3>
                        </div>

                        <div
                          className={`question-score ${getScoreClass(
                            Number(
                              evaluation.overall_score
                            )
                          )}`}
                        >
                          {Number(
                            evaluation.overall_score
                          ).toFixed(1)}
                          /10
                        </div>
                      </div>

                      <div className="answer-box">
                        <span>
                          YOUR ANSWER
                        </span>

                        <p>
                          {answer?.answer ||
                            "No answer available."}
                        </p>
                      </div>

                      <div className="mini-score-grid">
                        <MiniScore
                          title="Relevance"
                          score={
                            evaluation.relevance
                          }
                        />

                        <MiniScore
                          title="Technical"
                          score={
                            evaluation.technical_accuracy
                          }
                        />

                        <MiniScore
                          title="Communication"
                          score={
                            evaluation.communication
                          }
                        />

                        <MiniScore
                          title="Confidence"
                          score={
                            evaluation.confidence
                          }
                        />
                      </div>

                      <div className="evaluation-feedback">
                        <div>
                          <h4>Strengths</h4>

                          <ul>
                            {(
                              evaluation.strengths ||
                              []
                            ).map(
                              (
                                strength,
                                strengthIndex
                              ) => (
                                <li
                                  key={
                                    strengthIndex
                                  }
                                >
                                  {strength}
                                </li>
                              )
                            )}
                          </ul>
                        </div>

                        <div>
                          <h4>Weaknesses</h4>

                          <ul>
                            {(
                              evaluation.weaknesses ||
                              []
                            ).map(
                              (
                                weakness,
                                weaknessIndex
                              ) => (
                                <li
                                  key={
                                    weaknessIndex
                                  }
                                >
                                  {weakness}
                                </li>
                              )
                            )}
                          </ul>
                        </div>
                      </div>

                      <div className="improvement-box">
                        <h4>
                          Improvement Feedback
                        </h4>

                        <p>
                          {
                            evaluation.improvement_feedback
                          }
                        </p>
                      </div>
                    </div>
                  );
                }
              )}
            </div>
          </section>

          <section className="final-feedback">
            <span className="eyebrow">
              FINAL RECOMMENDATION
            </span>

            <h2>
              Keep Practicing and Improving
            </h2>

            <p>
              Your interview has been evaluated
              across relevance, technical accuracy,
              communication, and confidence. Use the
              feedback above to identify weak areas
              and practice similar questions before
              your next interview.
            </p>

            <button
              className="primary-button"
              onClick={restartInterview}
            >
              Practice Again
            </button>
          </section>
        </div>
      </Page>
    );
  }

  const question =
    questions[currentQuestion];

  const progress =
    ((currentQuestion + 1) /
      questions.length) *
    100;

  return (
    <Page>
      <div className="interview-container">
        <div className="top-header">
          <div>
            <span className="eyebrow">
              AI INTERVIEW
            </span>

            <h1>
              {interviewType
                .charAt(0)
                .toUpperCase() +
                interviewType.slice(1)}{" "}
              Interview
            </h1>
          </div>

          <div className="question-counter">
            Question{" "}
            <strong>
              {currentQuestion + 1}
            </strong>{" "}
            / {questions.length}
          </div>
        </div>

        <div className="progress-container">
          <div className="progress-track">
            <div
              className="progress-bar"
              style={{
                width: `${progress}%`,
              }}
            />
          </div>
        </div>

        {error && (
          <div className="alert">
            <span>!</span>
            {error}
          </div>
        )}

        <div className="interview-layout">
          <div className="main-column">
            <div className="question-card">
              <span className="question-label">
                INTERVIEW QUESTION
              </span>

              <h2>{question}</h2>

              <p className="question-help">
                Think about your answer and then
                record your response using the
                microphone.
              </p>
            </div>

            <div className="answer-card">
              <div className="answer-header">
                <div>
                  <span className="question-label">
                    YOUR ANSWER
                  </span>

                  <h3>
                    {transcribing
                      ? "Transcribing your answer..."
                      : recording
                      ? "Recording..."
                      : "Record your response"}
                  </h3>
                </div>

                {recording && (
                  <div className="recording-indicator">
                    <span />
                    Recording
                  </div>
                )}
              </div>

              <textarea
                value={currentAnswer}
                onChange={(event) =>
                  setCurrentAnswer(
                    event.target.value
                  )
                }
                placeholder="Your transcribed answer will appear here. You can also edit it before submitting."
                disabled={transcribing}
              />

              <div className="answer-actions">
                {!recording ? (
                  <button
                    className="record-button"
                    onClick={startRecording}
                    disabled={
                      transcribing ||
                      !micEnabled
                    }
                  >
                    🎙 Start Recording
                  </button>
                ) : (
                  <button
                    className="stop-button"
                    onClick={stopRecording}
                  >
                    ■ Stop Recording
                  </button>
                )}

                <button
                  className="submit-button"
                  onClick={saveCurrentAnswer}
                  disabled={
                    transcribing ||
                    recording ||
                    !currentAnswer.trim()
                  }
                >
                  {currentQuestion ===
                  questions.length - 1
                    ? "Finish Interview"
                    : "Submit & Next"}
                </button>
              </div>
            </div>
          </div>

          <aside className="side-column">
            <div className="camera-card">
              <div className="camera-header">
                <span className="question-label">
                  CAMERA
                </span>

                <span
                  className={
                    cameraEnabled
                      ? "status-online"
                      : "status-offline"
                  }
                >
                  {cameraEnabled
                    ? "● Live"
                    : "● Off"}
                </span>
              </div>

              <div className="video-container">
                {cameraEnabled ? (
                  <video
                    ref={videoRef}
                    autoPlay
                    muted
                    playsInline
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="camera-placeholder">
                    <div className="camera-icon">
                      ◉
                    </div>

                    <p>
                      Camera preview
                    </p>
                  </div>
                )}
              </div>

              <button
                className="camera-button"
                onClick={
                  cameraEnabled
                    ? stopMediaStream
                    : enableCameraAndMic
                }
              >
                {cameraEnabled
                  ? "Disable Camera & Mic"
                  : "Enable Camera & Mic"}
              </button>

              <div className="device-status">
                <div>
                  <span
                    className={
                      cameraEnabled
                        ? "device-on"
                        : ""
                    }
                  >
                    ●
                  </span>

                  Camera
                </div>

                <div>
                  <span
                    className={
                      micEnabled
                        ? "device-on"
                        : ""
                    }
                  >
                    ●
                  </span>

                  Microphone
                </div>
              </div>
            </div>

            <div className="tips-card">
              <span className="question-label">
                QUICK TIPS
              </span>

              <ul>
                <li>
                  Speak clearly and naturally.
                </li>

                <li>
                  Explain your reasoning.
                </li>

                <li>
                  Give examples when possible.
                </li>

                <li>
                  Keep your answer focused.
                </li>
              </ul>
            </div>
          </aside>
        </div>
      </div>
    </Page>
  );
}
function ScoreCard({ title, score }) {
  const numericScore = Number(score || 0);

  return (
    <div className="score-card">
      <div className="score-card-top">
        <span>{title}</span>

        <strong>
          {numericScore.toFixed(1)}
        </strong>
      </div>

      <div className="score-progress">
        <div
          style={{
            width: `${numericScore * 10}%`,
          }}
        />
      </div>

      <small>/ 10</small>
    </div>
  );
}

function MiniScore({ title, score }) {
  const numericScore = Number(score || 0);

  return (
    <div className="mini-score">
      <span>{title}</span>

      <strong>
        {numericScore.toFixed(1)}
      </strong>
    </div>
  );
}

function Page({ children }) {
  return (
    <>
      <style>{`
        * {
          box-sizing: border-box;
        }

        body {
          margin: 0;
          font-family:
            Inter,
            ui-sans-serif,
            system-ui,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
          background: #f6f7fb;
          color: #151923;
        }

        button,
        textarea,
        select {
          font: inherit;
        }

        button {
          cursor: pointer;
        }

        button:disabled {
          cursor: not-allowed;
          opacity: 0.55;
        }

        .page {
          min-height: 100vh;
          background:
            radial-gradient(
              circle at top right,
              rgba(79, 70, 229, 0.08),
              transparent 35%
            ),
            #f6f7fb;
        }

        .interview-container,
        .results-container {
          width: min(1180px, 94%);
          margin: 0 auto;
          padding: 42px 0 70px;
        }

        .top-header,
        .results-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 25px;
          margin-bottom: 28px;
        }

        .top-header h1,
        .results-header h1 {
          margin: 5px 0 0;
          font-size: 32px;
          letter-spacing: -0.7px;
        }

        .results-header p {
          margin: 8px 0 0;
          color: #69707d;
        }

        .eyebrow,
        .question-label {
          display: block;
          color: #6366f1;
          font-size: 11px;
          font-weight: 800;
          letter-spacing: 1.4px;
        }

        .question-counter {
          padding: 11px 16px;
          border: 1px solid #e2e5ec;
          border-radius: 12px;
          background: white;
          color: #69707d;
          font-size: 14px;
        }

        .question-counter strong {
          color: #151923;
        }

        .progress-container {
          margin-bottom: 25px;
        }

        .progress-track {
          width: 100%;
          height: 7px;
          overflow: hidden;
          border-radius: 20px;
          background: #e5e7eb;
        }

        .progress-bar {
          height: 100%;
          border-radius: inherit;
          background: #6366f1;
          transition: width 0.3s ease;
        }

        .alert {
          display: flex;
          align-items: center;
          gap: 10px;
          margin-bottom: 20px;
          padding: 13px 16px;
          border: 1px solid #fecaca;
          border-radius: 12px;
          background: #fff1f2;
          color: #b91c1c;
          font-size: 14px;
        }

        .alert span {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background: #ef4444;
          color: white;
          font-weight: 800;
        }

        .interview-layout {
          display: grid;
          grid-template-columns: minmax(0, 1fr) 350px;
          gap: 24px;
          align-items: start;
        }

        .main-column {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .side-column {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .question-card,
        .answer-card,
        .camera-card,
        .tips-card,
        .feedback-card,
        .evaluation-card,
        .score-card {
          border: 1px solid #e3e6ed;
          border-radius: 18px;
          background: white;
          box-shadow:
            0 8px 25px rgba(25, 30, 45, 0.04);
        }

        .question-card {
          padding: 30px;
        }

        .question-card h2 {
          margin: 12px 0 15px;
          font-size: 27px;
          line-height: 1.35;
          letter-spacing: -0.4px;
        }

        .question-help {
          margin: 0;
          color: #747b87;
          line-height: 1.6;
        }

        .answer-card {
          padding: 25px;
        }

        .answer-header,
        .camera-header,
        .score-card-top {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 15px;
        }

        .answer-header h3 {
          margin: 6px 0 0;
          font-size: 18px;
        }

        .recording-indicator {
          display: flex;
          align-items: center;
          gap: 7px;
          color: #dc2626;
          font-size: 13px;
          font-weight: 700;
        }

        .recording-indicator span {
          width: 9px;
          height: 9px;
          border-radius: 50%;
          background: #ef4444;
          animation: pulse 1s infinite;
        }

        @keyframes pulse {
          50% {
            opacity: 0.3;
          }
        }

        textarea {
          width: 100%;
          min-height: 190px;
          margin-top: 20px;
          padding: 17px;
          resize: vertical;
          border: 1px solid #dfe3ea;
          border-radius: 13px;
          outline: none;
          background: #fafbfc;
          color: #1f2937;
          line-height: 1.6;
        }

        textarea:focus {
          border-color: #818cf8;
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .answer-actions {
          display: flex;
          gap: 12px;
          margin-top: 15px;
        }

        .record-button,
        .stop-button,
        .submit-button,
        .primary-button,
        .secondary-button,
        .camera-button {
          border: none;
          border-radius: 11px;
          padding: 12px 17px;
          font-weight: 700;
          transition: 0.2s ease;
        }

        .record-button {
          background: #eef2ff;
          color: #4f46e5;
        }

        .stop-button {
          background: #fee2e2;
          color: #b91c1c;
        }

        .submit-button,
        .primary-button {
          background: #4f46e5;
          color: white;
        }

        .submit-button {
          margin-left: auto;
        }

        .submit-button:hover,
        .primary-button:hover {
          background: #4338ca;
        }

        .secondary-button {
          border: 1px solid #dfe3ea;
          background: white;
          color: #303643;
        }

        .secondary-button:hover {
          background: #f8f9fb;
        }

        .camera-card,
        .tips-card {
          padding: 20px;
        }

        .status-online {
          color: #16a34a;
          font-size: 12px;
          font-weight: 700;
        }

        .status-offline {
          color: #9ca3af;
          font-size: 12px;
          font-weight: 700;
        }

        .video-container {
          width: 100%;
          aspect-ratio: 4 / 3;
          margin: 15px 0;
          overflow: hidden;
          border-radius: 13px;
          background: #111827;
        }

        .video-container video {
          width: 100%;
          height: 100%;
          display: block;
          object-fit: cover;
        }

        .camera-placeholder {
          width: 100%;
          height: 100%;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          color: #9ca3af;
        }

        .camera-icon {
          margin-bottom: 10px;
          font-size: 38px;
        }

        .camera-placeholder p {
          margin: 0;
          font-size: 13px;
        }

        .camera-button {
          width: 100%;
          border: 1px solid #dfe3ea;
          background: white;
          color: #303643;
        }

        .device-status {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 10px;
          margin-top: 15px;
          color: #6b7280;
          font-size: 12px;
        }

        .device-status div {
          padding: 9px;
          border-radius: 9px;
          background: #f7f8fa;
          text-align: center;
        }

        .device-status span {
          margin-right: 5px;
          color: #cbd0d8;
        }

        .device-status .device-on {
          color: #22c55e;
        }

        .tips-card ul {
          margin: 14px 0 0;
          padding-left: 18px;
          color: #69707d;
          font-size: 13px;
          line-height: 1.8;
        }

        .center-card {
          width: min(500px, 92%);
          margin: 100px auto;
          padding: 45px;
          border: 1px solid #e3e6ed;
          border-radius: 20px;
          background: white;
          text-align: center;
          box-shadow: 0 15px 45px rgba(25, 30, 45, 0.06);
        }

        .center-card h2 {
          margin: 20px 0 8px;
        }

        .center-card p {
          color: #69707d;
          line-height: 1.6;
        }

        .spinner {
          width: 42px;
          height: 42px;
          margin: 0 auto;
          border: 4px solid #e5e7eb;
          border-top-color: #6366f1;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        .muted {
          font-size: 13px;
        }

        .error-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 52px;
          height: 52px;
          margin: 0 auto;
          border-radius: 50%;
          background: #fee2e2;
          color: #dc2626;
          font-size: 25px;
          font-weight: 800;
        }

        .error-card .primary-button {
          margin-top: 15px;
        }

        /* RESULTS */

        .results-header {
          align-items: flex-end;
        }

        .overall-card {
          display: flex;
          align-items: center;
          gap: 35px;
          margin-bottom: 45px;
          padding: 35px;
          border-radius: 22px;
          background: #111827;
          color: white;
          box-shadow: 0 15px 40px rgba(17, 24, 39, 0.12);
        }

        .overall-score {
          display: flex;
          align-items: baseline;
        }

        .score-number {
          font-size: 65px;
          line-height: 1;
          font-weight: 800;
          letter-spacing: -3px;
        }

        .score-out-of {
          margin-left: 5px;
          color: #9ca3af;
          font-size: 18px;
        }

        .overall-info h2 {
          margin: 7px 0;
          font-size: 25px;
        }

        .overall-info p {
          margin: 0;
          color: #aeb5c1;
        }

        .section {
          margin-bottom: 45px;
        }

        .section-heading {
          margin-bottom: 17px;
        }

        .section-heading h2 {
          margin: 6px 0 0;
          font-size: 23px;
        }

        .score-grid {
          display: grid;
          grid-template-columns:
            repeat(4, minmax(0, 1fr));
          gap: 15px;
        }

        .score-card {
          padding: 20px;
        }

        .score-card-top span {
          color: #69707d;
          font-size: 13px;
        }

        .score-card-top strong {
          font-size: 22px;
        }

        .score-progress {
          height: 7px;
          margin: 17px 0 7px;
          overflow: hidden;
          border-radius: 20px;
          background: #eef0f4;
        }

        .score-progress div {
          height: 100%;
          border-radius: inherit;
          background: #6366f1;
        }

        .score-card small {
          color: #9ca3af;
        }

        .feedback-card {
          padding: 22px 25px;
        }

        .feedback-list {
          display: grid;
          gap: 12px;
          margin: 0;
          padding: 0;
          list-style: none;
        }

        .feedback-list li {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          color: #454b57;
          line-height: 1.5;
        }

        .check,
        .warning {
          display: flex;
          flex: 0 0 auto;
          align-items: center;
          justify-content: center;
          width: 22px;
          height: 22px;
          border-radius: 50%;
          font-size: 12px;
          font-weight: 800;
        }

        .check {
          background: #dcfce7;
          color: #16a34a;
        }

        .warning {
          background: #fef3c7;
          color: #d97706;
        }

        .evaluation-list {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .evaluation-card {
          padding: 27px;
        }

        .evaluation-top {
          display: flex;
          justify-content: space-between;
          gap: 20px;
          align-items: flex-start;
        }

        .evaluation-top h3 {
          margin: 8px 0 0;
          font-size: 19px;
          line-height: 1.45;
        }

        .question-number {
          color: #6366f1;
          font-size: 10px;
          font-weight: 800;
          letter-spacing: 1.2px;
        }

        .question-score {
          flex: 0 0 auto;
          padding: 9px 13px;
          border-radius: 10px;
          font-size: 14px;
          font-weight: 800;
        }

        .score-good {
          background: #dcfce7;
          color: #15803d;
        }

        .score-average {
          background: #fef3c7;
          color: #b45309;
        }

        .score-low {
          background: #fee2e2;
          color: #b91c1c;
        }

        .answer-box {
          margin-top: 20px;
          padding: 17px;
          border-radius: 12px;
          background: #f8f9fb;
        }

        .answer-box span {
          color: #8b919d;
          font-size: 10px;
          font-weight: 800;
          letter-spacing: 1px;
        }

        .answer-box p {
          margin: 8px 0 0;
          color: #454b57;
          line-height: 1.6;
        }

        .mini-score-grid {
          display: grid;
          grid-template-columns:
            repeat(4, 1fr);
          gap: 10px;
          margin-top: 15px;
        }

        .mini-score {
          padding: 13px;
          border: 1px solid #eceef2;
          border-radius: 10px;
          background: white;
        }

        .mini-score span {
          display: block;
          color: #777e8b;
          font-size: 11px;
        }

        .mini-score strong {
          display: block;
          margin-top: 4px;
          font-size: 16px;
        }

        .evaluation-feedback {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
          margin-top: 20px;
        }

        .evaluation-feedback h4,
        .improvement-box h4 {
          margin: 0 0 9px;
          font-size: 13px;
        }

        .evaluation-feedback ul {
          margin: 0;
          padding-left: 18px;
          color: #626976;
          font-size: 13px;
          line-height: 1.7;
        }

        .improvement-box {
          margin-top: 20px;
          padding: 17px;
          border-left: 3px solid #6366f1;
          border-radius: 0 10px 10px 0;
          background: #f5f5ff;
        }

        .improvement-box p {
          margin: 0;
          color: #555c68;
          font-size: 13px;
          line-height: 1.65;
        }

        .final-feedback {
          margin-top: 15px;
          padding: 35px;
          border-radius: 20px;
          background: #eef2ff;
          text-align: center;
        }

        .final-feedback h2 {
          margin: 7px 0 10px;
          font-size: 25px;
        }

        .final-feedback p {
          max-width: 700px;
          margin: 0 auto 20px;
          color: #596170;
          line-height: 1.7;
        }

        @media (max-width: 900px) {
          .interview-layout {
            grid-template-columns: 1fr;
          }

          .side-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
          }

          .score-grid {
            grid-template-columns:
              repeat(2, 1fr);
          }
        }

        @media (max-width: 650px) {
          .interview-container,
          .results-container {
            width: 92%;
            padding-top: 25px;
          }

          .top-header,
          .results-header {
            flex-direction: column;
            align-items: flex-start;
          }

          .top-header h1,
          .results-header h1 {
            font-size: 26px;
          }

          .interview-layout,
          .side-column {
            display: flex;
          }

          .question-card,
          .answer-card,
          .camera-card,
          .tips-card,
          .evaluation-card {
            padding: 20px;
          }

          .question-card h2 {
            font-size: 22px;
          }

          .answer-actions {
            flex-direction: column;
          }

          .submit-button {
            margin-left: 0;
          }

          .overall-card {
            flex-direction: column;
            align-items: flex-start;
            gap: 18px;
            padding: 25px;
          }

          .score-number {
            font-size: 55px;
          }

          .score-grid {
            grid-template-columns: 1fr;
          }

          .mini-score-grid {
            grid-template-columns:
              repeat(2, 1fr);
          }

          .evaluation-feedback {
            grid-template-columns: 1fr;
          }

          .evaluation-top {
            flex-direction: column;
          }
        }
      `}</style>

      <main className="page">
        {children}
      </main>
    </>
  );
}

export default Interview;