"""
Configuration settings for the Multi-Agent Interview System.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Interview Configuration
MAX_INTERVIEW_ROUNDS = int(os.getenv("MAX_INTERVIEW_ROUNDS", "5"))
DEFAULT_INTERVIEW_DEPTH = int(os.getenv("DEFAULT_INTERVIEW_DEPTH", "2"))

# File Paths
SAMPLE_RESUME_PATH = "sample_resume.txt"
SAMPLE_JOB_DESCRIPTION_PATH = "sample_job_description.txt"

INTERVIEWER_TEMPERATURE = float(os.getenv("INTERVIEWER_TEMPERATURE", "0.7"))
TOPIC_MANAGER_TEMPERATURE = float(os.getenv("TOPIC_MANAGER_TEMPERATURE", "0.3"))
EVALUATOR_TEMPERATURE = float(os.getenv("EVALUATOR_TEMPERATURE", "0.2"))

# Available Interview Topics
INTERVIEW_TOPICS = [
    "Technical Skills",
    "Problem Solving", 
    "System Design",
    "Leadership/Management",
    "Behavioral",
    "Company Culture Fit"
]

# Depth Levels
DEPTH_LEVELS = {
    1: "Basic",
    2: "Intermediate", 
    3: "Advanced"
}
