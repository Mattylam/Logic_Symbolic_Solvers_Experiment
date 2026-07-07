"""Stage 1: generate raw logic programs from natural-language problems via an LLM."""

import json
import argparse
from tqdm import tqdm

from logic_solvers.llm.provider import LiteLLMProvider
from logic_solvers.llm.postprocess import clean_llm_output
from logic_solvers.config import raw_dataset_path, answered_dataset_path


def build_prompt(prompt_template: str, example: dict, append_z3_stub: bool = False) -> str:
    problem = example["context"]
    question = example["question"].strip()
    full_prompt = prompt_template.replace("[[PROBLEM]]", problem).replace("[[QUESTION]]", question)
    if append_z3_stub:
        full_prompt += "# solution in Python:\ndef solution():\n"
    return full_prompt


class LogicProgramGenerator:
    def __init__(self, args) -> None:
        self.args = args
        self.dataset_name = args.dataset_name
        self.depth = args.depth
        self.shot = args.shot
        self.world = args.World
        self.solver = args.solver
        self.model_name = args.model_name
        self.dataset_length = 200

        self.llm = LiteLLMProvider(args.model_name, api_key=args.api_key or None, max_new_tokens=args.max_new_tokens)
        self.load_prompt_templates()

    def load_prompt_templates(self) -> None:
        if self.dataset_name == "FOLIO" and self.shot in (2, 4):
            shot_label = "TwoShot" if self.shot == 2 else "FourShot"
            prompt_file = f"Prompts/{self.dataset_name}_{self.solver}_{shot_label}_Prompts.txt"
        else:
            prompt_file = f"Prompts/{self.dataset_name}_{self.solver}_Prompts.txt"

        if self.model_name.startswith("gpt-4"):
            prompt_file = prompt_file.replace("_Prompts", "_Prompts_GPT4")
        if self.model_name == "command-r-plus":
            prompt_file = prompt_file.replace("_Prompts", "_Prompts_Cohere")

        with open(prompt_file, "r") as f:
            self.prompt_template = f.read()

    def logic_program_generation(self) -> None:
        with open(raw_dataset_path(self.dataset_name, self.world, self.depth), "r", errors="ignore") as f:
            raw_dataset = json.load(f)
        if self.dataset_length < len(raw_dataset):
            raw_dataset = raw_dataset[: self.dataset_length]
        print(f"Loaded {len(raw_dataset)} examples from {self.dataset_name}.")

        append_z3_stub = self.solver.lower() == "z3" and not self.model_name.startswith("gpt-4")

        outputs = []
        for example in tqdm(raw_dataset):
            try:
                full_prompt = build_prompt(self.prompt_template, example, append_z3_stub)
                raw_output = self.llm.generate(full_prompt)
                output_text = clean_llm_output(raw_output)
                outputs.append({
                    "id": example["id"],
                    "context": example["context"],
                    "question": example["question"],
                    "answer": example["answer"],
                    "options": example["options"],
                    "raw_logic_programs": [output_text],
                })
            except Exception as exc:
                print(f"Error generating logic program for example {example['id']}: {exc}")

        save_path = answered_dataset_path(self.dataset_name, self.solver, self.model_name, self.world, self.depth, self.shot)
        with open(save_path, "w", errors="ignore") as f:
            json.dump(outputs, f, indent=2, ensure_ascii=False)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str)
    parser.add_argument("--depth", type=str, default="d5")
    parser.add_argument("--World", type=str, default="")
    parser.add_argument("--solver", type=str)
    parser.add_argument("--shot", type=int, default=1)
    parser.add_argument("--api_key", type=str)
    parser.add_argument("--model_name", type=str, default="gpt-3.5-turbo")
    parser.add_argument("--max_new_tokens", type=int, default=2000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    LogicProgramGenerator(args).logic_program_generation()


if __name__ == "__main__":
    main()
