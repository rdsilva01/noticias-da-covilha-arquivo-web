import json
import os
import re
import time
from bs4 import BeautifulSoup
import requests


def get_news_front(json_file, headers, year, debug=True):
    print(f'\n{year}')
    with open(json_file, 'r') as f:
        data = json.load(f)

    url_list = data[str(year)]
    main_url_dict = {} 
    
    for i, url in enumerate(url_list):
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')    
        
        bloco_capaedicao = soup.find(id='bloco_capaedicao') 
        
        if bloco_capaedicao:
            image = bloco_capaedicao.find('img')
            if image:
                image_url = image.get('src')
                if image_url not in main_url_dict.values():
                    image_url_reversed = image_url[::-1]
                    content = ""
                    for j, image_url_reversed_tmp in enumerate(image_url_reversed):
                        if image_url_reversed_tmp == "/":
                            break
                        else:
                            content += image_url_reversed_tmp
                    content = content[::-1]
                    match = re.search(r'\d{4}', content)
                    if match:
                        four_digits = match.group()
                        # print(four_digits)
                        main_url_dict[four_digits] = image_url

            else:
                print("not found")
        
        if debug:
            print(f"\rProgress: {100 * (i + 1) / len(url_list):.2f}%", end='')
    
    main_url_dict = dict(sorted(main_url_dict.items()))
    return main_url_dict
    
def get_main_page_dataset(s_year, e_year, header, debug=True):
    execution_time_dict = {}
    main_page_dataset = {}
    
    print("FRONT PAGE DATA")
    for i in range(s_year, e_year+1, 1):
        start_time = time.time()
        json_file =  './data/{}/versions_{}.json'.format(i,i)
        main_page_dict = get_news_front(json_file=json_file, headers=header, year=i, debug=debug)
        main_page_dict_tmp = { 
                i: main_page_dict 
            }
        folder_name = "{}".format(i)
        folder_path = "./data/{}".format(folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, "cover_urls_{}.json".format(i))
        with open(file_path, "w") as file:
            json.dump(main_page_dict_tmp, file, indent=4, ensure_ascii=False)
        
        main_page_dataset.update(main_page_dict_tmp)
        if debug:
            end_time = time.time()
            execution_time = end_time - start_time 
            execution_time_dict_tmp = {
                                    i: {
                                        "front_page_data_extraction_time": round(execution_time,2)
                                        }
                                    }
            execution_time_dict.update(execution_time_dict_tmp)
    
    return execution_time_dict
        