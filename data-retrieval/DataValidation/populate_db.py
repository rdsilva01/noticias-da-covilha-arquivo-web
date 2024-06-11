import json
import numpy as np
import redis
from redis.commands.search.field import TextField, VectorField
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

def index_documents(r, doc_prefix, documents, *vector_field):
    for i, doc in enumerate(documents):
        key = f"{doc_prefix}{str(i)}"
        
        for field in vector_field:
            text_embedding = np.array(doc[field], dtype=np.float32).tobytes()
            doc[field] = text_embedding
        
        r.hset(key, mapping=doc)
    
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
    
def convert_lists_to_strings_images(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if value is None:
                new_data[key] = ""  
            elif isinstance(value, list):
                new_data[key] = ":".join(str(item) for item in value) 
            elif isinstance(value, dict):
                new_data[key] = convert_lists_to_strings_images(value)  
            else:
                new_data[key] = value
        return new_data
    elif isinstance(data, list):
        new_list = []
        for item in data:
            new_list.append(convert_lists_to_strings_images(item))
        return new_list
    else:
        return data

def main(year):
    
    if year is not None:
            r = connect_redis(host=host, port=port)
            # # NOTÍCIAS
            # index_name = 'idx:news'
            
            # doc_prefix = f'nc_news:{year}'  
            # with open(f"news_data/{year}/validated_{year}.json", "r", encoding="utf8") as readfile:
            #     key_moments = json.load(readfile)

            # key_moments = convert_lists_to_strings(key_moments)
            # # Constants
            # vector_field1 = 'title_emb'
            # vector_field2 = 'content_emb'
            # VECTOR_DIM = len(key_moments[0][vector_field1]) # length of the vectors
            # VECTOR_NUMBER = len(key_moments) # initial number of vectors
            # DISTANCE_METRIC = "COSINE" 
            
            # title_emb = VectorField(vector_field1,
            #     "FLAT", {
            #         "TYPE": "FLOAT32",
            #         "DIM": VECTOR_DIM,
            #         "DISTANCE_METRIC": DISTANCE_METRIC,
            #         "INITIAL_CAP": VECTOR_NUMBER,
            #     }
            # )
              
            # content_emb = VectorField(vector_field2,
            #     "FLAT", {
            #         "TYPE": "FLOAT32",
            #         "DIM": VECTOR_DIM,
            #         "DISTANCE_METRIC": DISTANCE_METRIC,
            #         "INITIAL_CAP": VECTOR_NUMBER,
            #     }
            # )

            # fields_news = [TextField(name="url"),
            #     TextField(name="title"),
            #     title_emb,
            #     TextField(name="subtitle"),
            #     TextField(name="nid"),
            #     TextField(name="content"),
            #     content_emb,
            #     TextField(name="image_desc"),
            #     TextField(name="date"),
            #     TextField(name="author"),
            #     TextField(name="category"),
            #     TextField(name="sub_category")]
            
            # create_index(r, index_name, "", fields_news) 
            # index_documents(r, doc_prefix, key_moments) 
            
            if int(year) == 2009:
                 # IMAGENS
                index_name = 'idx:images'
                fields_images = [TextField(name="image_url"),
                        TextField(name="image_desc"),
                        TextField(name="news_url"),
                        TextField(name="news_title"),
                        TextField(name="news_subtitle"),
                        TextField(name="news_text_snippet"),
                        TextField(name="news_date")]
                
                create_index(r, index_name, "nc_images:", fields_images)
                
                # it has no year
                doc_prefix = 'nc_images:'
                with open(f"news_data/image_dataset.json", "r", encoding="utf8") as readfile:
                    image_dataset = json.load(readfile)
                    
                image_dataset = convert_lists_to_strings_images(image_dataset)    
                index_documents(r, doc_prefix, image_dataset) 

    
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-y', '--year', help='Year', required=True, type=int)
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    
    arguments = parse_arguments()
    main(arguments.year)
