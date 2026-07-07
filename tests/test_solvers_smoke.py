import pytest

from logic_solvers.solvers.prover9_solver import FOL_Prover9_Program


def test_pyke_program_importable_and_constructible():
    pytest.importorskip(
        "pyke",
        reason=(
            "pyke has no installable PyPI distribution (see pyproject.toml "
            "'pyke' extra); requires a manually-installed Python-3 fork."
        ),
    )
    from logic_solvers.solvers.pyke_solver import Pyke_Program

    program = Pyke_Program("Facts:\nfoo(bar)\nRules:\nQuery:\nfoo(bar)", dataset_name="ProntoQA")
    assert hasattr(program, "flag")


def test_prover9_program_importable():
    assert FOL_Prover9_Program is not None
