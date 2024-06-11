    
import json
import os

import urllib3

def sort_data(input_file, output_file, year):
    with open(input_file, 'r') as f:
        data = json.load(f)

    new_list_articles = []
    
    for i, article in enumerate(data):
        new_article = {}
        # adding just the necessary parameters 
        new_article["nid"] = article["nid"]
        new_article["url"] = article["url"]
        new_article["title"] = article["title"]
        new_article["subtitle"] = article["subtitle"]
        new_article["category"] = article["category"]
        new_article["sub_category"] = article["sub_category"]
        new_article["date"] = article["date"]
        new_article["image_url"] = article["image_url"]
        new_article["image_desc"] = article["image_desc"]
        new_article["content"] = article["content"]
        new_article["text_snippet"] = article["text_snippet"]
        new_article["author"] = article["author"]
        new_article["formatted_html_content"] = article["formatted_html_content"]
        new_article["formatted_html_content_normal"] = article["formatted_html_content_normal"]
        new_article["formatted_html_keywords"] = article["formatted_html_keywords"][2:]
        new_article["sim_1"] = article["sim_1"]
        new_article["sim_1_score"] = article["sim_1_score"]
        new_article["sim_2"] = article["sim_2"]
        new_article["sim_2_score"] = article["sim_2_score"]
        new_article["sim_3"] = article["sim_3"]
        new_article["sim_3_score"] = article["sim_3_score"]
        new_article["sim_4"] = article["sim_4"]
        new_article["sim_4_score"] = article["sim_4_score"]
        new_article["sim_5"] = article["sim_5"]
        new_article["sim_5_score"] = article["sim_5_score"]

        new_list_articles.append(new_article)
    
    # Sort articles by date if present
    new_list_articles.sort(key=lambda x: x.get("date", ""))

    with open(output_file, "w") as outfile:
        json.dump(new_list_articles, outfile, indent=4, ensure_ascii=False)
    
    return len(new_list_articles)

def main(s_year, e_year):
    for year in range(s_year, e_year + 1):
            input_file = f'./news_data/{year}/key_moments_{year}.json'
            output_file = f'./news_data/{year}/key_moments_{year}.json'
            
            if os.path.exists(input_file):
                sort_data(input_file, output_file, year)
            else:
                print(f"Input file not found for year {year}")
                
# main(2009, 2019)

import json
import time

def date_to_unix_epoch(date_str):
    """Converts a date string in 'YYYY-MM-DD' format to UNIX Epoch timestamp."""
    return int(time.mktime(time.strptime(date_str, '%Y-%m-%d')))

def adding_unix_epoch_time():
    for year in range(2009, 2020):
        input_file = f'./news_data/{year}/key_moments_{year}.json'
        output_file = f'./news_data/{year}/key_moments_{year}.json'
        
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        for article in data:
            # Calculate the UNIX Epoch time for the article date
            article_date = article["date"]
            unix_epoch_time = date_to_unix_epoch(article_date)
            article["unix_epoch_time"] = unix_epoch_time
            # drop unix_epoch_time_lisbon
            article.pop("unix_epoch_time_lisbon", None)
        
        with open(output_file, "w") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

# Example usage:
# adding_unix_epoch_time()

def fix_content():
    for year in range(2009, 2020):
        input_file = f'./news_data/{year}/key_moments_{year}.json'
        output_file = f'./news_data/{year}/key_moments_{year}.json'
            
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        for article in data:
            # fix the html content of the article
            article_content = article["formatted_html_content"]
            if article_content.startswith("<br>") or article_content.startswith("<br><br>") or article_content.startswith("<br><br><br>") or article_content.startswith("<br><br><br><br>"):
                article_content = article_content[4:]
            if article_content.endswith("<br>"):
                article_content = article_content[:-4]
            article_content = article_content.replace("<br><br><br>", "<br><br>")
            article_content = article_content.replace("<br><br><br><br>", "<br><br>")
            article["formatted_html_content"] = article_content
            
            article_content_normal = article["formatted_html_content_normal"]
            if article_content_normal.startswith("<br>") or article_content_normal.startswith("<br><br>") or article_content_normal.startswith("<br><br><br>") or article_content_normal.startswith("<br><br><br><br>"):
                article_content_normal = article_content_normal[4:]
            if article_content_normal.endswith("<br>"):
                article_content_normal = article_content_normal[:-4]
            article_content_normal = article_content_normal.replace("<br><br><br>", "<br><br>")
            article_content_normal = article_content_normal.replace("<br><br><br><br>", "<br><br>")
            article["formatted_html_content_normal"] = article_content_normal
            
        with open(output_file, "w") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        
# fix_content()

import os
import json
import urllib.request
import urllib.parse

def download_images():
    for year in range(2009, 2020):
        input_file = f'./news_data/{year}/key_moments_{year}.json'
        output_file = f'./news_data/{year}/key_moments_photos_{year}.json'
        image_dir = f'./news_data/{year}/images'
        
        os.makedirs(image_dir, exist_ok=True)
        
        with open(input_file, 'r') as f:
            data = json.load(f)
            
        for article in data:
            image_url = article["image_url"]
            if image_url:
                image_url = urllib.parse.quote(image_url, safe=':/')
                try:
                    image_name = image_url.split('/')[-1]
                    image_path = os.path.join(image_dir, article["nid"] + ".jpg")
                    if not os.path.exists(image_path):
                        urllib.request.urlretrieve(image_url, image_path)
                    article["image_url"] = f'./images/{article["nid"]}.jpg'
                    print(f"Downloaded image for article {article['nid']}")
                    
                except Exception as e:
                    print(f"Error downloading image for article {article['nid']}: {e}")
                        
        with open(output_file, "w") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

# download_images()


def fix_image_url():
    for year in range(2009, 2020):
        input_file = f"/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/{year}/key_moments_photos_{year}_tmp.json"
        output_file = f"/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/{year}/key_moments_photos_{year}_tmp.json"
        # input_file = f'./news_data/{year}/key_moments_photos_{year}.json'
        # output_file = f'./news_data/{year}/key_moments_photos_{year}_tmp.json'
        
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        for article in data:
            image_url = article["image_url"]
            if image_url and image_url.startswith("static/images"):
                article["image_url"] = article["image_url"].replace("static/images", "static/img/news_images")
        
        with open(output_file, "w") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

# fix_image_url()

def fix_image_url_2():
    for year in range(2009, 2020):
        input_file = f"/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/{year}/key_moments_photos_{year}_tmp.json"
        output_file = f"/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/{year}/key_moments_photos_{year}_tmp2.json"
        
        with open(input_file, 'r') as f:
            data = json.load(f)
            
        for article in data:
            input_file_2 = f"/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/{year}/key_moments_tmp_{year}.json"
            with open(input_file_2, 'r') as f:
                data_2 = json.load(f)
                
            for article_2 in data_2:
                if article["nid"] == article_2["nid"]:
                    if article["image_url"].startswith("static/img/news_image"):
                        article["image_url"] = f"static/img/news_images/{article['nid']}.jpg"
                        article["formatted_html_content"] = article_2["formatted_html_content"]
                        article["formatted_html_content_normal"] = article_2["formatted_html_content_normal"]
                        article["formatted_html_keywords"] = article_2["formatted_html_keywords"]
                    else:
                        article["image_url"] = article_2["image_url"]
                        article["formatted_html_content"] = article_2["formatted_html_content"]
                        article["formatted_html_content_normal"] = article_2["formatted_html_content_normal"]
                        article["formatted_html_keywords"] = article_2["formatted_html_keywords"]
                        break
                    
        with open(output_file, "w") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        
# fix_image_url_2 ()

def image_dataset_comp():
    with open(f"/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/image_dataset.json", "r") as f:
        image_data = json.load(f)

    for image in image_data:
        for year in range(2009, 2020):
            with open(f"/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis//news_data/{year}/key_moments_photos_{year}_tmp2.json", "r") as f:
                articles_data = json.load(f)

            for article in articles_data:
                if image["news_nid"] == article["nid"]:
                    image["image_url"] = article["image_url"]
                    break
                
    with open(f"/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/MyWebsites/websites/arquivonc/redis/news_data/image_dataset_tmp.json", "w") as f:
        json.dump(image_data, f, indent=4, ensure_ascii=False)
        
        
# image_dataset_comp()

def replace_image_url():
    with open(f"./news_data/image_dataset_tmp.json", "r") as f:
        image_data = json.load(f)

    for image in image_data:
        image["image_url"] = image["image_url"].replace("./images", "static/images")
                
    with open(f"./news_data/image_dataset_tmp.json", "w") as f:
        json.dump(image_data, f, indent=4, ensure_ascii=False)
        
    for year in range(2009, 2020):
        with open(f"./news_data/{year}/key_moments_photos_{year}.json", "r") as f:
            articles_data = json.load(f)
        
        for article in articles_data:
            article["image_url"] = article["image_url"].replace("./images", "static/images")
        
        with open(f"./news_data/{year}/key_moments_photos_{year}.json", "w") as f:
            json.dump(articles_data, f, indent=4, ensure_ascii=False)
    
# replace_image_url()