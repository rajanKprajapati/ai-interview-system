import { useEffect, useRef, useState } from "react";

function Interview() {
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const [cameraOn, setCameraOn] = useState(false);
  const [micOn, setMicOn] = useState(false);
  const [error, setError] = useState("");

  const startCamera = async () => {
    try {
      setError("");

      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setError("Your browser does not support camera access.");
        return;
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: true,
      });

      streamRef.current = stream;

      const video = videoRef.current;

if (video) {
  video.onloadedmetadata = async () => {
    try {
      await video.play();
    } catch (err) {
      console.error("Video play error:", err);
      setError("The camera stream was received, but the video could not play.");
    }
  };

  video.srcObject = stream;
}if (video) {
  video.onloadedmetadata = async () => {
    try {
      await video.play();
    } catch (err) {
      console.error("Video play error:", err);
      setError("The camera stream was received, but the video could not play.");
    }
  };

  video.srcObject = stream;
}

      setCameraOn(true);
      setMicOn(true);

    } catch (err) {
      console.error("Camera error:", err);

      if (err.name === "NotAllowedError") {
        setError("Camera or microphone permission was denied.");
      } else if (err.name === "NotFoundError") {
        setError("No camera or microphone was found.");
      } else if (err.name === "NotReadableError") {
        setError("Camera may already be in use by another application.");
      } else {
        setError("Could not access the camera or microphone.");
      }
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        track.stop();
      });

      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setCameraOn(false);
    setMicOn(false);
  };

  const toggleCamera = () => {
    if (!streamRef.current) return;

    const videoTrack = streamRef.current.getVideoTracks()[0];

    if (videoTrack) {
      videoTrack.enabled = !videoTrack.enabled;
      setCameraOn(videoTrack.enabled);
    }
  };

  const toggleMic = () => {
    if (!streamRef.current) return;

    const audioTrack = streamRef.current.getAudioTracks()[0];

    if (audioTrack) {
      audioTrack.enabled = !audioTrack.enabled;
      setMicOn(audioTrack.enabled);
    }
  };

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => {
          track.stop();
        });
      }
    };
  }, []);

  return (
    <div className="interview-page">

      <div className="interview-header">
        <h1>AI Interview</h1>
        <p>Camera Interview Room</p>
      </div>

      <div className="camera-container">

        {!cameraOn && (
          <div className="camera-placeholder">
            <h2>Camera is off</h2>
            <p>Start your camera and microphone to begin.</p>
          </div>
        )}

        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className={cameraOn ? "camera-video" : "camera-video hidden"}
        />

      </div>

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      <div className="controls">

        {!cameraOn ? (
          <button onClick={startCamera}>
            Start Camera & Microphone
          </button>
        ) : (
          <>
            <button onClick={toggleCamera}>
              {cameraOn ? "Turn Camera Off" : "Turn Camera On"}
            </button>

            <button onClick={toggleMic}>
              {micOn ? "Mute Microphone" : "Unmute Microphone"}
            </button>

            <button onClick={stopCamera}>
              End Camera
            </button>
          </>
        )}

      </div>

    </div>
  );
}

export default Interview;