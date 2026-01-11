"""
GEMINI + FRAGMENT IR INTEGRATION
=================================

Combines Gemini's orchestration with Fragment IR for mathematical reasoning.

Workflow:
1. User gives a mathematical problem
2. Gemini analyzes and breaks it down into fragments
3. Claude implements using Fragment IR
4. Result is a typed fragment graph
"""

import os
from typing import Dict, Any, Optional
from gemini_client import GeminiOrchestrator
from fragment_ir_pipeline import FragmentIRPipeline
from fragment_graph import FragmentGraph
import json


class MathOrchestrator:
    """
    Orchestrates mathematical problem-solving using Gemini + Fragment IR.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the math orchestrator."""
        self.gemini = GeminiOrchestrator(api_key)
        self.fragment_pipeline = FragmentIRPipeline()

    def analyze_mathematical_concept(self, concept: str) -> Dict[str, Any]:
        """
        Analyze a mathematical concept and decompose it into fragments.

        Args:
            concept: Mathematical concept to analyze (e.g., "derivative", "fibonacci")

        Returns:
            Dictionary with analysis and fragment decomposition
        """
        prompt = f"""You are analyzing a mathematical concept for decomposition into typed fragments.

Mathematical Concept: {concept}

Analyze this concept and identify which of these 8 fragment types are present:
1. ENTITY - Atomic objects (variables, constants, values)
2. RELATION - Typed predicates (equals, less than, belongs to)
3. OPERATOR - Typed functions (addition, multiplication, differentiation)
4. CONSTRAINT - Guards on states (conditions, bounds, requirements)
5. MEASURE - Evaluation functionals (norm, length, energy)
6. STRUCTURE - Containers with laws (groups, fields, vector spaces)
7. TRANSFORM - Rewrites/maps (Fourier transform, isomorphisms)
8. RECURSION - Self-application (recursive definitions, induction)

For each fragment type you identify, explain:
- What it represents in this concept
- Its type signature
- How it connects to other fragments

Provide your analysis in a structured format."""

        response = self.gemini.model.generate_content(prompt)
        return {
            "concept": concept,
            "analysis": response.text,
            "next_step": "Use Fragment IR to formalize this analysis"
        }

    def orchestrate_problem(self, problem: str) -> Dict[str, Any]:
        """
        Orchestrate solving a mathematical problem.

        Args:
            problem: The mathematical problem to solve

        Returns:
            Orchestration plan and implementation strategy
        """
        prompt = f"""You are orchestrating the solution to a mathematical problem using Fragment IR.

Problem: {problem}

The Fragment IR system decomposes mathematics into 8 typed fragments:
- ENTITY: Atomic objects
- RELATION: Typed predicates
- OPERATOR: Typed functions
- CONSTRAINT: Guards/conditions
- MEASURE: Evaluation functionals
- STRUCTURE: Containers + laws
- TRANSFORM: Maps between structures
- RECURSION: Self-application

Your task:
1. Identify what mathematical concepts are involved
2. Determine which fragments are needed
3. Describe how these fragments should connect
4. Outline the implementation approach

Provide a clear plan that Claude can use to implement this using the Fragment IR."""

        response = self.gemini.model.generate_content(prompt)

        return {
            "problem": problem,
            "plan": response.text,
            "implementation_ready": True
        }

    def decompose_with_guidance(self, expression: str, expression_type: str = "math") -> Dict[str, Any]:
        """
        Decompose a mathematical expression with Gemini's guidance.

        Args:
            expression: Mathematical expression (e.g., "x^2 + 2x + 1")
            expression_type: Type of expression ("math", "equation", "definition")

        Returns:
            Decomposition results with Gemini's analysis
        """
        # First, get Gemini's analysis
        analysis_prompt = f"""Analyze this mathematical expression and describe its structure:

Expression: {expression}
Type: {expression_type}

Identify:
1. What are the entities (variables, constants)?
2. What operators are being used?
3. Are there any constraints or conditions?
4. What is the mathematical meaning?

Be specific and technical."""

        gemini_response = self.gemini.model.generate_content(analysis_prompt)
        gemini_analysis = gemini_response.text

        # Then, decompose using Fragment IR
        try:
            fragment_result = self.fragment_pipeline.round_trip(
                expression,
                input_type=expression_type,
                output_type="latex"
            )

            return {
                "expression": expression,
                "gemini_analysis": gemini_analysis,
                "fragment_graph": fragment_result["graph"],
                "normalized_graph": fragment_result["normalized"],
                "reconstructed": fragment_result["output"],
                "meaning_preserved": fragment_result["preserved_meaning"],
                "num_fragments": len(fragment_result["graph"].nodes)
            }
        except Exception as e:
            return {
                "expression": expression,
                "gemini_analysis": gemini_analysis,
                "error": str(e),
                "fallback": "Fragment decomposition failed, but analysis available"
            }

    def explain_fragment_graph(self, graph: FragmentGraph) -> str:
        """
        Use Gemini to explain a fragment graph in plain English.

        Args:
            graph: The fragment graph to explain

        Returns:
            Natural language explanation
        """
        # Serialize graph info
        graph_info = {
            "name": graph.name,
            "num_nodes": len(graph.nodes),
            "num_edges": len(graph.edges),
            "fragment_types": list(set(n.fragment_type for n in graph.nodes)),
            "nodes": [
                {
                    "type": n.fragment_type,
                    "name": n.name,
                    "properties": n.properties
                }
                for n in graph.nodes[:10]  # Limit to first 10 for context
            ]
        }

        prompt = f"""Explain this fragment graph in plain English.

Graph: {graph.name}
Fragments: {graph_info['fragment_types']}
Structure: {graph_info['num_nodes']} nodes, {graph_info['num_edges']} edges

Nodes (sample):
{json.dumps(graph_info['nodes'], indent=2)}

Provide a clear, intuitive explanation of what this mathematical structure represents
and how the different fragments work together."""

        response = self.gemini.model.generate_content(prompt)
        return response.text

    def suggest_transformations(self, concept: str) -> Dict[str, Any]:
        """
        Use Gemini to suggest mathematical transformations and related concepts.

        Args:
            concept: Starting mathematical concept

        Returns:
            Suggested transformations and related ideas
        """
        prompt = f"""Given the mathematical concept: {concept}

Suggest:
1. Equivalent representations (different fragment decompositions)
2. Generalizations (what broader structures does this fit into?)
3. Specializations (what simpler cases are there?)
4. Dual concepts (what's the dual/opposite structure?)
5. Applications (where is this concept used?)

Focus on structural relationships that Fragment IR could represent."""

        response = self.gemini.model.generate_content(prompt)

        return {
            "original_concept": concept,
            "suggestions": response.text,
            "actionable": "These suggestions can be formalized as fragment graphs"
        }


def demo_gemini_fragment_integration():
    """Demonstrate Gemini + Fragment IR working together."""
    print("=" * 80)
    print("GEMINI + FRAGMENT IR INTEGRATION DEMO")
    print("=" * 80)
    print()

    try:
        orchestrator = MathOrchestrator()

        # Demo 1: Analyze a concept
        print("DEMO 1: Concept Analysis")
        print("-" * 60)
        result = orchestrator.analyze_mathematical_concept("derivative")
        print(f"Concept: {result['concept']}")
        print(f"\nGemini's Analysis:")
        print(result['analysis'][:500] + "...")
        print()

        # Demo 2: Decompose with guidance
        print("\n" + "=" * 80)
        print("DEMO 2: Guided Decomposition")
        print("-" * 60)
        result = orchestrator.decompose_with_guidance("x^2", "math")
        print(f"Expression: {result['expression']}")
        print(f"\nGemini's Analysis:")
        print(result['gemini_analysis'][:500] + "...")
        if "fragment_graph" in result:
            print(f"\nFragment decomposition:")
            print(f"  Fragments: {result['num_fragments']}")
            print(f"  Reconstructed: {result['reconstructed']}")
            print(f"  Meaning preserved: {result['meaning_preserved']}")
        print()

        # Demo 3: Orchestrate a problem
        print("\n" + "=" * 80)
        print("DEMO 3: Problem Orchestration")
        print("-" * 60)
        result = orchestrator.orchestrate_problem(
            "Find the derivative of f(x) = x^2 + 3x + 1"
        )
        print(f"Problem: {result['problem']}")
        print(f"\nGemini's Plan:")
        print(result['plan'][:600] + "...")
        print()

        # Demo 4: Suggest transformations
        print("\n" + "=" * 80)
        print("DEMO 4: Transformation Suggestions")
        print("-" * 60)
        result = orchestrator.suggest_transformations("linear transformation")
        print(f"Original: {result['original_concept']}")
        print(f"\nSuggestions:")
        print(result['suggestions'][:600] + "...")
        print()

        print("=" * 80)
        print("✓ Gemini + Fragment IR integration working!")
        print("=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: You need to set GEMINI_API_KEY in your .env file")
        print("Get your key from: https://makersuite.google.com/app/apikey")


if __name__ == "__main__":
    demo_gemini_fragment_integration()
