"""Additive SQLAlchemy models for Phase 9/10.

Re-exports unified models from models.py for backward compatibility.
"""
from models import (
    CommunicationMetric,
    ResumeRecord,
    JobDescriptionRecord,
)

__all__ = [
    "CommunicationMetric",
    "ResumeRecord",
    "JobDescriptionRecord",
]
