import json
import os

def sort_data(input_file, output_file):
    print()
def data_validation(s_year, e_year):
    for year in range(s_year, e_year + 1):
        input_file = f'./data/data_{year}/{year}.json'
        output_file = f'./data/data_{year}/validated_{year}.json'
        if os.path.exists(input_file):
            sort_data(input_file, output_file)
        else:
            print(f"Input file not found for year {year}")
