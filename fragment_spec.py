"""
FRAGMENT IR SPECIFICATION
=========================

The 8 Core Fragments - Universal IR for Mathematical Ideas
Like LLVM IR, but for math.

Each fragment is typed and composable.
"""

from typing import Any, Callable, TypeVar, Generic
from dataclasses import dataclass
from enum import Enum

# Type variables for generic fragments
A = TypeVar('A')
B = TypeVar('B')
T = TypeVar('T')


class FragmentType(Enum):
    """The 8 fundamental fragment types."""
    ENTITY = "entity"           # Atomic objects
    RELATION = "relation"       # Typed predicates
    OPERATOR = "operator"       # Typed functions/morphisms
    CONSTRAINT = "constraint"   # Filters/guards on states
    MEASURE = "measure"         # Evaluation functionals
    STRUCTURE = "structure"     # Containers + laws
    TRANSFORM = "transform"     # Rewrites/maps between structures
    RECURSION = "recursion"     # Self-application + stop rule


# =============================================================================
# 1. ENTITY (or Element)
# =============================================================================
# Type signature: Entity[T] - atomic object of type T
# Purpose: The "nouns" of your mathematical universe

@dataclass
class Entity(Generic[T]):
    """
    An atomic object in the mathematical universe.

    Signature: Entity[T]

    Example:
        n = Entity(value=5, type_name="Natural")  # A natural number
        x = Entity(value="x", type_name="Variable")  # A symbolic variable
    """
    value: T
    type_name: str
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


# Example usage:
ENTITY_EXAMPLE = Entity(value=5, type_name="Natural")


# =============================================================================
# 2. RELATION
# =============================================================================
# Type signature: Relation[A, B] -> Bool
# Purpose: Typed predicates that connect entities

@dataclass
class Relation(Generic[A, B]):
    """
    A typed predicate between two types.

    Signature: Relation[A, B]: (A, B) -> Bool

    Example:
        less_than = Relation(
            name="<",
            predicate=lambda x, y: x < y,
            domain_type="Real",
            codomain_type="Real"
        )

        # Test: 3 < 5 ?
        less_than.test(3, 5)  # Returns True
    """
    name: str
    predicate: Callable[[A, B], bool]
    domain_type: str
    codomain_type: str
    properties: list = None  # e.g., ["reflexive", "transitive"]

    def __post_init__(self):
        if self.properties is None:
            self.properties = []

    def test(self, a: A, b: B) -> bool:
        """Test if the relation holds between a and b."""
        return self.predicate(a, b)


# Example usage:
RELATION_EXAMPLE = Relation(
    name="<",
    predicate=lambda x, y: x < y,
    domain_type="Real",
    codomain_type="Real",
    properties=["transitive", "irreflexive"]
)


# =============================================================================
# 3. OPERATOR
# =============================================================================
# Type signature: Operator[A, B]: A -> B
# Purpose: Typed functions/morphisms

@dataclass
class Operator(Generic[A, B]):
    """
    A typed function/morphism from one type to another.

    Signature: Operator[A, B]: A -> B

    Example:
        square = Operator(
            name="square",
            function=lambda x: x ** 2,
            domain_type="Real",
            codomain_type="Real"
        )

        square.apply(5)  # Returns 25
    """
    name: str
    function: Callable[[A], B]
    domain_type: str
    codomain_type: str
    properties: list = None  # e.g., ["linear", "bijective", "continuous"]

    def __post_init__(self):
        if self.properties is None:
            self.properties = []

    def apply(self, x: A) -> B:
        """Apply the operator to input x."""
        return self.function(x)


# Example usage:
OPERATOR_EXAMPLE = Operator(
    name="square",
    function=lambda x: x ** 2,
    domain_type="Real",
    codomain_type="Real",
    properties=["continuous", "monotonic_positive"]
)


# =============================================================================
# 4. CONSTRAINT
# =============================================================================
# Type signature: Constraint[A]: A -> Bool
# Purpose: Guards/filters on states

@dataclass
class Constraint(Generic[A]):
    """
    A filter or guard on states.

    Signature: Constraint[A]: A -> Bool

    Example:
        positive = Constraint(
            name="positive",
            predicate=lambda x: x > 0,
            type_name="Real"
        )

        positive.check(5)   # True
        positive.check(-3)  # False
    """
    name: str
    predicate: Callable[[A], bool]
    type_name: str
    description: str = ""

    def check(self, x: A) -> bool:
        """Check if x satisfies the constraint."""
        return self.predicate(x)


# Example usage:
CONSTRAINT_EXAMPLE = Constraint(
    name="positive",
    predicate=lambda x: x > 0,
    type_name="Real",
    description="Value must be greater than zero"
)


# =============================================================================
# 5. MEASURE
# =============================================================================
# Type signature: Measure[A]: A -> Real
# Purpose: Evaluation functionals

@dataclass
class Measure(Generic[A]):
    """
    An evaluation functional that maps to a real number.

    Signature: Measure[A]: A -> ℝ

    Example:
        length = Measure(
            name="length",
            function=lambda lst: len(lst),
            domain_type="List",
            properties=["non-negative", "integer-valued"]
        )

        length.evaluate([1, 2, 3])  # Returns 3
    """
    name: str
    function: Callable[[A], float]
    domain_type: str
    properties: list = None  # e.g., ["non-negative", "additive", "normalized"]

    def __post_init__(self):
        if self.properties is None:
            self.properties = []

    def evaluate(self, x: A) -> float:
        """Evaluate the measure on x."""
        return self.function(x)


# Example usage:
MEASURE_EXAMPLE = Measure(
    name="norm",
    function=lambda x: abs(x),
    domain_type="Real",
    properties=["non-negative", "definite", "subadditive"]
)


# =============================================================================
# 6. STRUCTURE
# =============================================================================
# Type signature: Structure[T] = (Container[T], Laws)
# Purpose: Container + laws that govern it

@dataclass
class Structure(Generic[T]):
    """
    A container with laws that govern its behavior.

    Signature: Structure[T] = (Container[T], Laws)

    Example:
        group = Structure(
            name="Group",
            elements=[0, 1, 2, 3],  # Z/4Z
            operations={
                "add": lambda x, y: (x + y) % 4
            },
            laws=[
                "associative",
                "has_identity",
                "has_inverses"
            ]
        )
    """
    name: str
    elements: list[T]
    operations: dict[str, Callable]
    laws: list[str]
    properties: dict = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}


# Example usage:
STRUCTURE_EXAMPLE = Structure(
    name="Group_Z4",
    elements=[0, 1, 2, 3],
    operations={
        "add": lambda x, y: (x + y) % 4,
        "inv": lambda x: (4 - x) % 4
    },
    laws=["associative", "identity", "inverse", "closure"]
)


# =============================================================================
# 7. TRANSFORM
# =============================================================================
# Type signature: Transform[A, B]: Structure[A] -> Structure[B]
# Purpose: Rewrite/map between structures

@dataclass
class Transform(Generic[A, B]):
    """
    A rewrite or map between structures.

    Signature: Transform[A, B]: Structure[A] -> Structure[B]

    Example:
        fourier = Transform(
            name="Fourier Transform",
            mapping=lambda signal: fft(signal),
            source_structure="Time Domain",
            target_structure="Frequency Domain",
            preserves=["energy", "information"]
        )
    """
    name: str
    mapping: Callable[[Any], Any]
    source_structure: str
    target_structure: str
    preserves: list[str] = None  # What invariants are preserved?
    properties: list[str] = None  # e.g., ["linear", "bijective"]

    def __post_init__(self):
        if self.preserves is None:
            self.preserves = []
        if self.properties is None:
            self.properties = []

    def apply(self, source: Any) -> Any:
        """Apply the transform to the source structure."""
        return self.mapping(source)


# Example usage:
TRANSFORM_EXAMPLE = Transform(
    name="log_transform",
    mapping=lambda x: __import__('math').log(x),
    source_structure="Multiplicative Group",
    target_structure="Additive Group",
    preserves=["ordering"],
    properties=["bijective", "continuous"]
)


# =============================================================================
# 8. RECURSION
# =============================================================================
# Type signature: Recursion[T] = (step: T -> T, seed: T, stop: T -> Bool) -> T
# Purpose: Self-application + stop rule

@dataclass
class Recursion(Generic[T]):
    """
    Self-application with a stop rule.

    Signature: Recursion[T] = (step: T -> T, seed: T, stop: T -> Bool) -> T

    Example:
        fibonacci = Recursion(
            name="fibonacci",
            step=lambda state: (state[1], state[0] + state[1]),
            seed=(0, 1),
            stop=lambda state: state[0] >= 100,
            result_extractor=lambda state: state[0]
        )

        fibonacci.execute()  # Returns 89 (largest fib < 100)
    """
    name: str
    step: Callable[[T], T]
    seed: T
    stop: Callable[[T], bool]
    result_extractor: Callable[[T], Any] = None

    def execute(self) -> Any:
        """Execute the recursion until the stop condition is met."""
        state = self.seed
        while not self.stop(state):
            state = self.step(state)

        if self.result_extractor:
            return self.result_extractor(state)
        return state


# Example usage:
RECURSION_EXAMPLE = Recursion(
    name="fibonacci",
    step=lambda state: (state[1], state[0] + state[1]),
    seed=(0, 1),
    stop=lambda state: state[0] >= 100,
    result_extractor=lambda state: state[0]
)


# =============================================================================
# COMPLETE FRAGMENT CATALOG
# =============================================================================

FRAGMENT_CATALOG = {
    "ENTITY": {
        "signature": "Entity[T]",
        "description": "Atomic object of type T",
        "example": ENTITY_EXAMPLE
    },
    "RELATION": {
        "signature": "Relation[A, B]: (A, B) -> Bool",
        "description": "Typed predicate between A and B",
        "example": RELATION_EXAMPLE
    },
    "OPERATOR": {
        "signature": "Operator[A, B]: A -> B",
        "description": "Typed function from A to B",
        "example": OPERATOR_EXAMPLE
    },
    "CONSTRAINT": {
        "signature": "Constraint[A]: A -> Bool",
        "description": "Guard or filter on type A",
        "example": CONSTRAINT_EXAMPLE
    },
    "MEASURE": {
        "signature": "Measure[A]: A -> ℝ",
        "description": "Evaluation functional to real numbers",
        "example": MEASURE_EXAMPLE
    },
    "STRUCTURE": {
        "signature": "Structure[T] = (Container[T], Laws)",
        "description": "Container with governing laws",
        "example": STRUCTURE_EXAMPLE
    },
    "TRANSFORM": {
        "signature": "Transform[A, B]: Structure[A] -> Structure[B]",
        "description": "Map between structures",
        "example": TRANSFORM_EXAMPLE
    },
    "RECURSION": {
        "signature": "Recursion[T] = (step, seed, stop) -> result",
        "description": "Self-application with termination",
        "example": RECURSION_EXAMPLE
    }
}


def print_catalog():
    """Print the complete fragment catalog."""
    print("=" * 80)
    print("FRAGMENT IR - THE 8 CORE FRAGMENTS")
    print("=" * 80)
    print()

    for fragment_name, info in FRAGMENT_CATALOG.items():
        print(f"{fragment_name}")
        print(f"  Signature: {info['signature']}")
        print(f"  Description: {info['description']}")
        print()

    print("=" * 80)
    print("Like LLVM IR, but for mathematical ideas.")
    print("Every concept decomposes into these 8 typed fragments.")
    print("=" * 80)


if __name__ == "__main__":
    print_catalog()

    # Test examples
    print("\n\nTEST EXAMPLES:")
    print("-" * 80)

    print(f"\n1. ENTITY: {ENTITY_EXAMPLE.value} (type: {ENTITY_EXAMPLE.type_name})")

    print(f"\n2. RELATION: 3 < 5 = {RELATION_EXAMPLE.test(3, 5)}")

    print(f"\n3. OPERATOR: square(5) = {OPERATOR_EXAMPLE.apply(5)}")

    print(f"\n4. CONSTRAINT: positive(5) = {CONSTRAINT_EXAMPLE.check(5)}")
    print(f"   CONSTRAINT: positive(-3) = {CONSTRAINT_EXAMPLE.check(-3)}")

    print(f"\n5. MEASURE: norm(-7) = {MEASURE_EXAMPLE.evaluate(-7)}")

    print(f"\n6. STRUCTURE: Group Z/4Z with elements {STRUCTURE_EXAMPLE.elements}")
    print(f"   2 + 3 (mod 4) = {STRUCTURE_EXAMPLE.operations['add'](2, 3)}")

    print(f"\n7. TRANSFORM: log_transform preserves {TRANSFORM_EXAMPLE.preserves}")

    print(f"\n8. RECURSION: fibonacci(n < 100) = {RECURSION_EXAMPLE.execute()}")
