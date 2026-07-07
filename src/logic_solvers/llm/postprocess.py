"""Model-agnostic cleanup of raw LLM completions before they're parsed as logic programs.

Replaces the old per-model format_gpt4/format_cohere/remove_strings hacks: every
model's completion goes through the same strip list, so adding a new model
requires no new cleanup code.
"""

_STRIP_SUBSTRINGS = [
    "[Problem Parse Output]:",
    "[Question Parse Output]:",
    "```python",
    "```",
    "def solution():",
]

_STRIP_CHARS = ["�"]


def clean_llm_output(text: str) -> str:
    cleaned = text
    for marker in _STRIP_SUBSTRINGS:
        cleaned = cleaned.replace(marker, "")
    for char in _STRIP_CHARS:
        cleaned = cleaned.replace(char, "")
    lines = [line.strip() for line in cleaned.splitlines()]
    lines = [line[2:] if line.startswith("- ") else line for line in lines]
    lines = [line for line in lines if line]
    return "\n".join(lines)
