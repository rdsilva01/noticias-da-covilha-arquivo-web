import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("NOVA-vision-language/GlorIA-1.3B")
model = AutoModelForCausalLM.from_pretrained("NOVA-vision-language/GlorIA-1.3B")


def getTextEmbeddings(text):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    outputs = model(input_ids, output_hidden_states=True)
    embeddings = outputs.hidden_states[-1]

    mean_embedding = torch.mean(embeddings[0], dim=1)
    
    
    return mean_embedding

