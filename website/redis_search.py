import json
import redis
from redis.commands.search.field import TextField, NumericField
from redis_service import connect_redis, create_index, index_documents, drop_data
from redis.commands.search.query import Query

def convert_lists_to_strings(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if value is None:
                new_data[key] = ""  # Replace None with empty string
            elif isinstance(value, list):
                new_data[key] = " ".join(value)
            elif isinstance(value, dict):
                new_data[key] = convert_lists_to_strings(value)
            else:
                new_data[key] = value
        return new_data
    elif isinstance(data, list):
        new_list = []
        for item in data:
            new_list.append(convert_lists_to_strings(item))
        return new_list
    else:
        return data

    
def get_search(query, page=1, per_page=8, s_year=2009, e_year=2019):
    search_results = []

    # Define variables
    index_name = 'idx:nc'  # the name of the index
    fields = [TextField(name="url"), TextField(name="title"), TextField(name="content")]

    r = connect_redis()
    create_index(r, index_name, "", fields)  # Create index without any prefix initially
    
    # Load and index data for all years
    for year in range(s_year, e_year + 1):
        doc_prefix = f'nc_news:{year}'  # Prefix for the document keys
        with open(f"static/news_data/{year}/validated_{year}.json", "r", encoding="utf8") as readfile:
            key_moments = json.load(readfile)

        key_moments = convert_lists_to_strings(key_moments)
        index_documents(r, doc_prefix, key_moments)  # Index data for the current year with its prefix

    # Search through all prefixes
    for year in range(s_year, e_year + 1):
        doc_prefix = f'nc_news:{year}'
        results = r.ft(index_name).search(Query(f'@content:{query}'))
        print(results)
        search_results.extend(results.docs)

    # Remove duplicates
    results = r.ft(index_name).search(Query(f'@content:{query}'))
    print(search_results)

    return results.total, results

def get_search(query, page=1, per_page=8):
    # Define variables
    index_name = 'idx:nc'  # the name of the index

    r = connect_redis()
    
    # Search the index for the query
    results = r.ft(index_name).search(Query(f'@content:{query}').paging(0, 10000))

    

    return results.total, results.docs



