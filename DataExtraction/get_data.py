import requests
from bs4 import BeautifulSoup
from publicnewsarchive import dataExtraction
import json
import re

def clean_string(input_string):
    cleaned_string = input_string.replace('\n', ' ')
    cleaned_string = cleaned_string.strip()

    return cleaned_string


def get_news_data(url, headers):
  # debug
  # print("url in use: ", url + "\n" + "*------------------"* 10 + "*")
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
            paragraphs = span_regions[1] # paragraphs
            full_paragraphs.append(paragraphs.text)
            if(len(span_regions) > 2):
              author = span_regions[2].text # author
              if(len(span_regions) > 3):
                tags = span_regions[3] # tags
                full_tags.append(tags.text)



          # print("paragraph: ", full_paragraphs) # the full paragraph text
          # print("author: ", author) # the author
          # print("tags: ", full_tags) # the full tags array

          return([full_paragraphs, author, full_tags])

          # unique_news_div.find_all('span').find(class_='georgia')

    else:
      print("nested_div not found.")
      return([])

  else:
      print("news content not found.")
      return([])

def get_news_page(url, headers):
  full_news_dict = []

  page = requests.get(pastURLs[12], headers=headers)
  soup = BeautifulSoup(page.text, 'html.parser')

  main_div = soup.find(id='div_conteudo_left')  # div that contains the news

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
                # region = clean_string(region_tmp)
                # print("region: ", region)
                date = text_date.text
                # date = clean_string(date_tmp)
                # print("date: ", date)

              text_title = text_element.find('h2') # 1 h2
              if text_title:
                text_title_text = text_title.text # the title text
                title = text_title_text
                # title = clean_string(title_tmp)

                # print("title: ", title)

              text_t_snippet = text_element.find('p') # 1 p
              if text_t_snippet:
                text_t_snippet_text = text_t_snippet.text # t_snippet text
                text_snippet = text_t_snippet_text
                # text_snippet = clean_string(text_snippet_tmp)
                # print("text snippet: ", text_snippet)


              image_link = image_element.find('a') # all the images are inside a link, that redirects to the news page
              if image_link:
                  image_src = image_link.find('img')
                  img_src = image_src.get('src')
                  # print("img src: ", img_src) # image src

                  image_link_href =  image_link.get('href')
                  href = image_link_href
                  # print("href: ", href ) # link to the news page

                  news_list = get_news_data(image_link_href, headers) # in here will try to scrap the "same way" as we do to get the news pages
                  paragraph = news_list[0]
                  author_tmp = news_list[1]
                  author = clean_string(author_tmp)
                  tags_tmp = news_list[2]

                  # cleaning
                  # for paragraph_s in paragraph_tmp:
                  #   clean_paragraph = clean_string(paragraph_s)
                  #   paragraph.append(clean_paragraph)

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
                  # print(news_dict)

                  # print("*------------------"* 10 + "*")


      # print(full_news_dict)
      # full_news_dict_json_string = json.dumps(full_news_dict, indent=4, ensure_ascii=False)
      # print(full_news_dict_json_string)

      # print("amount of news", total_news)

      return [full_news_dict, total_news]

      # with open("demo_data.json", "w") as file:
      #  json.dump(full_news_dict, file, indent=4, ensure_ascii=False)

      # print("data stored successfully!")

  else:
      print("div_conteudo_left not found.")



# debugging
pastURLs = dataExtraction.getPastURLs(year='2012', newspaper_url='https://noticiasdacovilha.pt/', startMonth='01', endMonth='01')
# print(len(pastURLs))

# user agent string
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


monthly_news = 0
for i, pastURL in enumerate(pastURLs):
  tmp_page = get_news_page(pastURL, headers)
  monthly_news += tmp_page[1]
  with open("{}.json".format(i), "w") as file:
        json.dump(tmp_page[0], file, indent=4, ensure_ascii=False)

  print("data stored successfully!")
  print('amount of news at the moment: ', monthly_news)

print("amount of news from month X: ", monthly_news)
