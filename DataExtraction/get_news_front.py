def get_news_front(json_file, headers):
    
    url_list = read_urls_from_json(json_file=json_file)
    
    for url in url_list:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')    
        
        date = ""
        image_url = ""
        
        d = {}
        
        top_div = soup.find(id='div_topo') 
        
        if top_div:
                nested_top_divs = top_div.find_all('div')
                for nested_top_div in nested_top_divs:
                    top_span = nested_top_div.find('span')
                    if top_span:
                        if "Quinta-Feira" in top_span.text:
                            d['date'] = top_span.text

        return d         