#!/usr/bin/env python3
"""
Gemini + Fragment IR Integration Demo

Shows how Gemini orchestrates mathematical reasoning using Fragment IR.
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adam_zero import AdamZero


def demo_orchestration():
    """
    Demonstrate Gemini orchestrating mathematical tasks with Fragment IR.
    """
    print("=" * 80)
    print("GEMINI + FRAGMENT IR ORCHESTRATION DEMO")
    print("=" * 80)
    print()
    print("This demo shows how Gemini orchestrates mathematical reasoning")
    print("and Fragment IR formalizes the concepts.")
    print()
    print("Note: Requires GEMINI_API_KEY in .env file")
    print("=" * 80)
    print()

    try:
        # Initialize ADAM-ZERO
        adam = AdamZero()

        # Example 1: Analyze a mathematical concept
        print("\n" + "=" * 80)
        print("EXAMPLE 1: Analyzing 'Derivative'")
        print("=" * 80)

        result = adam.analyze_concept("derivative")
        print(f"\nStatus: {result.get('next_step', 'Complete')}")

        # Example 2: Decompose an expression
        print("\n" + "=" * 80)
        print("EXAMPLE 2: Decomposing 'x^2'")
        print("=" * 80)

        result = adam.decompose_expression("x^2")

        if "fragment_graph" in result:
            print(f"\n✓ Successfully decomposed into {result['num_fragments']} fragments")
            print(f"  Reconstructed: {result['reconstructed']}")

        # Example 3: Solve a problem
        print("\n" + "=" * 80)
        print("EXAMPLE 3: Solving a Calculus Problem")
        print("=" * 80)

        result = adam.process_math_problem(
            "Find the derivative of f(x) = x^3 - 2x^2 + x"
        )

        # Summary
        print("\n" + "=" * 80)
        print("DEMO COMPLETE")
        print("=" * 80)
        print()
        print("What happened:")
        print("1. Gemini analyzed mathematical concepts")
        print("2. Fragment IR decomposed expressions into typed fragments")
        print("3. The system orchestrated the entire mathematical reasoning process")
        print()
        print("This is the foundation for:")
        print("  - Automated theorem proving")
        print("  - Math IDE with smart autocompletion")
        print("  - Cross-domain translation (topology ⇄ programming)")
        print("  - Generative mathematics")
        print("=" * 80)

    except ValueError as e:
        print(f"\n⚠️  Error: {e}")
        print()
        print("To run this demo, you need to:")
        print("1. Get a Gemini API key: https://makersuite.google.com/app/apikey")
        print("2. Add it to .env file: GEMINI_API_KEY=your_key_here")
        print()
        print("The Gemini API has a free tier, so you can get started at no cost!")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


def demo_without_api():
    """
    Demonstrate Fragment IR without API keys.
    """
    from fragment_ir_pipeline import FragmentIRPipeline
    from examples.fibonacci_graph import create_fibonacci_graph

    print("=" * 80)
    print("FRAGMENT IR DEMO (No API keys needed)")
    print("=" * 80)
    print()

    # Demo Fragment IR without Gemini
    pipeline = FragmentIRPipeline()

    print("Decomposing 'x^2' into fragments...")
    result = pipeline.round_trip("x^2", "math", "latex")

    print(f"Input:  {result['input']}")
    print(f"Output: {result['output']}")
    print(f"Fragments: {len(result['graph'].nodes)} nodes, {len(result['graph'].edges)} edges")
    print()

    print("Creating Fibonacci recursion graph...")
    fib_graph = create_fibonacci_graph()
    print(f"Fibonacci graph: {len(fib_graph.nodes)} nodes, {len(fib_graph.edges)} edges")
    print()

    print("✓ Fragment IR works without API keys!")
    print("  Add GEMINI_API_KEY to .env to enable orchestration.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--no-api":
        # Demo without API keys
        demo_without_api()
    else:
        # Full demo with Gemini orchestration
        demo_orchestration()
