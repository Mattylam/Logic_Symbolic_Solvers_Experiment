from logic_solvers.parsing.fol_parser import FOL_Parser


def test_fol_parser_parses_simple_formula():
    parser = FOL_Parser()
    tree = parser.parse_text_FOL_to_tree("∀x (Dog(x) → Animal(x))")
    assert tree is not None
