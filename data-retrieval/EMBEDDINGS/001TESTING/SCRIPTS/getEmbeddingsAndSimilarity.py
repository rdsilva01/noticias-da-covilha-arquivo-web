import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification, AutoModel
import torch
import numpy as np

def square_rooted(x):
    from math import sqrt 
    return round(sqrt(sum([a*a for a in x])),3)

def Cosine(x,y):
    numerator = sum([a*b for a,b in zip(x,y)])
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator),3)

# GET THE EMBEDDINGS
def getTextEmbeddings(text, model_name):
    # Load a pre-trained model and tokenizer
    model_name = model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    # Tokenize and encode the text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, )
    # Get the embeddings
    output = model(**inputs)
    document_embedding = output.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    return document_embedding

def getTextGloriaEmbeddings(text, model_name):
    model_name = model_name
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    inputs = tokenizer(text, return_tensors="pt")
    
    output = model(**inputs)
    document_embedding = output.last_hidden_state[0][-1].squeeze().detach().numpy()
    return document_embedding

# GUARDAR OS EMBEDDINGS NUM JSON
def save_embeddings(year, model, tokenizer, f_path, type_name, start_nid=None):
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/validated_{year}.json', "r", encoding="utf8") as readfile:
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
    
    for i, doc in enumerate(key_moments):
        title = doc['title']
        content = doc['content']
        title_plus_content = title + ". " + content
        
        title_embedding = getTextEmbeddings(title.lower(), model, tokenizer)
        content_embedding = getTextEmbeddings(content.lower(), model, tokenizer)
        title_plus_content_embedding = getTextEmbeddings(title_plus_content.lower(), model, tokenizer)
        
        doc['title_embedding'] = title_embedding
        doc['content_embedding'] = content_embedding
        doc['title_plus_content_embedding'] = title_plus_content_embedding
        
        print(f"Embeddings for article {doc['nid']} done")
        
        # Save embeddings for this document
        if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/embeddings_data_{f_path}') == False:
            os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/embeddings_data_{f_path}')
        
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/embeddings_data_{f_path}/embeddings_{year}_doc_{doc["nid"]}.json', "w") as writefile:
            json.dump(doc, writefile, indent=4, ensure_ascii=False)
        print(f"Embeddings for article {doc['nid']} saved")

    # Save all embeddings at the end
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/embeddings_data_{f_path}/embeddings_{year}.json', "w") as writefile:
        json.dump(key_moments, writefile, indent=4, ensure_ascii=False)
    print("All embeddings saved")


def get_similarity(year, articles, f_path, type_name):
    articles2 = articles
    # articles = articles[:10]
    for i, article in enumerate(articles):
        title_embedding = article['title_embedding']
        content_embedding = article['content_embedding']
        title_plus_content_embedding = article['title_plus_content_embedding']
        
        complete_sim_list = []
        
        for j, article2 in enumerate(articles2):
            
            title_embedding2 = article2['title_embedding']
            content_embedding2 = article2['content_embedding']
            title_plus_content_embedding2 = article2['title_plus_content_embedding']
            
            title_similarity = Cosine(title_embedding, title_embedding2)
            content_similarity = Cosine(content_embedding, content_embedding2)
            title_plus_content_similarity = Cosine(title_plus_content_embedding, title_plus_content_embedding2)
            
            if title_similarity != 1 and content_embedding != 1 and title_plus_content_similarity != 1:
                # print(f"Title similarity greater than 0.9 found between documents {article['nid']} and {article2['nid']}")
                # print(f"Title similarity: {title_similarity}")
                # print(f"Content similarity: {content_similarity}")
                # print(f"Title + content similarity: {title_plus_content_similarity}")
                # print(f"Title: {article['title']}")
                # print(f"Content: {article['content']}")
                # print(f"Title: {article2['title']}")
                # print(f"Content: {article2['content']}")
                
                sim_dict = {
                    'nid_1': article['nid'],
                    'nid_2': article2['nid'],
                    'title_1': article['title'],
                    'content_1': article['content'],
                    'title_2': article2['title'],
                    'content_2': article2['content'],
                    'title_similarity': title_similarity,
                    'content_similarity': content_similarity,
                    'title_plus_content_similarity': title_plus_content_similarity
                }
                
                complete_sim_list.append(sim_dict)
                #save to a file with both nids
                if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}') == False:
                    os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}')
                
                if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/similarities_{f_path}') == False:
                    os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/similarities_{f_path}')
                
                if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/similarities_{f_path}/similarities_{year}_{article["nid"]}') == False:
                    os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/similarities_{f_path}/similarities_{year}_{article["nid"]}')
                
                with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/similarities_{f_path}/similarities_{year}_{article["nid"]}/similarities_{year}_{article["nid"]}_{article2["nid"]}.json', "w") as writefile:
                    json.dump(sim_dict, writefile, indent=4, ensure_ascii=False)
                    
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/{type_name}/similarities_{f_path}/similarities_{year}_{article["nid"]}/full_similarities.json', "w") as writefile:
            json.dump(complete_sim_list, writefile, indent=4, ensure_ascii=False)
    


def getModelSimilarities(model_name, title_ref, text_ref, title_plus_text_ref, titles, texts, titles_plus_texts, type_name):
    if model_name == 'gloria':
        title_ref_embedding = getTextGloriaEmbeddings(title_ref, model_name="NOVA-vision-language/GlorIA-1.3B")
        text_ref_embedding = getTextGloriaEmbeddings(text_ref, model_name="NOVA-vision-language/GlorIA-1.3B")
        title_plus_text_ref_embedding = getTextGloriaEmbeddings(title_plus_text_ref, model_name="NOVA-vision-language/GlorIA-1.3B")
        dict = {}

        for i in range(10):
            title_embedding = getTextEmbeddings(titles[i], model_name="NOVA-vision-language/GlorIA-1.3B")
            text_embedding = getTextEmbeddings(texts[i], model_name="NOVA-vision-language/GlorIA-1.3B")
            title_plus_text_embedding = getTextEmbeddings(titles_plus_texts[i], model_name="NOVA-vision-language/GlorIA-1.3B")
            
            title_similarity = Cosine(title_ref_embedding, title_embedding)
            text_similarity = Cosine(text_ref_embedding, text_embedding)
            title_plus_text_similarity = Cosine(title_plus_text_ref_embedding, title_plus_text_embedding)
            
            dict[i] = {
                'id': i,
                'title_similarity': title_similarity,
                'text_similarity': text_similarity,
                'title_plus_text_similarity': title_plus_text_similarity
            }
            print(f'{i}')
            
        title_dict = sorted(dict.values(), key=lambda x: x['title_similarity'], reverse=True)
        text_dict = sorted(dict.values(), key=lambda x: x['text_similarity'], reverse=True)
        title_plus_text_dict = sorted(dict.values(), key=lambda x: x['title_plus_text_similarity'], reverse=True)
        main_list = [title_dict, text_dict, title_plus_text_dict]
        if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{type_name}') == False:
            os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{type_name}')
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{type_name}/similarities_{model_name}.json', "w") as writefile:
            json.dump(main_list, writefile, indent=4, ensure_ascii=False)
            
    elif model_name == 'bert':
        title_ref_embedding = getTextEmbeddings(title_ref, model_name="neuralmind/bert-base-portuguese-cased")
        text_ref_embedding = getTextEmbeddings(text_ref, model_name="neuralmind/bert-base-portuguese-cased")
        title_plus_text_ref_embedding = getTextEmbeddings(title_plus_text_ref, model_name="neuralmind/bert-base-portuguese-cased")

        dict = {}

        for i in range(10):
            title_embedding = getTextEmbeddings(titles[i], model_name="neuralmind/bert-base-portuguese-cased")
            text_embedding = getTextEmbeddings(texts[i], model_name="neuralmind/bert-base-portuguese-cased")
            title_plus_text_embedding = getTextEmbeddings(titles_plus_texts[i], model_name="neuralmind/bert-base-portuguese-cased")
            
            title_similarity = Cosine(title_ref_embedding, title_embedding)
            text_similarity = Cosine(text_ref_embedding, text_embedding)
            title_plus_text_similarity = Cosine(title_plus_text_ref_embedding, title_plus_text_embedding)
            
            dict[i] = {
                'id': i,
                'title_similarity': title_similarity,
                'text_similarity': text_similarity,
                'title_plus_text_similarity': title_plus_text_similarity
            }
            print(f'{i}')
            
        title_dict = sorted(dict.values(), key=lambda x: x['title_similarity'], reverse=True)
        text_dict = sorted(dict.values(), key=lambda x: x['text_similarity'], reverse=True)
        title_plus_text_dict = sorted(dict.values(), key=lambda x: x['title_plus_text_similarity'], reverse=True)
        main_list = [title_dict, text_dict, title_plus_text_dict]
        if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{type_name}') == False:
            os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{type_name}')
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{type_name}/similarities_{model_name}.json', "w") as writefile:
            json.dump(main_list, writefile, indent=4, ensure_ascii=False)
            
    elif model_name == 'albertina':
        title_ref_embedding = getTextEmbeddings(title_ref, model_name="PORTULAN/albertina-ptpt")
        text_ref_embedding = getTextEmbeddings(text_ref, model_name="PORTULAN/albertina-ptpt")
        title_plus_text_ref_embedding = getTextEmbeddings(title_plus_text_ref, model_name="PORTULAN/albertina-ptpt")

        dict = {}

        for i in range(10):
            title_embedding = getTextEmbeddings(titles[i], model_name="PORTULAN/albertina-ptpt")
            text_embedding = getTextEmbeddings(texts[i], model_name="PORTULAN/albertina-ptpt")
            title_plus_text_embedding = getTextEmbeddings(titles_plus_texts[i], model_name="PORTULAN/albertina-ptpt")
            
            title_similarity = Cosine(title_ref_embedding, title_embedding)
            text_similarity = Cosine(text_ref_embedding, text_embedding)
            title_plus_text_similarity = Cosine(title_plus_text_ref_embedding, title_plus_text_embedding)
            
            dict[i] = {
                'id': i,
                'title_similarity': title_similarity,
                'text_similarity': text_similarity,
                'title_plus_text_similarity': title_plus_text_similarity
            }
            print(f'{i}')
            
        title_dict = sorted(dict.values(), key=lambda x: x['title_similarity'], reverse=True)
        text_dict = sorted(dict.values(), key=lambda x: x['text_similarity'], reverse=True)
        title_plus_text_dict = sorted(dict.values(), key=lambda x: x['title_plus_text_similarity'], reverse=True)
        main_list = [title_dict, text_dict, title_plus_text_dict]
        if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{type_name}') == False:
            os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{type_name}')
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{type_name}/similarities_{model_name}.json', "w") as writefile:
            json.dump(main_list, writefile, indent=4, ensure_ascii=False)

def getThreeModelsSimilarities(title_ref, text_ref, title_plus_text_ref, titles, texts, titles_plus_texts, type_name):
    getModelSimilarities(title_ref=title_ref, text_ref=text_ref, title_plus_text_ref=title_plus_text_ref, titles=titles, texts=texts, titles_plus_texts=titles_plus_texts, model_name='bert', type_name=type_name) 
    getModelSimilarities(title_ref=title_ref, text_ref=text_ref, title_plus_text_ref=title_plus_text_ref, titles=titles, texts=texts, titles_plus_texts=titles_plus_texts, model_name='gloria', type_name=type_name) 
    getModelSimilarities(title_ref=title_ref, text_ref=text_ref, title_plus_text_ref=title_plus_text_ref, titles=titles, texts=texts, titles_plus_texts=titles_plus_texts, model_name='albertina', type_name=type_name) 


def main():
    model = AutoModelForCausalLM.from_pretrained('neuralmind/bert-base-portuguese-cased')
    tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=True)
    
    save_embeddings(year="2009", model=model, tokenizer=tokenizer, f_path='bert')
    
    # open the articles 
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/embeddings_data_bert/embeddings_2009.json', "r") as readfile:
        articles = json.load(readfile)
    get_similarity(year="2009", articles=articles, f_path='bert')
    
    
    tokenizer = AutoTokenizer.from_pretrained("NOVA-vision-language/GlorIA-1.3B")
    model = AutoModelForCausalLM.from_pretrained("NOVA-vision-language/GlorIA-1.3B")
    
    save_embeddings(year="2009", model=model, tokenizer=tokenizer, f_path='gloria')
    
    # open the articles 
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/embeddings_data_gloria/embeddings_2009.json', "r") as readfile:
        articles = json.load(readfile)
    get_similarity(year="2009", articles=articles, f_path='gloria')
    
    
    tokenizer = AutoTokenizer.from_pretrained("PORTULAN/albertina-ptpt")
    model = AutoModelForSequenceClassification.from_pretrained("PORTULAN/albertina-ptpt", num_labels=2)

    save_embeddings(year="2009", model=model, tokenizer=tokenizer, f_path='albertina')
    
    # open the articles 
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/embeddings_data_albertina/embeddings_2009.json', "r") as readfile:
        articles = json.load(readfile)
    get_similarity(year="2009", articles=articles, f_path='albertina')
    
    # select top 10 similarities from each model
    # each one is saved here (given its model) /Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/similarities_{f_path}/similarities_{year}_{article["nid"]}/similarities_{year}_{article["nid"]}_{article2["nid"]}.json'
    
# main()

#model = AutoModelForCausalLM.from_pretrained('neuralmind/bert-base-portuguese-cased')
#tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=True)
#getTextGloriaEmbeddings("O que é a GlorIA?", model, tokenizer)