from logic_solvers.pipeline.generate import build_prompt


def test_build_prompt_substitutes_problem_and_question():
    template = "Problem: [[PROBLEM]]\nQuestion: [[QUESTION]]\n"
    example = {"context": "All cats are mammals.", "question": "Is Tom a mammal?"}
    result = build_prompt(template, example)
    assert result == "Problem: All cats are mammals.\nQuestion: Is Tom a mammal?\n"


def test_build_prompt_appends_z3_solution_stub_when_requested():
    template = "Problem: [[PROBLEM]]\nQuestion: [[QUESTION]]\n"
    example = {"context": "ctx", "question": "q"}
    result = build_prompt(template, example, append_z3_stub=True)
    assert result.endswith("# solution in Python:\ndef solution():\n")
