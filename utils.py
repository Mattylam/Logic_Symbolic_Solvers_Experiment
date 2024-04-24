import openai
# create the openAI class
class OpenAIModel:
    def __init__(self, API_KEY, model_name, max_new_tokens) -> None:
        openai.api_key = API_KEY
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens

    def generate(self, input_string, temperature = 0.0):
        if self.model_name in ['gpt-4', 'gpt-3.5-turbo']:
            return self.chat_generate(input_string, temperature)
        else:
            raise Exception("Model name not recognized")

    def chat_generate(self, input_string, temperature = 0.0):
        response = openai.chat.completions.create(
                model = self.model_name,
                messages=[
                        {"role": "user", "content": input_string}
                    ],
                max_tokens = self.max_new_tokens,
                temperature = temperature,
                top_p = 1.0
        )
        generated_text = response.choices[0].message.content
        return generated_text