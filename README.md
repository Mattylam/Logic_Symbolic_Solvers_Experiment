# Logic Symbolic Solvers Experiment

Data and Code for **A Closer Look at Logical Reasoning with LLMs: The Choice of Tool Matters**

Authors: Matthew Lam, Ramya Thatikonda, Ehsan Shareghi — Monash University

## Introduction

The emergence of Large Language Models (LLMs) has demonstrated promising progress in solving logical reasoning tasks effectively. Several recent approaches have proposed changing the role of the LLM from reasoner to translator between natural language statements and symbolic representations, which are then sent to external symbolic solvers to resolve. This paradigm has established the current state-of-the-art result in logical reasoning (i.e., deductive reasoning). This repo evaluates three symbolic solvers (Z3, Pyke, Prover9) across three deductive reasoning benchmarks (FOLIO, ProofWriter, ProntoQA) using multiple LLMs, to isolate how much of the reported performance variance is driven by solver choice versus method.

## Install

Requires Python 3.10+. Install the package with:

```bash
pip install -e .
```

**Core dependencies:** `litellm`, `z3-solver`, `nltk`, `tqdm`, `ply`.

**For Pyke support**, install the optional extra:
```bash
pip install -e ".[pyke]"
```

Note: `pyke3` has no installable distribution on PyPI (metadata exists, release files do not). The above install will always fail. To use `--solver Pyke`, manually install a Python-3-compatible Pyke fork from source first (e.g., `pip install git+https://github.com/pythological/pyke.git`).

**For Prover9 support**, Prover9 must be installed separately on your system.

The package uses [litellm](https://github.com/BerriAI/litellm) as a unified LLM adapter, so any model litellm supports (OpenAI, Gemini, Cohere, Anthropic, local models via Ollama, etc.) works by passing its model name — no new provider code needed. Set the relevant provider API key as an environment variable (e.g. `OPENAI_API_KEY`, `GEMINI_API_KEY`, `COHERE_API_KEY`) or pass `--api_key` directly.

## Datasets

- [ProntoQA](https://github.com/asaparov/prontoqa)
- [ProofWriter](https://allenai.org/data/proofwriter)
- [FOLIO](https://github.com/Yale-LILY/FOLIO)

`Datasets/*.json` is included in the repo, reconstructed from `Processed_Datasets/*.json` (the original raw benchmark releases were never checked into this repo). Reconstructed files are missing the original `options` field (`null` — not recoverable from the processed results); fetch the original benchmark files directly if you need that field. `Prompts/` (few-shot prompt templates) is still not included in the repo.

## Pipeline

```bash
python scripts/generate_logic_programs.py \
    --api_key "your API key" \
    --solver "Z3/Pyke/Prover9" \
    --depth "d2/d3/d5" \
    --dataset_name "ProntoQA|ProofWriter|FOLIO" \
    --model_name "any litellm-supported model name" \
    --shot "1/2/4" \
    --max_new_tokens 2000
```

Saves to `Answered_Datasets/`.

```bash
python scripts/run_inference.py \
    --solver "Z3/Pyke/Prover9" \
    --depth "d2/d3/d5" \
    --dataset_name "ProntoQA|ProofWriter|FOLIO" \
    --model_name "..." \
    --shot "1/2/4"
```

Saves to `Processed_Datasets/`.

```bash
python scripts/run_evaluation.py \
    --solver "Z3/Pyke/Prover9" \
    --depth "d2/d3/d5" \
    --dataset_name "ProntoQA|ProofWriter|FOLIO" \
    --model_name "..." \
    --shot "1/2/4"
```

## Development

Install the dev extra first:
```bash
pip install -e ".[dev]"
```

Then run tests:
```bash
pytest tests/ -v
```

This paper's code was inspired by SatLM and LogicLM.
