"""
Presentation Generator for AI Interview Preparation & Evaluation System
Generates an impressive, visually engaging 8-slide PowerPoint presentation (16:9 widescreen)
with deep navy theme, custom cards, genuine application screenshots, and professional typography.
"""
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- THEME COLOR PALETTE ---
    BG_DARK = RGBColor(10, 15, 29)          # Deep obsidian navy #0A0F1D
    CARD_BG = RGBColor(19, 27, 46)          # Dark slate glass #131B2E
    CARD_BORDER = RGBColor(42, 54, 79)      # Subtle border #2A364F
    CYAN_ACCENT = RGBColor(0, 210, 255)     # Electric cyan #00D2FF
    BLUE_ACCENT = RGBColor(59, 130, 246)    # Cobalt blue #3B82F6
    GREEN_ACCENT = RGBColor(16, 185, 129)   # Emerald #10B981
    RED_ACCENT = RGBColor(244, 63, 94)      # Rose red #F43F5E
    AMBER_ACCENT = RGBColor(245, 158, 11)   # Warm amber #F59E0B
    PURPLE_ACCENT = RGBColor(139, 92, 246)  # Electric purple #8B5CF6
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(148, 163, 184)    # Cool slate #94A3B8
    TEXT_BODY = RGBColor(226, 232, 240)     # Light slate #E2E8F0

    # Helper: Set dark background
    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    # Helper: Add header block
    def add_header(slide, eyebrow, title, subtitle=None):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Eyebrow
        p0 = tf.paragraphs[0]
        p0.text = eyebrow.upper()
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = CYAN_ACCENT
        p0.space_after = Pt(2)

        # Title
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_after = Pt(2)

        # Subtitle
        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(11)
            p2.font.color.rgb = TEXT_MUTED

    # Helper: Add a card container
    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: INTRODUCTION
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Title Banner Box
    title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(2.0))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_eye = tf1.paragraphs[0]
    p_eye.text = "COLLEGE HACKATHON & PROJECT DEFENSE • 2025–2026"
    p_eye.font.name = "Segoe UI"
    p_eye.font.size = Pt(11)
    p_eye.font.bold = True
    p_eye.font.color.rgb = CYAN_ACCENT
    p_eye.space_after = Pt(6)

    p_title = tf1.add_paragraph()
    p_title.text = "AI Interview Preparation & Evaluation System"
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_after = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "An Intelligent Multi-Modal Platform for Automated Mock Interview Simulation, Local Speech Recognition & Privacy-Preserving Behavioral Telemetry"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = TEXT_MUTED

    # Left Column: Project Info Card
    add_card(slide1, Inches(0.8), Inches(2.9), Inches(5.6), Inches(4.0))
    info_box = slide1.shapes.add_textbox(Inches(1.1), Inches(3.1), Inches(5.0), Inches(3.6))
    tf_info = info_box.text_frame
    tf_info.word_wrap = True

    p = tf_info.paragraphs[0]
    p.text = "PROJECT METADATA & ACADEMIC CREDENTIALS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(12)

    details = [
        ("Candidate / Developer:", "Rajan Kumar Prajapati"),
        ("Branch & Specialization:", "B.Tech — CSE (Artificial Intelligence)"),
        ("Academic Institution:", "Bansal Institute of Engineering & Technology"),
        ("Location & Affiliation:", "Lucknow • Dr. A.P.J. Abdul Kalam Tech. Univ."),
        ("Project Classification:", "B.Tech Final Year Mini Project"),
        ("System Architecture:", "Full-Stack (React 19 + FastAPI + PostgreSQL)"),
    ]
    for label, val in details:
        p = tf_info.add_paragraph()
        p.text = f"{label} "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        run = p.add_run()
        run.text = val
        run.font.bold = True
        run.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(5)

    # Right Column: Visual Highlight Card
    add_card(slide1, Inches(6.7), Inches(2.9), Inches(5.8), Inches(4.0))
    if os.path.exists("screenshots/4_live_interview.png"):
        slide1.shapes.add_picture("screenshots/4_live_interview.png", Inches(6.9), Inches(3.1), Inches(5.4), Inches(3.0))

    caption_box = slide1.shapes.add_textbox(Inches(6.9), Inches(6.25), Inches(5.4), Inches(0.55))
    tf_cap = caption_box.text_frame
    tf_cap.word_wrap = True
    p = tf_cap.paragraphs[0]
    p.text = "🤖 Live System Interface: Dual WebRTC Camera & Local Neural Audio Simulation"
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: PROBLEM & OUR SOLUTION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(
        slide2,
        "THE CHALLENGE & OUR SOLUTION",
        "Bridging the College-to-Corporate Placement Gap",
        "Why conventional interview preparation fails engineering candidates, and how autonomous AI solves it."
    )

    col_w = Inches(5.7)
    card_h = Inches(4.7)

    # Problem Card (Left)
    add_card(slide2, Inches(0.8), Inches(1.8), col_w, card_h)
    prob_box = slide2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.3))
    tf_prob = prob_box.text_frame
    tf_prob.word_wrap = True

    p = tf_prob.paragraphs[0]
    p.text = "❌ TRADITIONAL INTERVIEW PREPARATION"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RED_ACCENT
    p.space_after = Pt(14)

    prob_points = [
        ("Subjective Peer Mock Feedback", "Peer mock interviews lack rigorous technical depth and objective, standardized evaluation rubrics."),
        ("Hidden Verbal Deficiencies", "Students are blind to repetitive filler words ('um', 'like', 'basically') and speaking pace outliers (>180 or <90 WPM)."),
        ("Overlooked Camera Presence", "In virtual placement drives, poor eye-gaze and slouching lead to silent candidate disqualifications."),
        ("Cost-Prohibitive Coaching", "Commercial interview platforms charge ₹5,000–₹15,000/month, creating an unfair barrier for college students."),
    ]
    for title, desc in prob_points:
        p = tf_prob.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Solution Card (Right)
    add_card(slide2, Inches(6.8), Inches(1.8), col_w, card_h)
    sol_box = slide2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.3))
    tf_sol = sol_box.text_frame
    tf_sol.word_wrap = True

    p = tf_sol.paragraphs[0]
    p.text = "✅ OUR AI-POWERED SOLUTION"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.space_after = Pt(14)

    sol_points = [
        ("Objective Multi-Axis Scoring", "Gemini AI grades answers across 4 verified dimensions: Relevance, Technical Accuracy, Clarity, and Confidence."),
        ("Deterministic Speech Analytics", "Quantifies conversational pace (120–160 WPM benchmark) and calculates exact lexical filler density."),
        ("Privacy-Preserving Telemetry", "Browser-side canvas heuristics quantify eye contact, head stability, posture, and room lighting."),
        ("Always-Available & Zero-Cost", "Unlimited, private, on-demand practice sessions on standard laptops with local neural transcription."),
    ]
    for title, desc in sol_points:
        p = tf_sol.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Bottom Pill
    pill = add_card(slide2, Inches(0.8), Inches(6.7), Inches(11.733), Inches(0.45), bg_color=RGBColor(24, 34, 58))
    pill_box = slide2.shapes.add_textbox(Inches(0.8), Inches(6.7), Inches(11.733), Inches(0.45))
    tf_p = pill_box.text_frame
    p = tf_p.paragraphs[0]
    p.text = "💡 Transformation: Replaces placement anxiety with quantifiable, evidence-based corporate interview readiness."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 3: KEY FEATURES
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(
        slide3,
        "CORE CAPABILITIES",
        "Engineered for Real-World Placement Success",
        "Six production-verified modules driving the mock interview and evaluation lifecycle."
    )

    features = [
        ("🤖 Dynamic AI Questions",
         "Technical, Behavioral (STAR), and System Design modes adapting dynamically to Beginner, Intermediate, and Advanced tiers with role targeting.",
         CYAN_ACCENT),
        ("📄 Resume & JD Skill Matching",
         "Native PDF text parsing via pypdf extracting 60+ industry competencies, computing set overlap, and targeting candidate skill gaps.",
         BLUE_ACCENT),
        ("🎙️ Local Neural Speech-to-Text",
         "faster-whisper base model quantized to int8 on CPU; delivers sub-3s local transcription with zero voice cloud leakage.",
         GREEN_ACCENT),
        ("👁️ Camera Behavioral Telemetry",
         "HTML5 canvas frame differencing at 2.5 FPS tracking eye gaze, head pose, posture, and lighting with student-centric disclaimers.",
         AMBER_ACCENT),
        ("📊 Multi-Dimensional AI Rubrics",
         "Structured Gemini evaluation scoring Relevance, Accuracy, Communication, and Confidence (0–10 scale) with tailored action plans.",
         PURPLE_ACCENT),
        ("📈 Performance Dashboard & History",
         "PostgreSQL relational persistence powering chronological score progression charts, competency breakdowns, and past report reviews.",
         CYAN_ACCENT),
    ]

    card_w = Inches(3.75)
    card_h = Inches(2.35)
    xs = [Inches(0.8), Inches(4.8), Inches(8.8)]
    ys = [Inches(1.85), Inches(4.5)]

    for idx, (title, desc, color) in enumerate(features):
        col = idx % 3
        row = idx // 3
        add_card(slide3, xs[col], ys[row], card_w, card_h)
        fbox = slide3.shapes.add_textbox(xs[col] + Inches(0.2), ys[row] + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
        tf_f = fbox.text_frame
        tf_f.word_wrap = True

        p0 = tf_f.paragraphs[0]
        p0.text = title
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = color
        p0.space_after = Pt(8)

        p1 = tf_f.add_paragraph()
        p1.text = desc
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(10)
        p1.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 4: HOW THE SYSTEM WORKS
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(
        slide4,
        "SYSTEM WORKFLOW",
        "End-to-End Candidate Practice Lifecycle",
        "A streamlined, high-throughput pipeline from candidate profile setup to deep rubric analysis."
    )

    steps = [
        ("01", "SETUP & TARGETING",
         "Candidate selects target role, difficulty, and interview mode. Uploads resume PDF; system extracts skills and identifies target job gaps.",
         CYAN_ACCENT),
        ("02", "AI SYNTHESIS",
         "Gemini 3.5 Flash Lite receives contextual parameters (role, difficulty, resume gaps) to formulate tailored questions without generic trivia.",
         BLUE_ACCENT),
        ("03", "LIVE INTERVIEW",
         "WebRTC enables live camera preview. Candidate records spoken answer; browser canvas captures frame differencing metrics concurrently.",
         GREEN_ACCENT),
        ("04", "LOCAL SPEECH-TO-TEXT",
         "faster-whisper base CPU int8 model transcribes WebM audio locally. Calculates exact speaking tempo (WPM) and filler word rate.",
         AMBER_ACCENT),
        ("05", "RUBRIC EVALUATION",
         "Gemini evaluates responses across 4 rubric axes. Atomic transaction commits session to PostgreSQL; updates dashboard and history.",
         PURPLE_ACCENT),
    ]

    step_w = Inches(2.2)
    step_h = Inches(4.5)
    step_gap = Inches(0.18)

    for i, (num, title, body, color) in enumerate(steps):
        cur_left = Inches(0.8) + i * (step_w + step_gap)
        add_card(slide4, cur_left, Inches(1.85), step_w, step_h)

        sbox = slide4.shapes.add_textbox(cur_left + Inches(0.15), Inches(2.0), step_w - Inches(0.3), step_h - Inches(0.3))
        tf_s = sbox.text_frame
        tf_s.word_wrap = True

        p_num = tf_s.paragraphs[0]
        p_num.text = num
        p_num.font.name = "Segoe UI"
        p_num.font.size = Pt(28)
        p_num.font.bold = True
        p_num.font.color.rgb = color
        p_num.space_after = Pt(4)

        p_t = tf_s.add_paragraph()
        p_t.text = title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE
        p_t.space_after = Pt(10)

        p_b = tf_s.add_paragraph()
        p_b.text = body
        p_b.font.name = "Segoe UI"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = TEXT_MUTED

    # Bottom Pill
    pill = add_card(slide4, Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.45), bg_color=RGBColor(24, 34, 58))
    pill_box = slide4.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.45))
    tf_p = pill_box.text_frame
    p = tf_p.paragraphs[0]
    p.text = "⚡ Performance: Sub-3.5s answer transcription latency • 100% Client-Side Audio/Video Privacy • Single-Transaction ACID Persistence"
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 5: TECHNOLOGY STACK
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(
        slide5,
        "ENGINEERING ARCHITECTURE",
        "Production-Grade, Modular Technology Stack",
        "Every technology listed is actively implemented and verified in the codebase."
    )

    techs = [
        ("💻 Frontend Layer",
         [("Framework", "React 19 & Vite 8 SPA"),
          ("Design System", "CSS Custom Properties (Zero bulky UI bloat)"),
          ("Media Streams", "WebRTC MediaStream & Web Audio APIs"),
          ("Client State", "Tab-based SPA routing with auto track shutdown")],
         CYAN_ACCENT),
        ("⚡ Backend Engine",
         [("Framework", "FastAPI (High-performance async ASGI)"),
          ("ASGI Server", "Uvicorn (Production reload worker)"),
          ("Schema Validation", "Pydantic v2 (Strict typing & serialization)"),
          ("Runtime", "Python 3.13 (Native 64-bit Windows)")],
         BLUE_ACCENT),
        ("🗄️ Database & Storage",
         [("Database", "PostgreSQL 16 Relational Engine"),
          ("ORM Engine", "SQLAlchemy 2.0 (pool_pre_ping enabled)"),
          ("Migrations", "Alembic additive versioning (zero data loss)"),
          ("Integrity", "Atomic multi-table transaction rollback")],
         GREEN_ACCENT),
        ("🧠 Generative AI Pipeline",
         [("Model", "Google Gemini 3.5 Flash Lite"),
          ("SDK", "Official google-genai Python Client"),
          ("Prompt Engine", "Role, difficulty & resume gap injection"),
          ("Evaluation", "Multi-axis structured JSON scoring schema")],
         PURPLE_ACCENT),
        ("🗣️ Speech Recognition",
         [("Engine", "faster-whisper (CTranslate2 accelerated)"),
          ("Model Size", "Base model (~73M parameters)"),
          ("Quantization", "int8 CPU inference (sub-3s latency)"),
          ("Privacy", "Zero cloud audio upload; temporary files deleted")],
         AMBER_ACCENT),
        ("👁️ Vision & Documents",
         [("Vision Engine", "HTML5 Canvas temporal frame differencing"),
          ("Telemetry", "Camera gaze, head pose, posture, and lighting"),
          ("PDF Parsing", "pypdf (v7.1.0) in-memory text extraction"),
          ("Skill Engine", "Regex word-boundary scanner (60+ skills)")],
         CYAN_ACCENT),
    ]

    for idx, (title, items, color) in enumerate(techs):
        col = idx % 3
        row = idx // 3
        add_card(slide5, xs[col], ys[row], card_w, card_h)
        tbox = slide5.shapes.add_textbox(xs[col] + Inches(0.2), ys[row] + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.35))
        tf_t = tbox.text_frame
        tf_t.word_wrap = True

        p0 = tf_t.paragraphs[0]
        p0.text = title
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = color
        p0.space_after = Pt(8)

        for label, val in items:
            p = tf_t.add_paragraph()
            p.text = f"• {label}: "
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_WHITE
            run = p.add_run()
            run.text = val
            run.font.bold = False
            run.font.color.rgb = TEXT_MUTED
            p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 6: ACTUAL PROJECT DEMONSTRATION
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(
        slide6,
        "LIVE PRODUCT SHOWCASE",
        "Actual Working Interface in Action",
        "Authentic screenshots captured directly from the live application and PostgreSQL database."
    )

    shot_w = Inches(5.7)
    shot_h = Inches(2.35)
    s_xs = [Inches(0.8), Inches(6.8)]
    s_ys = [Inches(1.85), Inches(4.55)]

    screens = [
        ("screenshots/1_interview_setup.png", "1. Setup & Resume PDF Skill Matching",
         "Adaptive configuration for role, difficulty tier, and automated resume PDF skill gap extraction.", s_xs[0], s_ys[0]),
        ("screenshots/4_live_interview.png", "2. Live Camera & Speech Simulation",
         "WebRTC camera viewport, microphone capture controls, local Whisper transcription, and STAR guidance.", s_xs[1], s_ys[0]),
        ("screenshots/3_performance_report.png", "3. Performance Report & Visual Telemetry",
         "Overall score (8.9/10), speaking tempo (140 WPM), camera gaze (84%), posture (90%), and action plan.", s_xs[0], s_ys[1]),
        ("screenshots/2_dashboard_analytics.png", "4. Candidate Analytics & Longitudinal Trends",
         "Aggregate performance KPIs, score progression trendline, and competency distributions.", s_xs[1], s_ys[1]),
    ]

    for img_path, title, caption, left, top in screens:
        add_card(slide6, left, top, shot_w, shot_h)
        if os.path.exists(img_path):
            slide6.shapes.add_picture(img_path, left + Inches(0.1), top + Inches(0.1), shot_w - Inches(0.2), shot_h - Inches(0.7))

        cbox = slide6.shapes.add_textbox(left + Inches(0.1), top + shot_h - Inches(0.55), shot_w - Inches(0.2), Inches(0.5))
        tf_c = cbox.text_frame
        tf_c.word_wrap = True
        p0 = tf_c.paragraphs[0]
        p0.text = title
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = CYAN_ACCENT

        p1 = tf_c.add_paragraph()
        p1.text = caption
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(8.5)
        p1.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 7: RESULTS, IMPACT & FUTURE SCOPE
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(
        slide7,
        "VERIFIED IMPACT & ROADMAP",
        "Measurable Value & Future Enhancements",
        "Tangible student placement outcomes and future roadmap for institutional adoption."
    )

    # Left: Impact Card
    add_card(slide7, Inches(0.8), Inches(1.8), col_w, card_h)
    imp_box = slide7.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.1), Inches(4.3))
    tf_imp = imp_box.text_frame
    tf_imp.word_wrap = True

    p = tf_imp.paragraphs[0]
    p.text = "🎯 VERIFIED EDUCATIONAL IMPACT"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.space_after = Pt(14)

    impact_items = [
        ("Actionable Delivery Diagnostics", "Eliminates conversational pace outliers (target: 120–160 WPM) and identifies habitual vocalized fillers."),
        ("Targeted Technical Revision", "Dynamically generates questions challenging the candidate's exact resume gaps rather than generic trivia."),
        ("Placement Anxiety Reduction", "Provides an unconstrained, private sandbox for students to practice speaking aloud before high-stakes drives."),
        ("Zero Privacy Vulnerabilities", "Audio processed locally via faster-whisper; zero camera video transmitted over external cloud networks."),
    ]
    for title, desc in impact_items:
        p = tf_imp.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Right: Future Scope Card
    add_card(slide7, Inches(6.8), Inches(1.8), col_w, card_h)
    fut_box = slide7.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.3))
    tf_fut = fut_box.text_frame
    tf_fut.word_wrap = True

    p = tf_fut.paragraphs[0]
    p.text = "🚀 SCALABILITY & FUTURE ROADMAP"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(14)

    future_items = [
        ("Gemini Live Audio API", "Enable full-duplex conversational interruptions and adaptive follow-up probing when candidates hesitate."),
        ("In-Browser Coding Sandbox", "Integrate Monaco Editor + WebAssembly runtime for live algorithm design and data structure execution."),
        ("Institutional T&P Coordinator Portal", "Role-based access control (RBAC) allowing college placement officers to assign batches and track cohorts."),
        ("Client WebAssembly Vision", "WebGL-accelerated FaceMesh landmarks for real-time facial micro-expression and head pose analysis."),
    ]
    for title, desc in future_items:
        p = tf_fut.add_paragraph()
        p.text = f"• {title}: "
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Bottom Pill
    pill = add_card(slide7, Inches(0.8), Inches(6.7), Inches(11.733), Inches(0.45), bg_color=RGBColor(24, 34, 58))
    pill_box = slide7.shapes.add_textbox(Inches(0.8), Inches(6.7), Inches(11.733), Inches(0.45))
    tf_p = pill_box.text_frame
    p = tf_p.paragraphs[0]
    p.text = "💡 Practical Impact: Empowering engineering students to transition from theoretical knowledge to corporate placement readiness."
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 8: CONCLUSION & THANK YOU
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(
        slide8,
        "PROJECT SUMMARY & DEFENSE",
        "Empowering Every Candidate with Objective AI Mentorship",
        "Summary of key achievements, architectural integrity, and live demonstration invitation."
    )

    t_cards = [
        ("🏆 Fully Functional & Verified",
         "Complete multi-modal platform operating seamlessly across React 19, FastAPI, PostgreSQL, Gemini, and faster-whisper. Zero mock data or simulated scores in production.",
         CYAN_ACCENT),
        ("🔒 Privacy-First & Cost-Free",
         "Local neural speech transcription and client-side canvas vision heuristics eliminate cloud API subscription costs while guaranteeing complete student data privacy.",
         GREEN_ACCENT),
        ("🎓 Standalone & Production-Ready",
         "Automated test suite (test_system.py) passing 100%. One-click operational batch launcher (START_PROJECT.bat) enables independent execution without IDE tools.",
         PURPLE_ACCENT),
    ]

    for idx, (title, desc, color) in enumerate(t_cards):
        add_card(slide8, xs[idx], Inches(1.85), card_w, Inches(2.55))
        cbox = slide8.shapes.add_textbox(xs[idx] + Inches(0.2), Inches(2.05), card_w - Inches(0.4), Inches(2.15))
        tf_c = cbox.text_frame
        tf_c.word_wrap = True

        p0 = tf_c.paragraphs[0]
        p0.text = title
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = color
        p0.space_after = Pt(10)

        p1 = tf_c.add_paragraph()
        p1.text = desc
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = TEXT_BODY

    # Presenter & Thank You Card (Bottom)
    add_card(slide8, Inches(0.8), Inches(4.65), Inches(11.733), Inches(2.35), bg_color=RGBColor(24, 34, 58))
    ty_box = slide8.shapes.add_textbox(Inches(1.1), Inches(4.8), Inches(11.133), Inches(2.05))
    tf_ty = ty_box.text_frame
    tf_ty.word_wrap = True

    p0 = tf_ty.paragraphs[0]
    p0.text = "THANK YOU! QUESTIONS & LIVE DEMONSTRATION"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    p0.alignment = PP_ALIGN.CENTER
    p0.space_after = Pt(8)

    p1 = tf_ty.add_paragraph()
    p1.text = "Student Presenter: Rajan Kumar Prajapati • Branch: B.Tech Computer Science & Engineering (Artificial Intelligence)"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(4)

    p2 = tf_ty.add_paragraph()
    p2.text = "Department of Computer Science & Engineering • Bansal Institute of Engineering & Technology, Lucknow (AKTU Code: 422)"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER
    p2.space_after = Pt(8)

    p3 = tf_ty.add_paragraph()
    p3.text = "We invite the respected examination panel for technical evaluation, feedback, and interactive live demonstration."
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(10)
    p3.font.bold = True
    p3.font.color.rgb = GREEN_ACCENT
    p3.alignment = PP_ALIGN.CENTER

    output_path = os.path.abspath("AI_Interview_System_Presentation.pptx")
    prs.save(output_path)
    print(f"[SUCCESS] Presentation generated successfully: {output_path}")

if __name__ == "__main__":
    create_presentation()
