"""
EXAMPLE: Fibonacci Recursion as Fragment Graph
===============================================

Decomposes the Fibonacci sequence into typed fragments.

Mathematical definition:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2)  for n > 1

Fragment decomposition:
    - ENTITY: Natural numbers (0, 1, n)
    - OPERATOR: Addition, Subtraction
    - RECURSION: The recursive definition itself
    - CONSTRAINT: n > 1 guard
    - BASE_CASE: F(0) = 0, F(1) = 1
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fragment_graph import FragmentGraph, EdgeType
from uuid import uuid4
import json


def create_fibonacci_graph() -> FragmentGraph:
    """
    Create a fragment graph for Fibonacci recursion.

    Fibonacci definition:
        fib(n) = 0                           if n = 0
        fib(n) = 1                           if n = 1
        fib(n) = fib(n-1) + fib(n-2)         if n > 1
    """

    graph = FragmentGraph(
        id=str(uuid4()),
        name="Fibonacci Recursion",
        nodes=[],
        edges=[],
        metadata={
            "category": "recursion",
            "domain": "number_theory",
            "complexity": "O(2^n) naive, O(n) memoized"
        }
    )

    # =========================================================================
    # ENTITIES: The values involved
    # =========================================================================

    # Input variable 'n'
    n_input = graph.add_node(
        fragment_type="ENTITY",
        name="n",
        properties={
            "type": "Natural",
            "role": "input_parameter",
            "description": "The index of Fibonacci number to compute"
        }
    )

    # Base case values
    zero = graph.add_node(
        fragment_type="ENTITY",
        name="0",
        properties={"value": 0, "type": "Natural", "role": "constant"}
    )

    one = graph.add_node(
        fragment_type="ENTITY",
        name="1",
        properties={"value": 1, "type": "Natural", "role": "constant"}
    )

    two = graph.add_node(
        fragment_type="ENTITY",
        name="2",
        properties={"value": 2, "type": "Natural", "role": "constant"}
    )

    # Result entity
    result = graph.add_node(
        fragment_type="ENTITY",
        name="F(n)",
        properties={
            "type": "Natural",
            "role": "output",
            "description": "The nth Fibonacci number"
        }
    )

    # =========================================================================
    # CONSTRAINTS: Guards for different cases
    # =========================================================================

    # Base case constraints
    constraint_n_eq_0 = graph.add_node(
        fragment_type="CONSTRAINT",
        name="n = 0",
        properties={
            "predicate": "equality",
            "left": "n",
            "right": "0",
            "description": "Check if n equals 0"
        }
    )

    constraint_n_eq_1 = graph.add_node(
        fragment_type="CONSTRAINT",
        name="n = 1",
        properties={
            "predicate": "equality",
            "left": "n",
            "right": "1",
            "description": "Check if n equals 1"
        }
    )

    constraint_n_gt_1 = graph.add_node(
        fragment_type="CONSTRAINT",
        name="n > 1",
        properties={
            "predicate": "greater_than",
            "left": "n",
            "right": "1",
            "description": "Check if n is greater than 1 (recursive case)"
        }
    )

    # =========================================================================
    # OPERATORS: Operations performed
    # =========================================================================

    # Subtraction for computing n-1 and n-2
    subtract_op = graph.add_node(
        fragment_type="OPERATOR",
        name="subtract",
        properties={
            "operation": "subtraction",
            "domain": "Natural × Natural",
            "codomain": "Natural",
            "symbol": "-"
        }
    )

    # Addition for combining F(n-1) + F(n-2)
    add_op = graph.add_node(
        fragment_type="OPERATOR",
        name="add",
        properties={
            "operation": "addition",
            "domain": "Natural × Natural",
            "codomain": "Natural",
            "symbol": "+",
            "properties": ["commutative", "associative"]
        }
    )

    # =========================================================================
    # RECURSION: The self-referential structure
    # =========================================================================

    # Main recursion node
    fibonacci_recursion = graph.add_node(
        fragment_type="RECURSION",
        name="Fibonacci",
        properties={
            "type": "tree_recursion",
            "branching_factor": 2,
            "base_cases": 2,
            "recurrence": "F(n) = F(n-1) + F(n-2)",
            "termination": "n ≤ 1"
        }
    )

    # Recursive calls
    fib_n_minus_1 = graph.add_node(
        fragment_type="ENTITY",
        name="F(n-1)",
        properties={
            "type": "Natural",
            "role": "recursive_call",
            "description": "Fibonacci of n-1"
        }
    )

    fib_n_minus_2 = graph.add_node(
        fragment_type="ENTITY",
        name="F(n-2)",
        properties={
            "type": "Natural",
            "role": "recursive_call",
            "description": "Fibonacci of n-2"
        }
    )

    # =========================================================================
    # EDGES: Connecting the fragments
    # =========================================================================

    # Recursion takes input
    graph.add_edge(
        fibonacci_recursion.id, n_input.id, "applies_to",
        properties={"role": "input"}
    )

    # Recursion produces result
    graph.add_edge(
        fibonacci_recursion.id, result.id, "produces",
        properties={"role": "output"}
    )

    # Base case 1: n = 0 guards result = 0
    graph.add_edge(constraint_n_eq_0.id, n_input.id, "constrains")
    graph.add_edge(constraint_n_eq_0.id, zero.id, "produces",
                   properties={"case": "base_case_1"})

    # Base case 2: n = 1 guards result = 1
    graph.add_edge(constraint_n_eq_1.id, n_input.id, "constrains")
    graph.add_edge(constraint_n_eq_1.id, one.id, "produces",
                   properties={"case": "base_case_2"})

    # Recursive case: n > 1 guards recursive computation
    graph.add_edge(constraint_n_gt_1.id, n_input.id, "constrains")

    # Compute n-1
    graph.add_edge(subtract_op.id, n_input.id, "applies_to",
                   properties={"operand": "left"})
    graph.add_edge(subtract_op.id, one.id, "applies_to",
                   properties={"operand": "right"})

    # Compute n-2
    graph.add_edge(subtract_op.id, n_input.id, "applies_to",
                   properties={"operand": "left"})
    graph.add_edge(subtract_op.id, two.id, "applies_to",
                   properties={"operand": "right"})

    # Recursive calls
    graph.add_edge(fibonacci_recursion.id, fib_n_minus_1.id, "wraps",
                   properties={"recursion_depth": "-1"})
    graph.add_edge(fibonacci_recursion.id, fib_n_minus_2.id, "wraps",
                   properties={"recursion_depth": "-2"})

    # Add the results
    graph.add_edge(add_op.id, fib_n_minus_1.id, "applies_to",
                   properties={"operand": "left"})
    graph.add_edge(add_op.id, fib_n_minus_2.id, "applies_to",
                   properties={"operand": "right"})

    # Addition produces final result (when n > 1)
    graph.add_edge(add_op.id, result.id, "produces",
                   properties={"case": "recursive_case"})

    return graph


def analyze_fibonacci_structure(graph: FragmentGraph):
    """Analyze the structure of the Fibonacci graph."""
    print("=" * 80)
    print("FIBONACCI FRAGMENT ANALYSIS")
    print("=" * 80)
    print()

    # Count fragment types
    type_counts = {}
    for node in graph.nodes:
        ftype = node.fragment_type
        type_counts[ftype] = type_counts.get(ftype, 0) + 1

    print("Fragment Composition:")
    for ftype, count in sorted(type_counts.items()):
        print(f"  {ftype}: {count}")

    print()
    print("Edge Types:")
    edge_type_counts = {}
    for edge in graph.edges:
        etype = edge.edge_type
        edge_type_counts[etype] = edge_type_counts.get(etype, 0) + 1

    for etype, count in sorted(edge_type_counts.items()):
        print(f"  {etype}: {count}")

    print()
    print("Structural Properties:")
    print(f"  Total nodes: {len(graph.nodes)}")
    print(f"  Total edges: {len(graph.edges)}")
    print(f"  Base cases: 2 (n=0, n=1)")
    print(f"  Recursive branching: 2 (F(n-1), F(n-2))")


if __name__ == "__main__":
    print("=" * 80)
    print("FIBONACCI RECURSION AS FRAGMENT GRAPH")
    print("=" * 80)
    print()

    # Create the graph
    fib_graph = create_fibonacci_graph()

    # Visualize
    print(fib_graph.visualize())

    print()
    analyze_fibonacci_structure(fib_graph)

    # Save to JSON
    json_output = fib_graph.to_json()

    print()
    print("=" * 80)
    print("JSON REPRESENTATION (first 1500 chars):")
    print("=" * 80)
    print(json_output[:1500] + "...")

    # Save to file
    output_file = "fibonacci_fragment_graph.json"
    with open(output_file, 'w') as f:
        f.write(json_output)
    print()
    print(f"Full graph saved to: {output_file}")

    # Test round-trip
    print()
    print("=" * 80)
    print("ROUND-TRIP TEST:")
    print("=" * 80)
    reconstructed = FragmentGraph.from_json(json_output)
    print(f"Original: {len(fib_graph.nodes)} nodes, {len(fib_graph.edges)} edges")
    print(f"Reconstructed: {len(reconstructed.nodes)} nodes, {len(reconstructed.edges)} edges")
    print(f"Round-trip successful: {len(fib_graph.nodes) == len(reconstructed.nodes)}")
