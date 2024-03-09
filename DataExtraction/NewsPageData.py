import datetime
import locale
import time
import requests
from bs4 import BeautifulSoup
import json
import os
import yake
from cleantext import clean
import spacy
import urllib.parse

locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8')

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

def get_news_data_func(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        title = ""
        subtitle = ""
        date = ""
        image_url = ""
        image_desc = ""
        author = ""
        content = ""
        text_snippet = ""
        category = ""
        sub_category = ""
        
        # spaCy entities
        data_PER = []
        data_ORG = []
        data_LOC = []
                        
        # YAKE args
        language = "pt"
        windowSize = 1
        numOfKeywords = 10
        keywords = []
        
        custom_kw_extractor = yake.KeywordExtractor(lan=language, windowsSize=windowSize, top=numOfKeywords, features=None)
        
        # entities scrapping using spaCy
        model = 'pt_core_news_lg' # lg over sm, to get accuracy over efficieny
        nlp = spacy.load(model, disable=['tagger', 'parser'])
            
        path_div = soup.find(id='div_caminho') # div that contains the path info

        if path_div:
            
            nested_path_div = path_div.find('div')
            path_span = nested_path_div.find('span')
            path_category = path_span.find('b').text
            category = path_category
            path_a = nested_path_div.find('a')
            path_sub_category = path_a.find('b').text
            sub_category = path_sub_category

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

                        contents = span_text_list
                        content = clean_span_mtexto
                        
                        author_tmp = span_regions[2].text # author
                        author = clean(author_tmp, to_ascii=False ,fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)
                        
                        for i in range(0,3):
                            if i == 0:
                                doc = nlp(content)
                            elif i == 1:
                                doc = nlp(author)
                            elif i == 2:
                                doc = nlp(title)
                            
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
                        
                        # KEYWORDS
                        content_plus_title = title
                        content_plus_title += " {}".format(span_mtexto.text)
                        keywords_tmp = custom_kw_extractor.extract_keywords(content_plus_title)
                        
                        for kw in keywords_tmp:
                            keywords.append(kw[0])
                        
                        for i, content_tmp in enumerate(contents):
                            if i == 0:
                                text_snippet_tmp = content_tmp
                                text_snippet = clean(text_snippet_tmp, to_ascii=False, fix_unicode=True, no_line_breaks=True, lang="pt", lower=False) # text_snippet cleaned!                      

                    else:
                        print("news content not found.")
                        return []
        else:
            path_div = soup.find('div', class_="main col-md-8") # div that contains the path info
            # from APRIL 2019 until the rest        
            if path_div:
                header = path_div.find("div", class_="s-post-header")
                if header:
                    categories_div = header.find("div", class_="post-category")
                    if categories_div:
                        categories = categories_div.find_all("a")
                        for category_s in categories:
                            category += f'{category_s.text} '
                    
                    sub_category = category

                    title = header.find("h1")  # title
                    if title:
                        title = title.text
                        title = clean(title, to_ascii=False ,fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)
                    
                    subtitle = header.find("div", class_="bk-post-subtitle")
                    if subtitle:
                        subtitle = subtitle.text # subtitle
                        subtitle = clean(subtitle, to_ascii=False ,fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)

                    meta = header.find("div", class_="meta")
                    
                    author = meta.find("div", class_="post-author").text # author
                    author = clean(author, to_ascii=False ,fix_unicode=True, no_line_breaks=True, lang="pt", lower=False)
                    
                    date = meta.find("div", class_="post-date").text # date, need formatting
                    date = datetime.datetime.strptime(date, "%d de %B, %Y")
                    formated_date = date.strftime("%Y-%m-%d")
                    date = formated_date

                    image_div = path_div.find("div", id="bk-normal-feat")
                    if image_div:
                        image = image_div.find("img")
                        if image:
                            image_url = image['data-src'] # image_url
                            image_desc_tmp = image_url[::-1] # to get the file name, so we can link the image to some entity/person
                            for image_desc_c in image_desc_tmp:
                                if image_desc_c == "/":
                                    image_desc = image_desc[::-1]
                                    image_desc = urllib.parse.unquote(image_desc)
                                    image_desc = os.path.splitext(image_desc)[0]
                                    break
                                else:
                                    image_desc += image_desc_c
                        
                    content = path_div.find("div", class_="article-content clearfix").text
                    first_sentence = content.split('.')[0]
                    text_snippet = first_sentence.strip() 

                    content_plus_title = title
                    content_plus_title += " {}".format(content)
                    keywords_tmp = custom_kw_extractor.extract_keywords(content_plus_title)
                    for kw in keywords_tmp:
                        keywords.append(kw[0])
                        
                    for i in range(0,3):
                        if i == 0:
                            doc = nlp(content)
                        elif i == 1:
                            doc = nlp(author)
                        elif i == 2:
                            doc = nlp(title)
                                
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
                        
                
            else:
                print(" news content not found.")
                return []
        
        news_dict = {
                    "url": url,
                    "title": title,
                    "subtitle": subtitle,
                    "date": date,
                    "image_url": image_url,
                    "image_desc": image_desc,
                    "content": content,
                    "author": author,
                    "text_snippet": text_snippet,
                    "category": category,
                    "sub_category": sub_category,
                    "keywords": keywords,
                    "spacy_entities_per": data_PER,
                    "spacy_entites_org": data_ORG,
                    "spacy_entities_loc": data_LOC,
                }
        
        return news_dict
        
def save_to_file(folder_path_arg, file_name_arg, json_file_path, debug=False, demo=False):
    json_file = json_file_path
    urls = read_urls_from_json(json_file)
    
    full_news_list = []
    urls_list = []
    
    for i, url in enumerate(urls):
            urls_list.append(url)
            news_demo = get_news_data_func(url)
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
        

    file_path = os.path.join(folder_path, file_name_arg)
    with open(file_path, "w") as file:
        json.dump(full_news_list, file, indent=4, ensure_ascii=False)
        
        
def get_news_data(s_year, e_year, debug=True, demo=False):
    execution_time_dict = {}
    
    print("NEWS PAGE DATA")
    for i in range(s_year, e_year+1, 1):
        print(f'\n{i}')
        start_time = time.time()
        folder_path = "./data/data_{}".format(i)
        json_file =  './data/data_{}/validated_urls_{}.json'.format(i,i)
        file_name = "{}.json".format(i)
        save_to_file(folder_path_arg=folder_path, file_name_arg=file_name, json_file_path=json_file, debug=debug)
        if debug:
            end_time = time.time()
            execution_time = end_time - start_time 
            execution_time_dict_tmp ={
                                    i: {
                                        "news_page_data_extraction_time": round(execution_time,2)
                                        }
                                    }
            execution_time_dict.update(execution_time_dict_tmp)
    
    return execution_time_dict