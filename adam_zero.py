"""ADAM-ZERO: Adam's agency core module."""


class Agent:
    """A simple agent with a name and a list of tasks."""

    def __init__(self, name: str):
        self.name = name
        self.tasks = []

    def add_task(self, task: str):
        """Add a task to the agent's queue."""
        if not task or not task.strip():
            raise ValueError("Task cannot be empty")
        self.tasks.append(task.strip())

    def complete_task(self) -> str:
        """Remove and return the next task."""
        if not self.tasks:
            raise IndexError("No tasks to complete")
        return self.tasks.pop(0)

    def pending_count(self) -> int:
        """Return the number of pending tasks."""
        return len(self.tasks)


def greet(name: str) -> str:
    """Return a greeting string."""
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")
    return f"Hello, {name.strip()}!"
