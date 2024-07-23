import cohere
import os

class CohereModel:
    def __init__(self, API_KEY, model_name, max_new_tokens) -> None:
        self.API_KEY =API_KEY
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens


    def generate(self, input_string, temperature=0):
        if self.model_name in ["command-r-plus"]:
            co = cohere.Client(api_key=self.API_KEY)
            response = co.chat(
              model= self.model_name,
              message= input_string,
              max_tokens= self.max_new_tokens,  # Adjust this value based on your needs and the model's limits
              temperature= temperature
            )
            return response.text
        else:
            raise Exception("Model name not recognized")

