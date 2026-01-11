# ADAM-ZERO Architecture

## System Overview

ADAM-ZERO combines multi-AI orchestration with a universal mathematical IR (Intermediate Representation), creating a system where:
- **Gemini** orchestrates and plans
- **Claude** codes and implements
- **Fragment IR** formalizes mathematics
- **ChatGPT** (optional) reviews and suggests

```
┌─────────────────────────────────────────────────────────────┐
│                        ADAM-ZERO                            │
│                   Multi-AI Orchestration                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   User Request / Problem      │
              └───────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Gemini Orchestrator         │
              │   - Analyzes request          │
              │   - Creates plan              │
              │   - Breaks into tasks         │
              └───────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
        ┌─────────────────┐   ┌──────────────────┐
        │ Software Tasks  │   │  Math Tasks      │
        │ (Claude codes)  │   │  (Fragment IR)   │
        └─────────────────┘   └──────────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
              ┌───────────────────────────────┐
              │   ChatGPT Reviewer            │
              │   (Optional)                  │
              └───────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Result / Implementation     │
              └───────────────────────────────┘
```

## Fragment IR Architecture

The mathematical compiler at the heart of ADAM-ZERO:

```
┌────────────────────────────────────────────────────────────┐
│                     FRAGMENT IR PIPELINE                    │
└────────────────────────────────────────────────────────────┘

Input (LaTeX, Python, English)
        │
        ▼
┌────────────────┐
│  DECOMPOSER    │  Parses input → Fragment Graph
└────────────────┘
        │
        ▼
Fragment Graph (Nodes + Edges)
┌─────────────────────────────────────┐
│ Nodes = 8 Fragment Types:          │
│  • ENTITY     - Atomic objects      │
│  • RELATION   - Typed predicates    │
│  • OPERATOR   - Functions/morphisms │
│  • CONSTRAINT - Guards/conditions   │
│  • MEASURE    - Evaluation functionals │
│  • STRUCTURE  - Containers + laws   │
│  • TRANSFORM  - Rewrites/maps       │
│  • RECURSION  - Self-application    │
│                                     │
│ Edges = Typed Bindings:            │
│  • uses, guards, wraps, applies_to  │
│  • relates, transforms_to, etc.     │
└─────────────────────────────────────┘
        │
        ▼
┌────────────────┐
│  NORMALIZER    │  Graph → Canonical Form
└────────────────┘       (enables "same idea" detection)
        │
        ▼
Canonical Fragment Graph
        │
        ▼
┌────────────────┐
│  RECOMPOSER    │  Graph → Target Language
└────────────────┘
        │
        ▼
Output (LaTeX, Python, Lean, English)
```

## Integration: Gemini + Fragment IR

How the orchestration works:

```
┌──────────────────────────────────────────────────────────────┐
│  USER: "Find the derivative of f(x) = x^2 + 3x + 1"         │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  GEMINI ORCHESTRATOR:                                        │
│  1. Analyzes: This is a calculus problem                     │
│  2. Identifies fragments needed:                             │
│     - ENTITY (x, constants)                                  │
│     - OPERATOR (derivative, addition, power)                 │
│     - CONSTRAINT (continuity, differentiability)             │
│  3. Plans approach: Apply power rule + sum rule              │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  CLAUDE (via Fragment IR):                                   │
│  1. Creates fragment graph for f(x) = x^2 + 3x + 1           │
│  2. Applies derivative operator fragments                    │
│  3. Constructs result: f'(x) = 2x + 3                        │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  FRAGMENT IR:                                                │
│  - Normalizes both input and output                          │
│  - Verifies transformation preserves meaning                 │
│  - Can recompose to any target language                      │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  RESULT: f'(x) = 2x + 3                                      │
│  + Formal verification via fragment graphs                   │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Standard Software Task
```
User → Gemini → Plan → Claude → Code → ChatGPT Review → Result
```

### 2. Mathematical Task (NEW!)
```
User → Gemini → Math Analysis → Fragment IR → Formalization → Result
                     │
                     └→ Identifies fragments
                     └→ Plans decomposition
                     └→ Verifies correctness
```

### 3. Hybrid Task
```
User → Gemini → {Software Plan, Math Plan}
              ↓                    ↓
           Claude              Fragment IR
              ↓                    ↓
           Code          Formalized Math
              └────────┬─────────┘
                       ▼
                Integrated Result
```

## Component Responsibilities

### Gemini Orchestrator (`gemini_client.py`)
- **Role**: High-level planning and orchestration
- **Strengths**: Breaking down complex tasks, architectural decisions
- **Output**: Plans, task lists, design decisions

### MathOrchestrator (`gemini_fragment_integration.py`)
- **Role**: Mathematical reasoning coordination
- **Functions**:
  - `analyze_mathematical_concept()`: Identifies fragment types
  - `orchestrate_problem()`: Plans mathematical solutions
  - `decompose_with_guidance()`: Guides fragment decomposition
  - `explain_fragment_graph()`: Natural language explanations

### Fragment IR (`fragment_spec.py`, `fragment_graph.py`, `fragment_ir_pipeline.py`)
- **Role**: Universal mathematical representation
- **Components**:
  - 8 typed fragments (the atoms of math)
  - Graph structure (nodes + edges)
  - Pipeline (decompose → normalize → recompose)
  - Round-trip testing (verify meaning preservation)

### AdamZero (`adam_zero.py`)
- **Role**: Main coordination hub
- **Methods**:
  - `process_request()`: Software engineering tasks
  - `process_math_problem()`: Mathematical problems
  - `decompose_expression()`: Fragment decomposition
  - `analyze_concept()`: Concept analysis

## Key Innovations

### 1. Universal Translation Layer
Fragment IR acts as a universal translator:
```
Topology ←→ Fragment IR ←→ Logic
    ↕                          ↕
Programming ←→ Fragment IR ←→ Physics
```

### 2. Cognitive Compression
Instead of storing surface syntax, store the role graph:
```
Traditional: "f(x) = x^2" (string)
Fragment IR: Graph of ENTITY, OPERATOR, RELATION (structure)
```

### 3. Machine-Testable Invariance
```python
# What stays the same when we transform?
original_graph = decompose("x^2")
transformed_graph = decompose("x * x")
assert normalizer.are_equivalent(original_graph, transformed_graph)
# → True! They're the same mathematical idea
```

### 4. Generative Mathematics
New fields = new fragment compositions:
```
Group Theory = {STRUCTURE, OPERATOR, CONSTRAINT}
Topology = {STRUCTURE, MEASURE, CONSTRAINT, TRANSFORM}
Category Theory = {STRUCTURE, TRANSFORM, RELATION}
```

## Testing Strategy

### 5 Canonical Test Cases
1. **Derivative definition** (Calculus)
2. **Group action** (Algebra)
3. **Shortest path** (Optimization)
4. **Fibonacci recursion** (Recursion)
5. **Energy conservation** (Physics)

These prove the IR can handle diverse mathematical concepts.

### Round-Trip Verification
```
Input → Graph → Output → Graph'
assert Graph ≅ Graph'  # Structural equivalence
```

## Usage Patterns

### Pattern 1: Concept Exploration
```python
adam = AdamZero()
result = adam.analyze_concept("derivative")
# Gemini breaks down the concept into fragments
```

### Pattern 2: Expression Decomposition
```python
result = adam.decompose_expression("x^2 + 3x + 1")
# Fragment IR creates formal graph representation
```

### Pattern 3: Problem Solving
```python
result = adam.process_math_problem(
    "Find the derivative of f(x) = x^3"
)
# Gemini plans, Fragment IR formalizes
```

## Future Extensions

### Planned Enhancements
- [ ] Automated theorem proving
- [ ] Math IDE with smart autocompletion
- [ ] Visual fragment graph editor
- [ ] Cross-domain translation toolkit
- [ ] Proof verification system
- [ ] Math-preserving refactoring tools

### Research Directions
- Fragment discovery (finding new atomic fragments)
- Field synthesis (generating new mathematical fields)
- Proof search via fragment composition
- Mathematical creativity metrics

## Technical Details

### Fragment Type Signatures
```python
ENTITY[T]                                    # Atomic object
RELATION[A, B]: (A, B) → Bool               # Predicate
OPERATOR[A, B]: A → B                       # Function
CONSTRAINT[A]: A → Bool                     # Guard
MEASURE[A]: A → ℝ                           # Evaluation
STRUCTURE[T] = (Container[T], Laws)         # Container + laws
TRANSFORM[A, B]: Structure[A] → Structure[B] # Map
RECURSION[T] = (step, seed, stop) → result  # Self-application
```

### Graph Schema
```json
{
  "nodes": [
    {
      "id": "uuid",
      "fragment_type": "OPERATOR",
      "name": "derivative",
      "properties": {"order": 1, "variable": "x"}
    }
  ],
  "edges": [
    {
      "source_id": "uuid1",
      "target_id": "uuid2",
      "edge_type": "applies_to"
    }
  ]
}
```

## Why This Matters

**Traditional Approach:**
- Math is opaque strings
- "Same idea" is manual recognition
- Translation requires expert knowledge
- No machine verification

**Fragment IR Approach:**
- Math is typed fragment graphs
- "Same idea" is structural equivalence (computable!)
- Translation is graph recomposition
- Round-trip tests verify correctness

This is **LLVM for mathematics** - the compiler that makes abstract ideas executable.
