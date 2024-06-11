from datetime import datetime, timedelta
import json
import time
import redis
from redis.commands.search.field import TextField, NumericField
from redis_service import connect_redis, create_index, index_documents, drop_data
from redis.commands.search.query import Query
from cleantext import clean 

index_name = 'idx:news'
r = connect_redis()

# para obter a última newsletter (que vai ser apresentada por defeito)
def get_last_newsletter():
    index_name = 'idx:newsletter'
    query = '*'
    try:
        # Perform the search to get the latest newsletter
        result = r.execute_command('FT.SEARCH', index_name, query, 'SORTBY', 'data', 'DESC', 'LIMIT', '0', '1')
        
        if len(result) <= 1:
            return {}

        # Parse the result
        doc_id = result[1]
        fields = result[2]

        # Convert the list of fields into a dictionary
        field_dict = {fields[i]: fields[i + 1] for i in range(0, len(fields), 2)}

        return {
            "key": doc_id,
            "date": field_dict.get("date"),
            "nids": field_dict.get("nids"),
            "capaId": field_dict.get("capaId")
        }
    except redis.exceptions.ResponseError as e:
        # print("Error executing RediSearch query:", e)
        return {}


# para obter as newsletters por data
def get_newsletter_by_date(date):
    key_prefix = 'newsletter_item'
    key = f'{key_prefix}:{date}'
    try:
        result = r.hgetall(key)
        if not result:
            return {}  
    except redis.exceptions.ResponseError as e:
        return {}

    return {
        "date": result.get("date"),
        "nids": result.get("nids"),
        "capaId": result.get("capaId")
    }

def save_email_redis(email, token, active):
    key = f"newsletter_email:{email}"
    r.hset(key, mapping={'email': email, 'token': token, 'active': active})
    print(f"Email {email} saved to Redis")
    
def get_email_redis(email):
    key = f"newsletter_email:{email}"
    email_data = r.hgetall(key)
    return email_data

def get_token_redis(token):
    query = f"*"
    print(token)
    results = r.ft('idx:emails').search(Query(query).paging(0, 3000))
    return results.docs

def activate_email(email):
    key = f"newsletter_email:{email}"
    r.hset(key, mapping={'active': 1})
    print(f"Email {email} activated")
    
def deactivate_email(email):
    key = f"newsletter_email:{email}"
    r.hset(key, mapping={'active': 0})
    print(f"Email {email} deactivated")


def get_news_year_sub_category(year, category, subcategory):
    index_name = 'idx:news'
    query = f'@date:{year} @category:{category} @sub_category:{subcategory}'
   
    try:
        results = r.ft(index_name).search(Query(query).paging(0, 3000))
    except redis.exceptions.ResponseError as e:
        print("Error executing RediSearch query:", e)
        return [] 

    print(f"Results from sub category {subcategory}: {results.total}") 
        
    return results.docs

def get_news_year_category(year, category):
    index_name = 'idx:news'
    query = f'@date:{year} @category:{category}'
   
    try:
        results = r.ft(index_name).search(Query(query).paging(0, 3000))
    except redis.exceptions.ResponseError as e:
        print("Error executing RediSearch query:", e)
        return [] 

    print(f"Results from category {category}: {results.total}") 
        
    return results.docs


def get_news_25_abril():
    query_nids = ["2010-232", "2011-313", "2013-35", "2014-30", "2014-54", "2015-6", "2018-30", "2019-207", "2019-319"]
    all_docs = []
    for year in range(2009, 2020):
        if year == 2010 or year == 2011 or year == 2013 or year == 2014 or year == 2015 or year == 2018 or year == 2019:
            year_doc = get_news_year(year)
            for article in year_doc:
                if article.nid in query_nids:
                    all_docs.append(article)

    print(f"Total results from query 25 de abril:", len(all_docs)) 
        
    return all_docs

def get_news_nid(nid):
    year, numeric_id = nid.split('-')
    key = f'nc_news:{year}{numeric_id}'
    print(key)
    index_name = 'idx:news'
    
    try:
        results = r.ft(index_name).search(Query(f'@__key:{key}').paging(0, 3000))
        print(f"NID: {nid}: {results.docs}")
        print(f"Total results found for NID {nid}: {results.total}") 
        return results.docs
    except redis.exceptions.ResponseError as e:
        print("Error executing RediSearch query:", e)
        return []
    
def get_news_year(year):
    index_name = 'idx:news'
    query = f'@date:{year}'

    try:
        results = r.ft(index_name).search(Query(query).paging(0, 3000))
    except redis.exceptions.ResponseError as e:
        print("Error executing RediSearch query:", e)
        return [] 

    print(f"Results from year {year}:", results.total) 
        
    return results.docs

def get_all_news():
    index_name = 'idx:news'
    all_results = []
    for year in range(2009, 2021):
        query = f'@date:{year}'
        try:
            results = r.ft(index_name).search(Query(query).paging(0, 3000))
            all_results.extend(results.docs)
            print(f"Results from year {year}:", results.total)
        except redis.exceptions.ResponseError as e:
            print("Error executing RediSearch query:", e)
            return []
    print("Total results from all years:", len(all_results))
    return all_results

def get_search_author(author):
    index_name = 'idx:news'
    query = f'@author:{author}'
    try:
        results = r.ft(index_name).search(Query(query).paging(0, 3000))
    except redis.exceptions.ResponseError as e:
        print("Error executing RediSearch query:", e)
        return [] 

    print(f"Results from author {author}:", results.total) 
        
    return results.total, results.docs

def get_search_capas(query, start_year, end_year):
    query_string = ''
    words = query.strip('|').split()

    if len(words) == 1:
        query_string += f'"{query}" '
    else:
        query_string += f'{query} '

    # # Performing the search with the constructed query string
    # results = r.ft("idx:capas").search(Query("*").paging(0, 3000))
    # total = results.total
    # for i in range(int(start_year[1]), int(end_year[1])+1):
    #     query_string += f"@data:{i}|"    
    query_string += "@attributes" + f':{query} '
    query_string = query_string.rstrip('|')
    
    #query_string = f"@date:2009 @date:2010 @date:2011 @date:2012 @date:2013 @date:2014 @date:2015 @content:{query}"
    
    results = r.ft("idx:capas").search(Query(query_string).paging(0, 3500))
    
    # Filter documents to include only those with the "nc_capas" prefix
    nc_capas_documents = [doc for doc in results.docs if doc['id'].startswith('nc_capas')]
    
    # after filtering, sort by data (that is date)
    # nc_filtered_docs = sorted(nc_capas_documents, key=lambda x: x['data'])

    total = len(nc_capas_documents)
    return total, nc_capas_documents

def get_capas_per_year(year):
    query_string = f"@data:{year}"
    
    results = r.ft("idx:capas").search(Query(query_string).paging(0, 3500))
    
    # Filter documents to include only those with the "nc_capas" prefix
    nc_capas_documents = [doc for doc in results.docs if doc['id'].startswith('nc_capas')]
    
    # after filtering, sort by data (that is date)
    nc_filtered_docs = sorted(nc_capas_documents, key=lambda x: x['data'])

    total = len(nc_filtered_docs)
    return total, nc_filtered_docs


def get_capas_this_week():
    current_date = datetime.today()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    capas_this_week = []
    
    for year in range(2009, 2020):
        query_string = f"@data:{year}"
        
        results = r.ft("idx:capas").search(Query(query_string).paging(0, 3500))
        
        nc_capas_documents = [doc for doc in results.docs if doc['id'].startswith('nc_capas')]
        
        for doc in nc_capas_documents:
            try:
                doc_date = datetime.strptime(doc['data'], '%Y-%m-%d')
            except ValueError:
                # Skip this document if the date format is incorrect
                # print(f"Document {doc['id']} has an invalid date format: {doc['data']}")
                continue
            
            if start_of_week <= doc_date <= end_of_week:
                # print(doc)
                capas_this_week.append(doc)
    
    # Count the total number of capas documents from this week
    total = len(capas_this_week)
    # print("TOTAL  DE CAPAS DESTA SEMANA: ", total)
    
    return total, capas_this_week



def get_all_capas():
    query_string = ''
        
    for i in range(2009, 2019):
        query_string += f"@data:{i}|"    
    query_string = query_string.rstrip('|')
    
    results = r.ft("idx:capas").search(Query(query_string).paging(0, 3500))
    
    # Filter documents to include only those with the "nc_capas" prefix
    nc_capas_documents = [doc for doc in results.docs if doc['id'].startswith('nc_capas')]
    
    # after filtering, sort by data (that is date)
    nc_filtered_docs = sorted(nc_capas_documents, key=lambda x: x['data'])

    total = len(nc_filtered_docs)
    return total, nc_filtered_docs


def get_search_image(query, exact_match, start_date, end_date):
   
    # Construct search query
    search_options = {
        'image_desc': "1",
        'news_title': "1",
        'news_subtitle': "1",
        'news_content': "1",
        'spacy': "1"
    }

    count = 0
    
    # Construct query string for Redisearch
    query_string = '@'
    for key, value in search_options.items():
        if value == "1":
            count += 1
            query_string += f'{key}|'
   
    # Verify if the query is a single word or more
    words = query.strip('|').split()

    if len(words) == 1:
        if exact_match[1] == "1":
            query_string = query_string.rstrip('|') + f':"{query}" '
        else:
            query_string = query_string.rstrip('|') + f':{query} '
    else:
        if exact_match[1] == "1":
            query_string = query_string.rstrip('|') + f':"{query}" '
        else:
            query_string = query_string.rstrip('|') + f':{query} '

    index_name = 'idx:images'
    # Execute Redisearch query
    results = r.ft(index_name).search(Query(query_string).paging(0, 3000))
    
    # remove the duplicates, by order, the first one is the one that stays
    unique_results = []
    unique_urls = []
    for doc in results.docs:
        if doc['image_desc'] not in unique_urls:
            unique_results.append(doc)
            unique_urls.append(doc['image_desc'])
            
    # return 
    return len(unique_results), unique_results


        
def date_to_unix_epoch(date_str):
    """Converts a date string in 'YYYY-MM-DD' format to UNIX Epoch timestamp."""
    print(date_str)
    return int(time.mktime(time.strptime(date_str, '%Y-%m-%d')))

def get_search_text(query, exact_match, start_date, end_date):
    
    # Convert start_date and end_date to UNIX Epoch timestamps
    start_timestamp = date_to_unix_epoch(start_date[1])
    end_timestamp = date_to_unix_epoch(end_date[1])
    
    print("Start Timestamp:", start_timestamp)
    print("End Timestamp:", end_timestamp)

    # Construct search query
    search_options = {
        'title': "1",
        'content': "1",
        'author': "1",
        'keyword': "1",
        'category': "1",
        'subcategory': "1",
    }

    count = 0
    
    # Construct query string for Redisearch
    query_string = '@'
    for key, value in search_options.items():
        if value == "1":
            count += 1
            query_string += f'{key}|'
            
    if count == 0:
        query_string = '@content|'

    words = query.strip('|').split()

    if len(words) == 1:
        if exact_match[1] == "1":
            query_string = query_string.rstrip('|') + f':"{query}" '
        else:
            query_string = query_string.rstrip('|') + f':{query} '
    else:
        if exact_match[1] == "1":
            query_string = query_string.rstrip('|') + f':"{query}" '
        else:
            query_string = query_string.rstrip('|') + f':{query} '
    

    # Execute Redisearch query
    results = r.ft(index_name).search(Query(query_string).paging(0, 3000))
    
    # Filter results by start_date and end_date
    filtered_results = []
    for doc in results.docs:
        try:
            # Ensure 'unix_epoch_time' field is accessible and contains expected value
            unix_epoch_time = int(doc['unix_epoch_time'])
            doc_date = datetime.fromtimestamp(unix_epoch_time).date()
            
            # Convert start_date and end_date to date objects
            start_date_obj = datetime.strptime(start_date[1], '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date[1], '%Y-%m-%d').date()
            
            # Compare dates
            if start_date_obj <= doc_date <= end_date_obj:
                filtered_results.append(doc)
        except (KeyError, ValueError):
            # Handle cases where 'unix_epoch_time' field is missing or not convertible to integer
            pass

    print(len(filtered_results))

    return len(filtered_results), filtered_results

