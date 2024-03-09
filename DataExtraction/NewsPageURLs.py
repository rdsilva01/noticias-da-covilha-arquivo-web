import time
import requests
from bs4 import BeautifulSoup
from publicnewsarchive import dataExtraction
import json
import os

def get_links(type, class_, soup):
    temporary_links = []
    
    temporary_soup = soup.find_all(type, class_=class_)
    if temporary_soup:
        for temporary_soup_single in temporary_soup:
            temporary_soup_links = temporary_soup_single.find_all("a")
            for temporary_soup_link in temporary_soup_links:
                temporary_soup_link_href = temporary_soup_link.get("href")
                if temporary_soup_link_href not in temporary_links:
                    temporary_links.append(temporary_soup_link_href)
    
    return temporary_links


def get_news_urls(url, headers, news_div_id):
  page = requests.get(url, headers=headers)
  soup = BeautifulSoup(page.text, 'html.parser')

  temporary_links_list = []

  main_div = soup.find(id=news_div_id)  # ARG 1

  if main_div:
      h2_regions = main_div.find_all('h2')
      for extra in h2_regions:
        extra_link = extra.find('a')
        if extra_link:
          extra_link_href = extra_link.get('href')
          temporary_links_list.append(extra_link_href)

      nested_divs = main_div.find_all('div')

      for nested_div in nested_divs:
          href = ""

          div_elements = nested_div.find_all('div')

          if(len(div_elements) > 0):
            image_element = div_elements[0]

            image_link = image_element.find('a') # all the images are inside a link, that redirects to the news page
            if image_link:
                  href =  image_link.get('href')
                  temporary_links_list.append(href)

      return temporary_links_list

  else:
    temporary_links_list = []
    main_div = soup.find("div", class_="rubik-page-content-wrapper clearfix")
    if main_div:
            temporary_links_list = get_links(soup=main_div, type="ul", class_="block5-small-posts")  # cultura/actualidade
      
            temporary_links = get_links(soup=main_div, type="ul", class_="bk-blog-content")  # blog
            for temporary_link in temporary_links:
                if temporary_link not in temporary_links_list:
                    temporary_links_list.append(temporary_link)
                    
            temporary_links = get_links(soup=main_div, type="ul", class_="list post_list bk-widget-content")  # religiao
            for temporary_link in temporary_links:
                if temporary_link not in temporary_links_list:
                    temporary_links_list.append(temporary_link)
                    
            temporary_links = get_links(soup=main_div, type="ul", class_="row list post_list bk-widget-content")  # desporto
            for temporary_link in temporary_links:
                if temporary_link not in temporary_links_list:
                    temporary_links_list.append(temporary_link)
            
            # print(json.dumps(temporary_links_list, indent=4, ensure_ascii=False))
            # print(" news urls found at url {}".format(url))
            return temporary_links_list
    else:
          print(" ALT news urls not found at url: {}".format(url))
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

  return len(full_news_url_year)


def get_news_url_dataset(s_year, e_year, debug=True):

    # user agent string
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
  
    execution_time_dict = {}
    print("NEWS PAGE URLS")
    for i in range(s_year, e_year+1, 1):
        print("\nYEAR {}".format(i))
        
        json_file =  './data/data_{}/past_urls_{}.json'.format(i,i)
        if json_file:
            with open(json_file, 'r') as f:
                data = json.load(f)

            pastURLs = data["{}".format(i)]

            start_time = time.time()
            len_of_news = get_news_url_year(pastURLs, "{}".format(i), headers, debug=debug)
            if debug:
                        end_time = time.time()
                        execution_time = end_time - start_time 
                        execution_time_dict_tmp ={
                                                i: {
                                                    "news_page_urls_extraction_time": round(execution_time,2),
                                                    "news_page_urls_extraction_len": len_of_news
                                                    }
                                                }
                        execution_time_dict.update(execution_time_dict_tmp)
        else:
            print("FILE {} DOESN'T EXIST".format(i))
                    
    return execution_time_dict