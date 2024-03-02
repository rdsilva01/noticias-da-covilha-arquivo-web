# main.py
import time

from DataExtraction import get_news_data
from DataExtraction import get_news_url_dataset

from DataValidation import data_validation
from DataValidation import url_validation

# URL EXTRACTION
'''
start_time = time.time()
get_news_url_dataset.get_news_url_dataset(s_year=2019, e_year=2019, url="https://noticiasdacovilha.pt/" ,debug=True)
end_time = time.time()
execution_time = end_time - start_time 
print(f"URL Extraction execution time: {execution_time/60:.2f} minutes")
'''

'''
# URL VALIDATION
start_time = time.time()
url_validation.url_validation(s_year=2009, e_year=2019)
end_time = time.time()
execution_time = end_time - start_time 
print(f"URL Validation execution time: {execution_time/60:.2f} minutes")
'''

# DATA EXTRACTION
start_time = time.time()
get_news_data.get_news_data(s_year=2011, N=2, debug=True, demo=False)
end_time = time.time()
execution_time = end_time - start_time 
print(f"Data Extraction execution time: {execution_time/60:.2f} minutes")

