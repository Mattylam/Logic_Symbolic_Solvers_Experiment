from logic_solvers.solvers.z3_solver import Z3_Program

CWA_PROGRAM = """
quiet(Anne)
furry(Erin)
ForAll([x], Implies(quiet(x), furry(x)))
return furry(Anne)
"""


def test_cwa_execution_returns_true():
    program = Z3_Program(CWA_PROGRAM, assumption="CWA")
    assert program.flag is True
    answer, error_message = program.execute_program()
    assert answer == "True"
    assert error_message == ""


OWA_PROGRAM_WITH_EXISTS = """
Dog(Fido)
ForAll([x], Implies(Dog(x), Animal(x)))
Exists([x], Dog(x))
return Exists([x], Animal(x))
"""


def test_owa_execution_treats_exists_as_builtin_not_user_predicate():
    # Regression test: proof_OWA_exec's PREDEFINED_FUNCS list must exclude
    # "Exists" (matching proof_exec's list) so it isn't mistaken for a
    # user-defined 0-ary/uninterpreted predicate needing a Function() declaration.
    program = Z3_Program(OWA_PROGRAM_WITH_EXISTS, assumption="OWA")
    answer, error_message = program.execute_program()
    assert error_message == ""
    assert answer in ("True", "False", "Unknown")


def test_answer_mapping():
    program = Z3_Program(CWA_PROGRAM, assumption="CWA")
    assert program.answer_mapping("True") == "A"
    assert program.answer_mapping("False") == "B"
    assert program.answer_mapping("Unknown") == "C"
