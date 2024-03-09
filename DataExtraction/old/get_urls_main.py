import time
from publicnewsarchive import dataExtraction
import json
import os

def get_urls_main(s_year, e_year, url):
    list_of_d = []
    
    for i in range(s_year, e_year+1, 1):
        start_time_past_urls = time.time()
        print("\nYEAR {}".format(i))
        
        pastURLs = dataExtraction.getPastURLs(year=i, newspaper_url=url, startMonth="01", endMonth="12" )
        
        folder_name = "data_{}".format(i)
        folder_path = "./data/{}".format(folder_name) 

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        file_path = os.path.join(folder_path, "main_urls_{}.json".format(i))
        with open(file_path, "w") as file:
            json.dump(pastURLs, file, indent=4, ensure_ascii=False)
        
        end_time_past_urls = time.time()
        execution_time_past_urls = end_time_past_urls - start_time_past_urls
        execution_time_past_urls = round(execution_time_past_urls, 2)
        
        d = {
            "year": i,
            "main_url_len": len(pastURLs),
            "main_url_time": execution_time_past_urls,
        }
        
        list_of_d.append(d)
        
    folder_name = "stats_{}".format(i)
    folder_path = "./stats/{}".format(folder_name) 

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    file_path = os.path.join(folder_path, "stats_main_urls_{}.json".format(i))
    with open(file_path, "w") as file:
        json.dump(list_of_d, file, indent=4, ensure_ascii=False)    
        
    list_of_d.append(d)
    return list_of_d