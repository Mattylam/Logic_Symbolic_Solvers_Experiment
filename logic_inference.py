import json
import os
from tqdm import tqdm
from prover9_solver import FOL_Prover9_Program
# from symbolic_solvers.pyke_solver.pyke_solver import Pyke_Program
#from symbolic_solvers.z3_solver.sat_problem_solver import LSAT_Z3_Program
import argparse
import random


class LogicInferenceEngine:
    def __init__(self, args):
        self.args = args
        self.dataset_name = args.dataset_name
        self.depth = args.depth
        self.solver = args.solver
        self.model_name = args.model_name
        self.dataset = self.load_logic_programs()
        # Change Proofwriter name
        #program_executor_map = {'Prover9': FOL_Prover9_Program, 'ProofWriter': Pyke_Program}
        program_executor_map = {'Prover9': FOL_Prover9_Program}
        self.program_executor = program_executor_map[str(self.solver)]

    def load_logic_programs(self):
        if self.dataset_name == "ProofWriter":
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.depth}_{self.solver}_{self.model_name}.json'
        else:
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.solver}_{self.model_name}.json'
        with open(save_path) as f:
            dataset = json.load(f)
        print(f"Loaded {len(dataset)} examples from {self.dataset_name}")
        return dataset

    def save_results(self, outputs):
        if self.dataset_name == "ProofWriter":
            save_path = f'Processed_Datasets/{self.dataset_name}_{self.depth}_{self.solver}_{self.model_name}.json'
        else:
            save_path = f'Processed_Datasets/{self.dataset_name}_{self.solver}_{self.model_name}.json'
        #save_path = f'Processed_Datasets/{self.dataset_name}_{self.solver}_{self.model_name}.json'
        with open(save_path, 'w') as f:
            json.dump(outputs, f, indent=2, ensure_ascii=False)

    def safe_execute_program(self, id, logic_program):
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
        answer = program.answer_mapping(answer)
        return answer, 'success', ''

    def inference_on_dataset(self):
        outputs = []
        error_count = 0

        for example in tqdm(self.dataset):
            # execute the logic program
            answer, flag, error_message = self.safe_execute_program(example['id'],
                                                                    example['raw_logic_programs'][0].strip())
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
        #self.cleanup()
    # This method for Pyke I think
    # def cleanup(self):
    #     complied_krb_dir = './models/compiled_krb'
    #     if os.path.exists(complied_krb_dir):
    #         print('removing compiled_krb')
    #         os.system(f'rm -rf {complied_krb_dir}')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_name', type=str)
    parser.add_argument('--depth', type=str, default='d5')
    parser.add_argument('--solver', type=str)
    parser.add_argument('--model_name', type=str, default='text-davinci-003')
    parser.add_argument('--timeout', type=int, default=60)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    engine = LogicInferenceEngine(args)
    engine.inference_on_dataset()