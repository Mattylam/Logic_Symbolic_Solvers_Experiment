from logic_solvers.pipeline.evaluate import get_choice, compute_exact_match, evaluate_QA


def test_get_choice_strips_letter_prefix():
    assert get_choice("A) Tom is a mammal.") == "A"
    assert get_choice("B. False") == "B"


def test_get_choice_returns_none_for_unrecognized_format():
    assert get_choice("no letter here") is None


def test_compute_exact_match_normalizes_case_and_punctuation():
    assert compute_exact_match("The Cat.", "the cat") == 1


def test_evaluate_qa_computes_accuracy_over_samples():
    results = [
        {"answer": "A", "predicted_answer": "A"},
        {"answer": "B", "predicted_answer": "C"},
    ]
    assert evaluate_QA(results) == 0.5
