import json

# Load the original JSON data
for year in range(2019, 2020):
    with open(f'news_data/{year}/capa_{year}/capa_{year}.json', 'r') as file:
        original_data = json.load(file)

    # Create a new dictionary to store the modified data
    modified_data = {}

    # Iterate over the original data and add the date as an attribute in each dictionary
    for date, data in original_data.items():
        data["data"] = date
        modified_data[date] = data

    # Write the modified data to a new JSON file
    with open(f'news_data/{year}/capa_{year}/mod_capa_{year}.json', 'w') as file:
        json.dump(modified_data, file, indent=4, ensure_ascii=False)