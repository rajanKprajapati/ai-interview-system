import { useEffect, useRef, useState } from "react";

const questions = {
  technical: [
    "What is object-oriented programming and why is it useful?",
    "What is the difference between a list and a tuple in Python?",
    "What is a database and why do we use SQL?",
    "What is the difference between supervised and unsupervised learning?",
    "Explain the concept of an API."
  ],

  hr: [
    "Tell me about yourself.",
    "Why do you want to work in this field?",
    "What are your strengths?",
    "What is one weakness you are currently working on?",
    "Where do you see yourself in the next five years?"
  ],

  behavioral: [
    "Tell me about a difficult problem you solved.",
    "Describe a time when you worked in a team.",
    "Tell me about a time you made a mistake and what you learned.",
    "Describe a situation where you had to learn something quickly.",
    "Tell me about a time you handled pressure."
  ]
};

function Interview({ config }) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const [cameraOn, setCameraOn] = useState(false);
  const [micOn, setMicOn] = useState(false);

  const [questionIndex, setQuestionIndex] = useState(0);

  const [isRecording, setIsRecording] = useState(false);

  const [recordedAnswers, setRecordedAnswers] = useState([]);

  const [transcript, setTranscript] = useState("");
  const [transcribing, setTranscribing] = useState(false);

  const [error, setError] = useState("");

  const interviewQuestions =
    questions[config?.type] || questions.technical;

  const currentQuestion =
    interviewQuestions[questionIndex];

  /*
   * Start camera and microphone
   */
  const startCamera = async () => {
    try {
      setError("");

      const stream =
        await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true,
        });

      streamRef.current = stream;

      const video = videoRef.current;

      if (video) {
        video.srcObject = stream;

        video.onloadedmetadata = async () => {
          try {
            await video.play();
          } catch (err) {
            console.error(err);
          }
        };
      }

      setCameraOn(true);
      setMicOn(true);

    } catch (err) {
      console.error(err);

      setError(
        "Could not access camera or microphone. Please check browser permissions."
      );
    }
  };

  /*
   * Stop camera
   */
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current
        .getTracks()
        .forEach((track) => track.stop());

      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setCameraOn(false);
    setMicOn(false);
  };

  /*
   * Send recorded audio to FastAPI + Whisper
   */
  const transcribeAudio = async (audioBlob) => {
    try {
      setTranscribing(true);
      setError("");
      setTranscript("");

      const formData = new FormData();

      formData.append(
        "file",
        audioBlob,
        "answer.webm"
      );

      console.log("Sending audio to backend...");

      const response = await fetch(
        "http://127.0.0.1:8000/api/transcribe",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.text();

        console.error(
          "Backend error:",
          errorData
        );

        throw new Error(
          "Speech-to-text request failed."
        );
      }

      const data = await response.json();

      console.log(
        "Transcript received:",
        data.transcript
      );

      setTranscript(data.transcript);

      return data.transcript;

    } catch (err) {
      console.error(
        "Transcription error:",
        err
      );

      setError(
        "Could not convert your answer to text."
      );

      return "";

    } finally {
      setTranscribing(false);
    }
  };

  /*
   * Start recording answer
   */
  const startRecording = () => {
    if (!streamRef.current) {
      setError(
        "Please start the camera and microphone first."
      );
      return;
    }

    const audioTracks =
      streamRef.current.getAudioTracks();

    if (audioTracks.length === 0) {
      setError(
        "Microphone is not available."
      );
      return;
    }

    const audioStream =
      new MediaStream(audioTracks);

    const recorder =
      new MediaRecorder(audioStream);

    audioChunksRef.current = [];

    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunksRef.current.push(
          event.data
        );
      }
    };

    recorder.onstop = async () => {
      const audioBlob = new Blob(
        audioChunksRef.current,
        {
          type: "audio/webm",
        }
      );

      console.log(
        "Answer recorded:",
        audioBlob.size,
        "bytes"
      );

      /*
       * Send audio to Whisper
       */
      const text =
        await transcribeAudio(audioBlob);

      /*
       * Save answer and transcript
       */
      setRecordedAnswers((previous) => [
        ...previous,
        {
          question: currentQuestion,
          audio: audioBlob,
          transcript: text,
        },
      ]);

      console.log(
        "Answer transcript:",
        text
      );
    };

    mediaRecorderRef.current = recorder;

    recorder.start();

    setIsRecording(true);
    setError("");
    setTranscript("");
  };

  /*
   * Stop recording answer
   */
  const stopRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !== "inactive"
    ) {
      mediaRecorderRef.current.stop();
    }

    setIsRecording(false);
  };

  /*
   * Move to next question
   */
  const nextQuestion = () => {
    if (
      questionIndex <
      interviewQuestions.length - 1
    ) {
      setQuestionIndex(
        (previous) => previous + 1
      );

      setTranscript("");
    }
  };

  /*
   * Finish interview
   */
  const finishInterview = () => {
    console.log(
      "Interview completed"
    );

    console.log(
      "Recorded answers:",
      recordedAnswers
    );

    alert(
      "Interview completed."
    );

    stopCamera();
  };

  /*
   * Toggle camera
   */
  const toggleCamera = () => {
    if (!streamRef.current) return;

    const videoTrack =
      streamRef.current.getVideoTracks()[0];

    if (videoTrack) {
      videoTrack.enabled =
        !videoTrack.enabled;

      setCameraOn(
        videoTrack.enabled
      );
    }
  };

  /*
   * Toggle microphone
   */
  const toggleMic = () => {
    if (!streamRef.current) return;

    const audioTrack =
      streamRef.current.getAudioTracks()[0];

    if (audioTrack) {
      audioTrack.enabled =
        !audioTrack.enabled;

      setMicOn(
        audioTrack.enabled
      );
    }
  };

  /*
   * Cleanup
   */
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current
          .getTracks()
          .forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div className="interview-page">

      <div className="interview-header">

        <h1>AI Interview</h1>

        <p>
          {config?.type
            ? `${config.type.toUpperCase()} Interview`
            : "Technical Interview"}
        </p>

      </div>

      {/* Question */}

      <div className="question-card">

        <p className="question-number">
          Question {questionIndex + 1} of{" "}
          {Math.min(
            config?.questionCount || 5,
            interviewQuestions.length
          )}
        </p>

        <h2>
          {currentQuestion}
        </h2>

      </div>

      {/* Camera */}

      <div className="camera-container">

        {!cameraOn && (
          <div className="camera-placeholder">

            <h2>
              Camera is off
            </h2>

            <p>
              Start your camera and microphone
              to begin the interview.
            </p>

          </div>
        )}

        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className={
            cameraOn
              ? "camera-video"
              : "camera-video hidden"
          }
        />

      </div>

      {/* Error */}

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {/* Camera controls */}

      <div className="controls">

        {!cameraOn ? (

          <button onClick={startCamera}>
            Start Camera & Microphone
          </button>

        ) : (

          <>
            <button onClick={toggleCamera}>
              {cameraOn
                ? "Turn Camera Off"
                : "Turn Camera On"}
            </button>

            <button onClick={toggleMic}>
              {micOn
                ? "Mute Microphone"
                : "Unmute Microphone"}
            </button>

            <button onClick={stopCamera}>
              End Interview
            </button>
          </>

        )}

      </div>

      {/* Answer controls */}

      {cameraOn && micOn && (

        <div className="answer-controls">

          {!isRecording ? (

            <button
              className="record-button"
              onClick={startRecording}
            >
              🎙 Start Answer
            </button>

          ) : (

            <button
              className="stop-record-button"
              onClick={stopRecording}
            >
              ⏹ Stop Answer
            </button>

          )}

        </div>

      )}

      {/* Transcription status */}

      {transcribing && (
        <div className="transcript-box">

          <p>
            🎧 AI is converting your answer
            to text...
          </p>

        </div>
      )}

      {/* Transcript */}

      {transcript && !transcribing && (
        <div className="transcript-box">

          <h3>
            Your Answer
          </h3>

          <p>
            {transcript}
          </p>

        </div>
      )}

      {/* Next / Finish */}

      {!isRecording && cameraOn && (

        <div className="question-navigation">

          {questionIndex <
          Math.min(
            config?.questionCount || 5,
            interviewQuestions.length
          ) - 1 ? (

            <button
              onClick={nextQuestion}
            >
              Next Question →
            </button>

          ) : (

            <button
              onClick={finishInterview}
            >
              Finish Interview
            </button>

          )}

        </div>

      )}

    </div>
  );
}

export default Interview;