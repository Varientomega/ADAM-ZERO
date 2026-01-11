# ADAM-ZERO 🚀

**AI Development and Management System**

A multi-AI orchestration system where:
- 🧠 **Gemini** does the orchestration and planning
- 💻 **Claude** handles the coding and implementation
- 🔍 **ChatGPT** provides code review and suggestions

## Architecture

```
User Request
     ↓
Gemini (Orchestrator)
  - Analyzes the request
  - Creates detailed plan
  - Defines coding tasks
  - Makes architecture decisions
     ↓
Claude (Coder)
  - Implements the plan
  - Writes the code
  - Handles technical execution
     ↓
ChatGPT (Reviewer) [Optional]
  - Reviews code quality
  - Suggests improvements
  - Provides feedback
```

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API keys:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required API keys:
- `GEMINI_API_KEY` - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- `OPENAI_API_KEY` - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- `ANTHROPIC_API_KEY` - Optional, for future enhancements

## Usage

### Basic Example

```python
from adam_zero import AdamZero

# Initialize the system
adam = AdamZero()

# Give it a task - Gemini will orchestrate, then you implement
result = adam.process_request(
    "Build a REST API for a todo application with user authentication"
)

# The result contains:
# - plan: High-level plan from Gemini
# - coding_tasks: Specific tasks for Claude to implement
# - architecture: Design decisions and notes
```

### Individual Components

**Use Gemini for orchestration:**
```python
from gemini_client import GeminiOrchestrator

orchestrator = GeminiOrchestrator()
plan = orchestrator.plan_task("Create a web scraper")
print(plan)
```

**Use ChatGPT for code review:**
```python
from chatgpt_client import ChatGPTClient

chatgpt = ChatGPTClient()
review = chatgpt.review_code(your_code, language="python")
print(review)
```

## How It Works

1. **You give ADAM-ZERO a task**
   - Example: "Build a chat application with real-time messaging"

2. **Gemini orchestrates**
   - Analyzes the requirements
   - Creates a step-by-step plan
   - Defines what code needs to be written
   - Makes architectural decisions

3. **Claude codes**
   - Takes Gemini's plan
   - Implements the actual code
   - Handles technical details
   - Executes the tasks

4. **ChatGPT reviews** (optional)
   - Reviews the implemented code
   - Suggests improvements
   - Provides quality feedback

## Example Workflow

```bash
# Run the example
python adam_zero.py

# Output will show:
# 1. Gemini's orchestration plan
# 2. Specific coding tasks
# 3. Architecture notes
# 4. What Claude should implement next
```

## Project Structure

```
ADAM-ZERO/
├── adam_zero.py          # Main orchestration system
├── gemini_client.py      # Gemini API integration
├── chatgpt_client.py     # ChatGPT API integration
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Why This Architecture?

**Gemini as Orchestrator:**
- Excellent at planning and breaking down complex tasks
- Strong reasoning capabilities
- Good at architectural decisions

**Claude as Coder:**
- Superior coding abilities
- Great at implementation details
- Excellent at following specifications

**ChatGPT as Reviewer:**
- Strong code review capabilities
- Good at suggesting improvements
- Provides different perspective

## Future Enhancements

- [ ] Add persistent conversation memory
- [ ] Create web interface
- [ ] Add support for more AI models
- [ ] Implement automatic code testing
- [ ] Build project templates
- [ ] Add collaboration features

## License

MIT License - Feel free to use and modify!

## Contributing

Contributions welcome! This is an experimental project exploring multi-AI collaboration.
