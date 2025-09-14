from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class AnswerGen:
    def __init__(self, model_name: str = "google/flan-t5-large"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def generate(self, prompt: str, max_new_token: int = 256, IQ: float = 0.7, top_p: float = 0.9) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_token,
            do_sample=True,
            temperature=IQ,
            top_p=top_p,
            no_repeat_ngram_size=3
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
