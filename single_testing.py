import os
from bs4 import BeautifulSoup
import requests
import datetime
import locale
import urllib.parse

url="https://arquivo.pt/noFrame/replay/20190705171733/https://www.noticiasdacovilha.pt/amendoal-motiva-investimento-de-50-milhoes-no-fundao-e-idanha/"

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8')

path_div = soup.find('div', class_="main col-md-8")
            
header = path_div.find("div", class_="s-post-header")

title = header.find("h1")  # title
subtitle = header.find("div", class_="bk-post-subtitle") # subtitle

meta = header.find("div", class_="meta")
author = meta.find("div", class_="post-author").text # author
date = meta.find("div", class_="post-date").text # date, need formatting
date = datetime.datetime.strptime(date, "%d de %B, %Y")
formated_date = date.strftime("%Y-%m-%d")

print("Data formatada:", formated_date) 


image_div = path_div.find("div", id="bk-normal-feat")
image_desc = ""
if image_div:
                    image = image_div.find("img")
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
print(image_desc)
    
content = path_div.find("div", class_="article-content clearfix").text
first_sentence = content.split('.')[0]
text_snippet = first_sentence.strip() 
print(text_snippet)
    