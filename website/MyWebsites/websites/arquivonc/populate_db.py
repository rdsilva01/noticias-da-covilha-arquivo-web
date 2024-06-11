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

# def index_documents(r, doc_prefix, documents, *vector_field):
#     for i, doc in enumerate(documents): # so documents is LIST of
#         key = f"{doc_prefix}{str(i)}"
        
#         for field in vector_field:
#             # create byte vectors for item
#             text_embedding = np.array(doc[field], dtype=np.float32).tobytes()

#              # replace list of floats with byte vectors
#             doc[field] = text_embedding
        
#         r.hset(key, mapping=doc)
    
#     print("Documents indexed")
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

    
#######################################
# AUXILIAR: Convert lists to strings  #
#######################################
def convert_lists_to_strings(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if value is None:
                new_data[key] = ""  # Replace None with empty string
            elif isinstance(value, list):
                new_data[key] = " ".join(value)
            elif isinstance(value, dict):
                new_data[key] = convert_lists_to_strings(value)
            else:
                new_data[key] = value
        return new_data
    elif isinstance(data, list):
        new_list = []
        for item in data:
            new_list.append(convert_lists_to_strings(item))
        return new_list
    else:
        return data
    
def convert_lists_to_strings_capas(data):
    new_data = {}
    for key, value in data.items():
        if isinstance(value, list):
            new_data[key] = " ".join(str(item) for item in value)
        elif isinstance(value, dict):
            new_data[key] = convert_lists_to_strings(value)
        else:
            new_data[key] = value
    return new_data


def populate(year):
    if year is not None:
        r = connect_redis(host=host, port=port)
        
        # drop_data(r, 'idx:nc', delete_documents=True)
        # drop_data(r, 'idx:nc_capas', delete_documents=True)
        
        # NOTÍCIAS
        index_name = 'idx:news'
        fields_news = [TextField(name="url"),
                TextField(name="title"),
                TextField(name="subtitle"),
                TextField(name="nid"),
                TextField(name="content"),
                TextField(name="image_desc"),
                TextField(name="date"),
                TextField(name="author"),
                TextField(name="category"),
                TextField(name="sub_category")]

    
        create_index(r, index_name, "", fields_news) 
        
        for year in range(year, year + 1):
            print(year)
            doc_prefix = f'nc_news:{year}'  
            with open(f"news_data/{year}/validated_{year}.json", "r", encoding="utf8") as readfile:
                key_moments = json.load(readfile)

            key_moments = convert_lists_to_strings(key_moments)
            index_documents(r, doc_prefix, key_moments) 
        
        # CAPAS
        index_name_capas = 'idx:capas'
        fields_capas = [
            TextField(name="url"),
            TextField(name="title"),
            TextField(name="date")
        ]

        create_index(r, index_name_capas, "", fields_capas) 

        if year < 2016:
            for year in range(year, year+1):
                print("capa")
                print(year)
                doc_prefix = f'nc_capas'  
                with open(f"news_data/{year}/capa_{year}/capa_{year}.json", "r", encoding="utf8") as readfile:
                    key_moments = json.load(readfile)

                for date, info in key_moments.items():
                    key = f"{doc_prefix}:{date}"
                    for field, value in info.items():
                        # Ensure value is converted to string if necessary
                        value = str(value)
                        r.hset(key, field, value)

