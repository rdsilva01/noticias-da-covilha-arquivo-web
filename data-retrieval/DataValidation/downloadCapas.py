import json
import os
import urllib.request

def get_capas():
    '''This function gets all the capas from a file and download them'''
    # Get all the capas
    capas = []
    for year in range(2019, 2020):
        with open(f'./news_data/{year}/capa_{year}/capa_{year}.json', 'r') as f:
            data = json.load(f)
        
        # Create a directory to save the capas if it doesn't exist
        save_dir = f'./news_data/capas2/'
        os.makedirs(save_dir, exist_ok=True)
        
        # Download the capas to the "capas" directory
        for date, info in data.items():
            capa_url = info['url']
            filename = f"{date}.jpg"  # Save with the date as the filename
            filepath = os.path.join(save_dir, filename)
            urllib.request.urlretrieve(capa_url, filepath)
            capas.append(filepath)
            print(date)
    
    return capas

# Example usage:
downloaded_capas = get_capas()
print("Downloaded capas:", downloaded_capas)
