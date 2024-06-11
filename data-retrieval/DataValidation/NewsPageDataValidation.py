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
            if str(year) in article["date"]:
                article_id = f"{year}-{i}"
                article["nid"] = article_id
                
                # formatted_content + html
                content_list = article["formatted_content"]
                formatted_html_content = ""
                formatted_html_content_normal = ""
                cleaned_content = []
                
                image = article["image_url"]
                if "/0.jpg" in image:
                    article["image_url"] = "no_image"
                
                    # Generate unique IDs for keywords, but just for the top 10 keywords
                keyword_map = {}
                article["keywords"] = article["keywords"][:10]
                for keyword in article["keywords"]:
                    keyword_id = f"keyword_{hash(keyword)}"
                    keyword_map[keyword] = keyword_id

                for content in content_list:
                    cleaned_content.append(content)
                    formatted_content = content
                    # Replace keywords with spans containing unique IDs, but just for the top 10 keywords
                    for keyword, keyword_id in keyword_map.items():
                        formatted_content = formatted_content.replace(keyword, f'<span id="{keyword_id}" class="keyword" onmouseover="highlightKeywords(\'{keyword_id}\')" onmouseout="resetHighlight(\'{keyword_id}\')">{keyword}</span>')
                    formatted_html_content += formatted_content + "<br>"
                    formatted_html_content_normal += content + "<br>"  
                 
                # make a verification so that the formatted_html_content_normal doesnt start with a <br>
               

                article["formatted_html_content"] = formatted_html_content
                article["normal_formatted_html_content_normal"] = formatted_html_content_normal
                
                if formatted_html_content_normal.startswith("<br>"):
                    formatted_html_content_normal = formatted_html_content_normal[4:]
                    
                # create a formatted_html_content_normal with a max of 400 characters
                if len(formatted_html_content_normal) > 400:
                    formatted_html_content_normal = formatted_html_content_normal[:400] + "..."
                    
                article["formatted_html_content_normal"] = formatted_html_content_normal
                article["formatted_content"] = cleaned_content

                # Generate HTML for keywords
                formatted_html_keywords = ""
                for keyword, keyword_id in keyword_map.items():
                    formatted_html_keywords += f'/ <span id="{keyword_id}" class="keyword" onmouseover="highlightKeywords(\'{keyword_id}\')" onmouseout="resetHighlight(\'{keyword_id}\')">{keyword}</span> '

                article["formatted_html_keywords"] = formatted_html_keywords

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
        # input_file = f'../data/data_{year}/{year}.json'
        # output_file = f'../data/data_{year}/validated_{year}.json'
        input_file = f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/{year}/validated_{year}.json'
        output_file = f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/{year}/3validated_{year}.json'
        
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

# this function will switch the attributes of the json file, like the keywords from a article to another
# def switch_attributes():
#     for year in range(2009, 2020):
#         to_switch_file = f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/{year}/2validated_{year}.json'
#         reference_file = f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/{year}/3validated_{year}.json'
        
#         with open(to_switch_file, 'r') as f:
#             to_switch_data = json.load(f)
            
#         with open(reference_file, 'r') as f:
#             reference_data = json.load(f)
        
#         for i, article in enumerate(reference_data):
#             if "keywords" in article:
#                 to_switch_data[i]["keywords"] = article["keywords"]
#                 to_switch_data[i]["formatted_html_keywords"] = article["formatted_html_keywords"]
#                 to_switch_data[i]["formatted_html_content"] = article["formatted_html_content"]
#                 to_switch_data[i]["formatted_html_content_normal"] = article["formatted_html_content_normal"]
            
#         with open(to_switch_file, "w") as outfile:
#             json.dump(to_switch_data, outfile, indent=4, ensure_ascii=False)

# switch_attributes()

#switch_attributes()


            
