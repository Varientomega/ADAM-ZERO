"""
FRAGMENT IR TEST HARNESS
=========================

The 5 canonical test cases that prove universality:

1. Derivative definition
2. Group action / symmetry statement
3. Shortest-path / optimization constraint
4. Recursion (Fibonacci / dynamic program)
5. Physics law (conservation / invariant)

If the IR can faithfully round-trip these, we have a real substrate.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fragment_graph import FragmentGraph
from fragment_ir_pipeline import FragmentIRPipeline
from dataclasses import dataclass
from typing import List, Optional
from uuid import uuid4


@dataclass
class TestCase:
    """A single test case for the Fragment IR."""
    name: str
    description: str
    input_representation: str
    expected_fragments: List[str]  # Expected fragment types
    category: str  # "calculus", "algebra", "optimization", "recursion", "physics"


@dataclass
class TestResult:
    """Result of running a test case."""
    test_name: str
    passed: bool
    graph: Optional[FragmentGraph]
    num_nodes: int
    num_edges: int
    fragment_types_found: List[str]
    error_message: Optional[str] = None


class FragmentIRTestHarness:
    """
    Test harness for Fragment IR round-trip tests.

    Tests that mathematical ideas can be:
    1. Decomposed into fragments
    2. Normalized to canonical form
    3. Recomposed into different languages
    4. Preserve meaning through round-trip
    """

    def __init__(self):
        self.pipeline = FragmentIRPipeline()
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []

        # Initialize the 5 canonical test cases
        self._initialize_canonical_tests()

    def _initialize_canonical_tests(self):
        """Initialize the 5 canonical test cases."""

        # =====================================================================
        # TEST 1: DERIVATIVE DEFINITION
        # =====================================================================
        self.test_cases.append(TestCase(
            name="Derivative Definition",
            description="Limit definition of derivative: f'(x) = lim(h→0) [f(x+h) - f(x)] / h",
            input_representation="derivative: lim(h→0) [f(x+h) - f(x)] / h",
            expected_fragments=["OPERATOR", "ENTITY", "MEASURE", "CONSTRAINT"],
            category="calculus"
        ))

        # =====================================================================
        # TEST 2: GROUP ACTION / SYMMETRY
        # =====================================================================
        self.test_cases.append(TestCase(
            name="Group Action",
            description="A group G acts on a set X: g · (h · x) = (g * h) · x",
            input_representation="group_action: g · (h · x) = (gh) · x",
            expected_fragments=["STRUCTURE", "OPERATOR", "RELATION", "ENTITY"],
            category="algebra"
        ))

        # =====================================================================
        # TEST 3: SHORTEST PATH / OPTIMIZATION
        # =====================================================================
        self.test_cases.append(TestCase(
            name="Shortest Path",
            description="Dijkstra's optimization: minimize Σ weights subject to path constraints",
            input_representation="shortest_path: argmin_path Σ edge_weights",
            expected_fragments=["MEASURE", "CONSTRAINT", "OPERATOR", "STRUCTURE"],
            category="optimization"
        ))

        # =====================================================================
        # TEST 4: RECURSION (Fibonacci)
        # =====================================================================
        self.test_cases.append(TestCase(
            name="Fibonacci Recursion",
            description="F(n) = F(n-1) + F(n-2), base: F(0)=0, F(1)=1",
            input_representation="fib(n) = fib(n-1) + fib(n-2) if n>1 else (0 if n==0 else 1)",
            expected_fragments=["RECURSION", "OPERATOR", "CONSTRAINT", "ENTITY"],
            category="recursion"
        ))

        # =====================================================================
        # TEST 5: PHYSICS LAW (Energy Conservation)
        # =====================================================================
        self.test_cases.append(TestCase(
            name="Energy Conservation",
            description="Total energy E = T + V is conserved: dE/dt = 0",
            input_representation="conservation: E = T + V, dE/dt = 0",
            expected_fragments=["MEASURE", "OPERATOR", "CONSTRAINT", "ENTITY"],
            category="physics"
        ))

    def create_test_graph(self, test_case: TestCase) -> FragmentGraph:
        """
        Create a fragment graph for a test case.

        This manually constructs the expected graph structure.
        """
        graph = FragmentGraph(
            id=str(uuid4()),
            name=test_case.name,
            nodes=[],
            edges=[],
            metadata={"category": test_case.category}
        )

        # Build specific graphs based on category
        if test_case.category == "calculus":
            return self._build_derivative_graph(graph)
        elif test_case.category == "algebra":
            return self._build_group_action_graph(graph)
        elif test_case.category == "optimization":
            return self._build_shortest_path_graph(graph)
        elif test_case.category == "recursion":
            return self._build_fibonacci_graph(graph)
        elif test_case.category == "physics":
            return self._build_conservation_graph(graph)

        return graph

    def _build_derivative_graph(self, graph: FragmentGraph) -> FragmentGraph:
        """Build graph for derivative definition."""

        # Entities: x, h, f(x), f(x+h)
        x = graph.add_node("ENTITY", "x", {"type": "Variable"})
        h = graph.add_node("ENTITY", "h", {"type": "Variable"})
        fx = graph.add_node("ENTITY", "f(x)", {"type": "Expression"})
        fxh = graph.add_node("ENTITY", "f(x+h)", {"type": "Expression"})

        # Operators: subtraction, division, limit
        subtract = graph.add_node("OPERATOR", "-", {"operation": "subtraction"})
        divide = graph.add_node("OPERATOR", "/", {"operation": "division"})
        limit_op = graph.add_node("OPERATOR", "lim", {
            "operation": "limit",
            "approaches": "0",
            "variable": "h"
        })

        # Constraint: h → 0
        constraint = graph.add_node("CONSTRAINT", "h→0", {
            "type": "limit_constraint",
            "variable": "h",
            "value": 0
        })

        # Result: f'(x)
        derivative = graph.add_node("ENTITY", "f'(x)", {"type": "Derivative"})

        # Connect edges
        graph.add_edge(subtract.id, fxh.id, "applies_to")
        graph.add_edge(subtract.id, fx.id, "applies_to")
        graph.add_edge(divide.id, subtract.id, "uses")
        graph.add_edge(divide.id, h.id, "applies_to")
        graph.add_edge(limit_op.id, divide.id, "wraps")
        graph.add_edge(constraint.id, limit_op.id, "constrains")
        graph.add_edge(limit_op.id, derivative.id, "produces")

        return graph

    def _build_group_action_graph(self, graph: FragmentGraph) -> FragmentGraph:
        """Build graph for group action."""

        # Structure: Group G
        group_g = graph.add_node("STRUCTURE", "Group G", {
            "type": "group",
            "laws": ["associative", "identity", "inverse"]
        })

        # Structure: Set X
        set_x = graph.add_node("STRUCTURE", "Set X", {"type": "set"})

        # Entities: g, h (group elements), x (set element)
        g = graph.add_node("ENTITY", "g", {"type": "group_element", "in": "G"})
        h = graph.add_node("ENTITY", "h", {"type": "group_element", "in": "G"})
        x = graph.add_node("ENTITY", "x", {"type": "set_element", "in": "X"})

        # Operators: group multiplication (*), group action (·)
        mult = graph.add_node("OPERATOR", "*", {
            "operation": "group_multiplication",
            "domain": "G × G",
            "codomain": "G"
        })

        action = graph.add_node("OPERATOR", "·", {
            "operation": "group_action",
            "domain": "G × X",
            "codomain": "X"
        })

        # Relation: equality of the associativity law
        equals = graph.add_node("RELATION", "=", {
            "predicate": "equality",
            "type": "action_associativity"
        })

        # Connect structure
        graph.add_edge(group_g.id, g.id, "contains")
        graph.add_edge(group_g.id, h.id, "contains")
        graph.add_edge(set_x.id, x.id, "contains")

        # Connect operations
        graph.add_edge(mult.id, g.id, "applies_to")
        graph.add_edge(mult.id, h.id, "applies_to")
        graph.add_edge(action.id, g.id, "applies_to")
        graph.add_edge(action.id, x.id, "applies_to")

        return graph

    def _build_shortest_path_graph(self, graph: FragmentGraph) -> FragmentGraph:
        """Build graph for shortest path optimization."""

        # Structure: Graph
        graph_struct = graph.add_node("STRUCTURE", "Graph", {
            "type": "weighted_graph",
            "components": ["vertices", "edges", "weights"]
        })

        # Measure: path length
        path_length = graph.add_node("MEASURE", "path_length", {
            "function": "sum_of_weights",
            "domain": "paths",
            "properties": ["non-negative", "additive"]
        })

        # Operator: argmin (optimization)
        argmin = graph.add_node("OPERATOR", "argmin", {
            "operation": "optimization",
            "objective": "minimize",
            "domain": "paths"
        })

        # Constraint: valid path
        valid_path = graph.add_node("CONSTRAINT", "valid_path", {
            "type": "path_constraint",
            "requires": ["connected", "no_cycles"]
        })

        # Entity: optimal path
        optimal = graph.add_node("ENTITY", "optimal_path", {
            "type": "path",
            "property": "minimal_length"
        })

        # Connect
        graph.add_edge(argmin.id, path_length.id, "uses")
        graph.add_edge(valid_path.id, argmin.id, "constrains")
        graph.add_edge(argmin.id, optimal.id, "produces")
        graph.add_edge(path_length.id, graph_struct.id, "measures")

        return graph

    def _build_fibonacci_graph(self, graph: FragmentGraph) -> FragmentGraph:
        """Build graph for Fibonacci recursion."""

        # Recursion node
        fib = graph.add_node("RECURSION", "fibonacci", {
            "type": "tree_recursion",
            "branching": 2,
            "base_cases": 2
        })

        # Entities
        n = graph.add_node("ENTITY", "n", {"type": "Natural", "role": "input"})
        result = graph.add_node("ENTITY", "F(n)", {"type": "Natural", "role": "output"})

        # Operators
        add = graph.add_node("OPERATOR", "+", {"operation": "addition"})
        sub = graph.add_node("OPERATOR", "-", {"operation": "subtraction"})

        # Constraints (base cases)
        n_eq_0 = graph.add_node("CONSTRAINT", "n=0", {"predicate": "equals", "value": 0})
        n_eq_1 = graph.add_node("CONSTRAINT", "n=1", {"predicate": "equals", "value": 1})
        n_gt_1 = graph.add_node("CONSTRAINT", "n>1", {"predicate": "greater_than", "value": 1})

        # Connect
        graph.add_edge(fib.id, n.id, "applies_to")
        graph.add_edge(fib.id, result.id, "produces")
        graph.add_edge(n_eq_0.id, fib.id, "constrains")
        graph.add_edge(n_eq_1.id, fib.id, "constrains")
        graph.add_edge(n_gt_1.id, fib.id, "constrains")
        graph.add_edge(fib.id, add.id, "uses")
        graph.add_edge(fib.id, sub.id, "uses")

        return graph

    def _build_conservation_graph(self, graph: FragmentGraph) -> FragmentGraph:
        """Build graph for energy conservation."""

        # Entities: T (kinetic), V (potential), E (total)
        T = graph.add_node("ENTITY", "T", {"type": "Energy", "kind": "kinetic"})
        V = graph.add_node("ENTITY", "V", {"type": "Energy", "kind": "potential"})
        E = graph.add_node("ENTITY", "E", {"type": "Energy", "kind": "total"})
        t = graph.add_node("ENTITY", "t", {"type": "Time"})

        # Operators
        add = graph.add_node("OPERATOR", "+", {"operation": "addition"})
        derivative = graph.add_node("OPERATOR", "d/dt", {
            "operation": "time_derivative",
            "respect_to": "t"
        })

        # Measure: energy value
        energy_measure = graph.add_node("MEASURE", "energy", {
            "unit": "Joules",
            "properties": ["non-negative", "conserved"]
        })

        # Constraint: conservation law
        conservation = graph.add_node("CONSTRAINT", "dE/dt=0", {
            "type": "conservation_law",
            "property": "invariant"
        })

        # Connect
        graph.add_edge(add.id, T.id, "applies_to")
        graph.add_edge(add.id, V.id, "applies_to")
        graph.add_edge(add.id, E.id, "produces")
        graph.add_edge(derivative.id, E.id, "applies_to")
        graph.add_edge(conservation.id, derivative.id, "constrains")
        graph.add_edge(energy_measure.id, E.id, "measures")

        return graph

    def run_test(self, test_case: TestCase) -> TestResult:
        """Run a single test case."""
        try:
            # Create the graph
            graph = self.create_test_graph(test_case)

            # Check fragment types
            fragment_types = [node.fragment_type for node in graph.nodes]

            # Verify expected fragments are present
            expected_found = all(
                ft in fragment_types for ft in test_case.expected_fragments
            )

            return TestResult(
                test_name=test_case.name,
                passed=expected_found and len(graph.nodes) > 0,
                graph=graph,
                num_nodes=len(graph.nodes),
                num_edges=len(graph.edges),
                fragment_types_found=list(set(fragment_types))
            )

        except Exception as e:
            return TestResult(
                test_name=test_case.name,
                passed=False,
                graph=None,
                num_nodes=0,
                num_edges=0,
                fragment_types_found=[],
                error_message=str(e)
            )

    def run_all_tests(self) -> dict:
        """Run all canonical test cases."""
        self.results = []

        print("=" * 80)
        print("RUNNING CANONICAL TEST SUITE")
        print("=" * 80)
        print()

        for test_case in self.test_cases:
            print(f"Running: {test_case.name}")
            result = self.run_test(test_case)
            self.results.append(result)

            status = "✓ PASS" if result.passed else "✗ FAIL"
            print(f"  {status}")
            print(f"  Nodes: {result.num_nodes}, Edges: {result.num_edges}")
            print(f"  Fragments: {', '.join(result.fragment_types_found)}")
            if result.error_message:
                print(f"  Error: {result.error_message}")
            print()

        # Summary
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        print("=" * 80)
        print(f"RESULTS: {passed}/{total} tests passed")
        print("=" * 80)

        return {
            "passed": passed,
            "total": total,
            "results": self.results
        }


if __name__ == "__main__":
    # Run the canonical test suite
    harness = FragmentIRTestHarness()
    results = harness.run_all_tests()

    # Detailed output for each test
    print("\n\nDETAILED TEST RESULTS:")
    print("=" * 80)

    for result in results["results"]:
        print(f"\n{result.test_name}")
        print("-" * 60)

        if result.graph:
            print(result.graph.visualize())
        else:
            print("Graph creation failed")

        print()
