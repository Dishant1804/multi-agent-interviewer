"""
InterviewerAgent - Generates contextual questions based on resume, job description, and current topic.
"""

from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import OPENAI_MODEL, INTERVIEWER_TEMPERATURE
from .models import InterviewContext


class InterviewerAgent:
    """Generates contextual questions based on resume, job description, and current topic."""
    
    def __init__(self, model_name: str = None):
        model_name = model_name or OPENAI_MODEL
        self.llm = ChatOpenAI(model=model_name, temperature=INTERVIEWER_TEMPERATURE)
        self.question_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert technical interviewer. Generate relevant, challenging questions 
            based on the candidate's resume, job description, and current interview topic.
            
            Guidelines:
            - Ask questions that test both technical knowledge and practical experience
            - Vary question difficulty based on the candidate's experience level
            - Include behavioral questions that relate to the technical role
            - Avoid asking questions that have already been asked
            - Make questions specific to the job requirements
            
            Current topic: {topic}
            Interview depth: {depth} (1=basic, 2=intermediate, 3=advanced)
            """),
            ("human", """Resume: {resume}
            
            Job Description: {job_description}
            
            Previous questions asked: {previous_questions}
            
            Generate exactly 1 focused question for this candidate. Make it challenging but fair.
            Respond with a single question only."""),
        ])
    
    def generate_questions(self, context: InterviewContext) -> List[str]:
        """Generate contextual questions for the candidate."""
        try:
            chain = self.question_prompt | self.llm
            response = chain.invoke({
                "resume": context.resume_content,
                "job_description": context.job_description,
                "topic": context.current_topic,
                "depth": context.interview_depth,
                "previous_questions": context.previous_questions
            })
            
            questions = self._parse_questions(response.content)
            return questions
        except Exception as e:
            print(f"Error generating questions: {e}")
            return ["Could you tell me about your experience with Python development?"]
    
    def _parse_questions(self, content: str) -> List[str]:
        """Parse questions from LLM response."""
        questions = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and ('?' in line or line.startswith(('1.', '2.', '3.', '4.', '5.'))):
                question = line
                if question.startswith(('1.', '2.', '3.', '4.', '5.')):
                    question = question[3:].strip()
                if question:
                    questions.append(question)
        
        return questions if questions else ["Tell me about your experience with the technologies mentioned in the job description."]
