from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    interview_type = Column(String(50), nullable=False)
    question_count = Column(Integer, nullable=False)
    overall_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship(
        "InterviewQuestion",
        back_populates="interview",
        cascade="all, delete-orphan"
    )
    communication_metrics = relationship(
        "CommunicationMetric",
        back_populates="interview",
        cascade="all, delete-orphan"
    )
    resumes = relationship(
        "ResumeRecord",
        back_populates="interview"
    )
    job_descriptions = relationship(
        "JobDescriptionRecord",
        back_populates="interview"
    )


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(
        Integer,
        ForeignKey("interviews.id", ondelete="CASCADE"),
        nullable=False
    )

    question_number = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)

    relevance = Column(Float, nullable=True)
    technical_accuracy = Column(Float, nullable=True)
    communication = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)

    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    improvement_feedback = Column(Text, nullable=True)

    interview = relationship(
        "Interview",
        back_populates="questions"
    )
    communication_metrics = relationship(
        "CommunicationMetric",
        back_populates="question"
    )


class CommunicationMetric(Base):
    __tablename__ = "communication_metrics"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(
        Integer,
        ForeignKey("interviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    interview_question_id = Column(
        Integer,
        ForeignKey("interview_questions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    speaking_pace_wpm = Column(Float, nullable=True)
    filler_word_count = Column(Integer, nullable=True)
    filler_word_rate = Column(Float, nullable=True)
    audio_duration_seconds = Column(Float, nullable=True)
    pause_count = Column(Integer, nullable=True)
    pause_duration_seconds = Column(Float, nullable=True)
    face_present = Column(Boolean, nullable=True)
    camera_gaze_metric = Column(Float, nullable=True)
    posture_metric = Column(Float, nullable=True)
    measurement_source = Column(String(40), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    interview = relationship(
        "Interview",
        back_populates="communication_metrics"
    )
    question = relationship(
        "InterviewQuestion",
        back_populates="communication_metrics"
    )


class ResumeRecord(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(
        Integer,
        ForeignKey("interviews.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    original_filename = Column(String(255), nullable=False)
    extracted_text = Column(Text, nullable=True)
    extracted_skills = Column(Text, nullable=True)  # JSON-encoded string for broad compatibility
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    interview = relationship(
        "Interview",
        back_populates="resumes"
    )


class JobDescriptionRecord(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(
        Integer,
        ForeignKey("interviews.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    title = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    description_text = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=True)  # JSON-encoded string for broad compatibility
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    interview = relationship(
        "Interview",
        back_populates="job_descriptions"
    )


Index("ix_communication_metrics_interview_created", CommunicationMetric.interview_id, CommunicationMetric.created_at)
