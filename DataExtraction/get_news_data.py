import requests
from bs4 import BeautifulSoup
from publicnewsarchive import dataExtraction
import json
import os

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
        author = ""
        full_paragraphs = [] # storing in a array of strings for better storage in json (and later use)
        full_tags = [] # same thing as the paragraphs
        text_snippet = ""
        cathegory = ""
        sub_cathegory = ""

        path_div = soup.find(id='div_caminho') # div that contains the path info

        if path_div:
            nested_path_div = path_div.find('div')
            path_span = nested_path_div.find('span')
            path_cathegory = path_span.find('b').text
            cathegory = path_cathegory
            # print(path_cathegory)
            path_a = nested_path_div.find('a')
            path_sub_cathegory = path_a.find('b').text
            sub_cathegory = path_sub_cathegory
            # print(path_sub_cathegory)

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

                    date = span_regions[0].text # date

                    span_mtexto = unique_news_div.find('span', id='mtexto')
                    span_text_list = span_mtexto.get_text(separator='\n').splitlines()
                    span_text_list = [text for text in span_text_list if text.strip()]

                    paragraphs = span_text_list
                    for i, paragraph in enumerate(paragraphs):
                        if i != 0:
                            full_paragraphs.append(paragraph)
                        else:
                            text_snippet = paragraph


                    author = span_regions[2].text # author

                    tags = span_regions[3] # tags
                    full_tags.append(tags.text)

                    news_dict = {
                            "url": url,
                            "title": title,
                            "date": date,
                            "image": image,
                            "full_paragraphs": full_paragraphs,
                            "author": author,
                            "full_tags": full_tags,
                            "text_snippet": text_snippet,
                            "cathegory": cathegory,
                            "sub_cathegory": sub_cathegory
                    }
                    return news_dict

                else:
                    print("nested_div not found.")
                    return []

        else:
            print("news content not found.")
            return []

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    json_file = './data/data_2012/validated_urls_2012.json'
    urls = read_urls_from_json(json_file)
    
    full_news_list = []
    urls_list = []
    
    debug = True
    
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
    
    
    folder_name = "data_{}".format("2012")
    folder_path = "./data/{}".format(folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, "raw_{}.json".format("2012"))
    with open(file_path, "w") as file:
        json.dump(full_news_list, file, indent=4, ensure_ascii=False)
    # print(news_demo)
