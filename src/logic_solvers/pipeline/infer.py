"""Stage 2: execute generated logic programs against the chosen symbolic solver."""

import json
import os
import shutil
import argparse
from tqdm import tqdm

from logic_solvers.solvers.prover9_solver import FOL_Prover9_Program
from logic_solvers.solvers.z3_solver import Z3_Program
from logic_solvers.llm.postprocess import clean_llm_output
from logic_solvers.config import answered_dataset_path, processed_dataset_path

try:
    # NOTE: pyke3 has no installable PyPI distribution (see pyproject.toml's
    # 'pyke' extra) and requires a manually-installed Python-3 fork. Import it
    # lazily/guarded so this module (and anything importing strip_model_artifacts)
    # stays importable in environments without pyke installed, consistent with
    # the importorskip pattern used in tests/test_solvers_smoke.py.
    from logic_solvers.solvers.pyke_solver import Pyke_Program
except ImportError:
    Pyke_Program = None

_PROGRAM_EXECUTORS = {"Prover9": FOL_Prover9_Program, "Pyke": Pyke_Program, "Z3": Z3_Program}


def strip_model_artifacts(raw_program: str, model_name: str) -> str:
    # Generalized cleanup applies uniformly regardless of model_name; the
    # parameter is kept so call sites don't need to change if a future
    # model needs a model-specific rule again.
    return clean_llm_output(raw_program)


class LogicInferenceEngine:
    def __init__(self, args) -> None:
        self.args = args
        self.dataset_name = args.dataset_name
        self.depth = args.depth
        self.world = args.World
        self.shot = args.shot
        self.solver = args.solver
        self.model_name = args.model_name
        self.dataset = self.load_logic_programs()

        if self.dataset_name == "ProofWriter" and self.world == "CWA":
            self.assumption = "CWA"
        elif self.dataset_name in ("ProntoQA", "PrOntoQA"):
            self.assumption = "CWA"
        else:
            self.assumption = "OWA"

        self.program_executor = _PROGRAM_EXECUTORS[self.solver]

    def load_logic_programs(self):
        path = answered_dataset_path(self.dataset_name, self.solver, self.model_name, self.world, self.depth, self.shot)
        with open(path, errors="ignore") as f:
            dataset = json.load(f)
        print(f"Loaded {len(dataset)} examples from {self.dataset_name}")
        return dataset

    def save_results(self, outputs) -> None:
        path = processed_dataset_path(self.dataset_name, self.solver, self.model_name, self.world, self.depth, self.shot)
        with open(path, "w") as f:
            json.dump(outputs, f, indent=2, ensure_ascii=False)

    def safe_execute_program(self, logic_program: str):
        if self.solver.lower() == "z3":
            program = self.program_executor(logic_program, self.assumption)
        elif self.solver.lower() == "pyke":
            program = self.program_executor(logic_program, assumption=self.assumption, dataset_name=self.dataset_name)
        else:
            program = self.program_executor(logic_program)

        if not program.flag:
            return "Parse Error", "parsing error", ""

        answer, error_message = program.execute_program()
        if answer is None:
            return "Execution Error", "execution error", error_message

        if self.world == "CWA" and self.solver == "Prover9":
            answer = program.answer_mapping(answer, "CWA")
        else:
            answer = program.answer_mapping(answer)
        return answer, "success", ""

    def inference_on_dataset(self) -> None:
        outputs = []
        error_count = 0

        for example in tqdm(self.dataset):
            raw_program = strip_model_artifacts(example["raw_logic_programs"][0].strip(), self.model_name)
            answer, flag, error_message = self.safe_execute_program(raw_program)
            if flag != "success":
                error_count += 1

            outputs.append({
                "id": example["id"],
                "context": example["context"],
                "question": example["question"],
                "answer": example["answer"],
                "flag": flag,
                "error": str(error_message),
                "predicted_answer": answer,
            })

        print(f"Error count: {error_count}")
        self.save_results(outputs)
        self.cleanup()

    def cleanup(self) -> None:
        compiled_krb_dir = "./compiled_krb"
        if os.path.exists(compiled_krb_dir):
            print("removing compiled_krb")
            shutil.rmtree(compiled_krb_dir)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str)
    parser.add_argument("--depth", type=str, default="d5")
    parser.add_argument("--World", type=str, default="")
    parser.add_argument("--solver", type=str)
    parser.add_argument("--shot", type=int, default=1)
    parser.add_argument("--model_name", type=str, default="text-davinci-003")
    parser.add_argument("--timeout", type=int, default=60)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    LogicInferenceEngine(args).inference_on_dataset()


if __name__ == "__main__":
    main()
