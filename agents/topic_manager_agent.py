"""
TopicManagerAgent - Controls topic flow and depth throughout the interview.
"""

from typing import Tuple
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import OPENAI_MODEL, TOPIC_MANAGER_TEMPERATURE
from .models import InterviewContext


class TopicManagerAgent:
    """Controls topic flow and depth throughout the interview."""
    
    def __init__(self, model_name: str = None):
        model_name = model_name or OPENAI_MODEL
        self.llm = ChatOpenAI(model=model_name, temperature=TOPIC_MANAGER_TEMPERATURE)
        self.topic_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a topic manager for technical interviews. Your job is to:
            1. Determine the next topic to focus on
            2. Adjust interview depth based on candidate performance
            3. Ensure comprehensive coverage of job requirements
            
            Available topics: Technical Skills, Problem Solving, System Design, 
            Leadership/Management, Behavioral, Company Culture Fit
            
            Depth levels: 1=Basic, 2=Intermediate, 3=Advanced
            """),
            ("human", """Current topic: {current_topic}
            Current depth: {current_depth}
            Job requirements: {job_description}
            Candidate responses so far: {responses}
            Evaluation scores: {scores}
            
            Determine the next topic and appropriate depth level. Consider:
            - What areas haven't been covered yet?
            - How is the candidate performing?
            - What's most important for this role?
            
            Respond with: TOPIC: [topic name] | DEPTH: [1-3]"""),
        ])
    
    def determine_next_topic(self, context: InterviewContext) -> Tuple[str, int]:
        """Determine the next topic and depth level."""
        try:
            chain = self.topic_prompt | self.llm
            response = chain.invoke({
                "current_topic": context.current_topic,
                "current_depth": context.interview_depth,
                "job_description": context.job_description,
                "responses": context.candidate_responses[-3:] if context.candidate_responses else [],
                "scores": context.evaluation_scores[-3:] if context.evaluation_scores else []
            })

            content = response.content
            topic = "Technical Skills"
            depth = 2
            
            if "TOPIC:" in content:
                topic_part = content.split("TOPIC:")[1].split("|")[0].strip()
                if topic_part:
                    topic = topic_part
            
            if "DEPTH:" in content:
                depth_part = content.split("DEPTH:")[1].strip()
                try:
                    depth = int(depth_part)
                except:
                    depth = 2
            
            return topic, depth
        except Exception as e:
            print(f"Error determining topic: {e}")
            return "Technical Skills", 2
