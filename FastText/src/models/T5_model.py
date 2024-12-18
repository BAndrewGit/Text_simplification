import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

def load_t5_model():
    model = T5ForConditionalGeneration.from_pretrained("t5-3b")
    tokenizer = T5Tokenizer.from_pretrained("t5-3b")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return model, tokenizer