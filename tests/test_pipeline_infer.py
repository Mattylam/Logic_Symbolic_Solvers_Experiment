from logic_solvers.pipeline.infer import strip_model_artifacts


def test_strip_model_artifacts_uses_generalized_cleanup_regardless_of_model():
    raw = "```python\ndef solution():\n    return foo(bar)\n```"
    # No model-specific branching left: same cleanup for every model name.
    assert strip_model_artifacts(raw, "gemini-1.0-pro-latest") == strip_model_artifacts(raw, "gpt-4o")
    assert "def solution():" not in strip_model_artifacts(raw, "command-r-plus")
