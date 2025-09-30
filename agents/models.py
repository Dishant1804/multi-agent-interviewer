"""
Shared models and data structures for the interview system.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class InterviewContext:
    """Context information for the interview session."""
    resume_content: str
    job_description: str
    current_topic: str
    interview_depth: int
    previous_questions: List[str]
    candidate_responses: List[str]
    evaluation_scores: List[float]
    per_turn_evaluations: List[Dict[str, Any]]
