# Logic Symbolic Solvers Experiment

Data and Code for **A Closer Look at Logical Reasoning with LLMs: The Choice of Tool Matters**

Authors: Matthew Lam, Ramya Thatikonda, Ehsan Shareghi — Monash University

## Introduction

The emergence of Large Language Models (LLMs) has demonstrated promising progress in solving logical reasoning tasks effectively. Several recent approaches have proposed changing the role of the LLM from reasoner to translator between natural language statements and symbolic representations, which are then sent to external symbolic solvers to resolve. This paradigm has established the current state-of-the-art result in logical reasoning (i.e., deductive reasoning). This repo evaluates three symbolic solvers (Z3, Pyke, Prover9) across three deductive reasoning benchmarks (FOLIO, ProofWriter, ProntoQA) using multiple LLMs, to isolate how much of the reported performance variance is driven by solver choice versus method.

## Install

Requires Python 3.10+. Install the package with:

```bash
make install
# or: pip install -e .
```

To install everything needed for development and testing in one step (core + dev dependencies; the `pyke` extra is deliberately excluded since it cannot succeed — see below):
```bash
make install-all
```

**Core dependencies:** `litellm`, `z3-solver`, `nltk`, `tqdm`, `ply`.

**For Pyke support**, install the optional extra:
```bash
make install-pyke
# or: pip install -e ".[pyke]"
```

Note: `pyke3` has no installable distribution on PyPI (metadata exists, release files do not). The above install will always fail. To use `--solver Pyke`, you must manually install a Python-3-compatible Pyke fork from source yourself — there is no pip command that works out of the box.

**For Prover9 support**, Prover9 must be installed separately on your system.

The package uses [litellm](https://github.com/BerriAI/litellm) as a unified LLM adapter, so any model litellm supports (OpenAI, Gemini, Cohere, Anthropic, local models via Ollama, etc.) works by passing its model name — no new provider code needed.

**API keys:** copy `.env.example` to `.env` and fill in the keys for whichever providers you use:
```bash
cp .env.example .env
```
`.env` is gitignored — never commit it. The package loads it automatically (via `python-dotenv`) and litellm reads the provider-specific variable (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `COHERE_API_KEY`, `ANTHROPIC_API_KEY`, ...) straight from the environment. `--api_key` / `API_KEY=` on the CLI is only needed to override this for a single run.

## Datasets

- [ProntoQA](https://github.com/asaparov/prontoqa)
- [ProofWriter](https://allenai.org/data/proofwriter)
- [FOLIO](https://github.com/Yale-LILY/FOLIO)

`Datasets/*.json` is included in the repo, reconstructed from `Processed_Datasets/*.json` (the original raw benchmark releases were never checked into this repo). Reconstructed files are missing the original `options` field (`null` — not recoverable from the processed results); fetch the original benchmark files directly if you need that field. `Prompts/` (few-shot prompt templates) is still not included in the repo.

## Pipeline

Each stage has a `make` target — pass parameters as `VAR=value` (see `make help` for the full variable list and defaults). The underlying `python scripts/*.py` command works the same way if you'd rather call it directly.

```bash
make generate DATASET=FOLIO SOLVER=Z3 MODEL=gpt-4o
# or: python scripts/generate_logic_programs.py \
#     --solver "Z3/Pyke/Prover9" \
#     --depth "d2/d3/d5" \
#     --dataset_name "ProntoQA|ProofWriter|FOLIO" \
#     --model_name "any litellm-supported model name" \
#     --shot "1/2/4" \
#     --max_new_tokens 2000
```

Saves to `Answered_Datasets/`.

```bash
make infer DATASET=FOLIO SOLVER=Z3 MODEL=gpt-4o
# or: python scripts/run_inference.py \
#     --solver "Z3/Pyke/Prover9" \
#     --depth "d2/d3/d5" \
#     --dataset_name "ProntoQA|ProofWriter|FOLIO" \
#     --model_name "..." \
#     --shot "1/2/4"
```

Saves to `Processed_Datasets/`.

```bash
make evaluate DATASET=FOLIO SOLVER=Z3 MODEL=gpt-4o
# or: python scripts/run_evaluation.py \
#     --solver "Z3/Pyke/Prover9" \
#     --depth "d2/d3/d5" \
#     --dataset_name "ProntoQA|ProofWriter|FOLIO" \
#     --model_name "..." \
#     --shot "1/2/4"
```

For `ProofWriter`, also pass `WORLD=OWA` or `WORLD=CWA` (`--World` on the raw CLI) to any of the three commands above.

To run all three stages back-to-back for one dataset/solver/model combination:
```bash
make pipeline DATASET=FOLIO SOLVER=Z3 MODEL=gpt-4o
```

## Development

Install the dev extra first:
```bash
make install-dev
# or: pip install -e ".[dev]"
```

Then run tests:
```bash
make test
# or: pytest tests/ -v
```

`make clean` removes test/solver scratch artifacts (`tmp/`, `.cache_program/`, `compiled_krb/`, `__pycache__/`, `.pytest_cache/`).

This paper's code was inspired by SatLM and LogicLM.
