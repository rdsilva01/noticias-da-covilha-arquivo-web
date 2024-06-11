import json

def get_entities():
    
    for year in range(2009, 2020):
        with open(f'./news_data/{year}/key_moments_photos_{year}_tmp2.json', 'r') as f:
            data = json.load(f)
            
        for article in data:
            nid = article['nid']
            with open(f'./news_data/{year}/validated_{year}.json', 'r') as f:
                data2 = json.load(f)

            for article2 in data2:
                if article2['nid'] == nid:
                    all_entities = []
                    for entity in article2['spacy_entities_per']:
                        all_entities.append(entity)
                    for entity2 in article2['spacy_entites_org']:
                        all_entities.append(entity2)
                    for entity3 in article2['spacy_entities_loc']:
                        all_entities.append(entity3)
                    
                    if len(all_entities) > 5:
                        all_entities = all_entities[:5]
                    formatted_string = ''
                    for i, entity4 in enumerate(all_entities):
                        if i == 0:
                            formatted_string += f'<a href=\"pesquisa?query={entity4}&modo=text&exact_match=0&startDate=2009-01-01&endDate=2019-12-31\" class=\"link text-dark link-underline-opacity-25 link-underline-opacity-100-hover link-offset-2 link-underline-danger\">{entity4}</a>'
                        else:
                            formatted_string += f' / <a href=\"pesquisa?query={entity4}&modo=text&exact_match=0&startDate=2009-01-01&endDate=2019-12-31\" class=\"link text-dark link-underline-opacity-25 link-underline-opacity-100-hover link-offset-2 link-underline-danger\">{entity4}</a>'
                    
                    article['spacy_entities_formatted'] = formatted_string
                    break
            
        with open(f'./news_data/{year}/key_moments_photos_{year}_tmp_3.json', 'w') as f: 
            json.dump(data, f, indent=4, ensure_ascii=False)
            
get_entities()