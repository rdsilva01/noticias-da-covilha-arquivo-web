# main.py
import time

from DataExtraction import get_news_data
from DataExtraction import get_news_url_dataset

from DataValidation import data_validation
from DataValidation import url_validation


# URL EXTRACTION
def url_extraction_fun():
    start_time = time.time()
    get_news_url_dataset.get_news_url_dataset(s_year=2019, e_year=2019, url="https://noticiasdacovilha.pt/" ,debug=True)
    end_time = time.time()
    execution_time = end_time - start_time 
    print(f"URL Extraction execution time: {execution_time/60:.2f} minutes")

# URL VALIDATION
def url_validation_fun():
    start_time = time.time()
    url_validation.url_validation(s_year=2009, e_year=2019)
    end_time = time.time()
    execution_time = end_time - start_time 
    print(f"URL Validation execution time: {execution_time/60:.2f} minutes")

# DATA EXTRACTION
def data_extraction_fun():
    start_time = time.time()
    get_news_data.get_news_data(s_year=2009, e_year=2019, debug=True, demo=False)
    end_time = time.time()
    execution_time = end_time - start_time 
    print(f"Data Extraction execution time: {execution_time/60:.2f} minutes")

# DATA VALIDATION
def data_validation_fun():
    start_time = time.time()
    data_validation.data_validation(s_year=2009, e_year=2019)
    end_time = time.time()
    execution_time = end_time - start_time 
    print(f"Data Validation execution time: {execution_time/60:.2f} minutes")
    
def menu():
    print("MENU")
    print("1 - URL EXTRACTION")
    print("2 - URL VALIDATION")
    print("3 - DATA EXTRACTION")
    print("4 - DATA VALIDATION")
    numbers_input = input("Choose the numbers that match the functions (separated by spaces): ")
    numbers_list = numbers_input.split()
    numbers = [int(num) for num in numbers_list]
    return numbers

def main():
    options = menu()
    if not options:
        print("NO OPTIONS CHOSEN")
    else:
        for option in options:
            if option == 1:
                url_extraction_fun()
            elif option == 2:
                url_validation_fun()
            elif option == 3:
                data_extraction_fun()
            elif option == 4:
                data_validation_fun()
            else:
                print(f"INVALID OPTION: {option}")

if __name__ == "__main__":
    main()