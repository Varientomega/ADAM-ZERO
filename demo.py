#!/usr/bin/env python3
"""
FRAGMENT IR DEMO
================

Quick demonstration of the Fragment IR system.
"""

from fragment_spec import FRAGMENT_CATALOG, print_catalog
from fragment_ir_pipeline import FragmentIRPipeline
from examples.fibonacci_graph import create_fibonacci_graph

def main():
    print("=" * 80)
    print("FRAGMENT IR DEMO - Universal Math Compiler")
    print("=" * 80)
    print()

    # Part 1: Show the 8 fragments
    print("PART 1: THE 8 CORE FRAGMENTS")
    print("-" * 80)
    print_catalog()
    print()

    # Part 2: Simple expression decomposition
    print("\n" + "=" * 80)
    print("PART 2: DECOMPOSE & RECOMPOSE")
    print("=" * 80)
    print()

    pipeline = FragmentIRPipeline()

    # Test case 1: Power expression
    print("Test 1: Power expression")
    print("-" * 60)
    result = pipeline.round_trip("x^2", input_type="math", output_type="latex")
    print(f"Input:  {result['input']}")
    print(f"Output: {result['output']}")
    print(f"Nodes:  {len(result['graph'].nodes)}")
    print(f"Edges:  {len(result['graph'].edges)}")
    print()

    # Test case 2: Addition
    print("Test 2: Addition expression")
    print("-" * 60)
    result = pipeline.round_trip("a + b", input_type="math", output_type="english")
    print(f"Input:  {result['input']}")
    print(f"Output: {result['output']}")
    print(f"Nodes:  {len(result['graph'].nodes)}")
    print(f"Edges:  {len(result['graph'].edges)}")
    print()

    # Part 3: Complex example - Fibonacci
    print("=" * 80)
    print("PART 3: COMPLEX EXAMPLE - FIBONACCI RECURSION")
    print("=" * 80)
    print()

    fib_graph = create_fibonacci_graph()

    print("Fragment composition:")
    type_counts = {}
    for node in fib_graph.nodes:
        ftype = node.fragment_type
        type_counts[ftype] = type_counts.get(ftype, 0) + 1

    for ftype, count in sorted(type_counts.items()):
        print(f"  {ftype}: {count}")

    print()
    print(f"Total nodes: {len(fib_graph.nodes)}")
    print(f"Total edges: {len(fib_graph.edges)}")
    print()
    print("Mathematical definition:")
    print("  F(0) = 0")
    print("  F(1) = 1")
    print("  F(n) = F(n-1) + F(n-2)  for n > 1")
    print()
    print("This entire recursive definition is now represented as a typed")
    print("fragment graph that can be:")
    print("  - Normalized to canonical form")
    print("  - Translated to any language")
    print("  - Analyzed for properties")
    print("  - Compared with other definitions")

    # Part 4: What this unlocks
    print()
    print("=" * 80)
    print("WHAT THIS UNLOCKS")
    print("=" * 80)
    print()
    print("1. Universal Translation")
    print("   topology ⇄ logic ⇄ programming ⇄ physics")
    print()
    print("2. Cognitive Compression")
    print("   Store role graphs, not surface syntax")
    print()
    print("3. Machine-Testable Invariance")
    print("   Automatically detect symmetries and hidden structure")
    print()
    print("4. Generative Mathematics")
    print("   New fields = new fragment compositions")
    print()
    print("5. IDE Leverage")
    print("   Math-preserving refactors, smart autocompletion")
    print()
    print("=" * 80)
    print("The highest-leverage move: building the machine that births theorems.")
    print("=" * 80)


if __name__ == "__main__":
    main()
