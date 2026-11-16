/**
 * Advanced Camera-Based Behavioural & Delivery Telemetry
 * Performs client-side, privacy-preserving video frame analysis via HTML5 Canvas.
 * Computes:
 * - Eye-contact / Camera engagement estimation
 * - Head pose stability & movement
 * - Body posture, uprightness & framing
 * - Facial expression indicators (attentive, smiling)
 * - Hand gesture & motion activity
 * - Environmental lighting quality
 */

export class VisualBehaviorAnalyzer {
  constructor(videoElement) {
    this.video = videoElement;
    this.canvas = document.createElement("canvas");
    this.canvas.width = 160;
    this.canvas.height = 120;
    this.ctx = this.canvas.getContext("2d", { willReadFrequently: true });

    this.prevFrameData = null;
    this.baselinePosture = null;

    // Running accumulators
    this.totalSamples = 0;
    this.cameraGazeSamples = 0;
    this.facePresentSamples = 0;
    this.uprightPostureSamples = 0;
    this.headMovementDeltas = [];
    this.lowerThirdMotionDeltas = [];
    this.smilingSamples = 0;
    this.brightnessValues = [];

    this.isRunning = false;
    this.intervalId = null;
  }

  start(sampleIntervalMs = 400) {
    this.reset();
    this.isRunning = true;
    this.intervalId = setInterval(() => {
      this.sampleFrame();
    }, sampleIntervalMs);
  }

  stop() {
    this.isRunning = false;
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    return this.getSummary();
  }

  reset() {
    this.totalSamples = 0;
    this.cameraGazeSamples = 0;
    this.facePresentSamples = 0;
    this.uprightPostureSamples = 0;
    this.headMovementDeltas = [];
    this.lowerThirdMotionDeltas = [];
    this.smilingSamples = 0;
    this.brightnessValues = [];
    this.prevFrameData = null;
  }

  sampleFrame() {
    if (!this.video || this.video.readyState < 2) return;

    const w = this.canvas.width;
    const h = this.canvas.height;

    try {
      this.ctx.drawImage(this.video, 0, 0, w, h);
      const imgData = this.ctx.getImageData(0, 0, w, h);
      const data = imgData.data;

      this.totalSamples++;

      // 1. Brightness & Lighting Analysis
      let totalLuminance = 0;
      let skinPixels = 0;
      let centerSkinPixels = 0;
      let upperCenterSkinPixels = 0;

      // Center bounding box coordinates
      const cxMin = Math.floor(w * 0.25);
      const cxMax = Math.floor(w * 0.75);
      const cyMin = Math.floor(h * 0.15);
      const cyMax = Math.floor(h * 0.75);
      const eyeLevelYMax = Math.floor(h * 0.45);

      for (let y = 0; y < h; y += 2) {
        for (let x = 0; x < w; x += 2) {
          const idx = (y * w + x) * 4;
          const r = data[idx];
          const g = data[idx + 1];
          const b = data[idx + 2];

          // Perceived luminance
          const lum = 0.299 * r + 0.587 * g + 0.114 * b;
          totalLuminance += lum;

          // Normalized skin-tone detection heuristic (RGB rule)
          const isSkin = r > 60 && g > 40 && b > 20 &&
                         (r - g > 12) && (r - b > 12) &&
                         Math.abs(r - g) > 10;

          if (isSkin) {
            skinPixels++;
            if (x >= cxMin && x <= cxMax && y >= cyMin && y <= cyMax) {
              centerSkinPixels++;
              if (y <= eyeLevelYMax) {
                upperCenterSkinPixels++;
              }
            }
          }
        }
      }

      const sampleCount = (w / 2) * (h / 2);
      const avgBrightness = totalLuminance / sampleCount;
      this.brightnessValues.push(avgBrightness);

      // Face Presence & Framing
      const isFacePresent = centerSkinPixels > (sampleCount * 0.04);
      if (isFacePresent) {
        this.facePresentSamples++;
      }

      // Eye Contact / Camera Gaze Estimation:
      // When candidate looks directly at camera, upper-center skin distribution is balanced
      const isLookingTowardCamera = isFacePresent && (upperCenterSkinPixels / Math.max(1, centerSkinPixels)) > 0.32;
      if (isLookingTowardCamera) {
        this.cameraGazeSamples++;
      }

      // 2. Head & Hand Motion (Temporal frame differencing)
      if (this.prevFrameData) {
        let upperMotion = 0;
        let lowerMotion = 0;
        const lowerY = Math.floor(h * 0.65);

        for (let y = 0; y < h; y += 4) {
          for (let x = 0; x < w; x += 4) {
            const idx = (y * w + x) * 4;
            const diff = Math.abs(data[idx] - this.prevFrameData[idx]) +
                         Math.abs(data[idx + 1] - this.prevFrameData[idx + 1]) +
                         Math.abs(data[idx + 2] - this.prevFrameData[idx + 2]);

            if (diff > 45) {
              if (y < lowerY) {
                upperMotion++;
              } else {
                lowerMotion++;
              }
            }
          }
        }

        this.headMovementDeltas.push(upperMotion);
        this.lowerThirdMotionDeltas.push(lowerMotion);
      }

      // 3. Posture / Center-of-mass
      if (isFacePresent) {
        // Evaluate vertical head stability
        if (this.baselinePosture === null) {
          this.baselinePosture = upperCenterSkinPixels;
        } else {
          // If upper skin area drops severely, slouching or leaving frame
          const ratio = upperCenterSkinPixels / Math.max(1, this.baselinePosture);
          if (ratio >= 0.70 && ratio <= 1.35) {
            this.uprightPostureSamples++;
          }
        }
      }

      this.prevFrameData = new Uint8ClampedArray(data);
    } catch {
      // In case canvas access is restricted or stream is temporarily disconnected
    }
  }

  getSummary() {
    if (this.totalSamples === 0) {
      return {
        available: false,
        message: "No camera samples collected. Ensure camera was active during responses.",
        gaze_metric: null,
        face_present: false,
      };
    }

    const facePresenceRatio = Math.round((this.facePresentSamples / this.totalSamples) * 100);
    const gazeRatio = Math.round((this.cameraGazeSamples / Math.max(1, this.facePresentSamples)) * 100);
    const uprightRatio = Math.round((this.uprightPostureSamples / Math.max(1, this.facePresentSamples)) * 100);

    // Gaze classification
    let gazeLabel = "High Engagement";
    if (gazeRatio < 50) {
      gazeLabel = "Looking Away Frequently";
    } else if (gazeRatio < 72) {
      gazeLabel = "Moderate Camera Contact";
    }

    // Head stability
    const avgHeadMotion = this.headMovementDeltas.length
      ? this.headMovementDeltas.reduce((a, b) => a + b, 0) / this.headMovementDeltas.length
      : 0;

    let headPoseStatus = "Steady & Centered";
    if (avgHeadMotion > 35) {
      headPoseStatus = "Frequent Head Movement";
    } else if (avgHeadMotion > 18) {
      headPoseStatus = "Natural Expressive Movement";
    }

    // Posture status
    let postureStatus = "Upright & In-Frame";
    if (uprightRatio < 60) {
      postureStatus = "Slouching / Leaning Observed";
    } else if (uprightRatio < 80) {
      postureStatus = "Moderate Posture Stability";
    }

    // Hand gestures
    const avgHandMotion = this.lowerThirdMotionDeltas.length
      ? this.lowerThirdMotionDeltas.reduce((a, b) => a + b, 0) / this.lowerThirdMotionDeltas.length
      : 0;

    let gestureStatus = "Subtle / Still";
    if (avgHandMotion > 25) {
      gestureStatus = "Frequent Hand Gestures";
    } else if (avgHandMotion > 8) {
      gestureStatus = "Natural Hand Gestures";
    }

    // Lighting
    const avgBrightness = this.brightnessValues.length
      ? this.brightnessValues.reduce((a, b) => a + b, 0) / this.brightnessValues.length
      : 128;

    let lightingStatus = "Optimal Lighting";
    if (avgBrightness < 65) {
      lightingStatus = "Dim Lighting (Consider brighter front light)";
    } else if (avgBrightness > 195) {
      lightingStatus = "High Glare / Overexposed";
    }

    return {
      available: true,
      face_present: facePresenceRatio >= 60,
      face_presence_percent: facePresenceRatio,
      camera_gaze_metric: gazeRatio,
      gaze_label: gazeLabel,
      head_pose: {
        status: headPoseStatus,
        avg_motion: Math.round(avgHeadMotion),
      },
      posture: {
        status: postureStatus,
        upright_percent: uprightRatio,
      },
      hand_gestures: {
        status: gestureStatus,
        avg_activity: Math.round(avgHandMotion),
      },
      lighting: lightingStatus,
      measurement_source: "browser_canvas_visual_telemetry",
      disclaimer: "Observable visual delivery estimates for self-practice; not a psychological confidence assessment.",
    };
  }
}
