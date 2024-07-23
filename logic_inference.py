import json
import os
from tqdm import tqdm
from prover9_solver import FOL_Prover9_Program
from pyke_solver import Pyke_Program
from Z3_solver import Z3_Program
import argparse
import random
import shutil

class LogicInferenceEngine:
    def __init__(self, args):
        self.args = args
        self.dataset_name = args.dataset_name
        self.depth = args.depth
        self.World = args.World
        self.shot = args.shot
        self.solver = args.solver
        self.model_name = args.model_name
        self.dataset = self.load_logic_programs()
        # Change Proofwriter name
        if self.dataset_name == "ProofWriter" and self.World == "CWA":
            self.assumption = "CWA"
        elif self.dataset_name == "ProntoQA" or self.dataset_name == "PrOntoQA":
            self.assumption = "CWA"
        else:
            self.assumption = "OWA"
        program_executor_map = {'Prover9': FOL_Prover9_Program, 'Pyke': Pyke_Program, 'Z3':Z3_Program}
        self.program_executor = program_executor_map[str(self.solver)]

    def load_logic_programs(self):
        if self.dataset_name == "ProofWriter":
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.World}_{self.depth}_{self.solver}_{self.model_name}.json'
        elif self.dataset_name == "FOLIO" and self.shot > 1:
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.shot}Shot_{self.solver}_{self.model_name}.json'
        else:
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.solver}_{self.model_name}.json'
        with open(save_path, errors = "ignore") as f:
            dataset = json.load(f)
        print(f"Loaded {len(dataset)} examples from {self.dataset_name}")
        return dataset

    def save_results(self, outputs):
        if self.dataset_name == "ProofWriter":
            save_path = f'Processed_Datasets/{self.dataset_name}_{self.World}_{self.depth}_{self.solver}_{self.model_name}.json'
        elif self.dataset_name == "FOLIO" and self.shot > 1:
            save_path = f'Processed_Datasets/{self.dataset_name}_{self.shot}Shot_{self.solver}_{self.model_name}.json'
        else:
            save_path = f'Processed_Datasets/{self.dataset_name}_{self.solver}_{self.model_name}.json'
        #save_path = f'Processed_Datasets/{self.dataset_name}_{self.solver}_{self.model_name}.json'
        with open(save_path, 'w') as f:
            json.dump(outputs, f, indent=2, ensure_ascii=False)

    def safe_execute_program(self, id, logic_program):
        #program = self.program_executor(logic_program)
        if self.solver == "Z3" or self.solver == "z3":
            program = self.program_executor(logic_program, self.assumption)
        elif self.solver == "Pyke" or self.solver == "pyke":
            program = self.program_executor(logic_program, assumption=self.assumption, dataset_name=self.dataset_name )
        else:
            program = self.program_executor(logic_program)
        # cannot parse the program
        if program.flag == False:
            answer = "Parse Error"
            return answer, 'parsing error', ''

        # execute the program
        answer, error_message = program.execute_program()
        # not executable
        if answer is None:
            answer = "Execution Error"
            return answer, 'execution error', error_message
        # successfully executed
        if self.World == "CWA" and self.solver == "Prover9":
            answer = program.answer_mapping(answer, "CWA")
        else:
            answer = program.answer_mapping(answer)
        return answer, 'success', ''

    def inference_on_dataset(self):
        outputs = []
        error_count = 0

        for example in tqdm(self.dataset):
            # execute the logic program
            raw_program = example['raw_logic_programs'][0].strip()

            # need to do some trimmming for Gemini, gemini produces python method terms while we have provided it in the prompt.
            def remove_strings(text, strings_to_remove):
                """
                This function removes a list of specific strings from a given text.
                Args:
                    text: The original string.
                    strings_to_remove: A list of strings to be removed.
                Returns:
                    A new string with the specified strings removed.
                """
                for string in strings_to_remove:
                    text = text.replace(string, "")
                return text.strip()
            if self.model_name[:6] == "gemini" or self.model_name == "command-r-plus":
                strings_to_remove = ["```", "python", "def solution():"]
                raw_program = remove_strings(raw_program, strings_to_remove)

            if self.model_name[:5] == "gpt-4":
                gpt4_strings_to_remove = ['[Problem Parse Output]:', '[Question Parse Output]:']
                raw_program = remove_strings(raw_program, gpt4_strings_to_remove)
            answer, flag, error_message = self.safe_execute_program(example['id'], raw_program)
            if not flag == 'success':
                error_count += 1

            # create output
            output = {'id': example['id'],
                      'context': example['context'],
                      'question': example['question'],
                      'answer': example['answer'],
                      'flag': flag,
                      'error': str(error_message),
                      'predicted_answer': answer}
            outputs.append(output)

        print(f"Error count: {error_count}")
        self.save_results(outputs)
        self.cleanup()
    def cleanup(self):
        complied_krb_dir = './compiled_krb'
        if os.path.exists(complied_krb_dir):
            print('removing compiled_krb')
            shutil.rmtree(complied_krb_dir)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_name', type=str)
    parser.add_argument('--depth', type=str, default='d5')
    parser.add_argument('--World', type=str, default='')
    parser.add_argument('--solver', type=str)
    parser.add_argument('--shot', type=int, default=1)
    parser.add_argument('--model_name', type=str, default='text-davinci-003')
    parser.add_argument('--timeout', type=int, default=60)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    engine = LogicInferenceEngine(args)
    engine.inference_on_dataset()

