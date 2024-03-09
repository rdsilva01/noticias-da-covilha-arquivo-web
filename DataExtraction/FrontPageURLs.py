import time
from publicnewsarchive import dataExtraction
import json
import os

def get_past_urls(url, year=2009):
    pastURLs = dataExtraction.getPastURLs(year=year, newspaper_url=url, startMonth="01", endMonth="12")

    pastURLs_dict = {
        year: pastURLs
    }

    folder_name = "data_{}".format(year)
    folder_path = "./data/{}".format(folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, "past_urls_{}.json".format(year))
    with open(file_path, "w") as file:
        json.dump(pastURLs_dict, file, indent=4, ensure_ascii=False)
    
    return len(pastURLs)

def get_front_page_url_dataset(url, s_year, e_year, debug=True):
    # user agent string
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    # }
    execution_time_dict = {}

    print("FRONT PAGE URLS")
    for i in range(s_year, e_year+1, 1):
        print("\nYEAR {}".format(i))
        start_time = time.time()
        len_of_news = get_past_urls(url=url, year=i)
        if debug:
                end_time = time.time()
                execution_time = end_time - start_time 
                execution_time_dict_tmp ={
                                        i: {
                                            "front_page_urls_extraction_time": round(execution_time,2),
                                            "front_page_urls_extraction_len": len_of_news
                                            }
                                        }
                execution_time_dict.update(execution_time_dict_tmp)
                print(execution_time_dict_tmp)
                    
    return execution_time_dict