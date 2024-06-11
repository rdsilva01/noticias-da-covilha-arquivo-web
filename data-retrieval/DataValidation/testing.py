from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
import torch

# para efeitos de embeddings, considera-se a última camada
def square_rooted(x):
    from math import sqrt 
    return round(sqrt(sum([a*a for a in x])),3)

def Cosine(x,y):
    numerator = sum([a*b for a,b in zip(x,y)])
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator),3)

def get_embeddings_bert(text, model_name):
    # Load a pre-trained model and tokenizer
    model_name = model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    # Tokenize and encode the text
    inputs = tokenizer(text, return_tensors="pt")
    # Get the embeddings
    output = model(**inputs)
    document_embedding = output.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    return document_embedding

print(get_embeddings_bert("Ola", "neuralmind/bert-base-portuguese-cased"))