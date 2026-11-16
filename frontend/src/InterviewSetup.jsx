import { useState } from "react";
import { parseResumeAndJob } from "./services/api";

function InterviewSetup({ onStart }) {
  const [type, setType] = useState("technical");
  const [questionCount, setQuestionCount] = useState(5);
  const [difficulty, setDifficulty] = useState("intermediate");
  const [role, setRole] = useState("Software Engineer");
  const [subject, setSubject] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const [resumeFile, setResumeFile] = useState(null);
  const [resumeSkills, setResumeSkills] = useState([]);
  const [matchedSkills, setMatchedSkills] = useState([]);
  const [skillGaps, setSkillGaps] = useState([]);
  const [parsingResume, setParsingResume] = useState(false);
  const [parseError, setParseError] = useState("");

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
      setParseError("Please select a PDF file.");
      return;
    }

    setResumeFile(file);
    setParseError("");
    setParsingResume(true);

    try {
      const result = await parseResumeAndJob(file, jobDescription || "Software Engineer");
      setResumeSkills(result.resume_skills || []);
      setMatchedSkills(result.matched_skills || []);
      setSkillGaps(result.possible_skill_gaps || []);
    } catch (err) {
      console.warn("Resume parsing error:", err);
      setParseError(err.message || "Could not extract text from this PDF. You can still continue.");
    } finally {
      setParsingResume(false);
    }
  };

  const handleClearResume = () => {
    setResumeFile(null);
    setResumeSkills([]);
    setMatchedSkills([]);
    setSkillGaps([]);
    setParseError("");
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onStart({
      type,
      questionCount: Number(questionCount),
      difficulty,
      role: role.trim() || "Software Engineer",
      subject: subject.trim(),
      resumeSkills,
      skillGaps,
      resumeFilename: resumeFile ? resumeFile.name : null,
      jobDescription: jobDescription.trim() || null,
    });
  };

  return (
    <div className="setup-container">
      <div className="setup-header">
        <span className="setup-badge">CUSTOMIZE SESSION</span>
        <h1>AI Mock Interview Setup</h1>
        <p>Configure your target role, difficulty, and optional resume to personalize your interview questions.</p>
      </div>

      <form onSubmit={handleSubmit} className="setup-form">
        {/* Interview Type Selection */}
        <div className="form-group">
          <label className="form-label">Interview Type</label>
          <div className="type-grid">
            <button
              type="button"
              className={`type-card ${type === "technical" ? "active" : ""}`}
              onClick={() => setType("technical")}
            >
              <div className="type-icon">💻</div>
              <div className="type-content">
                <strong>Technical</strong>
                <p>Coding, system architecture, database design, and framework concepts.</p>
              </div>
            </button>

            <button
              type="button"
              className={`type-card ${type === "hr" ? "active" : ""}`}
              onClick={() => setType("hr")}
            >
              <div className="type-icon">🤝</div>
              <div className="type-content">
                <strong>HR & Fit</strong>
                <p>Cultural alignment, teamwork, workplace ethics, and career growth.</p>
              </div>
            </button>

            <button
              type="button"
              className={`type-card ${type === "behavioral" ? "active" : ""}`}
              onClick={() => setType("behavioral")}
            >
              <div className="type-icon">🎯</div>
              <div className="type-content">
                <strong>Behavioral (STAR)</strong>
                <p>Situational questions evaluated by Situation, Task, Action, and Result.</p>
              </div>
            </button>
          </div>
        </div>

        {/* Role & Subject */}
        <div className="form-row">
          <div className="form-group flex-1">
            <label className="form-label">Target Job Role</label>
            <input
              type="text"
              className="text-input"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              placeholder="e.g. Full Stack Developer, Data Scientist"
              required
            />
          </div>

          <div className="form-group flex-1">
            <label className="form-label">Specific Subject / Technology (Optional)</label>
            <input
              type="text"
              className="text-input"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="e.g. React, Python, PostgreSQL, System Design"
            />
          </div>
        </div>

        {/* Difficulty & Question Count */}
        <div className="form-row">
          <div className="form-group flex-1">
            <label className="form-label">Difficulty Level</label>
            <div className="segmented-control">
              {["easy", "intermediate", "advanced"].map((lvl) => (
                <button
                  key={lvl}
                  type="button"
                  className={`segment-btn ${difficulty === lvl ? "active" : ""}`}
                  onClick={() => setDifficulty(lvl)}
                >
                  {lvl.charAt(0).toUpperCase() + lvl.slice(1)}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group flex-1">
            <label className="form-label">Number of Questions</label>
            <select
              className="select-input"
              value={questionCount}
              onChange={(e) => setQuestionCount(Number(e.target.value))}
            >
              <option value={3}>3 Questions (~5 mins)</option>
              <option value={5}>5 Questions (~10 mins)</option>
              <option value={7}>7 Questions (~15 mins)</option>
              <option value={10}>10 Questions (~20 mins)</option>
            </select>
          </div>
        </div>

        {/* Optional Resume Upload */}
        <div className="form-group">
          <label className="form-label">
            Candidate Resume (Optional PDF)
            <span className="label-hint">Personalizes questions based on your background</span>
          </label>

          <div className="resume-box">
            {!resumeFile ? (
              <label className="file-upload-label">
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={handleFileUpload}
                  style={{ display: "none" }}
                />
                <div className="upload-prompt">
                  <span className="upload-icon">📄</span>
                  <span>Click or drag your <strong>PDF resume</strong> here</span>
                  <span className="upload-note">Max 10 MB text-based PDF</span>
                </div>
              </label>
            ) : (
              <div className="resume-attached">
                <div className="resume-info">
                  <span className="file-icon">✓</span>
                  <div>
                    <strong>{resumeFile.name}</strong>
                    <span className="file-size">({(resumeFile.size / 1024).toFixed(0)} KB)</span>
                  </div>
                </div>
                <button
                  type="button"
                  className="remove-btn"
                  onClick={handleClearResume}
                >
                  Remove
                </button>
              </div>
            )}

            {parsingResume && (
              <div className="parsing-status">
                <span className="spinner-sm" /> Analyzing resume skills with AI...
              </div>
            )}

            {parseError && (
              <div className="parse-warning">
                ⚠️ {parseError}
              </div>
            )}

            {resumeSkills.length > 0 && (
              <div className="skills-detected">
                <span className="skills-title">Skills detected from your resume:</span>
                <div className="skill-badges">
                  {resumeSkills.map((s, i) => (
                    <span key={i} className="skill-badge">{s}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Optional Job Description */}
        <div className="form-group">
          <label className="form-label">
            Target Job Description (Optional)
            <span className="label-hint">Paste key requirements to target your gaps</span>
          </label>
          <textarea
            className="textarea-input"
            rows={3}
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste job posting details, required skills, or responsibilities..."
          />
        </div>

        {/* Submit Action */}
        <button type="submit" className="start-btn">
          Start AI Mock Interview →
        </button>
      </form>
    </div>
  );
}

export default InterviewSetup;
