"""
FRAGMENT GRAPH SCHEMA
=====================

JSON representation of mathematical ideas as typed fragment graphs.

Nodes = Fragments (Entity, Relation, Operator, etc.)
Edges = Typed bindings between fragments

Example: "derivative of x²" becomes a graph of connected fragments.
"""

from typing import Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json
from uuid import uuid4


class EdgeType(Enum):
    """Types of edges between fragments."""
    USES = "uses"                    # Operator uses Measure
    GUARDS = "guards"                # Constraint guards State
    WRAPS = "wraps"                  # Recursion wraps Operator
    APPLIES_TO = "applies_to"        # Operator applies to Entity
    RELATES = "relates"              # Relation connects Entities
    TRANSFORMS_TO = "transforms_to"  # Transform maps Structure
    CONTAINS = "contains"            # Structure contains Entity
    MEASURES = "measures"            # Measure evaluates Entity
    CONSTRAINS = "constrains"        # Constraint limits Operator
    COMPOSES = "composes"            # Operator composes with Operator


@dataclass
class FragmentNode:
    """
    A node in the fragment graph.

    Each node represents one fragment with its type, properties, and data.
    """
    id: str                          # Unique identifier
    fragment_type: str               # One of the 8 fragment types
    name: str                        # Human-readable name
    properties: dict[str, Any]       # Fragment-specific properties
    metadata: Optional[dict] = None  # Optional metadata

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "fragment_type": self.fragment_type,
            "name": self.name,
            "properties": self.properties,
            "metadata": self.metadata or {}
        }

    @staticmethod
    def from_dict(data: dict) -> 'FragmentNode':
        """Create FragmentNode from dictionary."""
        return FragmentNode(
            id=data["id"],
            fragment_type=data["fragment_type"],
            name=data["name"],
            properties=data["properties"],
            metadata=data.get("metadata")
        )


@dataclass
class FragmentEdge:
    """
    An edge in the fragment graph.

    Edges represent typed relationships between fragments.
    """
    id: str                    # Unique identifier
    source_id: str             # Source node ID
    target_id: str             # Target node ID
    edge_type: str             # Type of relationship
    properties: Optional[dict] = None  # Optional edge properties

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": self.edge_type,
            "properties": self.properties or {}
        }

    @staticmethod
    def from_dict(data: dict) -> 'FragmentEdge':
        """Create FragmentEdge from dictionary."""
        return FragmentEdge(
            id=data["id"],
            source_id=data["source_id"],
            target_id=data["target_id"],
            edge_type=data["edge_type"],
            properties=data.get("properties")
        )


@dataclass
class FragmentGraph:
    """
    A complete fragment graph representing a mathematical idea.

    This is the IR - the universal intermediate representation.
    """
    id: str
    name: str
    nodes: list[FragmentNode]
    edges: list[FragmentEdge]
    metadata: Optional[dict] = None

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        data = {
            "id": self.id,
            "name": self.name,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "metadata": self.metadata or {}
        }
        return json.dumps(data, indent=indent)

    @staticmethod
    def from_json(json_str: str) -> 'FragmentGraph':
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        return FragmentGraph(
            id=data["id"],
            name=data["name"],
            nodes=[FragmentNode.from_dict(n) for n in data["nodes"]],
            edges=[FragmentEdge.from_dict(e) for e in data["edges"]],
            metadata=data.get("metadata")
        )

    def add_node(self, fragment_type: str, name: str, properties: dict,
                 metadata: Optional[dict] = None) -> FragmentNode:
        """Add a node to the graph."""
        node = FragmentNode(
            id=str(uuid4()),
            fragment_type=fragment_type,
            name=name,
            properties=properties,
            metadata=metadata
        )
        self.nodes.append(node)
        return node

    def add_edge(self, source_id: str, target_id: str, edge_type: str,
                 properties: Optional[dict] = None) -> FragmentEdge:
        """Add an edge to the graph."""
        edge = FragmentEdge(
            id=str(uuid4()),
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
            properties=properties
        )
        self.edges.append(edge)
        return edge

    def get_node(self, node_id: str) -> Optional[FragmentNode]:
        """Get a node by ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_edges_from(self, node_id: str) -> list[FragmentEdge]:
        """Get all edges originating from a node."""
        return [e for e in self.edges if e.source_id == node_id]

    def get_edges_to(self, node_id: str) -> list[FragmentEdge]:
        """Get all edges pointing to a node."""
        return [e for e in self.edges if e.target_id == node_id]

    def visualize(self) -> str:
        """Create a simple text visualization of the graph."""
        lines = [
            f"Graph: {self.name}",
            f"ID: {self.id}",
            "",
            "NODES:",
            "-" * 60
        ]

        for node in self.nodes:
            lines.append(f"  [{node.fragment_type}] {node.name}")
            lines.append(f"    ID: {node.id}")
            for key, value in node.properties.items():
                lines.append(f"    {key}: {value}")
            lines.append("")

        lines.append("EDGES:")
        lines.append("-" * 60)

        for edge in self.edges:
            source = self.get_node(edge.source_id)
            target = self.get_node(edge.target_id)
            lines.append(
                f"  {source.name} --[{edge.edge_type}]--> {target.name}"
            )

        return "\n".join(lines)


# =============================================================================
# JSON SCHEMA DEFINITION
# =============================================================================

FRAGMENT_GRAPH_JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "FragmentGraph",
    "description": "Universal IR for mathematical ideas",
    "type": "object",
    "required": ["id", "name", "nodes", "edges"],
    "properties": {
        "id": {
            "type": "string",
            "description": "Unique identifier for this graph"
        },
        "name": {
            "type": "string",
            "description": "Human-readable name for this mathematical idea"
        },
        "nodes": {
            "type": "array",
            "description": "Array of fragment nodes",
            "items": {
                "type": "object",
                "required": ["id", "fragment_type", "name", "properties"],
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Unique node identifier"
                    },
                    "fragment_type": {
                        "type": "string",
                        "enum": [
                            "ENTITY", "RELATION", "OPERATOR",
                            "CONSTRAINT", "MEASURE", "STRUCTURE",
                            "TRANSFORM", "RECURSION"
                        ],
                        "description": "Type of fragment"
                    },
                    "name": {
                        "type": "string",
                        "description": "Human-readable name"
                    },
                    "properties": {
                        "type": "object",
                        "description": "Fragment-specific properties"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata"
                    }
                }
            }
        },
        "edges": {
            "type": "array",
            "description": "Array of typed edges between nodes",
            "items": {
                "type": "object",
                "required": ["id", "source_id", "target_id", "edge_type"],
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Unique edge identifier"
                    },
                    "source_id": {
                        "type": "string",
                        "description": "ID of source node"
                    },
                    "target_id": {
                        "type": "string",
                        "description": "ID of target node"
                    },
                    "edge_type": {
                        "type": "string",
                        "enum": [
                            "uses", "guards", "wraps", "applies_to",
                            "relates", "transforms_to", "contains",
                            "measures", "constrains", "composes"
                        ],
                        "description": "Type of relationship"
                    },
                    "properties": {
                        "type": "object",
                        "description": "Optional edge properties"
                    }
                }
            }
        },
        "metadata": {
            "type": "object",
            "description": "Optional graph metadata"
        }
    }
}


def save_schema(filepath: str = "fragment_graph_schema.json"):
    """Save the JSON schema to a file."""
    with open(filepath, 'w') as f:
        json.dump(FRAGMENT_GRAPH_JSON_SCHEMA, f, indent=2)
    print(f"Schema saved to {filepath}")


# =============================================================================
# EXAMPLE: Simple arithmetic expression "2 + 3"
# =============================================================================

def example_simple_addition():
    """Example: Decompose '2 + 3' into fragment graph."""

    # Create graph
    graph = FragmentGraph(
        id=str(uuid4()),
        name="Simple Addition: 2 + 3",
        nodes=[],
        edges=[]
    )

    # Create entities for numbers
    two = graph.add_node(
        fragment_type="ENTITY",
        name="2",
        properties={"value": 2, "type": "Natural"}
    )

    three = graph.add_node(
        fragment_type="ENTITY",
        name="3",
        properties={"value": 3, "type": "Natural"}
    )

    # Create operator for addition
    add_op = graph.add_node(
        fragment_type="OPERATOR",
        name="+",
        properties={
            "operation": "addition",
            "domain": "Natural",
            "codomain": "Natural",
            "properties": ["commutative", "associative"]
        }
    )

    # Create result entity
    result = graph.add_node(
        fragment_type="ENTITY",
        name="5",
        properties={"value": 5, "type": "Natural"}
    )

    # Connect with edges
    graph.add_edge(add_op.id, two.id, "applies_to",
                   properties={"position": "left"})
    graph.add_edge(add_op.id, three.id, "applies_to",
                   properties={"position": "right"})
    graph.add_edge(add_op.id, result.id, "produces")

    return graph


if __name__ == "__main__":
    print("=" * 80)
    print("FRAGMENT GRAPH JSON SCHEMA")
    print("=" * 80)
    print()

    # Save schema
    save_schema()

    print()
    print("=" * 80)
    print("EXAMPLE: Simple Addition (2 + 3)")
    print("=" * 80)
    print()

    # Create example graph
    graph = example_simple_addition()

    # Visualize
    print(graph.visualize())

    print()
    print("=" * 80)
    print("JSON REPRESENTATION:")
    print("=" * 80)
    print(graph.to_json())

    # Test round-trip
    print()
    print("=" * 80)
    print("ROUND-TRIP TEST:")
    print("=" * 80)
    json_str = graph.to_json()
    reconstructed = FragmentGraph.from_json(json_str)
    print(f"Original nodes: {len(graph.nodes)}")
    print(f"Reconstructed nodes: {len(reconstructed.nodes)}")
    print(f"Round-trip successful: {len(graph.nodes) == len(reconstructed.nodes)}")
