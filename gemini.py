import google.generativeai as genai
from google.generativeai.types import ContentType
#from PIL import Image
#from IPython.display import Markdown
import time
#import cv2
import os

class GeminiModel:
    def __init__(self, API_KEY, model_name, max_new_tokens) -> None:
        os.environ["GOOGLE_API_KEY"] = API_KEY
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens


    def generate(self, input_string, temperature=0):
        if self.model_name in ['gemini-1.0-pro-latest', 'gemini-1.5-pro-latest']:
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_DANGEROUS",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]
            generation_config = {
                "temperature": temperature,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": self.max_new_tokens
            }
            model = genai.GenerativeModel(self.model_name, generation_config = generation_config, safety_settings=safety_settings)

            response = model.generate_content(input_string)
            for candidate in response.candidates:
                r = [part.text for part in candidate.content.parts]
                return r[0]
            #return response.candidates[0].content.parts.text
        else:
            raise Exception("Model name not recognized")