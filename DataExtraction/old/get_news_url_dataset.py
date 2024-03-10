import time
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

def get_news_urls(url, headers, news_div_id):
  page = requests.get(url, headers=headers)
  soup = BeautifulSoup(page.text, 'html.parser')

  full_extras_links = []

  main_div = soup.find(id=news_div_id)  # ARG 1

  if main_div:
      h2_regions = main_div.find_all('h2')
      for extra in h2_regions:
        extra_link = extra.find('a')
        if extra_link:
          extra_link_href = extra_link.get('href')
          full_extras_links.append(extra_link_href)

      nested_divs = main_div.find_all('div')

      for nested_div in nested_divs:
          href = ""

          div_elements = nested_div.find_all('div')

          if(len(div_elements) > 0):
            image_element = div_elements[0]

            image_link = image_element.find('a') # all the images are inside a link, that redirects to the news page
            if image_link:
                  href =  image_link.get('href')
                  full_extras_links.append(href)

      return full_extras_links

  else:
      print("news urls not found at url: {}".format(url))
      return []


def get_news_url_year(pastURLs, year, headers, debug):

  folder_name = "data_{}".format(year)
  folder_path = "./data/{}".format(folder_name)

  if not os.path.exists(folder_path):
    os.makedirs(folder_path)

  full_news_url_year = []

  for i, pastURL in enumerate(pastURLs):
        page = get_news_urls(pastURL, headers, "div_conteudo_left")
        if page != []:
          full_news_url_year.append(page)
          if i != 0 and i % 1 == 0:
            print(f"\r{100 * i / len(pastURLs):.2f}%", end='')
            if i == len(pastURLs) - 1:
              print(f"\r100.00%", end='')

  file_path = os.path.join(folder_path, "urls_{}.json".format(year))
  with open(file_path, "w") as file:
    json.dump(full_news_url_year, file, indent=4, ensure_ascii=False)


def get_news_url_dataset(url, s_year, e_year, debug=False):

  # user agent string
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
  }
  
  list_of_d = []

  for i in range(s_year, e_year+1, 1):
    print("\nYEAR {}".format(i))
    
    pastURLs = dataExtraction.getPastURLs(year=i, newspaper_url=url, startMonth="01", endMonth="12" )
   
    start_time = time.time()
    get_news_url_year(pastURLs, "{}".format(i), headers, debug=debug)
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time = round(execution_time, 2)
    
    d =  {
      "year": i,
      "news_url_time": execution_time
    }
    
    list_of_d.append(d)
    
  folder_name = "stats_{}".format(i)
  folder_path = "./stats/{}".format(folder_name) 

  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
      
  file_path = os.path.join(folder_path, "stats_news_urls_{}.json".format(i))
  with open(file_path, "w") as file:
    json.dump(list_of_d, file, indent=4, ensure_ascii=False)
    
  return list_of_d