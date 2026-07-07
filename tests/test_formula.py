from logic_solvers.formula import FOL_Formula


def test_valid_formula_is_valid_is_true_boolean():
    formula = FOL_Formula("∀x (Dog(x) → Animal(x))")
    assert formula.is_valid is True
    assert isinstance(formula.is_valid, bool)


def test_invalid_formula_is_valid_is_false_boolean():
    formula = FOL_Formula("this is not valid FOL (((")
    assert formula.is_valid is False
    assert isinstance(formula.is_valid, bool)
