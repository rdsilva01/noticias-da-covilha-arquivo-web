import requests
from bs4 import BeautifulSoup
from publicnewsarchive import dataExtraction
import json
import os

def clean_string(input_string):
    cleaned_string = input_string.replace('\n', ' ')
    cleaned_string = ' '.join(cleaned_string.split()) 
    cleaned_string = cleaned_string.strip()

    return cleaned_string



def get_news_data(url, headers):
  page = requests.get(url, headers=headers)
  soup = BeautifulSoup(page.text, 'html.parser')

  news_div = soup.find(id='div_conteudo') # div that contains the (1) news info

  if news_div:
    content_div = news_div.find(id='div_conteudo_left')
    nested_div = content_div.find('div')

    if nested_div:
          unique_news_div = nested_div.find('div')
          # already have the title (h1)
          # already have the date (span)
          # already have the image (img)

          full_paragraphs = [] # storing in a array of strings for better storage in json (and later use)
          full_tags = [] # same thing as the paragraphs
          # span_regions = unique_news_div.find(id="mtexto")
          span_regions = unique_news_div.find_all('span')

          if(len(span_regions) > 1):
            paragraphs = span_regions[1].find_all('p') # paragraphs
            for paragraph in paragraphs:
              # print(paragraph.text)
              full_paragraphs.append(paragraph.text)
            if(len(span_regions) > 2):
              author = span_regions[2].text # author
              if(len(span_regions) > 3):
                tags = span_regions[3] # tags
                full_tags.append(tags.text)



          # print("paragraph: ", full_paragraphs) # the full paragraph text
          # print("author: ", author) # the author
          # print("tags: ", full_tags) # the full tags array

          return [full_paragraphs, author, full_tags]

          # unique_news_div.find_all('span').find(class_='georgia')

    else:
      print("nested_div not found.")
      return []

  else:
      print("news content not found.")
      return []

def get_news_page(url, headers, news_div_id):
  full_news_dict = []

  page = requests.get(url, headers=headers)
  soup = BeautifulSoup(page.text, 'html.parser')

  main_div = soup.find(id=news_div_id)  # ARG 1

  total_news = 0

  if main_div:
      nested_divs = main_div.find_all('div')

      for nested_div in nested_divs:
          region = ""
          date = ""
          title = ""
          author = ""
          paragraph = []
          text_snippet = ""
          img_src = ""
          href = ""
          tags = []

          div_elements = nested_div.find_all('div')

          if(len(div_elements) > 0):
            image_element = div_elements[0]
            if(len(div_elements) > 1):
              text_element = div_elements[1]

            text_region = text_element.findAll('span') # 2 span
            if(len(text_region) > 0):
              text_region_text = text_region[0] # span
              text_date = text_region[1] # span

              if text_region_text:
                region = text_region_text.text
                date = text_date.text

              text_title = text_element.find('h2') # 1 h2
              if text_title:
                text_title_text = text_title.text # the title text
                title = text_title_text

              text_t_snippet = text_element.find('p') # 1 p
              if text_t_snippet:
                text_t_snippet_text = text_t_snippet.text # t_snippet text
                text_snippet = text_t_snippet_text

              image_link = image_element.find('a') # all the images are inside a link, that redirects to the news page
              if image_link:
                  image_src = image_link.find('img')
                  img_src = image_src.get('src')

                  image_link_href =  image_link.get('href')
                  href = image_link_href
                  # print("href: ", href ) # link to the news page

                  news_list = get_news_data(image_link_href, headers) # in here will try to scrap the "same way" as we do to get the news pages
                  paragraph_tmp = news_list[0]
                  author_tmp = news_list[1]
                  tags_tmp = news_list[2]

                  author = clean_string(author_tmp)

                  # cleaning
                  for paragraph_s in paragraph_tmp:
                    clean_paragraph = clean_string(paragraph_s)
                    paragraph.append(clean_paragraph)

                  for tag in tags_tmp:
                    clean_tag = clean_string(tag)
                    if clean_tag != 'Tags:':
                      tags.append(clean_tag)


                  news_dict = {
                    "region": region,
                    "date": date,
                    "title": title,
                    "author": author,
                    "paragraph": paragraph,
                    "text_snippet": text_snippet,
                    "img_src": img_src,
                    "href": href,
                    "tags": tags
                  }

                  total_news += 1

                  full_news_dict.append(news_dict)

      return full_news_dict
      
  else:
      print("news not found at url: {}".format(url))
      return []


def get_x_month_news_data(pastURLs, year, headers, debug):

  folder_name = "data_{}".format(year)
  folder_path = "./data/{}".format(folder_name)

  if not os.path.exists(folder_path):
    os.makedirs(folder_path)

  full_news_page = []

  for i, pastURL in enumerate(pastURLs):
        page = get_news_page(pastURL, headers, "div_conteudo_left")
        if page != []:
          full_news_page.append(page)
          if debug:
              if i != 0 and i % 1 == 0:
                  print(f"\r{100 * i / len(pastURLs):.2f}%", end='')       
                  if i == len(pastURLs) - 1:
                      print(f"\r100.00%", end='')
    
  file_path = os.path.join(folder_path, "{}.json".format(year))
  with open(file_path, "w") as file:
    json.dump(full_news_page, file, indent=4, ensure_ascii=False)

    



# debugging
# pastURLs = dataExtraction.getPastURLs(year='2012', newspaper_url='https://noticiasdacovilha.pt/', startMonth='01', endMonth='01')
# print(len(pastURLs))

# user agent string
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

url = "https://noticiasdacovilha.pt/"

# 2009
# pastURLs = dataExtraction.getPastURLs(year=2009, newspaper_url=url, startMonth="01", endMonth="12" )
# get_x_month_news_data(pastURLs, "2009", headers, True)


# 2010
# pastURLs = dataExtraction.getPastURLs(year=2010, newspaper_url=url, startMonth="01", endMonth="12")
# get_x_month_news_data(pastURLs, "2010", headers, True)


# 2011
pastURLs = dataExtraction.getPastURLs(year=2011, newspaper_url=url, startMonth="01", endMonth="01")
get_x_month_news_data(pastURLs, "2011", headers, True)
