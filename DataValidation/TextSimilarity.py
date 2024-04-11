import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("NOVA-vision-language/GlorIA-1.3B")
model = AutoModelForCausalLM.from_pretrained("NOVA-vision-language/GlorIA-1.3B")

def square_rooted(x):
    from math import sqrt 
    return round(sqrt(sum([a*a for a in x])),3)

def Cosine(x,y):
    numerator = sum([a*b for a,b in zip(x,y)])
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator),3)

def similarity_per_text(text1, text2):
    input_ids = tokenizer.encode(text1, return_tensors="pt")
    outputs = model(input_ids, output_hidden_states=True)
    embeddings = outputs.hidden_states[-1]

    input_ids2 = tokenizer.encode(text2, return_tensors="pt")
    outputs2 = model(input_ids2, output_hidden_states=True)
    embeddings2 = outputs2.hidden_states[-1]

    # calcular a média dos embeddings
    mean_embedding1 = torch.mean(embeddings[0], dim=1)
    mean_embedding2 = torch.mean(embeddings2[0], dim=1)

    # Calcular a similaridade entre os embeddings
    cosine_similarity = Cosine(mean_embedding1.tolist(), mean_embedding2.tolist())
    print("SIMILARIDADE: ", cosine_similarity)
    
    return cosine_similarity

def similarity_per_text_list(text1, text_list):
    similarities = []
    for text2 in text_list:
        similarity = similarity_per_text(text1, text2)
        similarities.append(similarity)
    return similarities

def similarity_per_file(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    for i, article in enumerate(data):
        list_of_similarities = []
        current_nid = article['nid']
        current_title = article['title']
        current_text = article['content']
        if current_title == "":
            continue
        else:
            # Open the similarity file for each article to check for existing comparisons
            with open(output_file, 'r') as f:
                similarity_data = json.load(f)

            for article2 in similarity_data:
                if article2['nid'] != current_nid: # and article2['nid'] not in [x[2] for x in list_of_similarities]
                    title2 = article2['title']
                    text2 = article2['content']
                    if title2 == "":
                        continue
                    else:
                        if len(list_of_similarities) < 3:
                            similarity = similarity_per_text(current_title, title2)
                            similarity2 = similarity_per_text(current_text, text2)
                            mean_similarity = (similarity + similarity2) / 2
                            if mean_similarity > 0.75:
                                list_of_similarities.append((similarity, current_nid, article2['nid']))
            
            article['similarities'] = list_of_similarities
            print(f"Article {i} done")
            
    # Save the updated data file after processing all articles
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main(year):
    for year in range(year, year + 1):
        input_file = f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/validated_{year}.json'
        output_file = f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/similarity_{year}.json'
        # input_file = f'../data/data_{year}/validated{year}.json'
        # output_file = f'../data/data_{year}/similarity_{year}.json'
        if os.path.exists(input_file):
            similarity_per_file(input_file, output_file)
        else:
            print(f"Input file not found for year {year}")
        
main(2009)