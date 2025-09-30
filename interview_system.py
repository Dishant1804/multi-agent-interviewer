"""
Multi-Agent Interview System
Main system that implements the router/orchestrator pattern from the architecture diagram.
"""

import os
from typing import Dict, Any
from agents import OrchestratorAgent


class InterviewSystem:
    """
    Main interview system that acts as the router/orchestrator.
    Coordinates all agents and manages the interview flow.
    """
    
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.is_interview_active = False
        self.current_round = 0
        self.max_rounds = 5
    
    def start_interview(self, resume_path: str, job_description_path: str) -> Dict[str, Any]:
        """
        Initialize and start a new interview session.
        This is the entry point that receives 'query' and 'user' inputs.
        """
        try:
            if not os.path.exists(resume_path):
                return {"error": f"Resume file not found: {resume_path}"}
            
            if not os.path.exists(job_description_path):
                return {"error": f"Job description file not found: {job_description_path}"}
            
            context = self.orchestrator.initialize_interview(resume_path, job_description_path)
            
            if not context:
                return {"error": "Failed to initialize interview"}
            
            self.is_interview_active = True
            self.current_round = 0
            
            interview_round = self.orchestrator.conduct_interview_round()
            
            return {
                "status": "interview_started",
                "message": "Interview session initialized successfully",
                "questions": interview_round.get("questions", []),
                "current_topic": interview_round.get("current_topic", "Technical Skills"),
                "depth": interview_round.get("depth", 2),
                "round": self.current_round + 1,
                "max_rounds": self.max_rounds
            }
            
        except Exception as e:
            return {"error": f"Failed to start interview: {str(e)}"}
    
    def process_candidate_response(self, response: str) -> Dict[str, Any]:
        """
        Process candidate's response and generate next questions.
        This implements the router functionality that coordinates all agents.
        """
        if not self.is_interview_active:
            return {"error": "No active interview session"}
        
        if not response.strip():
            return {"error": "Empty response provided"}
        
        try:
            result = self.orchestrator.process_response(response)
            
            if "error" in result:
                return result
            
            self.current_round += 1
            
            if self.current_round >= self.max_rounds:
                return self._end_interview(result)
            
            next_round = self.orchestrator.conduct_interview_round()
            
            return {
                "status": "response_processed",
                "evaluation": result["evaluation"],
                "next_questions": next_round.get("questions", []),
                "next_topic": result["next_topic"],
                "next_depth": result["next_depth"],
                "round": self.current_round + 1,
                "progress": result["overall_progress"]
            }
            
        except Exception as e:
            return {"error": f"Failed to process response: {str(e)}"}
    
    def get_interview_status(self) -> Dict[str, Any]:
        """Get current status of the interview."""
        if not self.is_interview_active:
            return {"status": "no_active_interview"}
        
        summary = self.orchestrator.get_interview_summary()
        
        return {
            "status": "interview_active",
            "round": self.current_round,
            "max_rounds": self.max_rounds,
            "summary": summary
        }
    
    def end_interview(self) -> Dict[str, Any]:
        """Manually end the interview and provide final summary."""
        if not self.is_interview_active:
            return {"error": "No active interview to end"}
        
        self.is_interview_active = False
        summary = self.orchestrator.get_interview_summary()
        report = self.orchestrator.get_final_report()
        
        return {
            "status": "interview_ended",
            "final_summary": summary,
            "final_report": report,
            "total_rounds": self.current_round
        }
    
    def _end_interview(self, last_result: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to end interview after max rounds."""
        self.is_interview_active = False
        summary = self.orchestrator.get_interview_summary()
        report = self.orchestrator.get_final_report()
        
        return {
            "status": "interview_completed",
            "message": f"Interview completed after {self.max_rounds} rounds",
            "final_evaluation": last_result["evaluation"],
            "final_summary": summary,
            "final_report": report,
            "total_rounds": self.current_round
        }
    
    def reset_interview(self):
        """Reset the interview system for a new session."""
        self.is_interview_active = False
        self.current_round = 0
        self.orchestrator = OrchestratorAgent()


class InterviewSession:
    """
    Wrapper class for managing interview sessions.
    Provides a clean interface for the interview system.
    """
    
    def __init__(self):
        self.system = InterviewSystem()
    
    def start_new_interview(self, resume_path: str, job_description_path: str) -> Dict[str, Any]:
        """Start a new interview session."""
        return self.system.start_interview(resume_path, job_description_path)
    
    def answer_question(self, response: str) -> Dict[str, Any]:
        """Submit an answer to the current question."""
        return self.system.process_candidate_response(response)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current interview status."""
        return self.system.get_interview_status()
    
    def end_interview(self) -> Dict[str, Any]:
        """End the current interview."""
        return self.system.end_interview()
    
    def is_active(self) -> bool:
        """Check if there's an active interview session."""
        return self.system.is_interview_active
