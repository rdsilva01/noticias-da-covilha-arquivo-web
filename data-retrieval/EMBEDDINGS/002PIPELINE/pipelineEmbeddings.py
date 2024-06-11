# pipeline de extrair os embeddings
import json
import os
from transformers import AutoTokenizer, AutoModel
from chunkipy import TextChunker, TokenEstimator
import torch
import numpy as np


class BertTokenEstimator():
    def __init__(self, model):
        self.bert_tokenizer = AutoTokenizer.from_pretrained(model)

    def estimate_tokens(self, text):
        return len(self.bert_tokenizer.encode(text))
    

model_name = "neuralmind/bert-base-portuguese-cased"  # "PORTULAN/albertina-ptpt"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embeddings_bert(text, tokenizer, model):
    # Tokenize and encode the text
    inputs = tokenizer(text, return_tensors="pt")

    # Get the embeddings
    output = model(**inputs)

    document_embedding = output.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    return document_embedding

def save_embeddings(year, start_nid=None):
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/DataValidation/pipeline/news_data/{year}/2validated_{year}.json', "r", encoding="utf8") as readfile:
        key_moments = json.load(readfile)
    
    # Sort key_moments by nid
    key_moments.sort(key=lambda x: x['nid'])
    # key_moments = key_moments[:10]
    
    if start_nid:
        # Find the index of the document with the specified nid
        start_index = next((i for i, doc in enumerate(key_moments) if doc['nid'] == start_nid), None)
        if start_index is None:
            print(f"Document with nid {start_nid} not found.")
            return
        # Start processing from the document with the specified nid
        key_moments = key_moments[start_index:]
    
    final_moments = []
    for i, doc in enumerate(key_moments):
        title = doc['title']
        content = doc['content']
        title_content = title + " " + content
        
        title_emb = get_embeddings_bert(title, tokenizer, model).tolist()


        content_chunker = TextChunker(512, tokens=True, token_estimator=BertTokenEstimator(model_name))
        content_chunks = content_chunker.chunk(content)
        content_emb = get_embeddings_bert(content_chunks[0], tokenizer, model).tolist()
        title_content_chunks = content_chunker.chunk(title_content)
        title_content_emb = get_embeddings_bert(title_content_chunks[0], tokenizer, model).tolist()

        doc['title_embedding'] = title_emb
        doc['content_embedding'] = content_emb
        doc['title_content_embedding'] = title_content_emb
    
        print(f"Embeddings for article {doc['nid']} done")
        
        final_moments.append(doc)
        # Save embeddings for this document
        if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/DataValidation/pipeline/news_data/{year}/embeddings') == False:
            os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/DataValidation/pipeline/news_data/{year}/embeddings')
        
        # with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/DataValidation/news_data/{year}/embeddings/embeddings_{year}_doc_{doc["nid"]}.json', "w") as writefile:
        #     json.dump(doc, writefile, indent=4, ensure_ascii=False)
        # print(f"Embeddings for article {doc['nid']} saved")

    # saving all embeddings at the end
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/DataValidation/pipeline/news_data/{year}/embeddings_{year}.json', "w") as writefile:
        json.dump(final_moments, writefile, indent=4, ensure_ascii=False)
    print("All embeddings saved")
    
def main():
    for i in range(2009, 2020):
        save_embeddings(i)
        
main()