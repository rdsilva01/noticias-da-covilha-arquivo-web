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
    
    min = 2009
    max = 2010
    
    for i in range(min,max+1):
        input_file = '../DataExtraction/data/data_{}/urls_{}.json'.format(i,i)
        output_file = '../DataExtraction/data/data_{}/validated_urls_{}.json'.format(i,i)
        remove_duplicates(input_file, output_file)
