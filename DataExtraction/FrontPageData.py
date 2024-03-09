import json
import os
import time
from bs4 import BeautifulSoup
import requests


def get_news_front(json_file, headers, year, debug=True):
    
    with open(json_file, 'r') as f:
        data = json.load(f)

    url_list = data["{}".format(year)]
    main_page_dataset_year = {}
    main_url_list = []
    
    for i, url in enumerate(url_list):
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')    
        
        bloco_capaedicao = soup.find(id='bloco_capaedicao') 
        
        if bloco_capaedicao:
                image = bloco_capaedicao.find('img')
                if image:
                        image_url = image.get('src')
                        if image_url not in main_url_list:
                            main_url_list.append(image_url)
                else:
                        print("not found")
        if debug:
                if i != 0 and i % 1 == 0:
                    print(f"\r{100 * i / len(url_list):.2f}%", end='')       
                    if i == len(url_list) - 1:
                        print(f"\r100.00%", end='')
                            
    return main_url_list
    
def get_main_page_dataset(s_year, e_year, header, debug=True):
    execution_time_dict = {}
    main_page_dataset = {}
    
    print("FRONT PAGE DATA")
    for i in range(s_year, e_year+1, 1):
        start_time = time.time()
        json_file =  './data/data_{}/past_urls_{}.json'.format(i,i)
        main_page_dict = get_news_front(json_file=json_file, headers=header, year=i, debug=debug)
        main_page_dict_tmp = { 
                i: main_page_dict 
            }
        folder_name = "data_{}".format(i)
        folder_path = "./data/{}".format(folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, "front_page_image_urls_{}.json".format(i))
        with open(file_path, "w") as file:
            json.dump(main_page_dict_tmp, file, indent=4, ensure_ascii=False)
        
        #print(main_page_dict_tmp)
        main_page_dataset.update(main_page_dict_tmp)
        if debug:
            end_time = time.time()
            execution_time = end_time - start_time 
            execution_time_dict_tmp ={
                                    i: {
                                        "front_page_data_extraction_time": round(execution_time,2)
                                        }
                                    }
            execution_time_dict.update(execution_time_dict_tmp)
    
    return execution_time_dict
        