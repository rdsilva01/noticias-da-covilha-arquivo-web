# main.py
import json
import os
import time

from DataExtraction import NewsPageData
from DataExtraction import NewsPageURLs
from DataExtraction import FrontPageURLs
from DataExtraction import FrontPageData

from DataStatistics import GetDataStatistics

from DataValidation import NewsPageURLsValidation
from DataValidation import NewsPageDataValidation

# global var
stats_dict = {}

def save_to_file(stats_dict, s_year=2009, e_year=2019):
    for i in range(s_year, e_year+1):
        if i not in stats_dict:
            stats_dict[i] = {}
        stats_dict[i].update(stats_dict[i])

    folder_path = './data/stats'
    file_name = f'{time.time()}.json'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w") as file:
        json.dump(stats_dict, file, indent=4, ensure_ascii=False)
        
def print_pretty_dict(dict):
    print(json.dumps(dict,  sort_keys=True, indent=4))
        
# URL EXTRACTION
def main_url_extraction_fun(url, s_year=2009, e_year=2019):
    front_page_url_dict = FrontPageURLs.get_front_page_url_dataset(url=url, s_year=s_year, e_year=e_year)
    print_pretty_dict(front_page_url_dict)
    save_to_file(front_page_url_dict)
    
def news_url_extraction_fun(s_year=2009, e_year=2019):
    news_url_dict = NewsPageURLs.get_news_url_dataset(s_year=s_year, e_year=e_year)
    print_pretty_dict(news_url_dict)
    save_to_file(news_url_dict)

# URL VALIDATION
def url_validation_fun(s_year=2009, e_year=2012):
    news_url_validation_dict = NewsPageURLsValidation.url_validation(s_year=s_year, e_year=e_year, debug=True)
    save_to_file(news_url_validation_dict)
    print_pretty_dict(news_url_validation_dict) 

# DATA EXTRACTION
def main_data_extraction_fun(header, s_year=2009, e_year=2012): # main data, the front page image
    front_page_data_dict = FrontPageData.get_main_page_dataset(s_year=s_year, e_year=e_year, header=header)
    save_to_file(front_page_data_dict)
    print_pretty_dict(front_page_data_dict)

def data_extraction_fun(s_year=2009, e_year=2019):
    news_data_dict = NewsPageData.get_news_data(s_year=s_year, e_year=e_year, debug=True, demo=False)
    save_to_file(news_data_dict)
    print_pretty_dict(news_data_dict)

# DATA VALIDATION
def data_validation_fun(s_year=2009, e_year=2019):
    news_url_validation_dict = NewsPageDataValidation.data_validation(s_year=s_year, e_year=e_year, debug=True)
    save_to_file(news_url_validation_dict)
    print_pretty_dict(news_url_validation_dict)

# DATA STATISTICS    
def show_statistics_fun(stats_dict):
    print_pretty_dict(stats_dict)

def data_statistics_fun(s_year, e_year):
    full_stats = {}
    for i in range(s_year, e_year+1):
        spacy_stats = GetDataStatistics.get_data_spacy_statistics(year=i)
        content_stats = GetDataStatistics.get_content_statistics(year=i)
        if i not in full_stats:
            full_stats[i] = {}
        full_stats[i].update(spacy_stats[i])
        full_stats[i].update(content_stats[i])
        
    folder_name = "data_all_years"
    folder_path = "./data/{}".format(folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, "statistics.json")
    with open(file_path, "w") as file:
        json.dump(full_stats, file, indent=4, ensure_ascii=False)
        
    return full_stats


def main(url, header):

    #main_url_extraction_fun(url=url, s_year=2009, e_year=2011)
    main_data_extraction_fun(header=header, s_year=2009, e_year=2015)
    #news_url_extraction_fun(s_year=2019, e_year=2019)
    #url_validation_fun(s_year=2009, e_year=2019)
    #data_extraction_fun(s_year=2019, e_year=2019)
    #data_validation_fun()

    statistics = data_statistics_fun(2009, 2019)
    print(json.dumps(statistics, indent=4, ensure_ascii=False))
    
                    
if __name__ == "__main__":
    url = "https://noticiasdacovilha.pt/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    main(url, header=headers)
    
    
