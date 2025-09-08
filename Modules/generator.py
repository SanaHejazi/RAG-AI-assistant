from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class AnswerGen:
    def __init__(self, Model_Name:str="google/mt5-small"):
        self.tokenizer = AutoTokenizer.from_pretrained(Model_Name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(Model_Name)
        if torch.cuda.is_available(): 
            self.device = "cuda"
        else:
            self.device = "cpu"
        self.model.to(self.device)

    def generate(self, promp:str, max_new_token:int=256, IQ:float=0.7, top_p: float = 0.9) -> str:

    

