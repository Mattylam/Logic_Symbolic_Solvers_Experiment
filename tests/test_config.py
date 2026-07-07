from logic_solvers.config import (
    raw_dataset_path,
    answered_dataset_path,
    processed_dataset_path,
)


def test_raw_dataset_path_default():
    assert raw_dataset_path("FOLIO") == "Datasets/FOLIO.json"


def test_raw_dataset_path_proofwriter_owa():
    assert (
        raw_dataset_path("ProofWriter", world="OWA", depth="d3")
        == "Datasets/Proof_OWA/Proofd3.json"
    )


def test_raw_dataset_path_proofwriter_cwa():
    assert (
        raw_dataset_path("ProofWriter", world="CWA", depth="d5")
        == "Datasets/Proof/Proofd5.json"
    )


def test_answered_dataset_path_proofwriter():
    path = answered_dataset_path(
        "ProofWriter", solver="Z3", model_name="gpt-4o", world="CWA", depth="d2"
    )
    assert path == "Answered_Datasets/ProofWriter_CWA_d2_Z3_gpt-4o.json"


def test_answered_dataset_path_folio_multi_shot():
    path = answered_dataset_path(
        "FOLIO", solver="Z3", model_name="gpt-4o", shot=4
    )
    assert path == "Answered_Datasets/FOLIO_4Shot_Z3_gpt-4o.json"


def test_answered_dataset_path_folio_single_shot():
    path = answered_dataset_path(
        "FOLIO", solver="Z3", model_name="gpt-4o", shot=1
    )
    assert path == "Answered_Datasets/FOLIO_Z3_gpt-4o.json"


def test_processed_dataset_path_matches_answered_naming():
    path = processed_dataset_path(
        "ProntoQA", solver="Pyke", model_name="command-r-plus"
    )
    assert path == "Processed_Datasets/ProntoQA_Pyke_command-r-plus.json"
