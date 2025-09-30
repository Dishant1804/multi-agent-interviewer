"""
Multi-Agent Interview System
Main entry point for the interview system.
"""

import os
from interview_system import InterviewSession


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("MULTI-AGENT INTERVIEW SYSTEM")
    print("=" * 60)
    print("Welcome to the AI-powered mock interview system!")
    print("This system uses 4 specialized agents to conduct interviews:")
    print("- InterviewerAgent: Generates contextual questions")
    print("- TopicManagerAgent: Controls topic flow and depth")
    print("- EvaluatorAgent: Evaluates responses in real-time")
    print("- OrchestratorAgent: Coordinates all agents")
    print("=" * 60)


def print_help():
    """Print help information."""
    print("\nAVAILABLE COMMANDS:")
    print("- start - Start a new interview")
    print("- answer <response> - Answer the current question")
    print("- status - Check interview status")
    print("- end - End the current interview")
    print("- help - Show this help message")
    print("- quit - Exit the program")


def format_evaluation(evaluation):
    """Format evaluation output for display."""
    print(f"\nEVALUATION:")
    print(f"Score: {evaluation.get('score', 'N/A')}/10")
    print(f"Feedback: {evaluation.get('feedback', 'No feedback available')}")
    strengths = evaluation.get('strengths')
    if strengths:
        print(f"Strengths: {', '.join(strengths)}")
    improvements = evaluation.get('improvements')
    if improvements:
        print(f"Improvements: {', '.join(improvements)}")


def format_questions(questions):
    """Format questions for display."""
    print(f"\nQUESTIONS:")
    for i, question in enumerate(questions, 1):
        print(f"{i}. {question}")


def format_final_report(report):
    """Pretty print the end-of-interview report."""
    if not report or 'error' in report:
        print("\nNo final report available.")
        return
    overall = report.get('overall', {})
    by_topic = report.get('by_topic', {})
    print("\nFINAL REPORT:")
    print(f"Overall Average Score: {overall.get('average_score', 'N/A')}/10")
    print(f"Total Questions: {overall.get('total_questions', 0)}")
    scores = by_topic.get('scores', {})
    if scores:
        print("\nScores by Topic:")
        for t, s in scores.items():
            print(f" - {t}: {s}/10")
    weakest = by_topic.get('weakest_topics', [])
    if weakest:
        print("\nWeakest Topics:")
        for t, s in weakest:
            print(f" - {t}: {s}/10")
    strengths = report.get('strengths_summary', [])
    if strengths:
        print("\nTop Strengths:")
        for item, count in strengths:
            print(f" - {item} (x{count})")
    improvements = report.get('improvement_summary', [])
    if improvements:
        print("\nTop Improvement Areas:")
        for item, count in improvements:
            print(f" - {item} (x{count})")
    recs = report.get('recommendations', [])
    if recs:
        print("\nRecommendations:")
        for r in recs:
            print(f" - {r}")


def main():
    """Main function to run the interview system."""
    print_banner()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\nWARNING: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key to use the interview system.")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    session = InterviewSession()
    
    print_help()
    print("\nReady to start! Type 'start' to begin an interview.")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "quit" or command == "exit":
                print("Goodbye!")
                break
            
            elif command == "help":
                print_help()
            
            elif command == "start":
                print("\nStarting new interview...")
                result = session.start_new_interview(
                    "sample_resume.txt", 
                    "sample_job_description.txt"
                )
                
                if "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Interview started!")
                    print(f"Topic: {result['current_topic']}")
                    print(f"Depth: {result['depth']}")
                    print(f"Round: {result['round']}/{result['max_rounds']}")
                    format_questions(result['questions'])
            
            elif command.startswith("answer "):
                if not session.is_active():
                    print("No active interview. Start an interview first.")
                    continue
                
                response = command[7:].strip()
                if not response:
                    print("Please provide a response.")
                    continue
                
                print(f"\nProcessing your response...")
                result = session.answer_question(response)
                
                if "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    format_evaluation(result['evaluation'])
                    
                    if result['status'] == "interview_completed":
                        print(f"\nInterview completed!")
                        print(f"Final Summary: {result['final_summary']}")
                        format_final_report(result.get('final_report'))
                        session = InterviewSession()
                    else:
                        print(f"\nNext Topic: {result['next_topic']}")
                        print(f"Next Depth: {result['next_depth']}")
                        print(f"Round: {result['round']}")
                        format_questions(result['next_questions'])
            
            elif command == "status":
                result = session.get_status()
                if result['status'] == "no_active_interview":
                    print("No active interview session.")
                else:
                    print(f"Interview Status:")
                    print(f"   Round: {result['round']}/{result['max_rounds']}")
                    print(f"   Summary: {result['summary']}")
            
            elif command == "end":
                if not session.is_active():
                    print("No active interview to end.")
                    continue
                
                result = session.end_interview()
                print(f"Interview ended!")
                print(f"Final Summary: {result['final_summary']}")
                format_final_report(result.get('final_report'))
                session = InterviewSession()
            
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
