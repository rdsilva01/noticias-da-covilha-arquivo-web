import json
import redis
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition

def connect_redis():    
    r = redis.Redis(
            host="localhost",
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
        
def index_documents(r, doc_prefix, documents):
    if documents is None:
        print("No documents to index")
        return
    
    for i, doc in enumerate(documents):
        key = f"{doc_prefix}{str(i)}"
        r.hset(key, mapping=doc)
    
    print("Documents indexed")