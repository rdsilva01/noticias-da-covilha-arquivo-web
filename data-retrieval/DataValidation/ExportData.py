import json
import os


def get_data(name):
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{name}/similarities_bert.json', "r") as readfile:
        bert = json.load(readfile)
        
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{name}/similarities_gloria.json', "r") as readfile:
        gloria = json.load(readfile)
        
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{name}/similarities_albertina.json', "r") as readfile:
        albertina = json.load(readfile)
        
    return bert, gloria, albertina

def data_to_csv():
    name_list = [
        'CULTURA', 
        'FUNICULAR', 
        'ORFEAO', 
        'POLITICA', 
        'RELIGIAO',
        'LEOES',
        'UBI',
        'PORTAGENS',
        'ACIDENTE',
        'MATERNIDADE'
        ]
    
    for i in name_list:
        bert,gloria,albertina = get_data(i)
        
        # print(i) 
        bert[0]
        # print("TITLE")
        title_str_list = []
        for j in range(0,10):
            id = bert[0][j]['id']
            title = bert[0][j]['title_similarity']
            title_str = f"{id}: {title}"
            title_str_list.append(title_str)
            # print(title_str)
            
        # print("TEXT")
        text_str_list = []
        for j in range(0,10):
            id = bert[0][j]['id']
            text = bert[1][j]['text_similarity']
            text_str = f"{id}: {text}"
            text_str_list.append(text_str)
            # print(text_str)

        # print("TITLE + TEXT") 
        title_plus_text_str_list = []
        for j in range(0,10):
            id = bert[0][j]['id']
            title_plus_text = bert[2][j]['title_plus_text_similarity']
            title_plus_text_str = f"{id}: {title_plus_text}"
            title_plus_text_str_list.append(title_plus_text_str)
            # print(title_plus_text_str)
           
        bert_dict = {
            'title': title_str_list,
            'text': text_str_list,
            'title_plus_text': title_plus_text_str_list
        }
            
        # print(bert_dict)
        
        gloria[0]
        # print("TITLE")
        title_str_list = []
        for j in range(0,10):
            id = gloria[0][j]['id']
            title = gloria[0][j]['title_similarity']
            title_str = f"{id}: {title}"
            title_str_list.append(title_str)
            # print(title_str)
            
        # print("TEXT")
        text_str_list = []
        for j in range(0,10):
            id = gloria[0][j]['id']
            text = gloria[1][j]['text_similarity']
            text_str = f"{id}: {text}"
            text_str_list.append(text_str)
            # print(text_str)

        # print("TITLE + TEXT") 
        title_plus_text_str_list = []
        for j in range(0,10):
            id = gloria[0][j]['id']
            title_plus_text = gloria[2][j]['title_plus_text_similarity']
            title_plus_text_str = f"{id}: {title_plus_text}"
            title_plus_text_str_list.append(title_plus_text_str)
            # print(title_plus_text_str)
           
        gloria_dict = {
            'title': title_str_list,
            'text': text_str_list,
            'title_plus_text': title_plus_text_str_list
        }
            
        # print(gloria_dict)
        
        albertina[0]
        # print("TITLE")
        title_str_list = []
        for j in range(0,10):
            id = albertina[0][j]['id']
            title = albertina[0][j]['title_similarity']
            title_str = f"{id}: {title}"
            title_str_list.append(title_str)
            # print(title_str)
            
        # print("TEXT")
        text_str_list = []
        for j in range(0,10):
            id = albertina[0][j]['id']
            text = albertina[1][j]['text_similarity']
            text_str = f"{id}: {text}"
            text_str_list.append(text_str)
            # print(text_str)

        # print("TITLE + TEXT") 
        title_plus_text_str_list = []
        for j in range(0,10):
            id = albertina[0][j]['id']
            title_plus_text = albertina[2][j]['title_plus_text_similarity']
            title_plus_text_str = f"{id}: {title_plus_text}"
            title_plus_text_str_list.append(title_plus_text_str)
            # print(title_plus_text_str)
           
        albertina_dict = {
            'title': title_str_list,
            'text': text_str_list,
            'title_plus_text': title_plus_text_str_list
        }
            
        # print(albertina_dict)
        
         # save to a csv file
        if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{i}') == False:
            os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{i}')
            
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{i}/similarities_title.csv', "w", encoding="utf8") as writefile:   
            writefile.write("ALBERTINA,BERT,GLORIA\n")
            for j in range(0,10):
                writefile.write(f"{albertina_dict['title'][j]},{bert_dict['title'][j]},{gloria_dict['title'][j]}\n")
                
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{i}/similarities_text.csv', "w", encoding="utf8") as writefile:   
            writefile.write("ALBERTINA,BERT,GLORIA\n")
            for j in range(0,10):
                writefile.write(f"{albertina_dict['text'][j]},{bert_dict['text'][j]},{gloria_dict['text'][j]}\n")
        
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_2009/{i}/similarities_title_plus_text.csv', "w", encoding="utf8") as writefile:   
            writefile.write("ALBERTINA,BERT,GLORIA\n")
            for j in range(0,10):
                writefile.write(f"{albertina_dict['title_plus_text'][j]},{bert_dict['title_plus_text'][j]},{gloria_dict['title_plus_text'][j]}\n")
        
data_to_csv()