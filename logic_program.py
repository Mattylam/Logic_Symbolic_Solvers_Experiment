# generate facts and rules based on the problem description

import json
from tqdm import tqdm
from utils import OpenAIModel
from gemini import GeminiModel
from cohere_API import CohereModel
import argparse


class LogicProgramGenerator:
    def __init__(self, args):
        self.args = args
        self.dataset_name = args.dataset_name
        self.depth = args.depth
        self.shot = args.shot
        self.World = args.World
        self.solver = args.solver
        self.model_name = args.model_name

        # Control the dataset length here
        self.dataset_length = 200
        if self.model_name[:6] == "gemini":
            self.openai_api = GeminiModel(args.api_key, args.model_name, args.max_new_tokens)
        elif self.model_name == "command-r-plus":
            self.openai_api = CohereModel(args.api_key, args.model_name, args.max_new_tokens)
        else:
            self.openai_api = OpenAIModel(args.api_key, args.model_name, args.max_new_tokens)
        self.prompt_creator = {'FOLIO': self.prompt_folio,
                               'ProntoQA': self.prompt_prontoqa,
                               'ProofWriter': self.prompt_proofwriter}
        self.load_prompt_templates()

    def load_prompt_templates(self):
        if self.dataset_name == "FOLIO":
            if self.shot == 2:
                prompt_file = f'Prompts/{self.dataset_name}_{self.solver}_TwoShot_Prompts.txt'
            elif self.shot == 4:
                prompt_file = f'Prompts/{self.dataset_name}_{self.solver}_FourShot_Prompts.txt'
            else:
                prompt_file = f'Prompts/{self.dataset_name}_{self.solver}_Prompts.txt'
        else:
            prompt_file = f'Prompts/{self.dataset_name}_{self.solver}_Prompts.txt'

        if self.model_name[:5] == "gpt-4":
            prompt_file = prompt_file.replace("_Prompts", "_Prompts_GPT4")
        if self.model_name == "command-r-plus":
            prompt_file = prompt_file.replace("_Prompts", "_Prompts_Cohere")
        with open(prompt_file, 'r') as f:
            self.prompt_template = f.read()
        # print(self.prompt_template)

    def prompt_folio(self, test_data):
        problem = test_data['context']
        question = test_data['question'].strip()
        full_prompt = self.prompt_template.replace('[[PROBLEM]]', problem).replace('[[QUESTION]]', question)
        if self.model_name[:5] != "gpt-4":
            if self.solver == "Z3" or self.solver == "z3":
                full_prompt = full_prompt + '# solution in Python:\n' + 'def solution():\n'
        return full_prompt


    def prompt_prontoqa(self, test_data):
        problem = test_data['context']
        question = test_data['question'].strip()
        full_prompt = self.prompt_template.replace('[[PROBLEM]]', problem).replace('[[QUESTION]]', question)
        if self.model_name[:5] != "gpt-4":
            if self.solver == "Z3" or self.solver == "z3":
                full_prompt = full_prompt + '# solution in Python:\n' + 'def solution():\n'
        return full_prompt

    def prompt_proofwriter(self, test_data):
        problem = test_data['context']
        question = test_data['question'].strip()
        full_prompt = self.prompt_template.replace('[[PROBLEM]]', problem).replace('[[QUESTION]]', question)
        if self.model_name[:5] != "gpt-4":
            if self.solver == "Z3" or self.solver == "z3":
                full_prompt = full_prompt + '# solution in Python:\n' + 'def solution():\n'
        return full_prompt

    def load_raw_dataset(self):
        if self.dataset_name == "ProofWriter":
            if self.World == "OWA":
                dataset_file = f'Datasets/Proof_OWA/Proof{self.depth}.json'
            else:
                dataset_file = f'Datasets/Proof/Proof{self.depth}.json'
        else:
            dataset_file = f'Datasets/{self.dataset_name}.json'
        # seems like FOLIO is decoded differently
        if self.dataset_name == "FOLIO":
            with open(dataset_file, 'r',  errors='ignore') as f:
                raw_dataset = json.load(f)
        else:
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
                #print(full_prompt)
                output = self.openai_api.generate(full_prompt)
                def format_gpt4(text):
                    text = text.replace('[Problem Parse Output]:', '')
                    text = text.replace('[Question Parse Output]:', '')
                    return text
                def format_cohere(text):
                    text = text.replace('[Problem Parse Output]:', '')
                    text = text.replace('[Question Parse Output]:', '')
                    text = text.replace('-', '')
                    text = text.replace('�', '')
                    return text
                if self.model_name[:5] == "gpt-4":
                    output = format_gpt4(output)
                if self.model_name == "command-r-plus":
                    output = format_cohere(output)
                programs = [output]

                # create output
                output = {'id': example['id'],
                          'context': example['context'],
                          'question': example['question'],
                          'answer': example['answer'],
                          'options': example['options'],
                          'raw_logic_programs': programs}
                outputs.append(output)
            except Exception as e:
                print(f"Error: {e}")
                print(" \n")
                full_prompt = self.prompt_creator[self.dataset_name](example)
                print(full_prompt)
                print('Error in generating logic programs for example: ', example['id'])
        # save outputs
        if self.dataset_name == "ProofWriter":
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.World}_{self.depth}_{self.solver}_{self.model_name}.json'
        elif self.dataset_name == "FOLIO" and self.shot > 1:
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.shot}Shot_{self.solver}_{self.model_name}.json'
        else:
            save_path = f'Answered_Datasets/{self.dataset_name}_{self.solver}_{self.model_name}.json'
        with open(save_path, 'w', errors='ignore') as f:
            json.dump(outputs, f, indent=2, ensure_ascii=False)

# I also want to control the number of shots here, we can add it later
# Control the number of examples
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_name', type=str)
    parser.add_argument('--depth', type=str, default='d5')
    parser.add_argument('--World', type=str, default='')
    parser.add_argument('--solver', type=str)
    parser.add_argument('--shot', type=int, default=1)
    parser.add_argument('--api_key', type=str)
    parser.add_argument('--model_name', type=str, default='gpt-3.5-turbo')
    parser.add_argument('--max_new_tokens', type=int, default=2000)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    logic_program_generator = LogicProgramGenerator(args)
    logic_program_generator.logic_program_generation()




