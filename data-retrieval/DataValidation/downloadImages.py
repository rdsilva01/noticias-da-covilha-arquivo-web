import json
import requests

def download_photo(url, file_path):
    ''' save the photos inside the images folder'''
    image_folder = "./images/"
    full_path = image_folder + file_path
    response = requests.get(url)
    if response.status_code == 200:
        with open(full_path, 'wb') as f:
            f.write(response.content)
        print("Photo downloaded successfully.")
    else:
        print("Failed to download photo.")

        
        
def main():
    for year in range(2019, 2020):
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/DataValidation/news_data/{year}/key_moments_photos_{year}_tmp_3.json', 'r') as f:
            data = json.load(f)
        
        for article in data:
            image_url = article['image_url']
            nid = article['nid']
            image_desc = article['image_desc']
            # if the image starts with static dont download
            if image_url and not image_url.startswith("static") and image_url != "no_image" and image_url != "":
                #download_photo(image_url, nid + ".jpg")
                print(nid + ".jpg downloaded.")
                image_url = "static/img/news_images/" + nid + ".jpg"
                article['image_url'] = image_url
                
        
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/DataValidation/news_data/{year}/key_moments_photos_{year}_tmp_4.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()