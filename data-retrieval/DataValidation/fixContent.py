import json
import yake

def fix_content():
    # YAKE args
    language = "pt"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20
    
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    
    for year in range(2009, 2020):
        with open(f'./news_data/{year}/validated_{year}.json', 'r') as f:
            data = json.load(f)
        for article in data:
            keywords = []
            keywords_tmp = custom_kw_extractor.extract_keywords(article['content'])
            for kw in keywords_tmp:
                # print(kw)
                keywords.append(kw[0])
                
            # join the formatted content in a single string a replace "" with <br><br>
            formatted_content = article['formatted_content']
            full_formatted_content = ""
            for single_content in formatted_content:
                if single_content == "":
                    full_formatted_content += "<br>"
                else:
                    full_formatted_content += single_content + "<br>"
                    
            # replace <br><br><br> with <br><br>
            article['formatted_html_content'] = full_formatted_content.replace('<br><br><br><br><br><br><br>', '<br><br>')
            article['formatted_html_content'] = full_formatted_content.replace('<br><br><br><br><br><br>', '<br><br>')
            article['formatted_html_content'] = full_formatted_content.replace('<br><br><br><br><br>', '<br><br>')
            article['formatted_html_content'] = full_formatted_content.replace('<br><br><br><br>', '<br><br>')
            article['formatted_html_content'] = full_formatted_content.replace('<br><br><br>', '<br><br>')
            
            article['keywords_3_gram'] = keywords[:10]
            # article['keywords_3_gram'] = keywords
            for i, kw in enumerate(keywords):
                if i == 0:
                    article['formatted_html_content'] = article['formatted_html_content'].replace(kw, f'<span class="bg-danger px-1 d-inline-block text-keywords-3-gram text-light">{kw}</span>')
                else:
                    article['formatted_html_content'] = article['formatted_html_content'].replace(kw, f'<span class="fw-bold text-keywords-3-gram">{kw}</span>')
        
        with open(f'./news_data/{year}/validated_tmp_{year}.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
def fix_html_content():
    for year in range(2009, 2020):
        with open(f'./news_data/{year}/key_moments_tmp_{year}.json', 'r') as f:
            data = json.load(f)
            
        for article in data:
            nid = article['nid']
            with open(f'./news_data/{year}/validated_tmp_{year}.json', 'r') as f:
                data2 = json.load(f)

            for article2 in data2:
                if article2['nid'] == nid:
                    article['formatted_html_content'] = article2['formatted_html_content']
                    break
            
        with open(f'./news_data/{year}/key_moments_tmp_{year}.json', 'w') as f: 
            json.dump(data, f, indent=4, ensure_ascii=False)
            
                
            
            
fix_content()
fix_html_content()