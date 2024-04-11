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
                
                    # Generate unique IDs for keywords
                keyword_map = {}
                for keyword in article["keywords"]:
                    keyword_id = f"keyword_{hash(keyword)}"
                    keyword_map[keyword] = keyword_id

                for content in content_list:
                    cleaned_content.append(content)
                    formatted_content = content
                    # Replace keywords with spans containing unique IDs
                    for keyword, keyword_id in keyword_map.items():
                        formatted_content = formatted_content.replace(keyword, f'<span id="{keyword_id}" class="keyword" onmouseover="highlightKeywords(\'{keyword_id}\')" onmouseout="resetHighlight(\'{keyword_id}\')">{keyword}</span>')
                    formatted_html_content += formatted_content + "<br>"
                    formatted_html_content_normal += content + "<br>"  
                 

                article["formatted_html_content"] = formatted_html_content
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


# def word_embeddings_url(url, file_dir):
#     # DEMO DEMO DEMO
#     from transformers import AutoTokenizer, AutoModelForCausalLM
#     tokenizer = AutoTokenizer.from_pretrained("NOVA-vision-language/GlorIA-1.3B")
#     model = AutoModelForCausalLM.from_pretrained("NOVA-vision-language/GlorIA-1.3B")
#     text = "Olá, tudo bem?"
#     input_ids = tokenizer.encode(text, return_tensors="pt")
#     print(input_ids.shape)  # torch.Size([1, 6])
#     outputs = model(input_ids, output_hidden_states=True)
#     embeddings = outputs.hidden_states[-1]
#     print(embeddings.shape)  # torch.Size([1, 6, 2048])

data_validation(2009, 2019, debug=True)
