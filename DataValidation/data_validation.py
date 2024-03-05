import os
import json
from datetime import datetime

def sort_data(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    sorted_articles = []

    for article in data:
        if "date" in article:
            sorted_articles.append(article)

    sorted_articles.sort(key=lambda x: x.get("date"))

    # for i, article in enumerate(sorted_articles):
    #     print("{} - {}".format(i, article["date"]))

    with open(output_file, "w") as outfile:
        json.dump(sorted_articles, outfile, indent=4, ensure_ascii=False)
   
def data_validation(s_year, e_year):
    for year in range(s_year, e_year + 1):
        input_file = f'./data/data_{year}/{year}.json'
        output_file = f'./data/data_{year}/validated_{year}.json'
        if os.path.exists(input_file):
            sort_data(input_file, output_file)
        else:
            print(f"Input file not found for year {year}")
