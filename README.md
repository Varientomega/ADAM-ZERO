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

---

## 🔑 Fragment IR: Mathematical Compiler

**The core innovation** - A universal intermediate representation (IR) for mathematics, like LLVM IR but for ideas.

### What It Unlocks

**Universal Translation Layer:**
- `topology ⇄ logic ⇄ programming ⇄ physics` becomes loss-minimized translation
- "This is the same idea" stops being vibes and becomes structural equivalence

**Cognitive Compression:**
- Store the role graph of an argument, not its surface syntax
- Reuse and remix by slot-filling instead of re-deriving

**Machine-Testable Invariance:**
- Automatically probe "what stays the same when I transform this?"
- Detect hidden symmetries, missing constraints, fake generalizations

### The 8 Core Fragments

Every mathematical concept decomposes into these typed fragments:

1. **ENTITY** - `Entity[T]` - Atomic objects
2. **RELATION** - `Relation[A, B]: (A, B) → Bool` - Typed predicates
3. **OPERATOR** - `Operator[A, B]: A → B` - Typed functions/morphisms
4. **CONSTRAINT** - `Constraint[A]: A → Bool` - Guards on states
5. **MEASURE** - `Measure[A]: A → ℝ` - Evaluation functionals
6. **STRUCTURE** - `Structure[T] = (Container[T], Laws)` - Containers + laws
7. **TRANSFORM** - `Transform[A, B]: Structure[A] → Structure[B]` - Rewrites
8. **RECURSION** - `Recursion[T] = (step, seed, stop) → result` - Self-application

### The IR Pipeline

```
Input → Decompose → Normalize → Recompose → Output
  ↓         ↓            ↓            ↓
LaTeX   Fragment     Canonical    Python
Math    Graph        Form         Code
```

**Round-trip test:** `Input → Graph → Output → Graph`
If graphs match (within equivalences), meaning is preserved.

### Usage Example

```python
from fragment_ir_pipeline import FragmentIRPipeline

pipeline = FragmentIRPipeline()

# Round-trip: LaTeX → Graph → Python
result = pipeline.round_trip("x^2", input_type="math", output_type="python")

print(result['input'])           # x^2
print(result['output'])          # def square(x): return x ** 2
print(result['preserved_meaning'])  # True
```

### The 5 Canonical Test Cases

Tests proving the IR is universal:

1. **Derivative definition** - `f'(x) = lim(h→0) [f(x+h) - f(x)] / h`
2. **Group action** - `g · (h · x) = (gh) · x`
3. **Shortest path** - `argmin_path Σ edge_weights`
4. **Fibonacci recursion** - `F(n) = F(n-1) + F(n-2)`
5. **Energy conservation** - `E = T + V, dE/dt = 0`

Run the tests:
```bash
python tests/test_harness.py
```

## Project Structure

```
ADAM-ZERO/
├── adam_zero.py                 # Main orchestration system
├── gemini_client.py             # Gemini API integration
├── chatgpt_client.py            # ChatGPT API integration
├── fragment_spec.py             # The 8 core fragments (typed)
├── fragment_graph.py            # Graph representation + JSON schema
├── fragment_ir_pipeline.py      # Decomposer, Normalizer, Recomposer
├── examples/
│   └── fibonacci_graph.py       # Fibonacci as fragment graph
├── tests/
│   └── test_harness.py          # 5 canonical test cases
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
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
