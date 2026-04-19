"""
Test for classify_memory utility in core.inference.classifier.
"""
from app.core.inference.classifier import classify_memory

def test_classify_memory_completed():
    assert classify_memory("I have completed the task") == "completed"
    assert classify_memory("This is done") == "completed"
    assert classify_memory("finished work") == "completed"

def test_classify_memory_project():
    assert classify_memory("I am working on the backend") == "project"
    assert classify_memory("building API") == "project"
    assert classify_memory("implementing feature") == "project"

def test_classify_memory_task():
    assert classify_memory("I need to write tests") == "task"
    assert classify_memory("todo: refactor code") == "task"
    assert classify_memory("to do: update docs") == "task"
    assert classify_memory("should improve performance") == "task"

def test_classify_memory_general():
    assert classify_memory("random note") == "general"
    assert classify_memory("") == "general"
