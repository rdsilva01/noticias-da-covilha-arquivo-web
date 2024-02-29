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

def get_news_data(url, headers):
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        title = ""
        date = ""
        image = ""
        image_desc = ""
        author = ""
        full_paragraphs = [] # storing in a array of strings for better storage in json (and later use)
        full_tags = [] # same thing as the paragraphs
        text_snippet = ""
        category = ""
        sub_category = ""
        

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
                content_div = news_div.find(id='div_conteudo_left')
                nested_div = content_div.find(id="tbl_print")

                if nested_div:
                    unique_news_div = nested_div.find('div')

                    title = unique_news_div.find('h1').text # title

                    span_regions = unique_news_div.find_all('span')
                    div_regions = unique_news_div.find_all('div')

                    image_tmp = div_regions[1].find('img') # image
                    if image_tmp:
                        image = image_tmp.get('src')
                        image_desc_tmp = image[::-1] # to get the file name, so we can link the image to some entity/person
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
                    clean_span_mtexto = clean(span_mtexto.text, fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)
                    span_text_list = span_mtexto.get_text(separator='\n').splitlines()
                    span_text_list = [text for text in span_text_list if text.strip()]

                    paragraphs = span_text_list
                    
                    # entities scrapping using spaCy
                    model = 'pt_core_news_sm'

                    nlp = spacy.load(model, disable=['tagger', 'parser'])
                    doc = nlp(clean_span_mtexto)

                    data = []

                    for ent in doc.ents:
                        # data.append({'token': ent.text, 'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_})
                        data.append({'token': ent.text, 'label': ent.label_})
                    
                    #df = pd.DataFrame(data)
                    # print(df)
                    
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
                    
                    for i, paragraph in enumerate(paragraphs):
                        if i != 0:
                            clean_paragraph = clean(paragraph, fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)
                            full_paragraphs.append(clean_paragraph)
                        else:
                            text_snippet = paragraph


                    author_tmp = span_regions[2].text # author
                    author = clean(author_tmp, fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)

                    tags = span_regions[3] # tags
                    full_tags.append(tags.text)

                    news_dict = {
                            "url": url,
                            "title": title,
                            "date": date,
                            "image": image,
                            "image_desc": image_desc,
                            "full_paragraphs": full_paragraphs,
                            "author": author,
                            "full_tags": full_tags,
                            "text_snippet": text_snippet,
                            "category": category,
                            "sub_category": sub_category,
                            "keywords": keywords,
                            "spaCy_entities": data
                    }
                    return news_dict

                else:
                    print("nested_div not found.")
                    return []

        else:
            print("news content not found.")
            return []
        
def save_to_file(folder_path_arg, file_name_arg, json_file_path, debug=False, demo=False):
    start_time = time.time()
    
    json_file = json_file_path
    urls = read_urls_from_json(json_file)
    
    full_news_list = []
    urls_list = []
    
    if demo:
        N = 3
        for i, url in enumerate(urls):
            if i < N+1:
                urls_list.append(url)
                news_demo = get_news_data(url, headers)
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
        
        # sorted_news_list = sorted(full_news_list, key=lambda x: x['date'])
        
        file_path = os.path.join(folder_path, "demo_{}".format(file_name_arg))
        with open(file_path, "w") as file:
            json.dump(full_news_list, file, indent=4, ensure_ascii=False)
        
        # print(news_demo)
    else:
        for i, url in enumerate(urls):
            urls_list.append(url)
            news_demo = get_news_data(url, headers)
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
        
        # sorted_news_list = sorted(full_news_list, key=lambda x: x['date'])
        
        file_path = os.path.join(folder_path, file_name_arg)
        with open(file_path, "w") as file:
            json.dump(full_news_list, file, indent=4, ensure_ascii=False)
        # print(news_demo)
    
    if debug:
        end_time = time.time()
        execution_time = end_time - start_time 
        print(f"Execution time: {execution_time:.2f} seconds")
    
    return("DONE\n")

if __name__ == '__main__':
    start_time = time.time()
     
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # 2009
    # folder_path = "./data/data_2009"
    # json_file =  './data/data_2009/validated_urls_2009.json'
    # file_name = "2009.json"
    # save_to_file(folder_path_arg=folder_path, file_name_arg=file_name, json_file_path=json_file, debug=True)
    
    # 2010
    folder_path = "./data/data_2010"
    json_file =  './data/data_2010/validated_urls_2010.json'
    file_name = "2010.json"
    save_to_file(folder_path_arg=folder_path, file_name_arg=file_name, json_file_path=json_file, debug=True)
    
    # 2011
    # folder_path = "./data/data_2011"
    # json_file =  './data/data_2011/validated_urls_2011.json'
    # file_name = "2011.json"
    # save_to_file(folder_path_arg=folder_path, file_name_arg=file_name, json_file_path=json_file)
    
    # 2012
    
    # 2013
    
    # 2014
