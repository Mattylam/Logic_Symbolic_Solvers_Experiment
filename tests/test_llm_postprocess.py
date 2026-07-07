from logic_solvers.llm.postprocess import clean_llm_output


def test_strips_problem_and_question_labels():
    raw = "[Problem Parse Output]:\nfoo(bar)\n[Question Parse Output]:\nbaz(qux)"
    assert clean_llm_output(raw) == "foo(bar)\nbaz(qux)"


def test_strips_markdown_code_fences_and_python_boilerplate():
    raw = "```python\ndef solution():\n    return foo(bar)\n```"
    cleaned = clean_llm_output(raw)
    assert "```" not in cleaned
    assert "def solution():" not in cleaned
    assert "return foo(bar)" in cleaned


def test_strips_stray_replacement_character():
    raw = "foo(bar)�\nbaz(qux)"
    assert "�" not in clean_llm_output(raw)


def test_strips_leading_dash_bullet_artifact():
    raw = "- foo(bar)\n- baz(qux)"
    cleaned = clean_llm_output(raw)
    assert cleaned == "foo(bar)\nbaz(qux)"


def test_passthrough_for_clean_input():
    raw = "foo(bar)\nbaz(qux)"
    assert clean_llm_output(raw) == raw
