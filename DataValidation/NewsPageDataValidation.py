import os
import json
import time

def sort_data(input_file, output_file, year):
    with open(input_file, 'r') as f:
        data = json.load(f)

    sorted_articles = []
    
    for i, article in enumerate(data):
        if "date" in article:
            # id
            article_id = f"{year}-{i}"
            article["nid"] = article_id
            
            # formatted_content + html
            content_list = article["formatted_content"]
            formatted_html_content = ""
            cleaned_content = []
            last_content_empty = False
            for content in content_list:
                if content == "":
                    if not last_content_empty: 
                        cleaned_content.append(content)
                        formatted_html_content += "<br><br>"
                        last_content_empty = True
                else:
                    formatted_html_content += content
                    cleaned_content.append(content)
                    last_content_empty = False
            
            article["formatted_html_content"] = formatted_html_content
            article["formatted_content"] = cleaned_content
            sorted_articles.append(article)
    
    # Sort articles by date if present
    sorted_articles.sort(key=lambda x: x.get("date", ""))

    with open(output_file, "w") as outfile:
        json.dump(sorted_articles, outfile, indent=4, ensure_ascii=False)
    
    return len(sorted_articles)
   
def data_validation(s_year, e_year, debug):
    execution_time_dict = {}
    len_of_news = None
    
    for year in range(s_year, e_year + 1):
        start_time = time.time()
        input_file = f'../data/data_{year}/{year}.json'
        output_file = f'../data/data_{year}/validated_{year}.json'
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

data_validation(2009, 2019, debug=True)
