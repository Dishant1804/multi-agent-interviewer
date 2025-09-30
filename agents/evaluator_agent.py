"""
EvaluatorAgent - Evaluates candidate responses in real-time.
"""

from typing import Dict, Any
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import OPENAI_MODEL, EVALUATOR_TEMPERATURE
from .models import InterviewContext


class EvaluatorAgent:
    """Evaluates candidate responses in real-time."""
    
    def __init__(self, model_name: str = None):
        model_name = model_name or OPENAI_MODEL
        self.llm = ChatOpenAI(model=model_name, temperature=EVALUATOR_TEMPERATURE)
        self.evaluation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert technical interviewer evaluating candidate responses.
            Provide detailed feedback and scoring based on:
            1. Technical accuracy and depth
            2. Problem-solving approach
            3. Communication clarity
            4. Relevance to job requirements
            5. Practical experience demonstrated
            
            Score on a scale of 1-10 (10 being excellent).
            Output MUST be a structured bullet list with clearly labeled sections:
            - SCORE: <number>
            - FEEDBACK: <detailed feedback paragraph(s)>
            - STRENGTHS: <comma-separated short phrases>
            - IMPROVEMENTS: <comma-separated short phrases>
            - FOLLOW_UPS: <1-3 short follow-up question suggestions>
            """),
            ("human", """Question asked: {question}
            Candidate response: {response}
            Job requirements: {job_description}
            Current topic: {topic}
            
            Evaluate this response and provide:
            1. A score (1-10)
            2. Detailed feedback
            3. Areas of strength
            4. Areas for improvement
            5. Follow-up question suggestions"""),
        ])
    
    def evaluate_response(self, question: str, response: str, context: InterviewContext) -> Dict[str, Any]:
        """Evaluate a candidate's response."""
        try:
            chain = self.evaluation_prompt | self.llm
            evaluation = chain.invoke({
                "question": question,
                "response": response,
                "job_description": context.job_description,
                "topic": context.current_topic
            })
            
            content = evaluation.content
            score = self._extract_score(content)
            strengths = self._extract_list_section(content, label="strengths")
            improvements = self._extract_list_section(content, label="improvements")
            follow_ups = self._extract_list_section(content, label="follow_ups")
            feedback = self._extract_feedback_section(content)
            
            return {
                "score": score,
                "feedback": feedback,
                "strengths": strengths,
                "improvements": improvements,
                "follow_ups": follow_ups,
                "question": question,
                "response": response
            }
        except Exception as e:
            print(f"Error evaluating response: {e}")
            return {
                "score": 5,
                "feedback": "Unable to evaluate response properly.",
                "strengths": [],
                "improvements": [],
                "follow_ups": [],
                "question": question,
                "response": response
            }
    
    def _extract_score(self, content: str) -> float:
        """Extract numerical score from evaluation content."""
        score_match = re.search(r'(\d+(?:\.\d+)?)/10|score[:\s]*(\d+(?:\.\d+)?)', content.lower())
        if score_match:
            return float(score_match.group(1) or score_match.group(2))
        return 5.0

    def _extract_list_section(self, content: str, label: str) -> Any:
        """Extract comma-separated list after a given label."""
        try:
            pattern = rf"{label}\s*[:|-]\s*(.*)"
            lines = content.splitlines()
            items = []
            for line in lines:
                lower = line.strip().lower()
                if lower.startswith(label + ":") or lower.startswith(label + "-") or lower.startswith(label):
                    after = line.split(":", 1)[-1] if ":" in line else line.split("-", 1)[-1]
                    parts = [p.strip().strip("•- ") for p in after.split(",") if p.strip()]
                    items.extend(parts)
            collecting = False
            for line in lines:
                if collecting:
                    if not line.strip():
                        break
                    if line.strip().startswith(("-", "•", "*")):
                        items.append(line.strip().lstrip("-•* "))
                    else:
                        break
                if line.strip().lower().startswith(label + ":"):
                    collecting = True
            return [i for i in items if i]
        except Exception:
            return []

    def _extract_feedback_section(self, content: str) -> str:
        """Extract feedback section if present, else return full content."""
        lines = content.splitlines()
        feedback_lines = []
        in_feedback = False
        for line in lines:
            lower = line.strip().lower()
            if lower.startswith("feedback:"):
                in_feedback = True
                feedback_lines.append(line.split(":", 1)[-1].strip())
                continue
            if in_feedback:
                if any(lower.startswith(h + ":") for h in ["strengths", "improvements", "follow_ups", "score", "recommendations", "next steps"]):
                    break
                feedback_lines.append(line)
        if feedback_lines:
            return "\n".join([l for l in feedback_lines if l is not None])
        return content
