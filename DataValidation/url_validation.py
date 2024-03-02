import json

def remove_duplicates(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    unique_urls = set()
    for urls_list in data:
        for url in urls_list:
            if "get.adobe.com/flashplayer/" not in url:
                unique_urls.add(url)

    unique_urls_json = {'urls': list(unique_urls)}

    with open(output_file, 'w') as f:
        json.dump(unique_urls_json, f, indent=4)
        
def url_validation(s_year, e_year):
    for year in range(s_year, e_year + 1):
        input_file = f'./data/data_{year}/urls_{year}.json'
        output_file = f'./data/data_{year}/validated_urls_{year}.json'
        remove_duplicates(input_file, output_file)
