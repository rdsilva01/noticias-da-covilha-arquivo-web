import json
import numpy as np
import redis
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition

def connect_redis():    
    r = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True,
        )

    return r

def create_index(r, index_name, doc_prefix, fields):    
    try:
        #  check if index exists
        r.ft(index_name).info()
        print("Index already exists!")
    except:
        # create index
        r.ft(index_name).create_index(fields=fields, definition=IndexDefinition(prefix=[doc_prefix]))
        print("Index created")

def drop_data(r, index_name, delete_documents=True):
    try:
        r.ft(index_name).dropindex(delete_documents=delete_documents)
        print('Index and data dropped')
    except:
        print('Index does not exist')
        
def index_documents(r, doc_prefix, documents, *vector_field):
    for i, doc in enumerate(documents): # so documents is LIST of
        key = f"{doc_prefix}{str(i)}"
        
        for field in vector_field:
            # create byte vectors for item
            text_embedding = np.array(doc[field], dtype=np.float32).tobytes()

             # replace list of floats with byte vectors
            doc[field] = text_embedding
        
        r.hset(key, mapping=doc)
    
    print("Documents indexed")

def get_embeddings_bert(text, model_name):
    from transformers import AutoTokenizer, AutoModel

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