"""Path-naming conventions shared by the generate/infer/evaluate pipeline stages."""


def raw_dataset_path(dataset_name: str, world: str = "", depth: str = "d5") -> str:
    if dataset_name == "ProofWriter":
        subdir = "Proof_OWA" if world == "OWA" else "Proof"
        return f"Datasets/{subdir}/Proof{depth}.json"
    return f"Datasets/{dataset_name}.json"


def _dataset_filename(dataset_name: str, solver: str, model_name: str,
                       world: str = "", depth: str = "d5", shot: int = 1) -> str:
    if dataset_name == "ProofWriter":
        return f"{dataset_name}_{world}_{depth}_{solver}_{model_name}.json"
    if dataset_name == "FOLIO" and shot > 1:
        return f"{dataset_name}_{shot}Shot_{solver}_{model_name}.json"
    return f"{dataset_name}_{solver}_{model_name}.json"


def answered_dataset_path(dataset_name: str, solver: str, model_name: str,
                           world: str = "", depth: str = "d5", shot: int = 1) -> str:
    filename = _dataset_filename(dataset_name, solver, model_name, world, depth, shot)
    return f"Answered_Datasets/{filename}"


def processed_dataset_path(dataset_name: str, solver: str, model_name: str,
                            world: str = "", depth: str = "d5", shot: int = 1) -> str:
    filename = _dataset_filename(dataset_name, solver, model_name, world, depth, shot)
    return f"Processed_Datasets/{filename}"
