from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import os
import json
from redis_search import get_search

app = Flask(__name__)

from datetime import datetime


def get_all_stats(s_year, e_year):
    stats_list = []
    for i in range(s_year, e_year+1):
        statistics_year = get_stats(i)
        stats_list.append(statistics_year)
        
    return stats_list

def get_redis_search(query):
    results = get_search(query)
    return results
   
def get_news_front_page(year):
        directory = os.path.join(app.static_folder, 'news_data', f'{year}', f'capa_{year}')
        json_file_path = os.path.join(directory, f'capa_{year}.json')
        
        with open(json_file_path, 'r') as f:
            news_data = json.load(f)
        
        return news_data

def get_today_date():
    today = datetime.now()
    
    current_year = today.year
    current_month = today.month
    current_day = today.day

    return current_month, current_day, current_year

def get_news_from_period():
    current_month, current_day, current_year = get_today_date()

    news_from_period = []
    for year in range(2009, 2020):
        news_data = load_data(year)

        news_from_period.extend([article for article in news_data if datetime.strptime(article['date'], '%Y-%m-%d').month == current_month and datetime.strptime(article['date'], '%Y-%m-%d').day in [current_day, current_day + 1]])
        news_from_period.extend([article for article in news_data if datetime.strptime(article['date'], '%Y-%m-%d').month == current_month and datetime.strptime(article['date'], '%Y-%m-%d').day in [current_day, current_day - 1]])


    return news_from_period


data_folder = os.path.join(app.root_path, 'static', 'news_data')
def load_data(year):
    file_path = os.path.join(data_folder, str(year), f'validated_{year}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return []
    
stats_data_folder = os.path.join(app.root_path, 'static', 'news_data')
def get_stats(year):
    file_path = os.path.join(stats_data_folder, str(year), f'statistics_{year}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {}
    
def get_news_by_id(article_id, year):
    dados = load_data(year)
    for article in dados:
        if article.get('nid') == article_id:
            return article
    return None


def get_news(offset=0, per_page=8, year=None):
    dados = load_data(year)
    return dados[offset: offset + per_page]


def paginacao(page, per_page=8, year=None):
    dados = load_data(year)
    total = len(dados)
    offset = (page - 1) * per_page
    return get_news(offset=offset, per_page=per_page, year=year), total

def paginacao_query(page, per_page=12, results=None):
    total, dados = results
    offset = (page - 1) * per_page
    # print(f"Total results: {total}")
    # print(f"Offset: {offset}")
    # print(f"Total documents: {len(dados)}")
    paginated_results = dados[offset: offset + per_page]
    # print(f"Paginated results: {paginated_results}")
    return paginated_results, total

def paginacao_capas(news_data, page, per_page=9):
    # Convert dictionary items to a list of tuples
    dados = list(news_data.items())
    total = len(dados)
    offset = (page - 1) * per_page
    return dados[offset: offset + per_page], total


@app.route('/capas')
def capas():
    all_news_data = {}
    for year in range(2009, 2016):
        news_data_year = get_news_front_page(year)
        all_news_data.update(news_data_year)
        
    page = int(request.args.get('page', 1))
    per_page = 9
    offset = (page - 1) * per_page
    
    current_page_results, total = paginacao_capas(page=page, per_page=per_page, news_data=all_news_data)
    pagination = Pagination(page=page, per_page=9, total=total, css_framework='bootstrap5')

    
    return render_template('capas.html', all_news_data=current_page_results, pagination=pagination)


@app.route('/pelacuriosidade')
def pelacuriosidade():
    query = request.args.get('query', '')
    results = get_redis_search(query=query)
    
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    current_page_results, total = paginacao_query(page=page, per_page=per_page, results=results)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    
    # Print debug information
    # print(f"Query: {query}")
    # print(f"Page: {page}")
    # print(f"Total pages: {pagination.total_pages}")
    # print(f"Total results: {total}")
    # print(f"Current page results: {current_page_results}")
    
    return render_template('query.html', results=current_page_results, pagination=pagination, query=query, total=total)


@app.route('/news')
def news():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    news, total = paginacao(page, per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    return render_template('news.html', news=news, pagination=pagination)


@app.route('/news/<article_id>')
def news_item(article_id):
    all_years = [str(year) for year in range(2009, 2020)] 
    for year in all_years:
        news_item = get_news_by_id(article_id, year)
        if news_item:
            return render_template('news_item.html', news=news_item)
    return render_template('404.html')


    
@app.route('/news/year=<int:year>')
def news_per_year(year):
    current_date = datetime.today()
    
    statistics_year = get_stats(year)
    
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    
    minimal_content = request.args.get('minimal_content', False)
    if minimal_content and minimal_content.lower() == 'true':
        minimal_content = True
    else:
        minimal_content = False

    news, total = paginacao(page, per_page, year)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap5')
    
    if year < 2020 and year > 2008:
        return render_template('news_per_year.html', news=news, pagination=pagination, year=year, current_date=current_date, news_total=total, minimal_content=minimal_content, statistics=statistics_year[f"{year}"])
    else:
        return render_template('404.html'), 404


def calculate_years_ago(date_str):
    first_date = datetime.strptime(date_str, "%Y-%m-%d")
    current_date = datetime.now()
    years_ago = current_date.year - first_date.year
    return years_ago

@app.template_filter('years_ago')
def years_ago(date_str):
    return calculate_years_ago(date_str)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/categoria/<categoria>')
def categoria(categoria):
    all_news = []
    curr_data = None
    for i in range(2009, 2020):
        curr_data = load_data(i)
        all_news.append(curr_data)
        
    news_in_category = [article for article in all_news if article.get('category') == categoria]
    # Pagination logic (similar to your existing routes)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(news_in_category)
    paginated_news = news_in_category[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')

    return render_template('categoria.html', news=paginated_news, pagination=pagination, categoria=categoria)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    directory = os.path.join(app.static_folder, 'news_data', '2009', 'capa_2009')
    json_file_path = os.path.join(directory, 'custom_news.json')
    
    stats_list = get_all_stats(2009, 2019)
    print(stats_list)
    
    news_front_page = get_news_front_page(2011)
    
    current_date = datetime.today()
    
    news_from_period = get_news_from_period()
    num_articles = len(news_from_period)
    return render_template('index.html', news=news_from_period, num_articles=num_articles, news_front_page=news_front_page, current_date = current_date, stats_list = stats_list)

if __name__ == '__main__':
    app.run(debug=True)
