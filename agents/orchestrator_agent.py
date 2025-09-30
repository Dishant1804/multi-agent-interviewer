"""
OrchestratorAgent - Coordinates all agents and manages the interview flow.
"""

from typing import Dict, Any, List
from .models import InterviewContext
from .interviewer_agent import InterviewerAgent
from .topic_manager_agent import TopicManagerAgent
from .evaluator_agent import EvaluatorAgent


class OrchestratorAgent:
    """Coordinates all agents and manages the interview flow."""
    
    def __init__(self):
        self.interviewer = InterviewerAgent()
        self.topic_manager = TopicManagerAgent()
        self.evaluator = EvaluatorAgent()
        self.context = None
    
    def initialize_interview(self, resume_path: str, job_description_path: str) -> InterviewContext:
        """Initialize the interview with resume and job description."""
        try:
            with open(resume_path, 'r') as f:
                resume_content = f.read()
            
            with open(job_description_path, 'r') as f:
                job_description = f.read()
            
            self.context = InterviewContext(
                resume_content=resume_content,
                job_description=job_description,
                current_topic="Technical Skills",
                interview_depth=2,
                previous_questions=[],
                candidate_responses=[],
                evaluation_scores=[],
                per_turn_evaluations=[]
            )
            
            return self.context
        except Exception as e:
            print(f"Error initializing interview: {e}")
            return None
    
    def conduct_interview_round(self) -> Dict[str, Any]:
        """Conduct one round of the interview."""
        if not self.context:
            return {"error": "Interview not initialized"}
        
        questions = self.interviewer.generate_questions(self.context)
        if isinstance(questions, list):
            questions = questions[:1]
        
        self.context.previous_questions.extend(questions)
        
        return {
            "questions": questions,
            "current_topic": self.context.current_topic,
            "depth": self.context.interview_depth
        }
    
    def process_response(self, response: str) -> Dict[str, Any]:
        """Process candidate response and evaluate."""
        if not self.context or not self.context.previous_questions:
            return {"error": "No questions to evaluate"}
        
        last_question = self.context.previous_questions[-1]
        
        evaluation = self.evaluator.evaluate_response(
            last_question, response, self.context
        )
        
        self.context.candidate_responses.append(response)
        self.context.evaluation_scores.append(evaluation["score"])
        detailed_eval = {
            "question": last_question,
            "response": response,
            "topic": self.context.current_topic,
            "score": evaluation.get("score"),
            "feedback": evaluation.get("feedback"),
            "strengths": evaluation.get("strengths", []),
            "improvements": evaluation.get("improvements", [])
        }
        self.context.per_turn_evaluations.append(detailed_eval)
        
        next_topic, next_depth = self.topic_manager.determine_next_topic(self.context)
        self.context.current_topic = next_topic
        self.context.interview_depth = next_depth
        
        return {
            "evaluation": evaluation,
            "next_topic": next_topic,
            "next_depth": next_depth,
            "overall_progress": len(self.context.previous_questions)
        }
    
    def get_interview_summary(self) -> Dict[str, Any]:
        """Get a summary of the interview so far."""
        if not self.context:
            return {"error": "No interview data available"}
        
        avg_score = sum(self.context.evaluation_scores) / len(self.context.evaluation_scores) if self.context.evaluation_scores else 0
        
        return {
            "total_questions": len(self.context.previous_questions),
            "average_score": round(avg_score, 2),
            "topics_covered": list(set([q.split(':')[0] for q in self.context.previous_questions if ':' in q])),
            "current_topic": self.context.current_topic,
            "interview_depth": self.context.interview_depth
        }

    def get_final_report(self) -> Dict[str, Any]:
        """Generate a detailed end-of-interview report with strengths and gaps."""
        if not self.context:
            return {"error": "No interview data available"}
        per_turn_evaluations = self.context.per_turn_evaluations or []
        all_scores = [turn_eval.get("score", 0) for turn_eval in per_turn_evaluations]
        average_score_overall = sum(all_scores) / len(all_scores) if all_scores else 0.0
        topic_to_details: Dict[str, Dict[str, Any]] = {}
        strength_to_count: Dict[str, int] = {}
        improvement_to_count: Dict[str, int] = {}

        for turn_eval in per_turn_evaluations:
            topic_name = turn_eval.get("topic", "Unknown")
            topic_details = topic_to_details.setdefault(topic_name, {"scores": [], "improvements": [], "strengths": []})
            topic_details["scores"].append(turn_eval.get("score", 0))
            for improvement_item in turn_eval.get("improvements", []) or []:
                normalized_improvement = improvement_item.strip()
                if normalized_improvement:
                    topic_details["improvements"].append(normalized_improvement)
                    improvement_to_count[normalized_improvement] = improvement_to_count.get(normalized_improvement, 0) + 1
            for strength_item in turn_eval.get("strengths", []) or []:
                normalized_strength = strength_item.strip()
                if normalized_strength:
                    topic_details["strengths"].append(normalized_strength)
                    strength_to_count[normalized_strength] = strength_to_count.get(normalized_strength, 0) + 1
        
        topic_to_average_score = {
            topic_name: round((sum(details["scores"]) / len(details["scores"]) if details["scores"] else 0.0), 2)
            for topic_name, details in topic_to_details.items()
        }

        weakest_topics_by_score = sorted(topic_to_average_score.items(), key=lambda item: item[1])[:3]
        top_improvement_themes = sorted(improvement_to_count.items(), key=lambda item: item[1], reverse=True)[:5]
        top_strength_themes = sorted(strength_to_count.items(), key=lambda item: item[1], reverse=True)[:5]
        recommendations: List[str] = []

        for topic_name, _ in weakest_topics_by_score:
            recommendations.append(f"Allocate more practice on {topic_name} with depth-aligned exercises and mock questions.")
        for improvement_item, _ in top_improvement_themes:
            recommendations.append(f"Address gap: {improvement_item}. Prepare concise explanations and hands-on examples.")
       
        return {
            "overall": {
                "average_score": round(average_score_overall, 2),
                "total_questions": len(self.context.previous_questions),
            },
            "by_topic": {
                "scores": topic_to_average_score,
                "weakest_topics": weakest_topics_by_score,
            },
            "strengths_summary": top_strength_themes,
            "improvement_summary": top_improvement_themes,
            "recommendations": recommendations,
            "evaluations": per_turn_evaluations,
        }
