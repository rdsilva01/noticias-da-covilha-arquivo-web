import json
from collections import Counter
import os

import json
from collections import Counter
import os

import os
import json
from collections import Counter

def get_data_spacy_statistics(year):
    json_file = f'../data/data_{year}/validated_{year}.json'
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    entity_types = ['spacy_entities_per', 'spacy_entites_org', 'spacy_entities_loc']
    statistics_by_type = {}

    for entity_type in entity_types:
        entity_counter = Counter()
        for entry in data:
            all_entities = entry.get(entity_type, [])  
            # filtering.........
            filtered_entities = [entity for entity in all_entities if entity not in ["NC", "Notícias da Covilhã"]]
            entity_counter.update(filtered_entities) 
        
        total_entities = sum(entity_counter.values())
        unique_entities = len(entity_counter)
        sorted_entities = entity_counter.most_common() 
        
        if year not in statistics_by_type:
            statistics_by_type[year] = {}
        
        statistics_by_type[year][entity_type] = {
            "total_entities": total_entities,
            "unique_entities": unique_entities,
            "most_common_entity": sorted_entities[0][0] if sorted_entities else None,
            "most_common_count": sorted_entities[0][1] if sorted_entities else None,
            "entity_frequency": dict(sorted_entities)
        }
    
    folder_name = f"data_{year}"
    folder_path = f"./data/{folder_name}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"statistics_{year}.json")
    with open(file_path, "w") as file:
        json.dump(statistics_by_type, file, indent=4, ensure_ascii=False)
        
    return statistics_by_type

def get_content_statistics(year):
    json_file = f'../data/data_{year}/validated_{year}.json'
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    content_statistics = {}
    year_total_words = 0
    year_total_chars = 0

    for entry in data:
        content = entry.get('content', '')
        words = content.split()
        num_words = len(words)
        year_total_words += num_words
        year_total_chars += sum(len(word) for word in words)
        avg_word_length = year_total_chars / year_total_words if year_total_words > 0 else 0
        avg_word_length = round(avg_word_length, 2)
        
        if year not in content_statistics:
            content_statistics[year] = {
                "content_stats": {
                    "num_words_year": year_total_words,
                    "avg_word_length_year": avg_word_length,
                    "num_words_per_news": {}
                }
            }
        
        content_statistics[year]["content_stats"]["num_words_per_news"][entry['url']] = {
            "num_words": num_words,
            "avg_word_length": avg_word_length
        }
    
    content_statistics[year]["content_stats"]["num_words_year"]=  year_total_words
    content_statistics[year]["content_stats"]["avg_word_length_year"]=  avg_word_length
    
    folder_name = f"data_{year}"
    folder_path = f"../data/{folder_name}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"content_statistics_{year}.json")
    with open(file_path, "w") as file:
        json.dump(content_statistics, file, indent=4, ensure_ascii=False)
        
    return content_statistics

def main():
    for i in range(2009, 2020):
        get_data_spacy_statistics(i)
        
main()