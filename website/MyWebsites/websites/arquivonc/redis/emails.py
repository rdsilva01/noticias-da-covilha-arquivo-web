import json
import numpy as np
import redis
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition
import time
import argparse
import os

host = 'localhost'
port = 6379

def connect_redis(host, port):    
    r = redis.Redis(
            host=host,
            port=port,
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
    for i, doc in enumerate(documents):
        key = f"{doc_prefix}{str(i)}"
        r.hset(key, mapping=doc)
    
    print("Documents indexed")
    
def index_documents_capas(r, doc_prefix, documents):
    for date, doc_data in documents.items():
        key = f"{doc_prefix}{date}"
        r.hmset(key, doc_data)
    
    print("Documents indexed")

def main():
    r = connect_redis(host=host, port=port)
    
    # EMAILS
    index_name = 'idx:emails'
    fields_news = [TextField(name="email"),
                   TextField(name="token"),
                   NumericField(name="active")]


    create_index(r, index_name, "newsletter_email:", fields_news) 
    
    index_name = 'idx:newsletter'
    fields_news = [TextField(name="data"),
                   TextField(name="nids"),
                   TextField(name="capaId"),]
    
    create_index(r, index_name, "newsletter_item:", fields_news) 
    
#       doc_prefix = f'newsletter_email:'  
#       index_documents(r, doc_prefix, key_moments) 
    
if __name__ == '__main__':
    main()
