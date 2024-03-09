import json
import os
import urllib3

def remove_duplicates(input_file, output_file, debug):
    with open(input_file, 'r') as f:
        data = json.load(f)

    unique_urls = set()
    nid_list = []

    for i,urls_list in enumerate(data):
        for url in urls_list:
            nid = ""
            if "get.adobe.com/flashplayer/" not in url:
                temp_full_url_reversed = url[::-1] 
                for temp_full_url_reversed_char in temp_full_url_reversed:
                    if temp_full_url_reversed_char == "=":
                        break
                    else:
                        nid += temp_full_url_reversed_char
                    if debug:
                        if i != 0 and i % 1 == 0:
                            print(f"\r{100 * i / len(data):.2f}%", end='')
                            if i == len(data) - 1:
                                print(f"\r100.00%", end='')
                        
                nid = nid[::-1]
                if nid not in nid_list:
                    nid_list.append(nid)
                    unique_urls.add(url)

    unique_urls_json = {'urls': list(unique_urls)}

    with open(output_file, 'w') as f:
        json.dump(unique_urls_json, f, indent=4)
        
def url_validation(s_year, e_year):
    for year in range(s_year, e_year + 1):
        input_file = f'./data/data_{year}/urls_{year}.json'
        output_file = f'./data/data_{year}/validated_urls_{year}.json'
        remove_duplicates(input_file, output_file)
