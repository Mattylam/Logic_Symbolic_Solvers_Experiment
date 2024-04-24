# generate facts and rules based on the problem description

import json
import os
from tqdm import tqdm
from collections import OrderedDict
from typing import Dict, List, Tuple
from utils import OpenAIModel
import argparse


class LogicProgramGenerator:
    def __init__(self, args):
        self.args = args
        self.dataset_name = args.dataset_name
        self.depth = args.depth
        self.solver = args.solver
        self.model_name = args.model_name

        # Control the dataset length here
        self.dataset_length = 200

        self.openai_api = OpenAIModel(args.api_key, args.model_name, args.max_new_tokens)
        self.prompt_creator = {'FOLIO': self.prompt_folio,
                               'ProntoQA': self.prompt_prontoqa,
                               'ProofWriter': self.prompt_proofwriter}
        self.load_prompt_templates()

    def load_prompt_templates(self):
        prompt_file = f'Prompts/{self.dataset_name}_{self.solver}_Prompts.txt'
        with open(prompt_file, 'r') as f:
            self.prompt_template = f.read()
        # print(self.prompt_template)

    def prompt_folio(self, test_data):
        problem = test_data['context']
        question = test_data['question'].strip()
        full_prompt = self.prompt_template.replace('[[PROBLEM]]', problem).replace('[[QUESTION]]', question)
        return full_prompt


    def prompt_prontoqa(self, test_data):
        problem = test_data['context']
        question = test_data['question'].strip()
        full_prompt = self.prompt_template.replace('[[PROBLEM]]', problem).replace('[[QUESTION]]', question)
        return full_prompt

    def prompt_proofwriter(self, test_data):
        problem = test_data['context']
        question = test_data['question'].strip()
        full_prompt = self.prompt_template.replace('[[PROBLEM]]', problem).replace('[[QUESTION]]', question)
        if self.solver == "Z3" or self.solver == "z3":
            full_prompt = full_prompt + '# solution in Python:\n' + 'def solution():\n'
        return full_prompt

    def load_raw_dataset(self):
        if self.dataset_name == "ProofWriter":
            dataset_file = f'Datasets/Proof/Proof{self.depth}.json'
        else:
            dataset_file = f'Datasets/{self.dataset_name}.json'
        with open(dataset_file ,'r') as f:
            raw_dataset = json.load(f)
        return raw_dataset

    def logic_program_generation(self):
        # load raw dataset
        raw_dataset = self.load_raw_dataset()
        # Cut the length here
        if self.dataset_length < len(raw_dataset):
            raw_dataset = raw_dataset[0:self.dataset_length]
        print(f"Loaded {len(raw_dataset)} examples from {self.dataset_name}.")

        outputs = []
        for example in tqdm(raw_dataset):
            # create prompt
            try:
                full_prompt = self.prompt_creator[self.dataset_name](example)
                output = self.openai_api.generate(full_prompt)
                # print(full_prompt)
                programs = [output]

                # create output
                output = {'id': example['id'],
                          'context': example['context'],
                          'question': example['question'],
                          'answer': example['answer'],
                          'options': example['options'],
                          'raw_logic_programs': programs}
                outputs.append(output)
            except:
                print('Error in generating logic programs for example: ', example['id'])
        # save outputs
        if self.dataset_name == "ProofWriter":
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.depth}_{self.solver}_{self.model_name}.json'
        else:
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.solver}_{self.model_name}.json'
        with open(save_path, 'w') as f:
            json.dump(outputs, f, indent=2, ensure_ascii=False)

# I also want to control the number of shots here, we can add it later
# Control the number of examples
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_name', type=str)
    parser.add_argument('--depth', type=str, default='d5')
    parser.add_argument('--solver', type=str)
    parser.add_argument('--api_key', type=str)
    parser.add_argument('--model_name', type=str, default='text-davinci-003')
    parser.add_argument('--max_new_tokens', type=int, default=1024)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logic_program_generator = LogicProgramGenerator(args)
    logic_program_generator.logic_program_generation()