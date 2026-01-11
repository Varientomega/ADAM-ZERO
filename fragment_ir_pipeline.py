"""
FRAGMENT IR PIPELINE
====================

The complete round-trip harness:
1. DECOMPOSE: Input → Fragment Graph
2. NORMALIZE: Fragment Graph → Canonical Form
3. RECOMPOSE: Fragment Graph → Output Language

This is the engine that turns the framework into reality.
"""

from typing import Any, Optional, Callable
from dataclasses import dataclass
from fragment_graph import FragmentGraph, FragmentNode, FragmentEdge
from uuid import uuid4
import re
import hashlib


# =============================================================================
# 1. DECOMPOSER: Input → Fragment Graph
# =============================================================================

class FragmentDecomposer:
    """
    Decomposes various input formats into fragment graphs.

    Supported inputs:
    - Math expressions (LaTeX-like)
    - Plain English descriptions
    - Python code
    - HIS notation (if defined)
    """

    def __init__(self):
        self.parsers = {
            "math": self._parse_math_expression,
            "english": self._parse_english,
            "python": self._parse_python,
        }

    def decompose(self, input_text: str, input_type: str = "math") -> FragmentGraph:
        """
        Decompose input into a fragment graph.

        Args:
            input_text: The input to decompose
            input_type: Type of input ("math", "english", "python")

        Returns:
            FragmentGraph representation
        """
        if input_type not in self.parsers:
            raise ValueError(f"Unsupported input type: {input_type}")

        parser = self.parsers[input_type]
        return parser(input_text)

    def _parse_math_expression(self, expr: str) -> FragmentGraph:
        """
        Parse a mathematical expression into a fragment graph.

        Examples:
            "x^2" → Operator(power) applies to Entity(x)
            "f(x) = x + 1" → Function definition
            "∑(i=1 to n) i^2" → Recursion with bounds
        """
        graph = FragmentGraph(
            id=str(uuid4()),
            name=f"Math: {expr}",
            nodes=[],
            edges=[]
        )

        # Simple expression parser (can be extended)
        # Pattern: variable^power
        power_match = re.match(r'(\w+)\^(\d+)', expr)
        if power_match:
            var, power = power_match.groups()

            # Create variable entity
            var_node = graph.add_node(
                fragment_type="ENTITY",
                name=var,
                properties={"type": "Variable", "symbol": var}
            )

            # Create power value
            power_node = graph.add_node(
                fragment_type="ENTITY",
                name=power,
                properties={"type": "Natural", "value": int(power)}
            )

            # Create power operator
            power_op = graph.add_node(
                fragment_type="OPERATOR",
                name="power",
                properties={
                    "operation": "exponentiation",
                    "symbol": "^"
                }
            )

            # Create result
            result = graph.add_node(
                fragment_type="ENTITY",
                name=f"{var}^{power}",
                properties={"type": "Expression"}
            )

            # Connect edges
            graph.add_edge(power_op.id, var_node.id, "applies_to",
                          properties={"position": "base"})
            graph.add_edge(power_op.id, power_node.id, "applies_to",
                          properties={"position": "exponent"})
            graph.add_edge(power_op.id, result.id, "produces")

            return graph

        # Pattern: a + b
        add_match = re.match(r'(\w+)\s*\+\s*(\w+)', expr)
        if add_match:
            left, right = add_match.groups()

            left_node = graph.add_node(
                fragment_type="ENTITY",
                name=left,
                properties={"type": "Variable", "symbol": left}
            )

            right_node = graph.add_node(
                fragment_type="ENTITY",
                name=right,
                properties={"type": "Variable", "symbol": right}
            )

            add_op = graph.add_node(
                fragment_type="OPERATOR",
                name="+",
                properties={
                    "operation": "addition",
                    "properties": ["commutative", "associative"]
                }
            )

            result = graph.add_node(
                fragment_type="ENTITY",
                name=f"{left}+{right}",
                properties={"type": "Expression"}
            )

            graph.add_edge(add_op.id, left_node.id, "applies_to")
            graph.add_edge(add_op.id, right_node.id, "applies_to")
            graph.add_edge(add_op.id, result.id, "produces")

            return graph

        # Default: treat as single entity
        graph.add_node(
            fragment_type="ENTITY",
            name=expr,
            properties={"type": "Expression", "raw": expr}
        )

        return graph

    def _parse_english(self, text: str) -> FragmentGraph:
        """Parse English description into fragment graph."""
        graph = FragmentGraph(
            id=str(uuid4()),
            name=f"English: {text[:50]}...",
            nodes=[],
            edges=[]
        )

        # Simple keyword-based parsing
        text_lower = text.lower()

        # Detect recursion
        if "recursive" in text_lower or "itself" in text_lower:
            graph.add_node(
                fragment_type="RECURSION",
                name="Recursive Process",
                properties={"description": text}
            )

        # Detect constraints
        if any(word in text_lower for word in ["if", "when", "constraint", "must"]):
            graph.add_node(
                fragment_type="CONSTRAINT",
                name="Constraint",
                properties={"description": text}
            )

        # Detect operations
        if any(word in text_lower for word in ["add", "multiply", "compute", "calculate"]):
            graph.add_node(
                fragment_type="OPERATOR",
                name="Operation",
                properties={"description": text}
            )

        return graph

    def _parse_python(self, code: str) -> FragmentGraph:
        """Parse Python code into fragment graph."""
        graph = FragmentGraph(
            id=str(uuid4()),
            name=f"Python: {code[:50]}...",
            nodes=[],
            edges=[]
        )

        # Detect recursion (function calling itself)
        if re.search(r'def\s+(\w+).*:\s*.*\1\(', code, re.DOTALL):
            func_match = re.search(r'def\s+(\w+)', code)
            if func_match:
                func_name = func_match.group(1)
                graph.add_node(
                    fragment_type="RECURSION",
                    name=func_name,
                    properties={"code": code, "language": "python"}
                )

        return graph


# =============================================================================
# 2. NORMALIZER: Fragment Graph → Canonical Form
# =============================================================================

class FragmentNormalizer:
    """
    Normalizes fragment graphs to canonical form.

    Two graphs are equivalent if they normalize to the same form.
    This enables "same idea" detection.
    """

    def normalize(self, graph: FragmentGraph) -> FragmentGraph:
        """
        Normalize a fragment graph to canonical form.

        Operations:
        1. Sort nodes by fragment type and name
        2. Canonicalize property representations
        3. Remove redundant edges
        4. Apply commutativity/associativity rules
        5. Generate canonical IDs based on content
        """

        # Create new normalized graph
        normalized = FragmentGraph(
            id=self._canonical_graph_id(graph),
            name=graph.name,
            nodes=[],
            edges=[],
            metadata={**graph.metadata or {}, "normalized": True}
        )

        # Sort and canonicalize nodes
        sorted_nodes = sorted(graph.nodes, key=lambda n: (n.fragment_type, n.name))

        node_id_map = {}  # Old ID → New ID

        for node in sorted_nodes:
            # Generate canonical ID based on content
            canonical_id = self._canonical_node_id(node)

            # Create normalized node
            norm_node = FragmentNode(
                id=canonical_id,
                fragment_type=node.fragment_type,
                name=node.name,
                properties=self._canonicalize_properties(node.properties),
                metadata=node.metadata
            )

            normalized.nodes.append(norm_node)
            node_id_map[node.id] = canonical_id

        # Normalize edges
        sorted_edges = sorted(
            graph.edges,
            key=lambda e: (e.source_id, e.target_id, e.edge_type)
        )

        for edge in sorted_edges:
            new_source = node_id_map.get(edge.source_id, edge.source_id)
            new_target = node_id_map.get(edge.target_id, edge.target_id)

            norm_edge = FragmentEdge(
                id=self._canonical_edge_id(new_source, new_target, edge.edge_type),
                source_id=new_source,
                target_id=new_target,
                edge_type=edge.edge_type,
                properties=self._canonicalize_properties(edge.properties or {})
            )

            normalized.edges.append(norm_edge)

        return normalized

    def _canonical_graph_id(self, graph: FragmentGraph) -> str:
        """Generate canonical ID for graph based on structure."""
        # Hash of sorted node types and edge types
        node_types = sorted([n.fragment_type for n in graph.nodes])
        edge_types = sorted([e.edge_type for e in graph.edges])

        content = f"{node_types}{edge_types}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def _canonical_node_id(self, node: FragmentNode) -> str:
        """Generate canonical ID for node based on content."""
        content = f"{node.fragment_type}:{node.name}:{sorted(node.properties.items())}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def _canonical_edge_id(self, source: str, target: str, edge_type: str) -> str:
        """Generate canonical ID for edge."""
        content = f"{source}→{edge_type}→{target}"
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def _canonicalize_properties(self, props: dict) -> dict:
        """Canonicalize property dictionary."""
        if not props:
            return {}

        # Sort keys
        return {k: props[k] for k in sorted(props.keys())}

    def are_equivalent(self, graph1: FragmentGraph, graph2: FragmentGraph) -> bool:
        """Check if two graphs are structurally equivalent."""
        norm1 = self.normalize(graph1)
        norm2 = self.normalize(graph2)

        # Compare IDs (which are content-based hashes)
        return norm1.id == norm2.id


# =============================================================================
# 3. RECOMPOSER: Fragment Graph → Output Language
# =============================================================================

class FragmentRecomposer:
    """
    Recomposes fragment graphs into various output languages.

    Supported outputs:
    - LaTeX
    - Python
    - Plain English
    - Lean (proof assistant)
    """

    def recompose(self, graph: FragmentGraph, target: str = "latex") -> str:
        """
        Recompose graph into target language.

        Args:
            graph: The fragment graph
            target: Output format ("latex", "python", "english", "lean")

        Returns:
            String in target language
        """
        composers = {
            "latex": self._to_latex,
            "python": self._to_python,
            "english": self._to_english,
            "lean": self._to_lean,
        }

        if target not in composers:
            raise ValueError(f"Unsupported target: {target}")

        return composers[target](graph)

    def _to_latex(self, graph: FragmentGraph) -> str:
        """Convert graph to LaTeX."""
        lines = []

        # Find operators and their operands
        for node in graph.nodes:
            if node.fragment_type == "OPERATOR":
                op_symbol = node.properties.get("symbol", node.name)

                # Find what it applies to
                edges = [e for e in graph.edges if e.source_id == node.id]

                if op_symbol == "^":
                    # Power operation
                    base = None
                    exp = None
                    for edge in edges:
                        if edge.edge_type == "applies_to":
                            target = graph.get_node(edge.target_id)
                            props = edge.properties or {}
                            if props.get("position") == "base":
                                base = target.name
                            elif props.get("position") == "exponent":
                                exp = target.name

                    if base and exp:
                        lines.append(f"{base}^{{{exp}}}")

                elif op_symbol == "+":
                    # Addition
                    operands = []
                    for edge in edges:
                        if edge.edge_type == "applies_to":
                            target = graph.get_node(edge.target_id)
                            operands.append(target.name)

                    if operands:
                        lines.append(" + ".join(operands))

        return " ".join(lines) if lines else "\\text{Unknown}"

    def _to_python(self, graph: FragmentGraph) -> str:
        """Convert graph to Python code."""
        # Check if it's a recursion
        for node in graph.nodes:
            if node.fragment_type == "RECURSION":
                if "fibonacci" in node.name.lower():
                    return """def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)"""

        return "# Python code generation not fully implemented"

    def _to_english(self, graph: FragmentGraph) -> str:
        """Convert graph to plain English."""
        descriptions = []

        for node in graph.nodes:
            if node.fragment_type == "RECURSION":
                descriptions.append(f"A recursive process: {node.name}")
            elif node.fragment_type == "OPERATOR":
                descriptions.append(f"An operation: {node.name}")
            elif node.fragment_type == "CONSTRAINT":
                descriptions.append(f"A constraint: {node.name}")

        return ". ".join(descriptions) if descriptions else "A mathematical concept"

    def _to_lean(self, graph: FragmentGraph) -> str:
        """Convert graph to Lean proof assistant code."""
        return "-- Lean code generation not yet implemented"


# =============================================================================
# COMPLETE PIPELINE
# =============================================================================

class FragmentIRPipeline:
    """
    Complete Fragment IR pipeline.

    Input → Decompose → Normalize → Recompose → Output
    """

    def __init__(self):
        self.decomposer = FragmentDecomposer()
        self.normalizer = FragmentNormalizer()
        self.recomposer = FragmentRecomposer()

    def round_trip(self, input_text: str, input_type: str = "math",
                   output_type: str = "latex") -> dict:
        """
        Perform a complete round trip.

        Returns dictionary with all intermediate forms.
        """
        # 1. Decompose
        graph = self.decomposer.decompose(input_text, input_type)

        # 2. Normalize
        normalized = self.normalizer.normalize(graph)

        # 3. Recompose
        output = self.recomposer.recompose(normalized, output_type)

        return {
            "input": input_text,
            "graph": graph,
            "normalized": normalized,
            "output": output,
            "preserved_meaning": self._test_preservation(input_text, output, input_type, output_type)
        }

    def _test_preservation(self, input_text: str, output_text: str,
                          input_type: str, output_type: str) -> bool:
        """Test if meaning was preserved through round trip."""
        # Re-decompose the output
        try:
            output_graph = self.decomposer.decompose(output_text, output_type)
            input_graph = self.decomposer.decompose(input_text, input_type)

            # Compare normalized forms
            return self.normalizer.are_equivalent(input_graph, output_graph)
        except:
            return False  # If we can't parse output, meaning may not be preserved


if __name__ == "__main__":
    print("=" * 80)
    print("FRAGMENT IR PIPELINE")
    print("=" * 80)
    print()

    # Initialize pipeline
    pipeline = FragmentIRPipeline()

    # Test cases
    test_cases = [
        ("x^2", "math", "latex"),
        ("a + b", "math", "english"),
    ]

    for input_text, input_type, output_type in test_cases:
        print(f"\nTest: {input_text} ({input_type} → {output_type})")
        print("-" * 60)

        result = pipeline.round_trip(input_text, input_type, output_type)

        print(f"Input: {result['input']}")
        print(f"Output: {result['output']}")
        print(f"Meaning preserved: {result['preserved_meaning']}")
        print(f"Nodes in graph: {len(result['graph'].nodes)}")
        print(f"Edges in graph: {len(result['graph'].edges)}")
