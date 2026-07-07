.PHONY: help install install-dev install-pyke test generate infer evaluate clean

# Overridable pipeline parameters — e.g. make generate DATASET=FOLIO SOLVER=Z3 MODEL=gpt-4o
DATASET       ?= FOLIO
SOLVER        ?= Z3
MODEL         ?= gpt-4o
DEPTH         ?= d5
SHOT          ?= 1
WORLD         ?=
API_KEY       ?=
MAX_NEW_TOKENS ?= 2000

help:
	@echo "Targets:"
	@echo "  install       Install the package (core dependencies only)"
	@echo "  install-dev   Install the package with dev/test dependencies"
	@echo "  install-pyke  Install the optional pyke extra (will fail — see README)"
	@echo "  test          Run the test suite"
	@echo "  generate      Run stage 1 (logic program generation)"
	@echo "  infer         Run stage 2 (symbolic solver inference)"
	@echo "  evaluate      Run stage 3 (scoring)"
	@echo "  clean         Remove caches and generated solver artifacts"
	@echo ""
	@echo "Pipeline variables (override on the command line):"
	@echo "  DATASET=$(DATASET) SOLVER=$(SOLVER) MODEL=$(MODEL) DEPTH=$(DEPTH) SHOT=$(SHOT) WORLD=$(WORLD)"
	@echo ""
	@echo "Example: make generate DATASET=ProofWriter SOLVER=Pyke MODEL=gpt-4o WORLD=CWA API_KEY=sk-..."

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-pyke:
	pip install -e ".[pyke]"

test:
	pytest tests/ -v

generate:
	python scripts/generate_logic_programs.py \
		--dataset_name $(DATASET) \
		--solver $(SOLVER) \
		--model_name $(MODEL) \
		--depth $(DEPTH) \
		--shot $(SHOT) \
		--World "$(WORLD)" \
		--api_key "$(API_KEY)" \
		--max_new_tokens $(MAX_NEW_TOKENS)

infer:
	python scripts/run_inference.py \
		--dataset_name $(DATASET) \
		--solver $(SOLVER) \
		--model_name $(MODEL) \
		--depth $(DEPTH) \
		--shot $(SHOT) \
		--World "$(WORLD)"

evaluate:
	python scripts/run_evaluation.py \
		--dataset_name $(DATASET) \
		--solver $(SOLVER) \
		--model_name $(MODEL) \
		--depth $(DEPTH) \
		--shot $(SHOT) \
		--World "$(WORLD)"

clean:
	rm -rf tmp .cache_program compiled_krb .pytest_cache
	find . -type d -name __pycache__ -not -path "./.git/*" -exec rm -rf {} +
