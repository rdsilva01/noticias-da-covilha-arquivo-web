from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import os
import json

app = Flask(__name__)

from datetime import datetime

def load_data_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return []

def get_news_front_page():
        directory = os.path.join(app.static_folder, 'news_data', '2011', 'capa_2011')
        json_file_path = os.path.join(directory, 'capa_2011.json')
        
        with open(json_file_path, 'r') as f:
            news_data = json.load(f)
        
        print(json.dumps(news_data, indent=4, ensure_ascii=False))
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

def get_news_by_id(article_id, year):
    dados = load_data(year)
    for article in dados:
        if article.get('id') == article_id:
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

@app.route('/news')
def news():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    news, total = paginacao(page, per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap5')
    return render_template('news.html', news=news, pagination=pagination)

@app.route('/news/article_id=<article_id>')
def news_item(article_id):
    year = request.args.get('year')
    news_item = get_news_by_id(article_id, year)

    if news_item:
        return render_template('news_item.html', news=news_item)
    else:
        return "Article not found"
    
@app.route('/news/year=<int:year>')
def news_per_year(year):
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    news, total = paginacao(page, per_page, year)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap5')
    return render_template('news_per_year.html', news=news, pagination=pagination, year=year)


def calculate_years_ago(date_str):
    first_date = datetime.strptime(date_str, "%Y-%m-%d")
    current_date = datetime.now()
    years_ago = current_date.year - first_date.year
    return years_ago

@app.template_filter('years_ago')
def years_ago(date_str):
    return calculate_years_ago(date_str)

@app.route('/')
def index():
    directory = os.path.join(app.static_folder, 'news_data', '2009', 'capa_2009')
    json_file_path = os.path.join(directory, 'custom_news.json')
    
    news_front_page = get_news_front_page()
    
    current_date = datetime.today()
    
    news_from_period = get_news_from_period()
    num_articles = len(news_from_period)
    return render_template('index.html', news=news_from_period, num_articles=num_articles, news_front_page=news_front_page, current_date = current_date)

if __name__ == '__main__':
    app.run(debug=True)
