"""
ADAM-ZERO: AI Development and Management System
Where Gemini orchestrates and Claude codes!
Now with Fragment IR - the mathematical compiler.
"""
import os
from typing import Optional, Dict, Any
from gemini_client import GeminiOrchestrator
from chatgpt_client import ChatGPTClient
from gemini_fragment_integration import MathOrchestrator
from fragment_ir_pipeline import FragmentIRPipeline


class AdamZero:
    """
    Main orchestration system combining Gemini's planning with Claude's coding.
    Now enhanced with Fragment IR for mathematical reasoning.
    """

    def __init__(self):
        """Initialize ADAM-ZERO with all AI components."""
        self.gemini = GeminiOrchestrator()
        self.chatgpt = ChatGPTClient()
        self.math_orchestrator = MathOrchestrator()
        self.fragment_pipeline = FragmentIRPipeline()
        print("🚀 ADAM-ZERO initialized!")
        print("  - Gemini: Orchestration & Planning")
        print("  - Claude: Coding & Implementation")
        print("  - ChatGPT: Code Review & Suggestions")
        print("  - Fragment IR: Mathematical Compiler")

    def process_request(self, user_request: str) -> Dict[str, Any]:
        """
        Process a user request through the full pipeline.

        1. Gemini creates the plan and defines tasks
        2. Returns the plan for Claude to implement
        3. ChatGPT can optionally review the results

        Args:
            user_request: What the user wants to build/do

        Returns:
            Dictionary with plan, tasks, and next steps
        """
        print(f"\n📝 Processing request: {user_request}")
        print("\n🧠 Gemini is orchestrating...")

        # Gemini creates the plan
        orchestration = self.gemini.orchestrate(user_request)

        print("\n✅ Orchestration complete!")
        print("\n" + "="*60)
        print("PLAN FROM GEMINI:")
        print("="*60)
        print(orchestration['plan'])

        print("\n" + "="*60)
        print("CODING TASKS FOR CLAUDE:")
        print("="*60)
        print(orchestration['coding_tasks'])

        if orchestration['architecture']:
            print("\n" + "="*60)
            print("ARCHITECTURE NOTES:")
            print("="*60)
            print(orchestration['architecture'])

        return {
            'orchestration': orchestration,
            'next_step': 'Claude should now implement the coding tasks above',
            'status': 'ready_for_coding'
        }

    def review_with_chatgpt(self, code: str, language: str = "python") -> str:
        """
        Use ChatGPT to review code that was implemented.

        Args:
            code: The code to review
            language: Programming language

        Returns:
            Review feedback
        """
        print("\n🔍 ChatGPT is reviewing the code...")
        review = self.chatgpt.review_code(code, language)
        print("\n✅ Review complete!")
        return review

    def process_math_problem(self, problem: str) -> Dict[str, Any]:
        """
        Process a mathematical problem using Gemini + Fragment IR.

        Args:
            problem: Mathematical problem or expression

        Returns:
            Dictionary with orchestration, analysis, and fragment decomposition
        """
        print(f"\n🔢 Processing mathematical problem: {problem}")
        print("\n🧠 Gemini is analyzing...")

        # Gemini orchestrates the mathematical problem
        orchestration = self.math_orchestrator.orchestrate_problem(problem)

        print("\n✅ Analysis complete!")
        print("\n" + "="*60)
        print("GEMINI'S PLAN:")
        print("="*60)
        print(orchestration['plan'][:500] + "...")

        return {
            'problem': problem,
            'orchestration': orchestration,
            'status': 'analyzed',
            'next_step': 'Use Fragment IR to formalize this problem'
        }

    def decompose_expression(self, expression: str, expression_type: str = "math") -> Dict[str, Any]:
        """
        Decompose a mathematical expression into fragments with Gemini's guidance.

        Args:
            expression: Mathematical expression (e.g., "x^2 + 3x + 1")
            expression_type: Type of expression

        Returns:
            Dictionary with Gemini's analysis and fragment decomposition
        """
        print(f"\n🔬 Decomposing: {expression}")
        print("\n🧠 Gemini is analyzing structure...")

        result = self.math_orchestrator.decompose_with_guidance(expression, expression_type)

        print("\n✅ Decomposition complete!")

        if "fragment_graph" in result:
            print(f"\n📊 Fragment Analysis:")
            print(f"  Total fragments: {result['num_fragments']}")
            print(f"  Reconstructed: {result['reconstructed']}")
            print(f"  Meaning preserved: {result['meaning_preserved']}")

        return result

    def analyze_concept(self, concept: str) -> Dict[str, Any]:
        """
        Analyze a mathematical concept using Gemini.

        Args:
            concept: Mathematical concept (e.g., "derivative", "group action")

        Returns:
            Dictionary with Gemini's analysis
        """
        print(f"\n🎓 Analyzing concept: {concept}")
        print("\n🧠 Gemini is thinking...")

        result = self.math_orchestrator.analyze_mathematical_concept(concept)

        print("\n✅ Analysis complete!")
        print("\n" + "="*60)
        print("GEMINI'S ANALYSIS:")
        print("="*60)
        print(result['analysis'][:600] + "...")

        return result


def main():
    """Example usage of ADAM-ZERO with Fragment IR."""
    print("=" * 80)
    print("ADAM-ZERO: Multi-AI Orchestration + Fragment IR")
    print("=" * 80)
    print()

    try:
        adam = AdamZero()

        # Demo 1: Standard software engineering task
        print("\n" + "=" * 80)
        print("DEMO 1: Software Engineering Task")
        print("=" * 80)
        result = adam.process_request(
            "Build a REST API that stores user preferences"
        )
        print("\n" + "="*60)
        print("🎯 NEXT STEPS:")
        print("="*60)
        print(result['next_step'])

        # Demo 2: Mathematical problem
        print("\n\n" + "=" * 80)
        print("DEMO 2: Mathematical Problem (NEW!)")
        print("=" * 80)
        result = adam.process_math_problem(
            "Find the derivative of f(x) = x^2 + 3x + 1"
        )

        # Demo 3: Expression decomposition
        print("\n\n" + "=" * 80)
        print("DEMO 3: Expression Decomposition (NEW!)")
        print("=" * 80)
        result = adam.decompose_expression("x^2")

        # Demo 4: Concept analysis
        print("\n\n" + "=" * 80)
        print("DEMO 4: Concept Analysis (NEW!)")
        print("=" * 80)
        result = adam.analyze_concept("group homomorphism")

        print("\n\n" + "=" * 80)
        print("✓ ADAM-ZERO fully operational!")
        print("  - Gemini orchestrates")
        print("  - Claude codes")
        print("  - Fragment IR formalizes mathematics")
        print("=" * 80)

    except Exception as e:
        print(f"\nError: {e}")
        print("\nNote: Set GEMINI_API_KEY and OPENAI_API_KEY in .env file")
        print("Get keys from:")
        print("  - Gemini: https://makersuite.google.com/app/apikey")
        print("  - OpenAI: https://platform.openai.com/api-keys")


def demo_math_only():
    """Quick demo of just the math capabilities."""
    print("=" * 80)
    print("FRAGMENT IR + GEMINI DEMO")
    print("=" * 80)

    try:
        adam = AdamZero()

        # Quick math demos
        print("\n📊 Analyzing: derivative")
        adam.analyze_concept("derivative")

        print("\n\n🔬 Decomposing: x^2 + 1")
        adam.decompose_expression("x^2 + 1")

    except Exception as e:
        print(f"Error: {e}")
        print("Set GEMINI_API_KEY in .env file")


if __name__ == "__main__":
    # Run full demo by default
    # Use demo_math_only() for quick math-focused demo
    main()
