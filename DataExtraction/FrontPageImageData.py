import os
import time
from PIL import Image
import pytesseract
import requests
from io import BytesIO
import re
import json
from PIL import UnidentifiedImageError
from datetime import datetime, timedelta
import numpy as np
import cv2

# in use
def get_front_page_image_data_year_algorithm(year, json_file, first_date=None, debug=True):
    print(f'\n{year}')

    with open(json_file, 'r') as f:
        data = json.load(f)

    urls = data[str(year)]
    front_page_dict = {}

    # set the date manually or with an argument
    if first_date is not None:
        current_date = datetime.strptime(first_date, "%Y-%m-%d")
    else:
        first_url_key = sorted(urls.keys())[0] 
        print(urls[first_url_key])
        current_date = input("Insert the first date (format YEAR-MONTH-DAY): ")
        current_date = datetime.strptime(current_date, "%Y-%m-%d")

    previous_key = None
    for key, url in sorted(urls.items(), key=lambda item: int(item[0])):
        try:
            url_number = int(key)
            if previous_key is not None:
                delta_days = url_number - int(previous_key)
                current_date += timedelta(days=delta_days*7) # each number of the front page means a week, so from 1001 to 1002, the +1 is 7 days!  

            formatted_date = current_date.strftime("%Y-%m-%d")
            front_page_dict[formatted_date] = url

            previous_key = key

        except Exception as e:
            print(f"Error processing URL: {url}. {e}")

    return front_page_dict

# deprecated
def get_front_page_image_data_year_ocr(year, json_file, debug=True):
    print(f'\n{year}')
    month_mapping = {
        'JANEIRO': 'January',
        'FEVEREIRO': 'February',
        'MARÇO': 'March',
        'ABRIL': 'April',
        'MAIO': 'May',
        'JUNHO': 'June',
        'JULHO': 'July',
        'AGOSTO': 'August',
        'SETEMBRO': 'September',
        'OUTUBRO': 'October',
        'NOVEMBRO': 'November',
        'DEZEMBRO': 'December'
    }

    with open(json_file, 'r') as f:
        data = json.load(f)

    urls = data[str(year)]
    date_list = []
    front_page_dict = {

    }

    for i, url in enumerate(urls):
        try:
            img_response = requests.get(url)
            imagem = Image.open(BytesIO(img_response.content)).convert('RGB')  # Pillow to get the image
            
            npimagem = np.asarray(imagem).astype(np.uint8)  # converting to a matrix
            
            # diminuição dos ruidos antes da binarização
            npimagem[:, :, 0] = 0 # zerando o canal R (RED)
            npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)
            
            # atribuição em escala de cinza
            im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 
            
            # aplicação da truncagem binária para a intensidade
            # pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
            # pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
            # A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
            ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 
            
            # reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
            binimagem = Image.fromarray(thresh) 

            text = pytesseract.image_to_string(binimagem)
            
            date_pattern = r'(\d{1,2}) DE ([A-Z]+) DE (\d{4})'
            matches = re.findall(date_pattern, text)  # to get the date only
            
            for match in matches:
                day, month, year = match
                english_month = month_mapping.get(month, '')
                if english_month:
                    try:
                        formatted_date = datetime.strptime(f"{day} {month} {year}", "%d %B %Y").strftime("%Y-%m-%d")
                        #if formatted_date not in date_list:
                        date_list.append(formatted_date)
                            # print(f'{formatted_date} - {url}')
                        front_page_dict[formatted_date] = url
                    except ValueError as e:
                        print(f"Error processing date from URL: {url}. {e}")

        except UnidentifiedImageError as e:
            print(f"Error processing image from URL: {url}. {e}")
        
        if debug:
            if i != 0 and i % 1 == 0:
                print(f"\r{100 * i / len(urls):.2f}%", end='')       
                if i == len(urls) - 1:
                    print(f"\r100.00%", end='')

    # print(front_page_dict)
    # print(len(front_page_dict))
    
    ordered_dict = dict(sorted(front_page_dict.items()))
    return ordered_dict
    
def get_front_page_image_data(s_year, e_year, debug=True, ocr=True):
    execution_time_dict = {}
    main_page_dataset = {}
    
    print("FRONT PAGE DATA")
    for i in range(s_year, e_year+1, 1):
        start_time = time.time()
        json_file =  f'./data/data_{i}/front_page_image_urls_{i}.json'
        if ocr:
            main_page_dict = get_front_page_image_data_year_ocr(year=i, json_file=json_file, debug=debug)
        else:
            main_page_dict = get_front_page_image_data_year_algorithm(year=i, json_file=json_file, debug=debug)
        main_page_dict_tmp = { 
                i: main_page_dict 
            }
        folder_name = "data_{}".format(i)
        folder_path = "./data/{}".format(folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, "front_page_image_data_{}.json".format(i))
        with open(file_path, "w") as file:
            json.dump(main_page_dict_tmp, file, indent=4, ensure_ascii=False)
        
        #print(main_page_dict_tmp)
        main_page_dataset.update(main_page_dict_tmp)
        if debug:
            end_time = time.time()
            execution_time = end_time - start_time 
            execution_time_dict_tmp = {
                                    i: {
                                        "front_page_image_data_extraction_time": round(execution_time,2)
                                        }
                                    }
            execution_time_dict.update(execution_time_dict_tmp)
    
    return execution_time_dict

def get_front_page_data_manual(year):
    folder_name = "data_{}/capa_{}".format(year, year)
    folder_path = "../data/{}".format(folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, "capa_{}.json".format(year))
    data_dict = {}

    # Check if the file already exists
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data_dict = json.load(file)

    num_capas = int(input("NÚMERO DE CAPAS: "))
    
    for _ in range(num_capas):
        date_input = input("DATA (YYYY-MM-DD): ")
        url_input = input("URL: ")
        num_attributes = int(input("NÚMERO DE NOTÍCAS: "))
        num_pubs = int(input("NÚMERO DE PUBLICIDADES: "))
        
        # Create a dictionary for the current date
        date_dict = {
            "url": url_input,
            "attributes": [],
            "pubs": []
        }
        
        # Input news (attributes)
        attribute_list = []
        for _ in range(num_attributes):
            attribute = input("NOTÍCIA {}: ".format(_ + 1))
            attribute_list.append(attribute)
        date_dict["attributes"] = attribute_list

        # Input advertisements (publicities) with empty image file names
        pubs_list = []
        for _ in range(num_pubs):
            pub = input("PUBLICIDADE {}: ".format(_ + 1))
            pubs_list.append({"ad_name": pub, "image_file": ""}) 
        date_dict["pubs"] = pubs_list

        # Add the date_dict to data_dict
        data_dict[date_input] = date_dict

        # Save the updated data to the file
        with open(file_path, "w") as file:
            json.dump(data_dict, file, indent=4, ensure_ascii=False)
        
# Example usage:
get_front_page_data_manual(2015)




