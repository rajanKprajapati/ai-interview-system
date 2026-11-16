import { useEffect, useRef, useState } from "react";
import { fetchQuestions, transcribeAudioBlob, submitEvaluation } from "./services/api";
import { VisualBehaviorAnalyzer } from "./utils/visualAnalysis";

function Interview({ config = {}, onNavigate, onRestart }) {
  const interviewType = config.type || "technical";
  const questionCount = Number(config.questionCount || 5);
  const difficulty = config.difficulty || "intermediate";
  const role = config.role || "Software Engineer";
  const subject = config.subject || "";
  const resumeSkills = config.resumeSkills || null;
  const skillGaps = config.skillGaps || null;
  const jobDescription = config.jobDescription || null;
  const resumeFilename = config.resumeFilename || null;

  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [answers, setAnswers] = useState([]);
  const [currentAnswer, setCurrentAnswer] = useState("");

  const [status, setStatus] = useState("loading"); // loading, interview, evaluating, results, error
  const [error, setError] = useState("");

  const [cameraEnabled, setCameraEnabled] = useState(false);
  const [micEnabled, setMicEnabled] = useState(false);
  const [recording, setRecording] = useState(false);

  const [transcribing, setTranscribing] = useState(false);
  const [evaluating, setEvaluating] = useState(false);

  // Result state
  const [resultData, setResultData] = useState(null);

  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const visualAnalyzerRef = useRef(null);

  const recordingStartTimeRef = useRef(null);
  const currentDurationRef = useRef(null);
  const sessionStartTimeRef = useRef(null);

  useEffect(() => {
    loadQuestions();
    sessionStartTimeRef.current = Date.now();

    return () => {
      stopMediaStream();
    };
  }, []);

  useEffect(() => {
    if (cameraEnabled && videoRef.current && streamRef.current) {
      videoRef.current.srcObject = streamRef.current;
      videoRef.current.play().catch((err) => {
        console.error("Camera playback error:", err);
      });
    }
  }, [cameraEnabled]);

  async function loadQuestions() {
    setStatus("loading");
    setError("");
    setQuestions([]);
    setAnswers([]);
    setCurrentQuestion(0);
    setCurrentAnswer("");
    setResultData(null);

    try {
      const data = await fetchQuestions({
        type: interviewType,
        questionCount,
        difficulty,
        role,
        subject,
        resumeSkills,
        skillGaps,
        jobDescription,
      });

      if (!data.questions || data.questions.length === 0) {
        throw new Error("No questions returned from AI service.");
      }

      setQuestions(data.questions);
      setStatus("interview");
    } catch (err) {
      console.error("Failed to load questions:", err);
      setError(err.message || "Failed to generate interview questions. Please verify backend connectivity.");
      setStatus("error");
    }
  }

  async function enableCameraAndMic() {
    try {
      setError("");
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: true,
      });

      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        try {
          await videoRef.current.play();
        } catch (err) {
          console.error("Video play error:", err);
        }
        visualAnalyzerRef.current = new VisualBehaviorAnalyzer(videoRef.current);
      }

      setCameraEnabled(true);
      setMicEnabled(true);
    } catch (err) {
      console.error("Camera/Mic error:", err);
      setError("Camera or microphone permission was denied. Please allow camera and microphone access in your browser settings.");
    }
  }

  function stopMediaStream() {
    if (visualAnalyzerRef.current) {
      visualAnalyzerRef.current.stop();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  }

  function startRecording() {
    if (!streamRef.current) {
      setError("Please enable your camera and microphone first.");
      return;
    }

    try {
      setError("");
      audioChunksRef.current = [];

      const audioTracks = streamRef.current.getAudioTracks();
      if (audioTracks.length === 0) {
        setError("Microphone is not active.");
        return;
      }

      const audioStream = new MediaStream(audioTracks);
      let options = {};
      if (typeof MediaRecorder !== "undefined") {
        if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
          options = { mimeType: "audio/webm;codecs=opus" };
        } else if (MediaRecorder.isTypeSupported("audio/webm")) {
          options = { mimeType: "audio/webm" };
        }
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

      recordingStartTimeRef.current = Date.now();
      recorder.start();
      setRecording(true);

      if (visualAnalyzerRef.current) {
        visualAnalyzerRef.current.start(400);
      }
    } catch (err) {
      console.error("Recording start error:", err);
      setError("Unable to start audio recording. Check microphone settings.");
    }
  }

  function stopRecording() {
    if (visualAnalyzerRef.current) {
      visualAnalyzerRef.current.stop();
    }

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      const elapsedSec = (Date.now() - (recordingStartTimeRef.current || Date.now())) / 1000;
      currentDurationRef.current = Math.max(1, Math.round(elapsedSec * 10) / 10);
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  }

  async function transcribeAudio(audioBlob) {
    try {
      setTranscribing(true);
      setError("");

      const data = await transcribeAudioBlob(audioBlob);
      const transcript = (data.transcript || "").trim();

      if (!transcript) {
        throw new Error("No speech was detected. Please try recording again.");
      }

      setCurrentAnswer(transcript);
      if (data.duration_seconds) {
        currentDurationRef.current = data.duration_seconds;
      }
    } catch (err) {
      console.error("STT Error:", err);
      setError(err.message || "Speech-to-text failed. You can type your answer manually.");
    } finally {
      setTranscribing(false);
    }
  }

  function saveCurrentAnswer() {
    const answer = currentAnswer.trim();
    if (!answer) {
      setError("Please record or type an answer before proceeding.");
      return;
    }

    const question = questions[currentQuestion];
    const duration = currentDurationRef.current || null;

    const updatedAnswers = [
      ...answers,
      {
        question,
        answer,
        duration_seconds: duration,
      },
    ];

    setAnswers(updatedAnswers);
    setCurrentAnswer("");
    currentDurationRef.current = null;
    setError("");

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
    } else {
      finishInterview(updatedAnswers);
    }
  }

  async function finishInterview(finalAnswers) {
    try {
      setEvaluating(true);
      setStatus("evaluating");
      setError("");

      const totalDuration = sessionStartTimeRef.current
        ? Math.round((Date.now() - sessionStartTimeRef.current) / 1000)
        : null;

      let visualMetrics = null;
      if (visualAnalyzerRef.current) {
        visualMetrics = visualAnalyzerRef.current.getSummary();
      }

      const data = await submitEvaluation({
        answers: finalAnswers,
        interviewType,
        difficulty,
        role,
        totalDurationSeconds: totalDuration,
        developmentMode: false,
        resumeSkills,
        resumeFilename,
        jobDescription,
        visualMetrics,
      });

      setResultData(data);
      setStatus("results");
      stopMediaStream();
    } catch (err) {
      console.error("Evaluation error:", err);
      setError(err.message || "Interview evaluation failed. Please check server logs.");
      setStatus("error");
    } finally {
      setEvaluating(false);
    }
  }

  function restartInterview() {
    if (onRestart) {
      onRestart();
    } else {
      loadQuestions();
    }
  }

  // --- RENDER STATES ---

  if (status === "loading") {
    return (
      <div className="center-view">
        <div className="spinner" />
        <h2>Generating Interview Questions</h2>
        <p>AI is tailoring {questionCount} {difficulty} questions for <strong>{role}</strong>...</p>
      </div>
    );
  }

  if (status === "evaluating") {
    return (
      <div className="center-view">
        <div className="spinner" />
        <h2>Evaluating Your Responses</h2>
        <p>Gemini AI is analyzing your technical accuracy, communication clarity, and response depth...</p>
        <p className="muted">Computing delivery signals and saving to your performance profile.</p>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="center-view error-view">
        <div className="error-icon">!</div>
        <h2>Something Went Wrong</h2>
        <p>{error}</p>
        <div className="btn-row">
          <button className="primary-btn" onClick={restartInterview}>Try Again</button>
          {onNavigate && (
            <button className="secondary-btn" onClick={() => onNavigate("dashboard")}>
              Go to Dashboard
            </button>
          )}
        </div>
      </div>
    );
  }

  // RESULTS SCREEN
  if (status === "results" && resultData) {
    const overallScore = Number(resultData.overall_score || 0);
    const cat = resultData.category_scores || {};
    const comm = resultData.communication_metrics || {};
    const feedback = resultData.personalized_feedback || {};
    const evaluations = resultData.evaluations || [];

    return (
      <div className="results-container">
        {/* Results Header */}
        <div className="results-header">
          <div>
            <span className="eyebrow">SESSION #{resultData.interview_id} • {interviewType.toUpperCase()} INTERVIEW</span>
            <h1>Interview Performance Report</h1>
            <p>Your answers have been evaluated with verified AI scoring and observable communication signals.</p>
          </div>

          <div className="results-actions">
            <button className="secondary-btn" onClick={restartInterview}>
              + Practice Again
            </button>
            {onNavigate && (
              <button className="primary-btn" onClick={() => onNavigate("dashboard")}>
                View Dashboard →
              </button>
            )}
          </div>
        </div>

        {/* Overall Card */}
        <div className="overall-card">
          <div className="overall-score">
            <div className="score-number">{overallScore.toFixed(1)}</div>
            <div className="score-out-of">/ 10</div>
          </div>

          <div className="overall-info">
            <span className="eyebrow">OVERALL VERDICT</span>
            <h2>
              {overallScore >= 8.5
                ? "Excellent Performance"
                : overallScore >= 7.0
                ? "Good Interview"
                : overallScore >= 5.5
                ? "Average / Passing"
                : "Needs Practice"}
            </h2>
            <p>
              Completed <strong>{answers.length}</strong> questions in {difficulty} {interviewType} mode for <strong>{role}</strong>.
            </p>
          </div>
        </div>

        {/* Competency Scores */}
        <section className="section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">COMPETENCIES</span>
              <h2>Core Performance Scores</h2>
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

        {/* Observable Delivery & Communication Indicators */}
        {comm && (
          <section className="section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">OBSERVABLE DELIVERY TELEMETRY</span>
                <h2>Verbal & Camera Delivery Indicators</h2>
              </div>
            </div>

            <h3 style={{ fontSize: "14px", textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--gray-600)", marginBottom: "10px" }}>
              Verbal Delivery Indicators
            </h3>
            <div className="comm-metrics-grid" style={{ marginBottom: "20px" }}>
              <div className="comm-card">
                <span className="comm-label">Speaking Pace</span>
                <strong className="comm-val">
                  {comm.speaking_pace_wpm ? `${comm.speaking_pace_wpm} WPM` : "Not measured"}
                </strong>
                <span className="comm-desc">
                  Rating: <strong>{comm.speaking_pace_label || "Normal"}</strong> (Target: 120–160 WPM)
                </span>
              </div>

              <div className="comm-card">
                <span className="comm-label">Filler Words</span>
                <strong className="comm-val">
                  {comm.filler_word_count !== undefined ? `${comm.filler_word_count}` : "0"} detected
                </strong>
                <span className="comm-desc">
                  Density: <strong>{comm.filler_label || "Low"}</strong> ({comm.filler_rate_percent ?? 0}%)
                </span>
              </div>

              <div className="comm-card">
                <span className="comm-label">Active Speaking Duration</span>
                <strong className="comm-val">
                  {comm.duration_seconds ? `${Math.round(comm.duration_seconds)}s` : "Calculated per answer"}
                </strong>
                <span className="comm-desc">Total captured microphone speech</span>
              </div>

              <div className="comm-card">
                <span className="comm-label">Voice Recording</span>
                <strong className="comm-val">
                  {comm.speaking_pace_wpm ? "Speech Recorded" : "Direct Input"}
                </strong>
                <span className="comm-desc">Microphone telemetry captured</span>
              </div>
            </div>

            <h3 style={{ fontSize: "14px", textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--gray-600)", marginBottom: "10px" }}>
              Visual & Camera Telemetry
            </h3>
            <div className="comm-metrics-grid">
              <div className="comm-card">
                <span className="comm-label">Camera Gaze & Eye Contact</span>
                <strong className="comm-val">
                  {comm.camera_gaze_metric !== null && comm.camera_gaze_metric !== undefined
                    ? `${Math.round(comm.camera_gaze_metric)}%`
                    : cameraEnabled ? "Engaged" : "N/A (Webcam Off)"}
                </strong>
                <span className="comm-desc">
                  {comm.visual_indicators?.gaze_label || (comm.camera_gaze_metric >= 70 ? "High Engagement" : comm.camera_gaze_metric >= 50 ? "Moderate Contact" : "Needs Eye Level Focus")}
                </span>
              </div>

              <div className="comm-card">
                <span className="comm-label">Head Pose & Stability</span>
                <strong className="comm-val">
                  {comm.visual_indicators?.head_pose?.status || (cameraEnabled ? "Steady & Centered" : "N/A")}
                </strong>
                <span className="comm-desc">Temporal head motion tracking</span>
              </div>

              <div className="comm-card">
                <span className="comm-label">Body Posture & Framing</span>
                <strong className="comm-val">
                  {comm.visual_indicators?.posture?.status || (comm.posture_metric ? `${Math.round(comm.posture_metric)}% Upright` : (cameraEnabled ? "Upright & In-Frame" : "N/A"))}
                </strong>
                <span className="comm-desc">Upper body alignment & framing</span>
              </div>

              <div className="comm-card">
                <span className="comm-label">Gestures & Hand Motion</span>
                <strong className="comm-val">
                  {comm.visual_indicators?.hand_gestures?.status || (cameraEnabled ? "Natural Gestures" : "N/A")}
                </strong>
                <span className="comm-desc">Lower-third gesture activity</span>
              </div>

              <div className="comm-card">
                <span className="comm-label">Environmental Lighting</span>
                <strong className="comm-val">
                  {comm.visual_indicators?.lighting || (cameraEnabled ? "Optimal Lighting" : "N/A")}
                </strong>
                <span className="comm-desc">Luminance & exposure analysis</span>
              </div>
            </div>

            <p className="metric-disclaimer" style={{ marginTop: "16px" }}>
              ℹ️ <strong>Educational Disclaimer:</strong> Observable delivery indicators are measured via privacy-preserving client-side canvas heuristics and audio transcription to assist candidate mock interview practice. These signals do not assess psychological confidence, internal emotional states, or personality traits.
            </p>
          </section>
        )}

        {/* Personalized Feedback */}
        <section className="section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">ACTION PLAN</span>
              <h2>Personalized Feedback & Recommendations</h2>
            </div>
          </div>

          <div className="feedback-split">
            <div className="feedback-box strengths-box">
              <h3>✓ Verified Strengths</h3>
              <ul>
                {(feedback.strengths || ["Solid subject fundamentals demonstrated."]).map((s, idx) => (
                  <li key={idx}>{s}</li>
                ))}
              </ul>
            </div>

            <div className="feedback-box weaknesses-box">
              <h3>! Areas to Improve</h3>
              <ul>
                {(feedback.weaknesses || ["No major low-scoring area flagged."]).map((w, idx) => (
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

        {/* Detailed Question by Question */}
        <section className="section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">REVIEW</span>
              <h2>Question-by-Question Analysis</h2>
            </div>
          </div>

          <div className="evaluation-list">
            {evaluations.map((ev, idx) => {
              const qScore = Number(ev.overall_score || 0);
              const answerObj = answers[idx] || {};
              return (
                <div key={idx} className="evaluation-card">
                  <div className="evaluation-top">
                    <div>
                      <span className="question-number">QUESTION {idx + 1}</span>
                      <h3>{answerObj.question || `Question ${idx + 1}`}</h3>
                    </div>
                    <div className={`question-score ${qScore >= 8 ? "score-high" : qScore >= 6 ? "score-mid" : "score-low"}`}>
                      {qScore.toFixed(1)} / 10
                    </div>
                  </div>

                  <div className="answer-box">
                    <span className="answer-label">YOUR ANSWER:</span>
                    <p>{answerObj.answer || "No response recorded."}</p>
                  </div>

                  <div className="mini-score-grid">
                    <div className="mini-score">
                      <span>Relevance</span>
                      <strong>{Number(ev.relevance || 0).toFixed(1)}</strong>
                    </div>
                    <div className="mini-score">
                      <span>Technical</span>
                      <strong>{Number(ev.technical_accuracy || 0).toFixed(1)}</strong>
                    </div>
                    <div className="mini-score">
                      <span>Communication</span>
                      <strong>{Number(ev.communication || 0).toFixed(1)}</strong>
                    </div>
                    <div className="mini-score">
                      <span>Confidence</span>
                      <strong>{Number(ev.confidence || 0).toFixed(1)}</strong>
                    </div>
                  </div>

                  <div className="qa-feedback-grid">
                    {ev.strengths && ev.strengths.length > 0 && (
                      <div className="qa-strengths">
                        <strong>Strengths:</strong>
                        <ul>
                          {ev.strengths.map((st, i) => <li key={i}>{st}</li>)}
                        </ul>
                      </div>
                    )}

                    {ev.weaknesses && ev.weaknesses.length > 0 && (
                      <div className="qa-weaknesses">
                        <strong>Weaknesses:</strong>
                        <ul>
                          {ev.weaknesses.map((wk, i) => <li key={i}>{wk}</li>)}
                        </ul>
                      </div>
                    )}
                  </div>

                  {ev.improvement_feedback && (
                    <div className="improvement-note">
                      <strong>AI Suggestion:</strong> {ev.improvement_feedback}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* Footer Actions */}
        <div className="results-footer-actions">
          <button className="primary-btn" onClick={restartInterview}>
            Start Another Mock Interview
          </button>
          {onNavigate && (
            <button className="secondary-btn" onClick={() => onNavigate("history")}>
              View in Interview History
            </button>
          )}
        </div>
      </div>
    );
  }

  // ACTIVE INTERVIEW VIEW
  const question = questions[currentQuestion];
  const progressPercent = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="interview-container">
      {/* Top Header */}
      <div className="top-header">
        <div>
          <span className="eyebrow">
            {role.toUpperCase()} • {difficulty.toUpperCase()} {interviewType.toUpperCase()}
          </span>
          <h1>AI Mock Interview Session</h1>
        </div>

        <div className="question-counter">
          Question <strong>{currentQuestion + 1}</strong> of {questions.length}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-container">
        <div className="progress-track">
          <div className="progress-bar" style={{ width: `${progressPercent}%` }} />
        </div>
      </div>

      {error && (
        <div className="alert-box">
          <span className="alert-icon">⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {/* Main Two-Column Layout */}
      <div className="interview-layout">
        <div className="main-column">
          {/* Question Card */}
          <div className="question-card">
            <span className="question-label">INTERVIEW QUESTION {currentQuestion + 1}</span>
            <h2>{question}</h2>
            <p className="question-help">
              Structure your response clearly. Use the microphone to record your verbal answer, or type into the response box.
            </p>
          </div>

          {/* Answer Card */}
          <div className="answer-card">
            <div className="answer-header">
              <div>
                <span className="question-label">YOUR RESPONSE</span>
                <h3>
                  {transcribing
                    ? "Transcribing with Whisper STT..."
                    : recording
                    ? "Recording your speech..."
                    : "Speak or edit your answer"}
                </h3>
              </div>

              {recording && (
                <div className="recording-indicator">
                  <span className="pulse-dot" />
                  Recording audio...
                </div>
              )}
            </div>

            <textarea
              value={currentAnswer}
              onChange={(e) => setCurrentAnswer(e.target.value)}
              placeholder="Your transcribed answer will appear here automatically. You can also edit or type your response before submitting."
              disabled={transcribing}
              rows={6}
            />

            <div className="answer-actions">
              {!recording ? (
                <button
                  type="button"
                  className="record-button"
                  onClick={startRecording}
                  disabled={transcribing || !micEnabled}
                >
                  🎙 Start Voice Answer
                </button>
              ) : (
                <button
                  type="button"
                  className="stop-button"
                  onClick={stopRecording}
                >
                  ■ Stop Recording
                </button>
              )}

              <button
                type="button"
                className="submit-button"
                onClick={saveCurrentAnswer}
                disabled={transcribing || recording || !currentAnswer.trim()}
              >
                {currentQuestion < questions.length - 1 ? "Submit & Next Question →" : "Finish & Evaluate →"}
              </button>
            </div>
          </div>
        </div>

        {/* Side Column: Camera & Controls */}
        <aside className="side-column">
          <div className="camera-card">
            <div className="camera-header">
              <span className="camera-title">Webcam Preview</span>
              <span className={`status-badge ${cameraEnabled ? "online" : "offline"}`}>
                {cameraEnabled ? "LIVE" : "OFFLINE"}
              </span>
            </div>

            <div className="camera-viewport">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className={`camera-video ${!cameraEnabled ? "hidden" : ""}`}
              />

              {!cameraEnabled && (
                <div className="camera-fallback">
                  <div className="fallback-icon">📷</div>
                  <p>Camera is currently off</p>
                  <button
                    type="button"
                    className="enable-btn"
                    onClick={enableCameraAndMic}
                  >
                    Enable Camera & Mic
                  </button>
                </div>
              )}
            </div>

            <div className="camera-footer">
              <span className="device-status">
                🎤 Mic: {micEnabled ? "Ready" : "Disabled"}
              </span>
              <span className="device-status">
                📷 Video: {cameraEnabled ? "Active" : "Disabled"}
              </span>
            </div>
          </div>

          {/* Quick Interview Tips */}
          <div className="tips-card">
            <h4>💡 Pro Interview Tips</h4>
            <ul>
              <li><strong>STAR Method:</strong> For situational questions, explain the Situation, Task, Action, and Result.</li>
              <li><strong>Directness:</strong> Answer the core question directly in your opening sentence.</li>
              <li><strong>Pace:</strong> Aim for 120–160 words per minute; pause silently rather than using filler words.</li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  );
}

export default Interview;
