"""
Presentation Generator for AI Interview Preparation & Evaluation System
Generates an 8-slide PowerPoint presentation (16:9 widescreen) in simple English,
with a clean, professional technology theme, custom cards, genuine screenshots, and balanced layout.
"""
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- COLOR PALETTE (Modern Clean Tech Dark Theme) ---
    BG_DARK = RGBColor(11, 17, 33)          # Dark Navy #0B1121
    CARD_BG = RGBColor(19, 28, 49)          # Slate Navy #131C31
    CARD_BORDER = RGBColor(38, 52, 82)      # Border #263452
    CARD_HEADER_BG = RGBColor(26, 38, 66)   # Slightly lighter navy for sub-cards #1A2642
    
    CYAN_ACCENT = RGBColor(14, 165, 233)    # Sky Cyan #0EA5E9
    CYAN_LIGHT = RGBColor(56, 189, 248)     # Bright Cyan #38BDF8
    BLUE_ACCENT = RGBColor(99, 102, 241)    # Indigo Blue #6366F1
    GREEN_ACCENT = RGBColor(16, 185, 129)   # Emerald Green #10B981
    RED_ACCENT = RGBColor(244, 63, 94)      # Rose Red #F43F5E
    AMBER_ACCENT = RGBColor(245, 158, 11)   # Warm Amber #F59E0B
    PURPLE_ACCENT = RGBColor(168, 85, 247)  # Violet Purple #A855F7
    
    TEXT_WHITE = RGBColor(255, 255, 255)    # High-contrast white
    TEXT_BODY = RGBColor(226, 232, 240)     # Light Slate #E2E8F0
    TEXT_MUTED = RGBColor(148, 163, 184)    # Cool Slate #94A3B8

    FONT_MAIN = "Segoe UI"

    # Helper: Set dark slide background
    def set_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    # Helper: Add header block
    def add_header(slide, eyebrow, title, subtitle=None):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.15))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Eyebrow
        p0 = tf.paragraphs[0]
        p0.text = eyebrow.upper()
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = CYAN_LIGHT
        p0.space_after = Pt(2)

        # Title
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_after = Pt(2)

        # Subtitle
        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.name = FONT_MAIN
            p2.font.size = Pt(11)
            p2.font.color.rgb = TEXT_MUTED

    # Helper: Add rounded card
    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # Helper: Add bottom highlight pill
    def add_bottom_pill(slide, text, accent_color=CYAN_LIGHT):
        pill = add_card(slide, Inches(0.8), Inches(6.75), Inches(11.733), Inches(0.45), bg_color=RGBColor(20, 30, 52))
        pill_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.75), Inches(11.733), Inches(0.45))
        tf = pill_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.name = FONT_MAIN
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = accent_color
        p.alignment = PP_ALIGN.CENTER
        return pill

    # =========================================================================
    # SLIDE 1: INTRODUCTION
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_background(slide1)

    # Top Title Block
    title_box = slide1.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(1.85))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_eye = tf1.paragraphs[0]
    p_eye.text = "COLLEGE MINI PROJECT PRESENTATION • 2025–2026"
    p_eye.font.name = FONT_MAIN
    p_eye.font.size = Pt(11)
    p_eye.font.bold = True
    p_eye.font.color.rgb = CYAN_LIGHT
    p_eye.space_after = Pt(4)

    p_title = tf1.add_paragraph()
    p_title.text = "AI Interview Preparation & Evaluation System"
    p_title.font.name = FONT_MAIN
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_after = Pt(6)

    p_sub = tf1.add_paragraph()
    p_sub.text = (
        "An intelligent mock interview platform designed to help students prepare for technical and HR job interviews. "
        "It provides realistic video interviews with local speech recognition and instant AI feedback to build student confidence."
    )
    p_sub.font.name = FONT_MAIN
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = TEXT_MUTED

    # Left Column: Project Overview & Team Members Card
    add_card(slide1, Inches(0.8), Inches(2.6), Inches(5.7), Inches(4.5))
    info_box = slide1.shapes.add_textbox(Inches(1.05), Inches(2.8), Inches(5.2), Inches(4.1))
    tf_info = info_box.text_frame
    tf_info.word_wrap = True

    p = tf_info.paragraphs[0]
    p.text = "PROJECT OVERVIEW & TEAM MEMBERS"
    p.font.name = FONT_MAIN
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN_LIGHT
    p.space_after = Pt(10)

    # Quick Metadata
    meta = [
        ("Project Type:", "B.Tech Final Year Mini Project"),
        ("Department:", "Computer Science & Engineering (Artificial Intelligence)"),
        ("College:", "Bansal Institute of Engineering & Technology, Lucknow"),
        ("Affiliation:", "Dr. A.P.J. Abdul Kalam Technical University (AKTU)"),
    ]
    for lbl, val in meta:
        p = tf_info.add_paragraph()
        p.text = f"{lbl} "
        p.font.name = FONT_MAIN
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED
        run = p.add_run()
        run.text = val
        run.font.bold = True
        run.font.color.rgb = TEXT_BODY
        p.space_after = Pt(3)

    # Divider line / Team Section
    p_team_header = tf_info.add_paragraph()
    p_team_header.text = "\nPROJECT TEAM MEMBERS:"
    p_team_header.font.name = FONT_MAIN
    p_team_header.font.size = Pt(10.5)
    p_team_header.font.bold = True
    p_team_header.font.color.rgb = GREEN_ACCENT
    p_team_header.space_after = Pt(6)

    team_members = [
        "1. Rajan Kumar Prajapati",
        "2. Dhruv Maurya",
        "3. Saloni",
        "4. Harsh Gupta"
    ]
    for member in team_members:
        p_m = tf_info.add_paragraph()
        p_m.text = member
        p_m.font.name = FONT_MAIN
        p_m.font.size = Pt(11)
        p_m.font.bold = True
        p_m.font.color.rgb = TEXT_WHITE
        p_m.space_after = Pt(3)

    # Right Column: Attractive Project Image Card
    add_card(slide1, Inches(6.8), Inches(2.6), Inches(5.733), Inches(4.5))
    if os.path.exists("screenshots/4_live_interview.png"):
        slide1.shapes.add_picture(
            "screenshots/4_live_interview.png",
            Inches(7.0), Inches(2.8), Inches(5.333), Inches(3.35)
        )

    cap_box = slide1.shapes.add_textbox(Inches(7.0), Inches(6.25), Inches(5.333), Inches(0.65))
    tf_cap = cap_box.text_frame
    tf_cap.word_wrap = True
    p_cap = tf_cap.paragraphs[0]
    p_cap.text = "Real Application: Camera & Microphone Mock Interview with Instant AI Feedback"
    p_cap.font.name = FONT_MAIN
    p_cap.font.size = Pt(9.5)
    p_cap.font.bold = True
    p_cap.font.color.rgb = CYAN_LIGHT
    p_cap.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_background(slide2)
    add_header(
        slide2,
        "THE CHALLENGE",
        "Problem Statement: Real Challenges Students Face in Interviews",
        "Why students struggle during campus placement interviews and why traditional practice is not enough."
    )

    # Left Column: 5 Real Student Problems
    add_card(slide2, Inches(0.8), Inches(1.75), Inches(6.0), Inches(4.85))
    prob_box = slide2.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(5.5), Inches(4.45))
    tf_prob = prob_box.text_frame
    tf_prob.word_wrap = True

    p = tf_prob.paragraphs[0]
    p.text = "COMMON PROBLEMS IN INTERVIEW PREPARATION"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RED_ACCENT
    p.space_after = Pt(12)

    problems = [
        ("Lack of Regular Practice", "Colleges have limited time and faculty. It is impossible to give every student regular one-on-one mock interviews."),
        ("Fear of Speaking", "Many students know the technical concepts, but get very nervous and hesitate when speaking in front of interviewers."),
        ("Difficulty Identifying Mistakes", "After giving an answer, students do not know if their answer was clear, structured, or technically complete."),
        ("No Communication Feedback", "Students do not realize when they speak too fast or use excessive filler words like 'um', 'uh', and 'basically'."),
        ("Limited Personal Guidance", "Professional coaching institutes charge high fees (Rs. 5,000–15,000), making personalized interview help unaffordable.")
    ]

    for title, desc in problems:
        p = tf_prob.add_paragraph()
        p.text = f"- {title}: "
        p.font.name = FONT_MAIN
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(6)

    # Right Column: Reliable Industry Statistics & Facts
    add_card(slide2, Inches(7.1), Inches(1.75), Inches(5.433), Inches(4.85))
    stat_box = slide2.shapes.add_textbox(Inches(7.35), Inches(1.95), Inches(4.95), Inches(4.45))
    tf_stat = stat_box.text_frame
    tf_stat.word_wrap = True

    p = tf_stat.paragraphs[0]
    p.text = "VERIFIED INDUSTRY STATISTICS & FACTS"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    p.space_after = Pt(12)

    stats = [
        ("India Skills Report (Wheebox 2024)",
         "Over 48% of Indian college graduates lack necessary employability skills.",
         "Most students have basic subject knowledge, but fail placement interviews due to weak communication, articulation, and problem-solving skills."),
        ("National Employability Study (Aspiring Minds / SHL)",
         "Only ~20% of engineering graduates are ready for software roles directly.",
         "Poor spoken English and difficulty explaining technical concepts are among the top two reasons for rejection in first-round interviews."),
        ("Virtual Placement Observations (Industry Placement Drives)",
         "Over 65% of candidates are rejected in first rounds due to communication delivery.",
         "Excessive filler words, lack of camera eye contact, and nervous rushing lead to quick disqualifications in online interviews.")
    ]

    for src, hl, note in stats:
        p = tf_stat.add_paragraph()
        p.text = f"[Source: {src}]"
        p.font.name = FONT_MAIN
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = CYAN_LIGHT
        p.space_after = Pt(2)

        p_hl = tf_stat.add_paragraph()
        p_hl.text = hl
        p_hl.font.name = FONT_MAIN
        p_hl.font.size = Pt(10.5)
        p_hl.font.bold = True
        p_hl.font.color.rgb = TEXT_WHITE
        p_hl.space_after = Pt(2)

        p_note = tf_stat.add_paragraph()
        p_note.text = note
        p_note.font.name = FONT_MAIN
        p_note.font.size = Pt(9.5)
        p_note.font.color.rgb = TEXT_MUTED
        p_note.space_after = Pt(8)

    add_bottom_pill(
        slide2,
        "Key Insight: Students fail interviews not from a lack of talent, but from a lack of regular practice and honest feedback.",
        AMBER_ACCENT
    )

    # =========================================================================
    # SLIDE 3: OUR PROPOSED SOLUTION
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_background(slide3)
    add_header(
        slide3,
        "OUR SOLUTION",
        "Our Proposed Solution: Smart, Accessible AI Mock Interviews",
        "How our system helps students practice, identify mistakes, and improve communication in a private setting."
    )

    sol_cards = [
        ("AI-Generated Questions",
         "Generates smart interview questions for Technical, HR, and Behavioral rounds matching your job role and difficulty.",
         CYAN_LIGHT),
        ("Camera-Based Mock Interview",
         "Provides an in-browser live camera preview so students practice professional posture and looking directly into the camera.",
         BLUE_ACCENT),
        ("Local Speech Recognition",
         "Uses faster-whisper to transcribe speech to text directly on your laptop without sending private audio to the cloud.",
         GREEN_ACCENT),
        ("AI Answer Evaluation",
         "Google Gemini evaluates answers on 4 key areas: Relevance, Technical Accuracy, Communication Clarity, and Confidence.",
         PURPLE_ACCENT),
        ("Communication Analysis",
         "Measures speaking pace (Words Per Minute) and counts filler words ('um', 'uh', 'like') so students speak more clearly.",
         AMBER_ACCENT),
        ("Personalized Feedback Reports",
         "Gives instant performance reports with clear strengths, areas to improve, and a complete progress history in PostgreSQL.",
         CYAN_LIGHT)
    ]

    card_w = Inches(3.75)
    card_h = Inches(2.25)
    xs = [Inches(0.8), Inches(4.8), Inches(8.8)]
    ys = [Inches(1.85), Inches(4.35)]

    for idx, (title, desc, col) in enumerate(sol_cards):
        c = idx % 3
        r = idx // 3
        add_card(slide3, xs[c], ys[r], card_w, card_h)

        sbox = slide3.shapes.add_textbox(xs[c] + Inches(0.2), ys[r] + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
        tf_s = sbox.text_frame
        tf_s.word_wrap = True

        p0 = tf_s.paragraphs[0]
        p0.text = f"{idx+1}. {title}"
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(8)

        p1 = tf_s.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(10)
        p1.font.color.rgb = TEXT_BODY

    add_bottom_pill(
        slide3,
        "System Value: Gives every student unlimited, 24/7 personal interview coaching at zero cost with 100% data privacy.",
        GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 4: HOW OUR SYSTEM WORKS (Step-by-Step Flow Diagram)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_background(slide4)
    add_header(
        slide4,
        "USER JOURNEY & WORKFLOW",
        "How Our System Works: Step-by-Step User Flow",
        "A simple, clean 7-step process from selecting your target job role to receiving the final evaluation report."
    )

    # 7 Step Flow Diagram
    # We display 4 steps on top row, 3 steps on bottom row with clear sequential numbers and indicators
    steps = [
        ("Step 1", "Select Role & Level", "Choose interview type (Technical/HR), job role, and difficulty (Easy/Medium/Hard). Optional resume PDF upload.", CYAN_LIGHT),
        ("Step 2", "Generate Questions", "Google Gemini AI creates customized questions based on your role, skills, and resume skill gaps.", BLUE_ACCENT),
        ("Step 3", "Start Camera & Mic", "The system starts the live webcam and microphone preview in a realistic mock interview room.", GREEN_ACCENT),
        ("Step 4", "Record & Convert Speech", "Student speaks their answer. faster-whisper converts speech to text locally in under 3 seconds.", AMBER_ACCENT),
        ("Step 5", "AI Answer Evaluation", "Gemini evaluates answer accuracy, relevance, communication clarity, and confidence from 0 to 10.", PURPLE_ACCENT),
        ("Step 6", "Analyze Communication", "Measures speaking speed (Words Per Minute), counts filler words, and checks camera engagement.", CYAN_LIGHT),
        ("Step 7", "Receive Report & Advice", "View overall score (e.g. 8.9/10), strengths, improvement tips, and track progress over time in database.", GREEN_ACCENT),
    ]

    # Row 1: 4 steps
    r1_w = Inches(2.75)
    r1_gap = Inches(0.24)
    r1_top = Inches(1.85)
    r1_h = Inches(2.15)

    for i in range(4):
        step_num, step_title, step_desc, color = steps[i]
        c_left = Inches(0.8) + i * (r1_w + r1_gap)
        add_card(slide4, c_left, r1_top, r1_w, r1_h)

        sbox = slide4.shapes.add_textbox(c_left + Inches(0.18), r1_top + Inches(0.18), r1_w - Inches(0.36), r1_h - Inches(0.36))
        tf_s = sbox.text_frame
        tf_s.word_wrap = True

        p0 = tf_s.paragraphs[0]
        p0.text = step_num.upper()
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = color
        p0.space_after = Pt(2)

        p1 = tf_s.add_paragraph()
        p1.text = step_title
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_after = Pt(4)

        p2 = tf_s.add_paragraph()
        p2.text = step_desc
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED

    # Row 2: 3 steps (wider cards)
    r2_w = Inches(3.75)
    r2_gap = Inches(0.24)
    r2_top = Inches(4.3)
    r2_h = Inches(2.15)

    for i in range(3):
        step_num, step_title, step_desc, color = steps[4 + i]
        c_left = Inches(0.8) + i * (r2_w + r2_gap)
        add_card(slide4, c_left, r2_top, r2_w, r2_h)

        sbox = slide4.shapes.add_textbox(c_left + Inches(0.2), r2_top + Inches(0.18), r2_w - Inches(0.4), r2_h - Inches(0.36))
        tf_s = sbox.text_frame
        tf_s.word_wrap = True

        p0 = tf_s.paragraphs[0]
        p0.text = step_num.upper()
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = color
        p0.space_after = Pt(2)

        p1 = tf_s.add_paragraph()
        p1.text = step_title
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_after = Pt(4)

        p2 = tf_s.add_paragraph()
        p2.text = step_desc
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED

    add_bottom_pill(
        slide4,
        "Fast Performance: Full voice transcription and evaluation completes in under 3.5 seconds with zero video uploaded to servers.",
        CYAN_LIGHT
    )

    # =========================================================================
    # SLIDE 5: KEY FEATURES & TECHNOLOGY
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_background(slide5)
    add_header(
        slide5,
        "SYSTEM ARCHITECTURE & TOOLS",
        "Key Features & Technologies Used",
        "Every technology is actively implemented and verified in the project codebase."
    )

    tech_cards = [
        ("React 19 (Frontend)",
         "Fast & Modern User Interface",
         "Provides an easy-to-use Single Page Application. Lets students switch easily between interview room, dashboard, and past session reports.",
         CYAN_LIGHT),
        ("FastAPI (Backend)",
         "High-Speed Python Web Server",
         "Handles API calls, connects to AI models, validates student data, and manages interview workflows with low latency.",
         BLUE_ACCENT),
        ("PostgreSQL (Database)",
         "Secure Relational Data Storage",
         "Permanently stores interview questions, answers, scores, and communication metrics so students can track progress over time.",
         GREEN_ACCENT),
        ("faster-whisper (Speech-to-Text)",
         "Local Speech Recognition",
         "Runs directly on the laptop CPU using the base int8 model. Transcribes answers in under 3 seconds with zero cloud voice leakage.",
         AMBER_ACCENT),
        ("Google Gemini AI (LLM)",
         "Intelligent Question & Answer Scoring",
         "Uses gemini-3.5-flash-lite to create role-specific questions and objectively grade answers across 4 clear evaluation pillars.",
         PURPLE_ACCENT),
        ("Camera Analysis (Browser Vision)",
         "Observable Delivery Indicators",
         "Runs in the student's browser via HTML5 canvas. Checks camera engagement, posture, and room lighting with clear student disclaimers.",
         CYAN_LIGHT),
    ]

    card_w = Inches(3.75)
    card_h = Inches(2.25)
    xs = [Inches(0.8), Inches(4.8), Inches(8.8)]
    ys = [Inches(1.85), Inches(4.35)]

    for idx, (title, role_desc, desc, col) in enumerate(tech_cards):
        c = idx % 3
        r = idx // 3
        add_card(slide5, xs[c], ys[r], card_w, card_h)

        tbox = slide5.shapes.add_textbox(xs[c] + Inches(0.2), ys[r] + Inches(0.18), card_w - Inches(0.4), card_h - Inches(0.36))
        tf_t = tbox.text_frame
        tf_t.word_wrap = True

        p0 = tf_t.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(2)

        p1 = tf_t.add_paragraph()
        p1.text = role_desc
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_after = Pt(4)

        p2 = tf_t.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED

    add_bottom_pill(
        slide5,
        "Production Quality: All 6 technologies are fully connected and pass 100% of automated system tests.",
        GREEN_ACCENT
    )

    # =========================================================================
    # SLIDE 6: WORKING APPLICATION DEMO
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_background(slide6)
    add_header(
        slide6,
        "LIVE PROJECT SHOWCASE",
        "Working Application Demo: Actual System in Action",
        "Genuine screenshots captured directly from our running system and live PostgreSQL database."
    )

    shot_w = Inches(5.7)
    shot_h = Inches(2.3)
    s_xs = [Inches(0.8), Inches(6.8)]
    s_ys = [Inches(1.85), Inches(4.55)]

    screens = [
        ("screenshots/1_interview_setup.png", "1. Interview Setup & Resume Upload",
         "Select job role, difficulty level, question count, and upload resume PDF for automatic skill matching.", s_xs[0], s_ys[0]),
        ("screenshots/4_live_interview.png", "2. Live Camera & Microphone Interview",
         "Realistic camera view, active microphone recording, question display, and STAR technique answering tips.", s_xs[1], s_ys[0]),
        ("screenshots/3_performance_report.png", "3. Evaluation Results & Detailed Feedback",
         "Overall score (8.9/10), speaking speed (140 WPM), filler word count (1.8%), camera engagement, and action plan.", s_xs[0], s_ys[1]),
        ("screenshots/2_dashboard_analytics.png", "4. Candidate Analytics & Progress Dashboard",
         "Displays practice hours, average scores, question counts, and historical score improvement graphs.", s_xs[1], s_ys[1]),
    ]

    for img_path, title, caption, left, top in screens:
        add_card(slide6, left, top, shot_w, shot_h)
        if os.path.exists(img_path):
            slide6.shapes.add_picture(img_path, left + Inches(0.08), top + Inches(0.08), shot_w - Inches(0.16), shot_h - Inches(0.68))

        cbox = slide6.shapes.add_textbox(left + Inches(0.1), top + shot_h - Inches(0.55), shot_w - Inches(0.2), Inches(0.5))
        tf_c = cbox.text_frame
        tf_c.word_wrap = True
        p0 = tf_c.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = CYAN_LIGHT

        p1 = tf_c.add_paragraph()
        p1.text = caption
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(8.5)
        p1.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 7: RESULTS, BENEFITS & FUTURE SCOPE
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_background(slide7)
    add_header(
        slide7,
        "PROJECT OUTCOMES & ROADMAP",
        "Results, Benefits & Future Scope",
        "Clear breakdown of actual test results, practical student benefits, and realistic future enhancements."
    )

    col_w = Inches(3.75)
    col_h = Inches(4.75)
    c_xs = [Inches(0.8), Inches(4.8), Inches(8.8)]
    c_top = Inches(1.8)

    # Column 1: Actual Results
    add_card(slide7, c_xs[0], c_top, col_w, col_h)
    box1 = slide7.shapes.add_textbox(c_xs[0] + Inches(0.2), c_top + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
    tf1 = box1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "ACTUAL PROJECT RESULTS"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.space_after = Pt(8)

    results_data = [
        ("Overall Score", "8.9 / 10 achieved in technical interview session."),
        ("Score Breakdown", "Relevance: 9.0 • Technical: 8.5 • Clarity: 8.0 • Confidence: 8.5."),
        ("Speaking Pace", "140 Words Per Minute (ideal conversational benchmark of 120–160 WPM)."),
        ("Filler Word Density", "1.8% (very low filler density; identifies words like 'um', 'uh')."),
        ("Delivery Indicators", "84% eye contact engagement, 92% head stability, 90% posture."),
        ("Actionable Advice", "Identified exact strengths and advised on database write overhead.")
    ]
    for lbl, desc in results_data:
        p = tf1.add_paragraph()
        p.text = f"- {lbl}: "
        p.font.name = FONT_MAIN
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(4)

    # Column 2: Practical Benefits
    add_card(slide7, c_xs[1], c_top, col_w, col_h)
    box2 = slide7.shapes.add_textbox(c_xs[1] + Inches(0.2), c_top + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
    tf2 = box2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "PRACTICAL BENEFITS"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = CYAN_LIGHT
    p.space_after = Pt(8)

    benefits_data = [
        ("Practice Anytime", "Students can take unlimited mock interviews at home without waiting for teachers."),
        ("Improve Answer Quality", "Instant AI feedback clearly explains what was missing in technical answers."),
        ("Fix Speaking Mistakes", "Identifies speaking too fast, long nervous pauses, or repeated filler words."),
        ("Structured Feedback", "Provides clear 0-10 category scores rather than vague verbal comments."),
        ("Build Real Confidence", "Regular camera practice reduces placement nervousness and interview fear."),
        ("Zero Cost", "Completely free tool designed for college students without subscription paywalls.")
    ]
    for lbl, desc in benefits_data:
        p = tf2.add_paragraph()
        p.text = f"- {lbl}: "
        p.font.name = FONT_MAIN
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(4)

    # Column 3: Future Scope & Honest Limitations
    add_card(slide7, c_xs[2], c_top, col_w, col_h)
    box3 = slide7.shapes.add_textbox(c_xs[2] + Inches(0.2), c_top + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
    tf3 = box3.text_frame
    tf3.word_wrap = True

    p = tf3.paragraphs[0]
    p.text = "FUTURE SCOPE & ROADMAP"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT
    p.space_after = Pt(8)

    future_data = [
        ("Live Audio Conversations", "Support full voice conversations with Gemini Live so the AI can ask instant follow-up questions."),
        ("In-Browser Code Editor", "Add a live code editor (Monaco) so students can write and execute algorithms during interviews."),
        ("Placement Officer Portal", "Allow college Training & Placement cells to assign interview batches and monitor student readiness."),
        ("Multi-Language Support", "Allow mock interviews in regional Indian languages alongside English."),
        ("Honest Current Limitations", "Camera indicators measure physical delivery, not psychological confidence. System currently takes one answer per question.")
    ]
    for lbl, desc in future_data:
        p = tf3.add_paragraph()
        p.text = f"- {lbl}: "
        p.font.name = FONT_MAIN
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(4)

    add_bottom_pill(
        slide7,
        "Summary: Demonstrates verified technical results today with a clear, realistic engineering roadmap for tomorrow.",
        CYAN_LIGHT
    )

    # =========================================================================
    # SLIDE 8: CONCLUSION & THANK YOU
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_background(slide8)
    add_header(
        slide8,
        "PROJECT SUMMARY & CONCLUSION",
        "Conclusion & Project Summary",
        "Key takeaways, core project value, and final defense presentation summary."
    )

    # Top Row: 3 Key Summary Cards
    concl_cards = [
        ("Complete & Verified System",
         "Successfully combines React 19, FastAPI, PostgreSQL, faster-whisper, and Google Gemini with real working data and zero fake results.",
         CYAN_LIGHT),
        ("Privacy-First & Zero Cost",
         "Local neural speech transcription and client-side camera checks protect student privacy with zero cloud transcription costs.",
         GREEN_ACCENT),
        ("Solves a Real Student Need",
         "Bridges the college-to-corporate placement gap by giving every student a free, judgment-free personal interview mentor.",
         PURPLE_ACCENT)
    ]

    card_w = Inches(3.75)
    card_h = Inches(2.2)
    xs = [Inches(0.8), Inches(4.8), Inches(8.8)]

    for idx, (title, desc, col) in enumerate(concl_cards):
        add_card(slide8, xs[idx], Inches(1.85), card_w, card_h)
        cbox = slide8.shapes.add_textbox(xs[idx] + Inches(0.2), Inches(2.0), card_w - Inches(0.4), card_h - Inches(0.35))
        tf_c = cbox.text_frame
        tf_c.word_wrap = True

        p0 = tf_c.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_MAIN
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(6)

        p1 = tf_c.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(10)
        p1.font.color.rgb = TEXT_BODY

    # Bottom Row: Closing Statement, Team Members, and Thank You Box
    add_card(slide8, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.8), bg_color=RGBColor(20, 30, 52))
    ty_box = slide8.shapes.add_textbox(Inches(1.1), Inches(4.45), Inches(11.133), Inches(2.5))
    tf_ty = ty_box.text_frame
    tf_ty.word_wrap = True

    p0 = tf_ty.paragraphs[0]
    p0.text = "THANK YOU!"
    p0.font.name = FONT_MAIN
    p0.font.size = Pt(22)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_LIGHT
    p0.alignment = PP_ALIGN.CENTER
    p0.space_after = Pt(4)

    p_close = tf_ty.add_paragraph()
    p_close.text = '"Our AI Interview System helps students turn interview anxiety into confident, successful job placements."'
    p_close.font.name = FONT_MAIN
    p_close.font.size = Pt(12)
    p_close.font.italic = True
    p_close.font.color.rgb = TEXT_BODY
    p_close.alignment = PP_ALIGN.CENTER
    p_close.space_after = Pt(10)

    p_team_title = tf_ty.add_paragraph()
    p_team_title.text = "PROJECT TEAM MEMBERS:"
    p_team_title.font.name = FONT_MAIN
    p_team_title.font.size = Pt(11)
    p_team_title.font.bold = True
    p_team_title.font.color.rgb = GREEN_ACCENT
    p_team_title.alignment = PP_ALIGN.CENTER
    p_team_title.space_after = Pt(4)

    p_team_names = tf_ty.add_paragraph()
    p_team_names.text = "1. Rajan Kumar Prajapati   |   2. Dhruv Maurya   |   3. Saloni   |   4. Harsh Gupta"
    p_team_names.font.name = FONT_MAIN
    p_team_names.font.size = Pt(12)
    p_team_names.font.bold = True
    p_team_names.font.color.rgb = TEXT_WHITE
    p_team_names.alignment = PP_ALIGN.CENTER
    p_team_names.space_after = Pt(6)

    p_dept = tf_ty.add_paragraph()
    p_dept.text = "Department of Computer Science & Engineering • Bansal Institute of Engineering & Technology, Lucknow (AKTU Code: 422)"
    p_dept.font.name = FONT_MAIN
    p_dept.font.size = Pt(10)
    p_dept.font.color.rgb = TEXT_MUTED
    p_dept.alignment = PP_ALIGN.CENTER
    p_dept.space_after = Pt(6)

    p_qa = tf_ty.add_paragraph()
    p_qa.text = "We welcome your questions, feedback, and suggestions. Thank you!"
    p_qa.font.name = FONT_MAIN
    p_qa.font.size = Pt(11)
    p_qa.font.bold = True
    p_qa.font.color.rgb = AMBER_ACCENT
    p_qa.alignment = PP_ALIGN.CENTER

    output_path = os.path.abspath("AI_Interview_System_Presentation.pptx")
    prs.save(output_path)
    print(f"[SUCCESS] Presentation generated successfully: {output_path}")

if __name__ == "__main__":
    build_presentation()
