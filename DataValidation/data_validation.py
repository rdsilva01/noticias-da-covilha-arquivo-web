import json
import os

def remove_duplicates(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    unique_paragraphs = set()
    unique_data = []

    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        for news_item in data:
            paragraph = news_item.get("paragraph")
            if paragraph is not None and paragraph not in unique_paragraphs:
                unique_paragraphs.add(paragraph)
                unique_data.append(news_item)
    else:
        raise ValueError("Data format error: Expected a list of dictionaries")

    with open(output_file, 'w') as f:
        json.dump(unique_data, f, indent=4)

def data_validation(s_year, e_year):
    for year in range(s_year, e_year + 1):
        input_file = f'./data/data_{year}/{year}.json'
        output_file = f'./data/data_{year}/validated_{year}.json'
        if os.path.exists(input_file):
            remove_duplicates(input_file, output_file)
        else:
            print(f"Input file not found for year {year}")
