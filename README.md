# Multi-Agent Interview System

A sophisticated AI-powered mock interview system that uses 4 specialized agents to conduct realistic technical interviews. The system follows a router/orchestrator architecture pattern where agents work together to provide comprehensive interview experiences.

## System Architecture

<img width="740" height="452" alt="Screenshot from 2025-09-30 11-23-46" src="https://github.com/user-attachments/assets/343964ad-d238-439b-bbbb-9252301b9197" />

https://github.com/user-attachments/assets/127995b5-726e-4579-b4a5-173ca705ee5d


### Core Agents

1. **InterviewerAgent**: Generates contextual questions based on resume, job description, and current topic
2. **TopicManagerAgent**: Controls topic flow and interview depth throughout the session
3. **EvaluatorAgent**: Evaluates candidate responses in real-time with detailed feedback
4. **OrchestratorAgent**: Coordinates all agents and manages the overall interview flow

### System Flow

```
Query + User Input -> Router/Orchestrator -> Specialized Agents
                                    |
                            InterviewerAgent (Questions)
                            TopicManagerAgent (Topic Control)  
                            EvaluatorAgent (Evaluation)
```

## Features

- **Contextual Question Generation**: Questions are tailored to the candidate's resume and job requirements
- **Dynamic Topic Management**: System adapts interview topics and depth based on candidate performance
- **Real-time Evaluation**: Immediate feedback and scoring for candidate responses
- **Intelligent Orchestration**: Seamless coordination between all agents
- **Interactive Interface**: User-friendly command-line interface
- **Configurable Parameters**: Customizable interview settings and agent behavior

## Prerequisites

- Python 3.10+
- OpenAI API key
- Required Python packages (see requirements.txt)

## Usage

### Interactive Mode

Run the main interview system:

```bash
python main.py
```

Available commands:
- `start` - Start a new interview
- `answer <response>` - Answer the current question
- `status` - Check interview status
- `end` - End the current interview
- `help` - Show help information
- `quit` - Exit the program

## Project Structure

```
finalround-assignment/
|-- main.py                 # Main entry point with interactive interface
|-- agents.py              # Core agent implementations
|-- interview_system.py    # Router/orchestrator system
|-- config.py              # Configuration settings
|-- demo.py                # Demo script
|-- sample_resume.txt      # Sample candidate resume
|-- sample_job_description.txt  # Sample job description
|-- requirements.txt       # Python dependencies
|-- pyproject.toml        # Project configuration
```

## Configuration

The system can be configured through environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)
- `MAX_INTERVIEW_ROUNDS`: Maximum interview rounds (default: 5)
- `DEFAULT_INTERVIEW_DEPTH`: Default interview depth (default: 2)
- `INTERVIEWER_TEMPERATURE`: Temperature for question generation (default: 0.7)
- `TOPIC_MANAGER_TEMPERATURE`: Temperature for topic management (default: 0.3)
- `EVALUATOR_TEMPERATURE`: Temperature for evaluation (default: 0.2)

## Agent Details

### InterviewerAgent
- Generates contextual questions based on resume and job description
- Adapts question difficulty based on interview depth
- Avoids repeating previously asked questions
- Focuses on job-relevant technical skills

### TopicManagerAgent
- Manages interview topic progression
- Adjusts interview depth based on candidate performance
- Ensures comprehensive coverage of job requirements
- Balances technical and behavioral questions

### EvaluatorAgent
- Provides real-time evaluation of candidate responses
- Scores responses on a 1-10 scale
- Offers detailed feedback and improvement suggestions
- Considers technical accuracy, communication, and relevance

### OrchestratorAgent
- Coordinates all other agents
- Manages interview session state
- Handles the overall interview flow
- Provides session summaries and progress tracking

## Interview Topics

The system covers various interview topics:

- **Technical Skills**: Programming languages, frameworks, tools
- **Problem Solving**: Algorithm design, debugging, optimization
- **System Design**: Architecture, scalability, performance
- **Leadership/Management**: Team leadership, mentoring, project management
- **Behavioral**: Past experiences, conflict resolution, growth mindset
- **Company Culture Fit**: Values alignment, work style, collaboration

## Example Usage

1. **Start an interview**:
   ```
   > start
   ```

2. **Answer questions**:
   ```
   > answer I have 5+ years of Python experience with Django and Flask frameworks...
   ```

3. **Check status**:
   ```
   > status
   ```

4. **End interview**:
   ```
   > end
   ```

## Sample Data

The system includes sample data files:

- **sample_resume.txt**: Contains a sample software engineer resume
- **sample_job_description.txt**: Contains a sample senior Python developer job description

You can replace these with your own resume and job description files.

- Built with LangChain and OpenAI
- Implements multi-agent architecture patterns
- Designed for realistic interview simulation
