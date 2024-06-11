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
            matches = re.findall(date_pattern, text) 
            
            for match in matches:
                day, month, year = match
                english_month = month_mapping.get(month, '')
                if english_month:
                    try:
                        formatted_date = datetime.strptime(f"{day} {month} {year}", "%d %B %Y").strftime("%Y-%m-%d")
                        date_list.append(formatted_date)
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
    
    ordered_dict = dict(sorted(front_page_dict.items()))
    return ordered_dict

def get_front_page_data_manual(year):
    folder_name = "{}/capa_{}".format(year, year)
    folder_path = "./data/{}".format(folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, "capa_{}.json".format(year))
    data_dict = {}

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data_dict = json.load(file)

    num_capas = int(input("NÚMERO DE CAPAS: "))
    
    for _ in range(num_capas):
        date_input = input("DATA (YYYY-MM-DD): ")
        url_input = input("URL: ")
        num_attributes = int(input("NÚMERO DE NOTÍCAS: "))
        num_pubs = int(input("NÚMERO DE PUBLICIDADES: "))
        
        date_dict = {
            "url": url_input,
            "attributes": [],
            "pubs": []
        }

        attribute_list = []
        for _ in range(num_attributes):
            attribute = input("NOTÍCIA {}: ".format(_ + 1))
            attribute_list.append(attribute)
        date_dict["attributes"] = attribute_list

        pubs_list = []
        for _ in range(num_pubs):
            pub = input("PUBLICIDADE {}: ".format(_ + 1))
            pubs_list.append({"ad_name": pub, "image_file": ""}) 
        date_dict["pubs"] = pubs_list

        data_dict[date_input] = date_dict

        with open(file_path, "w") as file:
            json.dump(data_dict, file, indent=4, ensure_ascii=False)
        
# Example usage:
# get_front_page_data_manual(2019)
