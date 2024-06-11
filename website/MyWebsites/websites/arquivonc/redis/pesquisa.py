import json
import numpy as np
import redis
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.query import Query

host = "localhost"
port = 6379

def connect_redis():    
    r = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
        )
    
    return r

def search_redis_all(return_fields):
    r = connect_redis()
       
    query = Query("*").return_fields(*return_fields).paging(0,10)
    results = r.ft("idx:news").search(query)
    
    return results.docs

def search_news_only(return_fields):
    r = connect_redis()
    index_name_news = 'idx:news' 
    
    query = Query("*").return_fields(*return_fields).paging(0, 10)
    results = r.ft(index_name_news).search(query)
    
    return results.docs


def search_redis(query_emb, index_name, k, vector_field, return_fields, hybrid_fields = "*"):
    r = connect_redis()
       
    # Prepare the Query
    query = (
        Query(f"{hybrid_fields}=>[KNN {k} @{vector_field} $vector as score]")
         .return_fields(*return_fields)
         .sort_by("score")
         .paging(0, k)
         .dialect(2)
    )

    query_params = {"vector": np.array(query_emb, dtype=np.float32).tobytes()}

    # perform vector search
    results = r.ft(index_name).search(query, query_params)
    return results.docs

def pesquisa_emb():

    # r = connect_redis() 
    
    k = 6 # pool das notícias semelhantes
    vector_field = "content_embedding"
    return_fields = ["url", "title", "subtitle", "nid", "content", "image_url", "image_desc", "date", "author", "category", "sub_category", "text_snippet", "formatted_html_content", "formatted_html_content_normal", "formatted_html_keywords", "score"]
    index_name = 'idx:news' 
    
    # print(search_news_only(return_fields)) 
    
    for year in range(2009, 2020):   
        with open(f"news_data/{year}/embeddings_{year}.json", "r", encoding="utf8") as readfile:
                key_moments = json.load(readfile)
        
        final_moments = []        
        for doc in key_moments:
            # doc.pop("keywords", None)
            query_emb = doc['content_embedding']
            
            # PARA IMPLEMENTAR
            # hybrid_fields = "@categoria"
            docs_redis = search_redis(query_emb=query_emb, index_name=index_name, k=k, vector_field=vector_field, return_fields=return_fields, )    
            
            for i, doc_redis in enumerate(docs_redis):
                if i != 0:
                    doc[f'sim_{i}'] = doc_redis['nid']
                    score = 1-float(doc_redis['score'])
                    doc[f'sim_{i}_score'] = f"{score:.3f}"
                    print(f"Similaridade {doc['nid']} com {doc_redis['nid']} = {score:.3f}")
                    
             # remove the embeddings (title_embedding, content,embedding,...) from the key moments  
            new_dict = {
                        "nid" : doc['nid'],
                        "url" : doc['url'],
                        "title" : doc['title'],
                        "subtitle" : doc['subtitle'],
                        "category" : doc['category'],
                        "sub_category" : doc['sub_category'],
                        "date" : doc['date'],
                        "content" : doc['content'],
                        "image_url" : doc['image_url'],
                        "image_desc" : doc['image_desc'],
                        "text_snippet" : doc['text_snippet'],
                        "author" : doc['author'],
                        "formatted_html_content" : doc['formatted_html_content'],
                        "formatted_html_content_normal" : doc['formatted_html_content_normal'],
                        "formatted_html_keywords" : doc['formatted_html_keywords'],
                        "sim_1" : doc['sim_1'],
                        "sim_1_score" : doc['sim_1_score'],
                        "sim_2" : doc['sim_2'],
                        "sim_2_score" : doc['sim_2_score'],
                        "sim_3" : doc['sim_3'],
                        "sim_3_score" : doc['sim_3_score'],
                        "sim_4" : doc['sim_4'],
                        "sim_4_score" : doc['sim_4_score'],
                        "sim_5" : doc['sim_5'],
                        "sim_5_score" : doc['sim_5_score']
                    }
            final_moments.append(new_dict)
        
        with open(f"news_data/{year}/key_moments_{year}.json", "w", encoding="utf8") as writefile:
            json.dump(final_moments, writefile, ensure_ascii=False, indent=4)



def search_all_images():
    r = connect_redis()
    index_name = 'idx:images'
    return_fields = ["image_url", "image_desc", "spacy"]
    
    query = Query("*").return_fields(*return_fields).paging(0, 3000)
    results = r.ft(index_name).search(query)
    
    return results.docs

def main():
    all_images = search_all_images()
    
    with open(f"news_data/image_dataset.json", "r", encoding="utf8") as readfile:
        key_moments = json.load(readfile)
    
    for i, image_redis in enumerate(all_images):
        image_redis_spacy_list = image_redis['spacy'].split(":") # separate the spacy entities, its a string where each entity is separated by :
        similar_images = []
        for j, image in key_moments:
            for entity in image_redis_spacy_list:
                if entity in image['spacy']:
                    similar_images.append(image['image_desc'])
                    
                    
    
        
if __name__ == "__main__":
    main()
