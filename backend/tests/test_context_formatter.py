"""
Test for format_temporal_context utility in context.formatter.
"""
from app.core.context.formatter import format_temporal_context

def test_format_temporal_context():
    data = {
        "today": ["Task A", "Task B"],
        "yesterday": ["Task C"],
        "this_week": ["Task D"]
    }
    result = format_temporal_context(data)
    assert "Today:" in result
    assert "- Task A" in result
    assert "Yesterday:" in result
    assert "- Task C" in result
    assert "This Week:" in result
    assert "- Task D" in result

def test_format_temporal_context_empty():
    data = {"today": [], "yesterday": [], "this_week": []}
    result = format_temporal_context(data)
    assert result == ""
