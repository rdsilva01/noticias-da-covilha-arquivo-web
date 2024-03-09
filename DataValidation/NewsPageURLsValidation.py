import json
import time

def remove_duplicates(input_file, output_file, debug):
    with open(input_file, 'r') as f:
        data = json.load(f)

    unique_urls = set()
    nid_list = []
    content_list = []

    for i,urls_list in enumerate(data):
        new_link = False
        for url in urls_list:
            nid = ""
            if ("get.adobe.com/flashplayer/" not in url) and ("category" not in url) and ("author" not in url):
                temp_full_url_reversed = url[::-1] 
                bar_count = 0
                content = ""
                for i, temp_full_url_reversed_char in enumerate(temp_full_url_reversed):
                    if i == 0 and temp_full_url_reversed_char != "/":
                        new_link = False
                        break
                    if temp_full_url_reversed_char == "/":
                        if(bar_count == 2):
                            new_link = True
                            break
                        bar_count += 1
                    else:
                        content += temp_full_url_reversed_char
                    if debug:
                        if i != 0 and i % 1 == 0:
                            print(f"\r{100 * i / len(data):.2f}%", end='')
                            if i == len(data) - 1:
                                print(f"\r100.00%", end='')
                content = content[::-1]
                if content not in content_list:
                        content_list.append(content)
                        unique_urls.add(url)
                if new_link == False:
                    for temp_full_url_reversed_char in temp_full_url_reversed:
                        if temp_full_url_reversed_char == "=":
                            break
                        else:
                            nid += temp_full_url_reversed_char
                        if debug:
                            if i != 0 and i % 1 == 0:
                                print(f"\r{100 * i / len(data):.2f}%", end='')
                                if i == len(data) - 1:
                                    print(f"\r100.00%", end='')
                            
                    nid = nid[::-1]
                    if nid not in nid_list:
                        nid_list.append(nid)
                        unique_urls.add(url)

    unique_urls_json = {'urls': list(unique_urls)}

    with open(output_file, 'w') as f:
        json.dump(unique_urls_json, f, indent=4)
        
    return len(unique_urls)
        
def url_validation(s_year, e_year, debug):
    execution_time_dict = {}
    
    for year in range(s_year, e_year + 1):
        start_time = time.time()
        input_file = f'./data/data_{year}/urls_{year}.json'
        output_file = f'./data/data_{year}/validated_urls_{year}.json'
        len_of_news = remove_duplicates(input_file, output_file, debug=debug)
        if debug:
            end_time = time.time()
            execution_time = end_time - start_time 
            execution_time_dict_tmp ={
                                    year: {
                                        "news_page_urls_validation_time": round(execution_time,2),
                                        }
                                    }
            execution_time_dict.update(execution_time_dict_tmp)
    
    return execution_time_dict
