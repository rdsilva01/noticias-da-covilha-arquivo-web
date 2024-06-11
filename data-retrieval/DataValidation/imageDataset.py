import json
import os
import numpy as np
import spacy

# class BertTokenEstimator():
#     def __init__(self, model):
#         self.bert_tokenizer = AutoTokenizer.from_pretrained(model)

#     def estimate_tokens(self, text):
#         return len(self.bert_tokenizer.encode(text))

# model_name = "neuralmind/bert-base-portuguese-cased"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)

# def get_embeddings_bert(text, tokenizer, model):
#     # Tokenize and encode the text
#     inputs = tokenizer(text, return_tensors="pt")

#     # Get the embeddings
#     output = model(**inputs)

#     document_embedding = output.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
#     return document_embedding

model = 'pt_core_news_lg' # lg over sm, to get accuracy over efficieny
nlp = spacy.load(model, disable=['tagger', 'parser'])

def same_images():
    '''this function collects all the images by their image_desc and save all the urls that have the same image_desc'''
    full_image_data = []
    
    for year in range(2009, 2020):
        with open(f'./news_data/{year}/key_moments_{year}.json', 'r') as f:
            data = json.load(f)
        
        full_image_data.extend(data)
    
    image_desc_dict = {}
    for article in full_image_data:
        image_desc = article['image_desc']
        if image_desc != "no_image" and image_desc != "":
            if image_desc not in image_desc_dict:
                image_desc_dict[image_desc] = []
            image_desc_dict[image_desc].append(article['image_url'])
        
    with open('./news_data/image_desc_dict.json', 'w') as outfile:
        json.dump(image_desc_dict, outfile, indent=4, ensure_ascii=False)
        
def count_images():
    with open('./news_data/image_desc_dict.json', 'r') as f:
        image_desc_dict = json.load(f)
        
    # count the len of the dict
    count = 0
    for key in image_desc_dict:
        count += 1
    
    print(count)
    
count_images()



def dataset_creation(output_file):
    data = []  # Initialize data list
    for year in range(2009, 2020):
        with open(f'./news_data/{year}/key_moments_{year}.json', 'r') as f:
            if year == 2009:
                data = json.load(f)
            else:
                data.extend(json.load(f))
                
    image_url_list = []
    image_data = []

    for article in data:
        if article['image_url'] and article['image_url'] != "no_image":
            image_url = article['image_url']
            if image_url not in image_url_list:
                image_info = {
                    'image_url': image_url,
                    'image_desc': article['image_desc'],
                    'spacy': []
                }
                image_data.append(image_info)
                image_url_list.append(image_url)

    for image in image_data:
        for article in data:
            if article['image_url'] == image['image_url']:
                content_3_phrases = article['content'].split(".")[:3]
                content_3_phrases_string = ". ".join(content_3_phrases)
                for k in range(4):
                    if k == 0:
                        doc = nlp(article['title'])
                    elif k == 1:
                        doc = nlp(article['text_snippet'])
                    elif k == 2:
                        doc = nlp(image['image_url'])
                    elif k == 3:
                        doc = nlp(content_3_phrases_string)
                    for ent in doc.ents:
                        if ent.label_ in ["PER", "ORG", "LOC"]:
                            if ent.text.lower() not in image['spacy']:
                                image['spacy'].append(ent.text.lower())
                
                image['news_nid'] = article['nid']
                image['news_url'] = article['url']
                image['news_title'] = article['title'].lower()
                image['news_subtitle'] = article['subtitle']
                image['news_text_snippet'] = article['text_snippet'].lower()
                image['news_content'] = content_3_phrases_string.lower()
                image['news_date'] = article['date']
                image['news_category'] = article['category']
                image['news_sub_category'] = article['sub_category']
        
    with open(output_file, "w") as outfile:
        json.dump(image_data, outfile, indent=4, ensure_ascii=False)
    
    return image_url_list, image_data


def similarity_image():
    with open('./news_data/image_dataset_tmp.json', 'r') as f:
        image_dataset_list = json.load(f)
        
    for i, image in enumerate(image_dataset_list):
        image_desc = image['image_desc']
        processed_desc = set()  # Keep track of processed image descriptions for each image
        image_spacy_list = set(image['spacy'])  # Convert to set for faster lookup
        similar_images_data = []
        
        for j, image2 in enumerate(image_dataset_list):
            if i != j and image2['image_desc'] not in processed_desc and image['image_desc'] != image2['image_desc']:
                common_entities = set(image_spacy_list).intersection(image2['spacy'])
                if common_entities:  # If there are common entities
                    similarity_score = len(common_entities)
                    similar_images_data.append((image2['news_date'], image2['image_url'], image2['news_url'], image2['news_nid'], similarity_score))
                    # add the image to the processed_desc
                    processed_desc.add(image2['image_desc'])
        
        # sort similar_images_data based on the similarity score (in descending order)
        similar_images_data.sort(key=lambda x: x[4], reverse=True)
        
        # extract dates, image URLs, news URLs, and news nids
        dates = [data[0] for data in similar_images_data[:12]]
        image_urls = [data[1] for data in similar_images_data[:12]]
        news_urls = [data[2] for data in similar_images_data[:12]]
        news_nids = [data[3] for data in similar_images_data[:12]]
        
        image['similar_dates'] = dates
        image['similar_image_urls'] = image_urls
        image['similar_news_urls'] = news_urls
        image['similar_news_nids'] = news_nids
        
        processed_desc.add(image_desc)  # Add the processed image_desc to the set
        
        print(f"Image {i} done")
        
    with open('./news_data/image_dataset2.json', 'w') as outfile:
        json.dump(image_dataset_list, outfile, indent=4, ensure_ascii=False)
        
    return image_dataset_list


def main():
    output_file = f'./news_data/image_dataset.json'
    # dataset_creation(output_file)
    # similarity_image()
    # same_images()
                
main()