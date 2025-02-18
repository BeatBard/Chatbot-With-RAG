import os
from dotenv import load_dotenv
from together import Together

# Load environment variables from .env file
load_dotenv()

# Retrieve API key
api_key = os.getenv("TOGETHER_API_KEY")
if not api_key:
    raise ValueError("Missing TogetherAI API key! Ensure it's set in the .env file.")

class TogetherChat:
    def __init__(self, model="meta-llama/Llama-3.3-70B-Instruct-Turbo"):
        self.client = Together(api_key=api_key)
        self.model = model

    def chat(self, messages, temperature=0.7, max_tokens=512):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>", "<|eom_id|>"],
            stream=True
        )
        reply = "".join(token.choices[0].delta.content for token in response if hasattr(token, 'choices'))
        return reply

