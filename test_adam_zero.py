"""Tests for ADAM-ZERO core module."""

import pytest
from adam_zero import Agent, greet


# --- greet() tests ---

def test_greet_basic():
    assert greet("Adam") == "Hello, Adam!"


def test_greet_strips_whitespace():
    assert greet("  Adam  ") == "Hello, Adam!"


def test_greet_empty_raises():
    with pytest.raises(ValueError):
        greet("")


def test_greet_whitespace_only_raises():
    with pytest.raises(ValueError):
        greet("   ")


# --- Agent tests ---

class TestAgent:
    def test_init(self):
        agent = Agent("ADAM")
        assert agent.name == "ADAM"
        assert agent.tasks == []

    def test_add_task(self):
        agent = Agent("ADAM")
        agent.add_task("research topic")
        assert agent.pending_count() == 1

    def test_add_task_strips_whitespace(self):
        agent = Agent("ADAM")
        agent.add_task("  clean data  ")
        assert agent.tasks[0] == "clean data"

    def test_add_empty_task_raises(self):
        agent = Agent("ADAM")
        with pytest.raises(ValueError):
            agent.add_task("")

    def test_add_whitespace_task_raises(self):
        agent = Agent("ADAM")
        with pytest.raises(ValueError):
            agent.add_task("   ")

    def test_complete_task_returns_first(self):
        agent = Agent("ADAM")
        agent.add_task("task one")
        agent.add_task("task two")
        result = agent.complete_task()
        assert result == "task one"
        assert agent.pending_count() == 1

    def test_complete_task_fifo_order(self):
        agent = Agent("ADAM")
        for task in ["a", "b", "c"]:
            agent.add_task(task)
        assert agent.complete_task() == "a"
        assert agent.complete_task() == "b"
        assert agent.complete_task() == "c"

    def test_complete_task_when_empty_raises(self):
        agent = Agent("ADAM")
        with pytest.raises(IndexError):
            agent.complete_task()

    def test_pending_count_accurate(self):
        agent = Agent("ADAM")
        assert agent.pending_count() == 0
        agent.add_task("x")
        assert agent.pending_count() == 1
        agent.add_task("y")
        assert agent.pending_count() == 2
        agent.complete_task()
        assert agent.pending_count() == 1
