# Logic_Symbolic_Solvers_Experiment

Data and Code for **A Closer Look at Logical Reasoning with LLMs: The Choice of Tool Matters**

Authors: Matthew Lam, Ehsan Shareghi

Monash University, Submission to CONNL2024

## Introduction

Existing published results try a variety of formalism and tools to compare the benefits of incorporating LLM with symbolic solvers (Pan et al., 2023; Ye et al., 2023; Gao
et al., 2023; Lyu et al., 2023). However, there is a degree of inconsistency in how these existing papers conduct experiments on different datasets, making it impossible to have a fair understanding of each approach. A contributing factor to this is the variability of tools and methods that are being used in different papers.  Pan et al. (2023) justifies the use of different solvers based on the type of reasoning dataset it is trying to solve (e.g.,  Pyke is used to solve a Deductive Reasoning Dataset ProofWriter), whereas Ye et al. (2023) uses Z3  an SMT solver on the same dataset exhibiting better performance. There is currently a lack of constituent comparison that will allow others to understand better where this performance gain stems from. In this paper, we take 3 widely used tools Z3 , Pyke and Prover9 and compare (1) the difficulty of translating natural language into their desired input format, and (2) the internal capability of these tools at solving certain satisfiability tasks. To conduct this, we choose GPT-3.5-Turbo  and LLaMA-13B, and 3 widely used benchmarks ProofWriter, FOLIO , ProntoQA, and conduct a fair side-by-side comparison of tools by trying various number of identical few-shots prompts, and minimal adjustment for each solver.

First, install all the required packages:

```bash
pip install -r requirements.txt
```

## Datasets

We evaluate on the following datasets:

- [ProntoQA](https://github.com/asaparov/prontoqa): Deductive resoning dataset. 
- [ProofWriter](https://allenai.org/data/proofwriter): Deductive resoning dataset. 
- [FOLIO](https://github.com/Yale-LILY/FOLIO): First-Order Logic reasoning dataset.

## Logic Program Generation

To generate logic programs for logical reasoning problems in each dataset, at the root directory, run the following commands:

```bash
python models/logic_program.py \
    --api_key "Your OpenAI API Key" \
    --solver "Z3/Pyke/Prover9"
    --depth "d2/d3/d5"
    --dataset_name "Dataset Name [ProntoQA | ProofWriter | FOLIO]" \
    --model_name "Model Name [text-davinci-003 | gpt-4]" \
    --max_new_tokens 2000 \
```
The generated logic programs will be saved in `Answered_Datasets`.

## Logic Inference with Symbolic Solver

After generating logic programs, we can perform inference with symbolic solvers. At the root directory, run the following commands:

```bash
python models/logic_inference.py \
    --solver "Z3/Pyke/Prover9"
    --depth "d2/d3/d5"
    --dataset_name "Dataset Name [ProntoQA | ProofWriter | FOLIO]" \
    --model_name "Model Name [text-davinci-003 | gpt-4]" \
```
The logic reasoning results will be saved in `Processed_Datasets`.

## Evaluation

To evaluate the logic reasoning results, please run the following commands:

```bash
python models/evaluation.py \
    --solver "Z3/Pyke/Prover9"
    --depth "d2/d3/d5"
    --dataset_name "Dataset Name [ProntoQA | ProofWriter | FOLIO]" \
    --model_name "Model Name [text-davinci-003 | gpt-4]"
```

This paper's code was inspired by SatLM and LogicLM. 
