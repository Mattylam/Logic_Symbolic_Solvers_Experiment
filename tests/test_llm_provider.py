from logic_solvers.llm.provider import LiteLLMProvider, normalize_model_name


def test_normalize_gemini_name_adds_provider_prefix():
    assert normalize_model_name("gemini-1.0-pro-latest") == "gemini/gemini-1.0-pro-latest"


def test_normalize_already_prefixed_gemini_name_is_unchanged():
    assert normalize_model_name("gemini/gemini-1.5-pro-latest") == "gemini/gemini-1.5-pro-latest"


def test_normalize_openai_and_cohere_names_are_unchanged():
    assert normalize_model_name("gpt-4o") == "gpt-4o"
    assert normalize_model_name("command-r-plus") == "command-r-plus"


def test_generate_calls_litellm_completion_with_expected_args(mocker):
    mock_completion = mocker.patch("logic_solvers.llm.provider.litellm.completion")
    mock_completion.return_value.choices = [
        mocker.Mock(message=mocker.Mock(content="foo(bar)"))
    ]

    provider = LiteLLMProvider(model_name="gpt-4o", api_key="sk-test", max_new_tokens=500)
    result = provider.generate("translate this", temperature=0.2)

    assert result == "foo(bar)"
    mock_completion.assert_called_once_with(
        model="gpt-4o",
        messages=[{"role": "user", "content": "translate this"}],
        max_tokens=500,
        temperature=0.2,
        api_key="sk-test",
    )


def test_generate_normalizes_gemini_model_name(mocker):
    mock_completion = mocker.patch("logic_solvers.llm.provider.litellm.completion")
    mock_completion.return_value.choices = [
        mocker.Mock(message=mocker.Mock(content="ok"))
    ]

    provider = LiteLLMProvider(model_name="gemini-1.0-pro-latest", api_key="key")
    provider.generate("prompt")

    called_model = mock_completion.call_args.kwargs["model"]
    assert called_model == "gemini/gemini-1.0-pro-latest"
