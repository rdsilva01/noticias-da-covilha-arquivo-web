from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
from publicnewsarchive import dataExtraction
import json
import os
import yake
from cleantext import clean
import spacy
import urllib.parse

def read_urls_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    urls_list = data['urls']
    return urls_list


def clean_string(input_string):
    cleaned_string = input_string.replace('\n', ' ')
    cleaned_string = ' '.join(cleaned_string.split())
    cleaned_string = cleaned_string.strip()

    return cleaned_string

def get_news_data_func(url, headers):
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        title = ""
        date = ""
        image_url = ""
        image_desc = ""
        author = ""
        paragraph = ""
        # full_paragraphs = [] # storing in a array of strings for better storage in json (and later use)
        text_snippet = ""
        category = ""
        sub_category = ""
        news_front_page_image_url = ""
        
        path_div = soup.find(id='div_caminho') # div that contains the path info

        if path_div:
            nested_path_div = path_div.find('div')
            path_span = nested_path_div.find('span')
            path_category = path_span.find('b').text
            category = path_category
            # print(path_category)
            path_a = nested_path_div.find('a')
            path_sub_category = path_a.find('b').text
            sub_category = path_sub_category
            # print(path_sub_category)   

        news_div = soup.find(id='div_conteudo') # div that contains the (1) news info

        if news_div:
                news_front_page_div = news_div.find(id='div_conteudo_140px')
                if news_front_page_div:
                    news_front_page_capaedicao = news_front_page_div.find(id='bloco_capaedicao')
                    news_front_page_image = news_front_page_capaedicao.find('img')
                    news_front_page_image_url = news_front_page_image.get('src') # front page image url
                
                content_div = news_div.find(id='div_conteudo_left')
                nested_div = content_div.find(id="tbl_print")

                if nested_div:
                    unique_news_div = nested_div.find('div')

                    title = unique_news_div.find('h1').text # title

                    span_regions = unique_news_div.find_all('span')
                    div_regions = unique_news_div.find_all('div')

                    image_tmp = div_regions[1].find('img') # image
                    if image_tmp:
                        image_url = image_tmp.get('src')
                        image_desc_tmp = image_url[::-1] # to get the file name, so we can link the image to some entity/person
                        for image_desc_c in image_desc_tmp:
                            if image_desc_c == "/":
                                image_desc = image_desc[::-1]
                                image_desc = urllib.parse.unquote(image_desc)
                                image_desc = os.path.splitext(image_desc)[0]
                                break
                            else:
                                image_desc += image_desc_c
                            
                    date = span_regions[0].text # date

                    span_mtexto = unique_news_div.find('span', id='mtexto')
                    clean_span_mtexto = clean(span_mtexto.text, to_ascii=False ,fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)
                    span_text_list = span_mtexto.get_text(separator='\n').splitlines()
                    span_text_list = [text for text in span_text_list if text.strip()]

                    paragraphs = span_text_list
                    paragraph = clean_span_mtexto
                    
                    author_tmp = span_regions[2].text # author
                    author = clean(author_tmp, to_ascii=False ,fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)
                    
                    # entities scrapping using spaCy
                    model = 'pt_core_news_lg' # lg over sm, to get accuracy over efficieny

                    nlp = spacy.load(model, disable=['tagger', 'parser'])
                    
                    # spaCy entities
                    data_PER = []
                    data_ORG = []
                    data_LOC = []
                    data_MISC = []
                    
                    for i in range(0,2):
                        if i == 0:
                            doc = nlp(paragraph)
                        elif i == 1:
                            doc = nlp(author)
                        
                        for ent in doc.ents:
                            if ent.label_ == "PER":
                                if ent.text not in [item['token'] for item in data_PER]:
                                    data_PER.append({'token': ent.text})
                            elif ent.label_ == "ORG":
                                if ent.text not in [item['token'] for item in data_ORG]:
                                    data_ORG.append({'token': ent.text})
                            elif ent.label_ == "LOC":
                                if ent.text not in [item['token'] for item in data_LOC]:
                                    data_LOC.append({'token': ent.text})
                            elif ent.label_ == "MISC":
                                if ent.text not in [item['token'] for item in data_MISC]:
                                    data_MISC.append({'token': ent.text})
                    
                    # keywords extracting using YAKE
                    language = "pt"
                    # max_ngram_size = 3, when in use add this as argument -> n=max_ngram_size
                    # deduplication_thresold = 0.9, arg: dedupLim=deduplication_thresold
                    # deduplication_algo = 'seqm', arg: dedupFunc=deduplication_algo
                    windowSize = 1
                    numOfKeywords = 10
                    keywords = []
                                        
                    custom_kw_extractor = yake.KeywordExtractor(lan=language, windowsSize=windowSize, top=numOfKeywords, features=None)  
                    keywords_tmp = custom_kw_extractor.extract_keywords(span_mtexto.text)
                    
                    for kw in keywords_tmp:
                        # print(kw[0])
                        keywords.append(kw[0])
                    
                    for i, paragraph_tmp in enumerate(paragraphs):
                        if i == 0:
                            text_snippet_tmp = paragraph_tmp
                            text_snippet = clean(text_snippet_tmp, to_ascii=False,fix_unicode=True, no_line_breaks=True, lang="pt", lower=False) # text_snippet cleaned!
                            # clean_paragraph = clean(paragraph, fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)
                            # full_paragraphs.append(clean_paragraph)                           

                    news_dict = {
                            "url": url,
                            "news_front_page_image_url": news_front_page_image_url,
                            "title": title,
                            "date": date,
                            "image_url": image_url,
                            "image_desc": image_desc,
                            "paragraph": paragraph,
                            "author": author,
                            "text_snippet": text_snippet,
                            "category": category,
                            "sub_category": sub_category,
                            "keywords": keywords,
                            "spacy_entities_per": data_PER,
                            "spacy_entites_org": data_ORG,
                            "spacy_entities_loc": data_LOC,
                            "spacy_entities_misc": data_MISC
                    }
                    return news_dict

                else:
                    print("nested_div not found.")
                    return []

        else:
            print("news content not found.")
            return []
        
def save_to_file(folder_path_arg, file_name_arg, headers, json_file_path, debug=False, demo=False):
    json_file = json_file_path
    urls = read_urls_from_json(json_file)
    
    full_news_list = []
    urls_list = []
    
    if demo:
        N = 3
        for i, url in enumerate(urls):
            if i < N+1:
                urls_list.append(url)
                news_demo = get_news_data_func(url, headers)
                # print(news_demo)
                full_news_list.append(news_demo)
                if debug:
                    if i != 0 and i % 1 == 0:
                        print(f"\r{100 * i / N:.2f}%", end='')       
                        if i == N:
                            print(f"\r100.00%", end='')
            
        folder_path = folder_path_arg

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # full_news_list = sorted(full_news_list, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        
        file_path = os.path.join(folder_path, "{}".format(file_name_arg))
        with open(file_path, "w") as file:
            json.dump(full_news_list, file, indent=4, ensure_ascii=False)
        
        # print(news_demo)
    else:
        for i, url in enumerate(urls):
            urls_list.append(url)
            news_demo = get_news_data_func(url, headers)
            # print(news_demo)
            full_news_list.append(news_demo)
            if debug:
                if i != 0 and i % 1 == 0:
                    print(f"\r{100 * i / len(urls):.2f}%", end='')       
                    if i == len(urls) - 1:
                        print(f"\r100.00%", end='')
            
        
        folder_path = folder_path_arg

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # full_news_list = sorted(full_news_list, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        
        file_path = os.path.join(folder_path, file_name_arg)
        with open(file_path, "w") as file:
            json.dump(full_news_list, file, indent=4, ensure_ascii=False)
        # print(news_demo)
    
    return("DONE\n")

def get_news_data(s_year, e_year, debug=True, demo=False):
     
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    if demo:
        print("DEMO")
        for i in range(s_year, e_year+1, 1):
            start_time = time.time()
            folder_path = "./data/data_{}".format(i)
            json_file =  './data/data_{}/validated_urls_{}.json'.format(i,i)
            file_name = "demo_{}.json".format(i)
            save_to_file(folder_path_arg=folder_path, file_name_arg=file_name, headers=headers, json_file_path=json_file, debug=debug, demo=True)
            end_time = time.time()
            execution_time = end_time - start_time 
            print(f"Execution time: {execution_time/60:.2f} minutes")
    else:
        for i in range(s_year, e_year+1, 1):
            start_time = time.time()
            folder_path = "./data/data_{}".format(i)
            json_file =  './data/data_{}/validated_urls_{}.json'.format(i,i)
            file_name = "{}.json".format(i)
            save_to_file(folder_path_arg=folder_path, file_name_arg=file_name, headers=headers, json_file_path=json_file, debug=debug)
            end_time = time.time()
            execution_time = end_time - start_time 
            print(f"Execution time: {execution_time/60:.2f} minutes")
      
    
    # 2009
    # folder_path = "./data/data_2009"
    # json_file =  './data/data_2009/validated_urls_2009.json'
    # file_name = "2009.json"
    # save_to_file(folder_path_arg=folder_path, file_name_arg=file_name, json_file_path=json_file, debug=True)
    
    # 2010
    # folder_path = "./data/data_2010"
    # json_file =  './data/data_2010/validated_urls_2010.json'
    # file_name = "2010.json"
    # save_to_file(folder_path_arg=folder_path, file_name_arg=file_name, json_file_path=json_file, debug=True)
    
    # 2011
    # folder_path = "./data/data_2011"
    # json_file =  './data/data_2011/validated_urls_2011.json'
    # file_name = "2011.json"
    # save_to_file(folder_path_arg=folder_path, file_name_arg=file_name, json_file_path=json_file)
    
    # 2012
    
    # 2013
    
    # 2014
