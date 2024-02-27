import json

def remove_duplicates(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    unique_urls = set()
    for urls_list in data:
        unique_urls.update(urls_list)

    unique_urls_json = {'urls': list(unique_urls)}

    with open(output_file, 'w') as f:
        json.dump(unique_urls_json, f, indent=4)

if __name__ == '__main__':
    input_file = '../DataExtraction/data/data_2012/urls_2012.json'
    output_file = '../DataExtraction/data/data_2012/validated_urls_2012.json'
    remove_duplicates(input_file, output_file)
