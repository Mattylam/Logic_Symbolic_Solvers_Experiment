"""Single any-model LLM adapter via litellm, replacing OpenAIModel/GeminiModel/CohereModel.

Adding support for a new model is a config change (extend _PROVIDER_PREFIX_RULES
below if litellm needs a provider-prefixed model string), not a new class.
"""

import litellm

# litellm routes by model-name prefix (e.g. "gemini/<model>"). Only Gemini
# currently needs prefixing for the model names used by this project;
# OpenAI and Cohere model names are already litellm-recognized as-is.
_PROVIDER_PREFIX_RULES = {
    "gemini": "gemini/",
}


def normalize_model_name(model_name: str) -> str:
    for bare_prefix, litellm_prefix in _PROVIDER_PREFIX_RULES.items():
        if model_name.startswith(litellm_prefix):
            return model_name
        if model_name.startswith(bare_prefix):
            return f"{litellm_prefix}{model_name}"
    return model_name


class LiteLLMProvider:
    def __init__(self, model_name: str, api_key: str | None = None, max_new_tokens: int = 2000) -> None:
        self.model_name = normalize_model_name(model_name)
        self.api_key = api_key
        self.max_new_tokens = max_new_tokens

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        response = litellm.completion(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_new_tokens,
            temperature=temperature,
            api_key=self.api_key,
        )
        return response.choices[0].message.content
