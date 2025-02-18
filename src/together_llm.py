 
from together import Together

class TogetherChat:
    def __init__(self, model="meta-llama/Llama-3.3-70B-Instruct-Turbo"):
        self.client = Together()
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
