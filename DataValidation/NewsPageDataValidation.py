import os
import json
import time

def sort_data(input_file, output_file, year):
    with open(input_file, 'r') as f:
        data = json.load(f)

    sorted_articles = []

    for i, article in enumerate(data):
        if "date" in article:
            # adding 'id' as an attribute to the article dictionary
            article_id = f"{year}-{i}"
            article["id"] = article_id
            sorted_articles.append(article)

    sorted_articles.sort(key=lambda x: x.get("date"))  # Sort by date

    with open(output_file, "w") as outfile:
        json.dump(sorted_articles, outfile, indent=4, ensure_ascii=False)
    
    return len(sorted_articles)
   
def data_validation(s_year, e_year, debug):
    execution_time_dict = {}
    
    for year in range(s_year, e_year + 1):
        start_time = time.time()
        input_file = f'./data/data_{year}/{year}.json'
        output_file = f'./data/data_{year}/validated_{year}.json'
        if os.path.exists(input_file):
            len_of_news = sort_data(input_file, output_file, year)
        else:
            print(f"Input file not found for year {year}")
        if debug:
            end_time = time.time()
            execution_time = end_time - start_time 
            execution_time_dict_tmp ={
                                    year: {
                                        "news_page_data_validation_time": round(execution_time,2),
                                        "news_page_data_validation_len": len_of_news
                                        }
                                    }
            execution_time_dict.update(execution_time_dict_tmp)
            
    return execution_time_dict
