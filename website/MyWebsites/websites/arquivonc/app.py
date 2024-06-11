import uuid
from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_args
import os
import json
from redis_search import get_all_capas, get_all_news, get_capas_per_year, get_news_year, get_news_year_category, get_news_year_sub_category, get_search_author, get_search_image, get_search_text, get_news_25_abril, get_search_capas, save_email_redis, get_email_redis, get_token_redis, activate_email, deactivate_email, get_last_newsletter, get_newsletter_by_date
from app_newsletter import send_email
import random
from datetime import datetime, timedelta
from flask_cors import CORS

def main():
    """The main function for this script."""
    app.run(host='0.0.0.0', port='443', debug=True)
    CORS(app)

app = Flask(__name__)

arrow_left_big = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-left-fill" viewBox="0 0 16 16"> <path d="m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z"/></svg>'
arrow_right_big = ' <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-right-fill" viewBox="0 0 16 16"><path d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"/></svg>'
arrow_left_small = '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" fill="currentColor" class="bi bi-caret-left-fill" viewBox="0 0 16 16"> <path d="m3.86 8.753 5.482 4.796c.646.566 1.658.106 1.658-.753V3.204a1 1 0 0 0-1.659-.753l-5.48 4.796a1 1 0 0 0 0 1.506z"/></svg>'
arrow_right_small = ' <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" fill="currentColor" class="bi bi-caret-right-fill" viewBox="0 0 16 16"><path d="m12.14 8.753-5.482 4.796c-.646.566-1.658.106-1.658-.753V3.204a1 1 0 0 1 1.659-.753l5.48 4.796a1 1 0 0 1 0 1.506z"/></svg>'


@app.route('/politicadeprivacidade', methods=['GET'])
def politica():
    return render_template('politica.html')

@app.route('/newsletter', methods=['GET'])
def newsletter():
    newsletter = request.args.get('id', '0')
    data = request.args.get('data', None)
    
    if data:
        content = get_newsletter_by_date(data)
        # content is a dict
        capa = content.get('capaId', None)
        noticias = content.get('nids', None)
        # split the noticias by ,
        noticias_list = noticias.split(',')
        # get the news articles for each nid
        news_articles = []
        for nid in noticias_list:
            news = get_news_by_id(nid, int(nid.split('-')[0]))
            if news:
                news_articles.append(news)
        
        # get the year
        year = capa.split('-')[0]
        current_date_time = datetime.now()
        current_year = current_date_time.year
        year_dif = current_year - int(year)
        year_formatted = f"{year_dif} anos" if year != current_date_time.year else "1 ano"
    
        month_list = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
        month_formatted = month_list[int(capa[5:7]) - 1]
        data_text_formatted = "Dia " + capa[8:] + " de " + month_formatted + " de " + capa[0:4]
        
        return render_template('newsletter_antiga.html', noticias=noticias_list, capa=capa, year=year_formatted, data_text_formatted=data_text_formatted, news_articles=news_articles)
        
    if newsletter == '1':
        return render_template('newsletter_exemplo.html')
    else:
        content = get_last_newsletter()
        print(content)
        # get the date of the newsletter
        last_newsletter = content.get('key', None)
        # split the newsletter_item:xxxx
        last_newsletter = last_newsletter.split(':')
        last_newsletter = last_newsletter[1]
        
        return render_template('newsletter.html', last_newsletter=last_newsletter)

@app.route('/register', methods=['GET'])
def register():
    token = str(uuid.uuid4())

    email = request.args.get('email')
    
    # verify if the email already exists
    email_exists = get_email_redis(email)
    if email_exists:
        if email_exists['active'] == 1 or email_exists['active'] == '1':
            return render_template('already_registered.html')
        

    save_email_redis(email, token, active=0)

    # Create a confirmation URL
    #confirm_url = url_for('confirm_email', token=token, _external=True)
    confirm_url="https://arquivonc.ubi.pt/arquivonc/confirmar?token=" + token
    
    subject = 'Confirme a subscrição da Newsletter do ArquivoNC'
    body = f'Por favor, clique no link para confirmar a subscrição: {confirm_url}'
    sender = 'newsletter.arquivonc@ubi.pt'
    recipients = [email]
    password = 'tphlrnczbyryrntn'
    html = f"""
    <html>
    <body>
        <p>Por favor, clique no link para confirmar a subscrição da newsletter do ArquivoNC - O arquivo web do Notícias da Covilhã:<br>
        <a href="{confirm_url}">{confirm_url}</a></p>
    </body>
    </html>
    """
    
    send_email(subject, body, sender, recipients, password, html=html)

    # Render a template for the "Thanks for registering" page and pass the email as a context variable
    return render_template('thanks.html', email=email)

@app.route('/confirmar', methods=['GET'])
def confirm_email():
    token = request.args.get('token')
    email = None
    redis_token = get_token_redis(token)
    
    if redis_token:
        for doc in redis_token:
            if doc['token'] == token:
                email = doc['email']
                active = doc['active']
                break
        
    if email is None:
        #flash('Invalid or expired token.', 'danger')
        return render_template('invalid_token.html')
    
    if active == 1 or active == '1':
        return render_template('already_activated.html')

    else:
        activate_email(email)
    
    #flash('Your account has been activated!', 'success')
    return render_template('activated.html')

@app.route('/remover', methods=['GET'])
def unsubscribe():
    token = request.args.get('token')
    email = None
    redis_token = get_token_redis(token)
    
    if redis_token:
        for doc in redis_token:
            if doc['token'] == token:
                email = doc['email']
                active = doc['active']
                break
        
    if email is None:
        return render_template('invalid_token.html')
    
    if active == 0 or active == '0':
        return render_template('invalid_token.html')

    else:
        deactivate_email(email)
    return render_template('deactivated.html')


@app.route('/index')
def home():
    current_date_time = datetime.now()
    
    stats_list = get_all_stats(2009, 2019)
    content_stats_list = get_all_content_stats(2009, 2019)
    
    total_capas = 0
    capas_per_day = []

    for year in range(2009, 2020):
        per_year = 0
        tmp_total_capas, tmp_capas_per_day = get_capas_per_year(year)
        for capa in tmp_capas_per_day:
            capa_date = datetime.strptime(capa['data'], '%Y-%m-%d')
            current_date = datetime(year, current_date_time.month, current_date_time.day)  # Set the current date to the capa's date
            week_ago = current_date - timedelta(days=7)
            while current_date >= week_ago:
                date_key = current_date.strftime('%Y-%m-%d')
                if date_key == capa['data'] and per_year == 0:
                    capas_per_day.append(capa)
                    total_capas += 1
                    per_year += 1
                    break 
                current_date -= timedelta(days=1)
                

    print("Total de Capas: ", total_capas)
    print("TOTAL DE CAPAS:", total_capas)
    
    news_from_period = get_news_from_period_redis()
    main_news_len = len(news_from_period)
   # print(main_news_len)
    num_articles = main_news_len # redundant, need to remove
    
    news_from_25_abril = get_news_25_abril()
    # news_from_25_abril = news_from_25_abril[:10]
    news_from_25_abril.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
    news_from_25_abril_len = len(news_from_25_abril)

    
    if main_news_len == 0:
        news_from_period = get_news_from_period_redis(week=True)
        main_news_len = len(news_from_period)
        num_articles = main_news_len # redundant, need to remove
        
    random_index = random.randint(0, num_articles - 1)
    
    return render_template('index.html', news=news_from_period, news_front_page_this_week = capas_per_day, total_capas = total_capas, main_news_len = main_news_len, num_articles=num_articles, current_date = current_date, stats_list = stats_list, content_stats_list=content_stats_list,random_index=random_index, news_25_abril = news_from_25_abril, news_25_abril_len = news_from_25_abril_len) # news_front_page=news_front_page


def get_all_content_stats(s_year, e_year):
    content_stats_list = []
    for i in range(s_year, e_year+1):
        statistics_year = get_content_stats(i)
        content_stats_list.append(statistics_year)
        
    return content_stats_list

content_stats_data_folder = os.path.join(app.root_path, 'static', 'news_data')
def get_content_stats(year):
    file_path = os.path.join(stats_data_folder, str(year), f'content_statistics_{year}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

def get_all_stats(s_year, e_year):
    stats_list = []
    for i in range(s_year, e_year+1):
        statistics_year = get_stats(i)
        stats_list.append(statistics_year)
        
    return stats_list

# REDIS
def get_redis_search(query, **kwargs):
    search_mode = kwargs.get('search_mode', 'text')
    exact_match = kwargs.get('exact_match', "0")
    start_date = kwargs.get('start_date', "2009-01-01")
    end_date = kwargs.get('end_date', "2019-12-31")
    
    if search_mode == 'text':
        return get_search_text(query, ("exact_match", exact_match), ("start_date", start_date), ("end_date", end_date))
     
    elif search_mode == 'imagens':
        return get_search_image(query, ("exact_match", exact_match), ("start_date", start_date), ("end_date", end_date))
    
    elif search_mode == 'capas':
        return get_search_capas(query, ("start_date", start_date), ("end_date", end_date))
    
    
def get_news_from_period_redis(week=False):
    current_date = datetime.now()
    yesterday_date = current_date - timedelta(days=1)
    current_month, current_day, current_year = current_date.month, current_date.day, current_date.year
    yesterday_month, yesterday_day, yesterday_year = yesterday_date.month, yesterday_date.day, yesterday_date.year

    max_articles_per_year = 2
    news_from_period = []
    articles_loaded_per_year = {}

    if week:
        for year in range(2009, 2020):
            if year not in articles_loaded_per_year:
                articles_loaded_per_year[year] = 0

            news_data = get_news_year(year)

            for article in news_data:
                article_date = datetime.strptime(article['date'], '%Y-%m-%d')
                for i in range(7):
                    yesterday_date = current_date - timedelta(days=i)
                    yesterday_month, yesterday_day, yesterday_year = yesterday_date.month, yesterday_date.day, yesterday_date.year
                    if (article_date.month == current_month and article_date.day == current_day) or (article_date.month == yesterday_month and article_date.day == yesterday_day):
                        if articles_loaded_per_year[year] < max_articles_per_year:
                            news_from_period.append(article)
                            articles_loaded_per_year[year] += 1

        # Sort news articles by date
        news_from_period.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

        return news_from_period
    else:
        for year in range(2009, 2020):
            if year not in articles_loaded_per_year:
                articles_loaded_per_year[year] = 0

            news_data = get_news_year(year)

            for article in news_data:
                article_date = datetime.strptime(article['date'], '%Y-%m-%d')
                if (article_date.month == current_month and article_date.day == current_day) or (article_date.month == yesterday_month and article_date.day == yesterday_day):
                    if articles_loaded_per_year[year] < max_articles_per_year:
                        news_from_period.append(article)
                        articles_loaded_per_year[year] += 1

        # Sort news articles by date
        news_from_period.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

        return news_from_period

def get_news_from_category_redis(category):
    news_from_category = []

    for year in range(2009, 2020):
        news_data = get_news_year_category(year, category)
        news_from_category.extend(news_data)

    return news_from_category

def get_news_from_sub_category_redis(category, subcategory):
    news_from_sub_category = []

    for year in range(2009, 2020):
        news_data = get_news_year_sub_category(year, category, subcategory)
        news_from_sub_category.extend(news_data)

    return news_from_sub_category

def get_all_capas_redis():
    total, capas = get_all_capas()
    
    return total, capas

def get_news_front_page_per_month_match(day, month):
    directory = os.path.join(app.static_folder, 'news_data')
    filtered_data = {}

    for year in range(2009, 2020):
        year_directory = os.path.join(directory, str(year), f'capa_{year}')
        json_file_path = os.path.join(year_directory, f'capa_{year}.json')
        
        if not os.path.exists(json_file_path):
            continue
        
        with open(json_file_path, 'r') as f:
            news_data = json.load(f)
        
        current_date = datetime(year, month, day)
        week_ago = current_date - timedelta(days=14)
        
        while current_date >= week_ago:
            date_key = current_date.strftime('%Y-%m-%d')
            if date_key in news_data:
                filtered_data[date_key] = news_data[date_key]
                break  # Found news for this date, move to next year
            current_date -= timedelta(days=1)
    
    return filtered_data


def get_news_front_page_per_month(year, month):
    directory = os.path.join(app.static_folder, 'news_data', str(year), f'capa_{year}')
    json_file_path = os.path.join(directory, f'capa_{year}.json')
        
    with open(json_file_path, 'r') as f:
        news_data = json.load(f)
    
    filtered_data = {}
    for date_key, data in news_data.items():
        news_year, news_month, _ = date_key.split('-')
        if int(news_year) == year and int(news_month) == month:
            filtered_data[date_key] = data
    
    sorted_data = dict(sorted(filtered_data.items()))
    
    return sorted_data

def get_today_date():
    today = datetime.now()
    
    current_year = today.year
    current_month = today.month
    current_day = today.day

    return current_month, current_day, current_year


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
    dados = get_news_year(year)

    for article in dados:
        if article.nid == article_id:
            return article
    return None


def get_news(offset=0, per_page=8, year=None):
    dados = get_news_year(year)
    dados.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
    return dados[offset: offset + per_page]

def paginacao_generic(data, page, per_page=8):
    total = len(data)
    offset = (page - 1) * per_page
    # data.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
    return data[offset: offset + per_page], total

def paginacao(page, per_page=8, year=None, order_by="oldest"):
    if order_by == "newest":
        dados = get_news_year(year)
        dados.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    elif order_by == "oldest":
        dados = get_news_year(year)
        dados.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
    else:
        dados = get_news_year(year)
        
    total = len(dados)
    offset = (page - 1) * per_page
    return get_news(offset=offset, per_page=per_page, year=year), total

def paginacao_query(page, per_page=12, order_by="best_match", btnoption="text", results=None):
    total, dados = results
    if order_by == "best_match":
        dados = dados
    elif order_by == "oldest":
        if btnoption == 'text':
            dados.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        elif btnoption == 'imagens':
            dados.sort(key=lambda x: datetime.strptime(x['news_date'], '%Y-%m-%d'))
        elif btnoption == 'capas':
            dados.sort(key=lambda x: datetime.strptime(x['data'], '%Y-%m-%d'))
            
    elif order_by == "newest":
        if btnoption == 'text':
            dados.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        elif btnoption == 'imagens':
            dados.sort(key=lambda x: datetime.strptime(x['news_date'], '%Y-%m-%d'), reverse=True)
        elif btnoption == 'capas':
            dados.sort(key=lambda x: datetime.strptime(x['data'], '%Y-%m-%d'), reverse=True)

    offset = (page - 1) * per_page
    paginated_results = dados[offset: offset + per_page]
    # print(f"Paginated results: {paginated_results}")
    return paginated_results, total

def paginacao_capas(news_data, page, per_page=9):
    # Convert dictionary items to a list of tuples
    dados = news_data
    total = len(dados)
    offset = (page - 1) * per_page
    return dados[offset: offset + per_page], total

@app.route('/autores')
def authors():
    
    # receive the name of the author
    author = request.args.get('nome')
    order_by = request.args.get('order_by', 'oldest')
    
    # ARR, Ana Ribeiro Rodrigues/Joao Alves
    # Ana Ribeiro Rodrigues: Ana Robeiro Rodrigues, Ana Ribiero Rodrigues, ARR
    # João Miguel Alves: João Alves, JA, João Alves, com RCB
    # Rui Delgado:
    # JA/Rui Delgado:

    # Alexandre Salgueiro   
    # Alberto Alçada Rosa
    # Ana Rita Pinto: Ana Rito Pinto
    # António Pinto Pires: Pinto Pires,
    # António Rodrigues de Assunção
    # Assunção Vaz Patto: A.Vaz Patto
    # Avelino Gonçalves
    # José Ayres de Sá: Ayres de Sá
    # Carlos Madaleno
    # Carlos Pinto
    # Cristela Bairrada
    # D. Manuel Felício: (Manuel Felício, Bispo da Guarda), (D. Manuel Felício, Bispo da Guarda)
    # Eduardo Alves
    # Filipe Pinto
    # Francisco Rodrigues S.J.
    # João Cunha
    # João de Jesus Nunes
    # João Filipe Pereira
    # João Morgado
    # João Santos
    # Joaquim Paulo Serra: Paulo Serra
    # Jorge Saraiva
    # José Gameiro
    # José Pinheiro Fonseca
    # José Rodrigues Pires Manso: J.R. Pires Manso, Pires Manso, José R. Pires Manso
    # José Vincente Ferreira
    # Luis Fiadeiro
    # Maria Eduarda Ribeiro
    # Neuza Correia
    # Paulo Antunes
    # Paulo Neves
    # Pedro Ferreira
    # Ricardo Cocchi
    # Rui Delgado
    # Rui Manique
    # Sérgio Gaspar Saraiva: Sergio Saraiva, Sergio Gaspar Saraiva, Sérgio Saraiva
    # Susana Garrido
    # Susana Proença
    # Tiago Serrão
    # Vítor Pereira
    # Vitor Pinho
    
    minimal_content = request.args.get('minimal_content', False)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    
    if author:
        
         # open the file to get the authors
        with open('static/news_data/author3.json', 'r') as f:
            authors = json.load(f)
            
        file_name = None
        for i,author_name in enumerate(authors):
            if author_name == author:
                file_name = f"{i}.jpeg"
                break
        
        if minimal_content == False or minimal_content == 'false':
            href=f'/arquivonc/autores?nome={author}&order_by={order_by}&page=' + '{0}'
        else:
            href=f'/arquivonc/autores?nome={author}&order_by={order_by}&page='+ '{0}'

        total, news_data = get_search_author(author)
        
        if order_by == "newest":
            news_data.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        else:
            news_data.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
            
        order_by_href = f'/arquivonc/autores?nome={author}&page=1&order_by='
        per_page = 12
        news, total = paginacao_generic(page=page, per_page=per_page, data=news_data)
        
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap5', href=href, bs_version = 5, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>")
        small_pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap5', href=href, bs_version = 5, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>", link_size='sm')
        
        
        return render_template('author.html', news=news, news_total=total, pagination=pagination, small_pagination=small_pagination, minimal_content=minimal_content, author=author, file_name=file_name, order_by_href=order_by_href, order_by=order_by)
    
    else:
        # open the file to get the authors
        with open('static/news_data/author3.json', 'r') as f:
            authors = json.load(f)
            
        total = len(authors)
        
        # create a list of tuples (author name, image)
        authors_list = []
        for i,author in enumerate(authors):
            author, image = (author, f"{i}.jpeg")
            authors_list.append((author, image))
        
        per_page = 12
        authors, total = paginacao_generic(page=page, per_page=per_page, data=authors_list)
        href=f'/arquivonc/autores?page='+ '{0}'
        
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap5', href=href, bs_version = 5, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> autores</p>")
        
        small_pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap5', href=href, bs_version = 5, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> autores</p>", link_size='sm')
        
        return render_template('all_authors.html', authors=authors, total=total, pagination=pagination, small_pagination=small_pagination)
    
        # # authors is a dict with the author's name as the key and the image name as the value
        # with open('static/news_data/authors.json', 'r') as f:
        #     authors = json.load(f)
            
        # total = len(authors)
        
        # # create a list of tuples (author name, image)
        # author_list = [(k, v) for k, v in authors]
        # print(author_list)
        
        # # Create a dictionary to store names by first letter
        # # authors_dict = {}

        # # # Iterate through the list of authors
        # # for author in authors:
        # #     if author == 'D. Manuel Felício':
        # #         author = 'Manuel Felício'
        # #     # Get the first letter of the author's name
        # #     first_letter = author[0].upper()
            
        # #     # Check if the first letter is already a key in the dictionary
        # #     if first_letter not in authors_dict:
        # #         authors_dict[first_letter] = []
            
        # #     authors_dict[first_letter].append(author)

        # # # Sort the names within each letter group
        # # for key in authors_dict:
        # #     authors_dict[key].sort()

        # # print(authors_dict)
                
        # # per_page = 12
        # authors, total = paginacao_generic(page=page, per_page=per_page, data=author_list)
        # href=f'/arquivonc/autores?page='+ '{0}'
        
        # pagination = Pagination(page=page, per_page=per_page, total=total,
        #                         css_framework='bootstrap5', href=href, bs_version = 5, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> autores</p>")
        
        # small_pagination = Pagination(page=page, per_page=per_page, total=total,
        #                         css_framework='bootstrap5', href=href, bs_version = 5, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> autores</p>", link_size='sm')
        
        # return render_template('all_authors.html', authors=authors, total=total, pagination=pagination, small_pagination=small_pagination)
        # # return render_template('all_authors.html', authors_list=authors_dict, total=total)


@app.route('/capas')
def capas_per_year():
    year = request.args.get('ano')
    order_by = request.args.get('order_by', 'oldest')
    
    if year:
        if int(year) < 2009 or int(year) > 2019:
            return render_template('notfound.html'), 404
        else:
            total, all_news_data = get_capas_per_year(int(year))
            num_capas = total

            page = int(request.args.get('page', 1))
            per_page = 18
            offset = (page - 1) * per_page

            if order_by == "newest":
                all_news_data.sort(key=lambda x: datetime.strptime(x['data'], '%Y-%m-%d'), reverse=True) 
            else:
                all_news_data.sort(key=lambda x: datetime.strptime(x['data'], '%Y-%m-%d'))
                
            current_page_results, total = paginacao_capas(page=page, per_page=per_page, news_data=all_news_data)
            
            order_by_href = f'/arquivonc/capas?ano={year}&page=1&order_by='
            href=f'/arquivonc/capas?ano={year}&order_by={order_by}&page=' + '{0}'
            pagination = Pagination(page=page, per_page=18, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> capas</p>")
            small_pagination = Pagination(page=page, per_page=18, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> capas</p>", link_size='sm')

            return render_template('capas_per_year.html', year=year, all_news_data=current_page_results, pagination=pagination, small_pagination=small_pagination, num_capas=num_capas, order_by_href=order_by_href, order_by=order_by)
    else:
        
        total, all_news_data = get_all_capas_redis()
        num_capas = total
            
        page = int(request.args.get('page', 1))
        per_page = 18
        offset = (page - 1) * per_page
        
        if order_by == "newest":
            all_news_data.sort(key=lambda x: datetime.strptime(x['data'], '%Y-%m-%d'), reverse=True) 
        else:
            all_news_data.sort(key=lambda x: datetime.strptime(x['data'], '%Y-%m-%d'))
        
        current_page_results, total = paginacao_capas(page=page, per_page=per_page, news_data=all_news_data)
        
        order_by_href = f'/arquivonc/capas?page=1&order_by='
        href=f'/arquivonc/capas?order_by={order_by}&page=' + '{0}'
        pagination = Pagination(page=page, per_page=18, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> capas</p>")
        small_pagination = Pagination(page=page, per_page=18, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> capas</p>", link_size='sm')

        
        return render_template('capas.html', all_news_data=current_page_results, pagination=pagination, small_pagination=small_pagination, num_capas=num_capas, order_by_href=order_by_href, order_by=order_by)


# @app.route('/newsletter', methods=['GET', 'POST'])
# def newsletter():
#     if request.method == 'POST':
#         email = request.form.get('email', '')
#         print(email)
#         # Perform any necessary actions with the email (e.g., saving it to a database)
#         # Redirect to the index page
#         return redirect(url_for('arquivonc/index'))
#     # If it's a GET request, render the newsletter subscription form (if you have one)
#     # return render_template('newsletter_form.html')
#     # If you don't have a separate form, you can just redirect to the index page for GET requests
#     return redirect(url_for('arquivonc/index'))


@app.route('/pesquisa', methods=['GET'])
def pesquisa():
    
    minimal_content = request.args.get('minimal_content', False)
    if minimal_content == False or minimal_content == 'false':
        minimal_content = False
    else:
        minimal_content = True
        
    minimal_content = False
    
    query = request.args.get('query', '')
    
    if query == '' or query == None:
        return render_template('pesquise.html')

    query = query.strip()
    
    exact_match = request.args.get('exact_match', "1")
    btnoption = request.args.get('modo')

    start_date = request.args.get('startDate', '2009-01-01')
    end_date = request.args.get('endDate', '2019-12-31')
    
    current_page = request.args.get('page', 1)
    
    order_by = request.args.get('order_by', 'best_match')

    results = get_redis_search(query, exact_match=exact_match, search_mode=btnoption, start_date=start_date, end_date=end_date)
    
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    if btnoption == 'imagens':
        total_tmp, results_tmp = results
        results = []
        for result in results_tmp:
            date = datetime.strptime(result['news_date'], '%Y-%m-%d')
            if date >= datetime.strptime(start_date, '%Y-%m-%d') and date <= datetime.strptime(end_date, '%Y-%m-%d'):
                results.append(result)
                
        results = len(results), results
        
        per_page = 24
     
    elif btnoption == 'text':
        total_tmp, results_tmp = results
        # compare with unix_epoch and start and end date
        results = []
        for result in results_tmp:
            date = datetime.strptime(result['date'], '%Y-%m-%d')
            if date >= datetime.strptime(start_date, '%Y-%m-%d') and date <= datetime.strptime(end_date, '%Y-%m-%d'):
                results.append(result)
                
        results = len(results), results
        per_page = 12
        
    elif btnoption == 'capas':
        total_tmp, results_tmp = results
        # compare with unix_epoch and start and end date
        results = []
        for result in results_tmp:
            date = datetime.strptime(result['data'], '%Y-%m-%d')
            if date >= datetime.strptime(start_date, '%Y-%m-%d') and date <= datetime.strptime(end_date, '%Y-%m-%d'):
                results.append(result)
                
        results = len(results), results
        per_page = 18
        
    current_page_results, total = paginacao_query(page=page, per_page=per_page, results=results, order_by=order_by, btnoption=btnoption)
    
    if minimal_content == False:
            href = f'/arquivonc/pesquisa?query={query}&modo={btnoption}&exact_match={exact_match}&startDate={start_date}&endDate={end_date}&order_by={order_by}&page=' + '{0}'
    else:
            href = f'/arquivonc/pesquisa?query={query}&modo={btnoption}&exact_match={exact_match}&startDate={start_date}&endDate={end_date}&order_by={order_by}&page=' + '{0}'
    
    # Print debug information
    # print(f"Query: {query}")
    # print(f"Page: {page}")
    # print(f"Total pages: {pagination.total_pages}")
    # print(f"Total results: {total}")
    # print(f"Current page results: {current_page_results}")
    
    order_by_href = f'/arquivonc/pesquisa?query={query}&modo={btnoption}&exact_match={exact_match}&startDate={start_date}&endDate={end_date}&page=1&order_by='
    
    if btnoption == 'text':
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>")
        small_pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>", link_size='sm')
        return render_template('query.html', order_by_href=order_by_href, results=current_page_results, pagination=pagination, small_pagination=small_pagination, query=query, order_by = order_by, total=total, minimal_content=minimal_content, startDate = start_date, endDate = end_date, modo=btnoption, current_page=current_page, exact_match=exact_match)
    elif btnoption == 'imagens':
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> imagens</p>")
        small_pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> imagens</p>", link_size='sm')
        return render_template('query_images.html', order_by_href=order_by_href, results=current_page_results, pagination=pagination, small_pagination=small_pagination, query=query, order_by = order_by, total=total, minimal_content=minimal_content, exact_match=exact_match,  modo=btnoption, current_page=current_page, startDate = start_date, endDate = end_date)
    elif btnoption == 'capas':
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> capas</p>")
        small_pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> capas</p>", link_size='sm')
        return render_template('query_capas.html', order_by_href=order_by_href, results=current_page_results, pagination=pagination, small_pagination=small_pagination, query=query, order_by = order_by, total=total, minimal_content=minimal_content, exact_match=exact_match, modo=btnoption, current_page=current_page, startDate = start_date, endDate = end_date)
    else:
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>")
        small_pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>", link_size='sm')
        return render_template('query.html', order_by_href=order_by_href, results=current_page_results, pagination=pagination, small_pagination=small_pagination, query=query, order_by = order_by, total=total, minimal_content=minimal_content, startDate = start_date, endDate = end_date, modo=btnoption, current_page=current_page, exact_match=exact_match)


@app.route('/noticias')
def all_news():
    
    article_id = request.args.get('nid')
    year = request.args.get('ano')
    order_by = request.args.get('order_by', 'oldest')
    
    minimal_content = request.args.get('minimal_content', False)
    if minimal_content == False:
        minimal_content = False
    else:
        minimal_content = True
    
    if year:
        if int(year) < 2009 or int(year) > 2019:
            return render_template('notfound.html'), 404
        
        year = int(year)
        current_date = datetime.today()
    
        statistics_year = get_stats(year)
        
        page, per_page, offset = get_page_args(page_parameter='page',
                                            per_page_parameter='per_page')
        
        if minimal_content == False:
            href=f'/arquivonc/noticias?ano={year}&order_by={order_by}&page=' + '{0}'
        else:
            href=f'/arquivonc/noticias?ano={year}&order_by={order_by}&page=' + '{0}'

        per_page = 12
        
        news, total = paginacao(page, per_page, year, order_by)
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>")
        small_pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>", link_size="sm")
        
        order_by_href = f'/arquivonc/noticias?ano={year}&page=1&order_by='
        if year < 2020 and year > 2008:
            current_page = request.args.get('page')
            if current_page:
                return render_template('news_per_year.html', news=news, pagination=pagination, small_pagination=small_pagination, year=year, current_date=current_date, news_total=total, minimal_content=minimal_content, statistics=statistics_year[f"{year}"], current_page=current_page, order_by=order_by, order_by_href=order_by_href)
            else:
                return render_template('news_per_year.html', news=news, pagination=pagination, small_pagination=small_pagination, year=year, current_date=current_date, news_total=total, minimal_content=minimal_content, statistics=statistics_year[f"{year}"], current_page=1, order_by=order_by, order_by_href=order_by_href)
        else:
            return render_template('notfound.html')
        
        
    elif article_id:
        all_years = [str(year) for year in range(2009, 2020)] 
        for year in all_years:
            news_item = get_news_by_id(article_id, year)
            
            if news_item is not None:
                male_names = ["João", "Manuel", "Rui", "Carlos", "José", "António", "Francisco", "Luís", "Pedro", "Paulo", "Vítor", "Filipe", "Avelino", "Eduardo", "Joaquim", "Jorge", "Tiago", "Alberto", "Vítor", "Vitor", "Ricardo", "Sérgio", "Ayres", "Carlos"]
                female_names = ["Ana", "Maria", "Susana", "Cristela", "Neuza", "Maria Eduarda", "Assunção", "Susana", "Ana Rita", "Maria Eduarda", "Maria", "Cristela", "Maria"]

                author = news_item['author']

                is_male = any(name in author for name in male_names)
                is_female = any(name in author for name in female_names)
                
                author_genre = ""

                if is_male and not is_female:
                    author_genre = "male"
                    print("male")
                elif is_female and not is_male:
                    author_genre = "female"
                    print("female")
                else:
                    author_genre = "female"
                            
                
                news_pool = []
                for i in range(1,4):
                    print(news_item[f'sim_{i}'])
                    news_pool.append(news_item[f'sim_{i}'])
                
                # randomize pool
                random.shuffle(news_pool)
                news_pool = news_pool[:2]    
                
                see_too_1 = {}
                see_too_2 = {}  
                
                for year2 in all_years:
                    see_too_1_tmp = get_news_by_id(news_pool[0], year2)
                    see_too_2_tmp = get_news_by_id(news_pool[1], year2)
                    if see_too_1_tmp is not None:
                        see_too_1 = see_too_1_tmp
                    if see_too_2_tmp is not None:
                        see_too_2 = see_too_2_tmp
                        
                
                return render_template('news_item.html', news=news_item, news_1 = see_too_1, news_2 = see_too_2, author_genre = author_genre)
            
            # prev_article = int(article_id.split('-')[1]) - 1
            # prev_article = str(article_id.split('-')[0]) + '-' + str(prev_article)
            # news_item_prev = get_news_by_id(str(prev_article), year)
            # next_article = int(int(article_id.split('-')[1])) + 1
            # next_article = str(article_id.split('-')[0]) + '-' + str(next_article)
            # news_item_next = get_news_by_id(str(next_article), year)
            # if news_item is not None and news_item_prev is not None and news_item_next is not None:
            #     return render_template('news_item.html', news=news_item, news_prev = news_item_prev, news_next = news_item_next)
            # elif news_item is not None and news_item_prev is not None and news_item_next is None:
            #     return render_template('news_item.html', news=news_item, news_prev = news_item_prev)
            # elif news_item is not None and news_item_prev is None and news_item_next is not None:
            #     return render_template('news_item.html', news=news_item, news_next = news_item_next)
            # elif news_item is not None and news_item_prev is None and news_item_next is None:
            #     return render_template('news_item.html', news=news_item)
        return render_template('notfound.html'), 404
        
    else:
        page, per_page, offset = get_page_args(page_parameter='page',
                                            per_page_parameter='per_page')
        
        if minimal_content == False:
            href=f'/arquivonc/noticias?order_by={order_by}&page=' + '{0}'
        else:
            href=f'/arquivonc/noticias?order_by={order_by}&page='+ '{0}'
            
        order_by_href = f'/arquivonc/noticias?page=1&order_by='

        news_data = get_all_news()
        
        if order_by == 'newest':
            news_data.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        else:
            news_data.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

        per_page = 12
        news, total = paginacao_generic(page=page, per_page=per_page, data=news_data)
        
        pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>")
        small_pagination = Pagination(page=page, per_page=per_page, total=total,
                                css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>", link_size='sm')
        
        return render_template('all_news.html', news=news, news_total=total, pagination=pagination, small_pagination=small_pagination, minimal_content=minimal_content, order_by=order_by, order_by_href=order_by_href)


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

# SUBCATEGORIAS
@app.route('/categoria')
def categoria(): 
    categoria = request.args.get('c')
    subcategoria = request.args.get('subcategoria')
    order_by = request.args.get('order_by', 'oldest')
    
    minimal_content = request.args.get('minimal_content', False)
    if minimal_content == False:
        minimal_content = False
    else:
        minimal_content = True
    
    if categoria and subcategoria:
        if categoria == 'Secções' or categoria == 'Secoes' or categoria == 'secoes' or categoria == 'secções' or categoria == 'seccoes' or categoria == 'Seccoes':
            categoria = 'secções'
        
        if categoria == 'Opinião' or categoria == 'Opiniao' or categoria == 'opiniao' or categoria == 'opinião':
            categoria = 'opinião'
        
        if subcategoria == 'Covilhã' or subcategoria == 'Covilha' or subcategoria == 'covilhã' or subcategoria == 'covilha':
            subcategoria = 'covilhã'
        
        if subcategoria == 'Religião' or subcategoria == 'Religiao' or subcategoria == 'religião' or subcategoria == 'religiao':
            subcategoria = 'religião'
            
        if subcategoria == 'castelo branco' or subcategoria == 'Castelo Branco' or subcategoria == 'Castelo branco' or subcategoria == 'castelo Branco' or subcategoria == 'castelobranco' or subcategoria == 'CasteloBranco':
            subcategoria = 'castelo branco'
            
        if subcategoria == 'região' or subcategoria == 'Região' or subcategoria == 'regiao' or subcategoria == 'Regiao':
            subcategoria = 'região'
        
        if subcategoria == 'fundão' or subcategoria == 'Fundão' or subcategoria == 'fundao' or subcategoria == 'Fundao':
            subcategoria = 'fundão'
        
        news_in_subcategory = get_news_from_sub_category_redis(category=categoria, subcategory=subcategoria)
        if order_by == 'newest':
            news_in_subcategory.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        else:
            news_in_subcategory.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        per_page = 12
        offset = (page - 1) * per_page
        total = len(news_in_subcategory) 
        paginated_news = news_in_subcategory[offset: offset + per_page]
        
        if minimal_content == False:
            href=f'/arquivonc/categoria?c={categoria}&subcategoria={subcategoria}&order_by={order_by}&page=' + '{0}'
        else:
            href=f'/arquivonc/categoria?c={categoria}&subcategoria={subcategoria}&order_by={order_by}&page='+ '{0}'
            
        order_by_href = f'/arquivonc/categoria?c={categoria}&subcategoria={subcategoria}&page=1&order_by='
        
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>")
        small_pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>", link_size='sm')
        current_page = request.args.get('page')
        if current_page:
                return render_template('subcategoria.html', news=paginated_news, pagination=pagination, small_pagination=small_pagination,  categoria=categoria, subcategoria=subcategoria, total=total, minimal_content=minimal_content, current_page=current_page, order_by_href=order_by_href, order_by=order_by)
        else:
                return render_template('subcategoria.html', news=paginated_news, pagination=pagination, small_pagination=small_pagination, categoria=categoria, subcategoria=subcategoria, total=total, minimal_content=minimal_content, current_page=1, order_by_href=order_by_href, order_by=order_by)

        
    else:
        if categoria == 'Secções' or categoria == 'Secoes' or categoria == 'secoes' or categoria == 'secções' or categoria == 'seccoes' or categoria == 'Seccoes':
            categoria = 'secções'
        
        if categoria == 'Opinião' or categoria == 'Opiniao' or categoria == 'opiniao' or categoria == 'opinião':
            categoria = 'opinião'
        
        news_in_category = get_news_from_category_redis(category=categoria)
        
        if order_by == 'newest':
            news_in_category.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        else:
            news_in_category.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        
        page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        per_page = 12
        offset = (page - 1) * per_page
        total = len(news_in_category) 
        if total != 0:
            paginated_news = news_in_category[offset: offset + per_page]
            
            if minimal_content == False:
                href=f'/arquivonc/categoria?c={categoria}&order_by={order_by}&page=' + '{0}'
            else:
                href=f'/arquivonc/categoria?c={categoria}&order_by={order_by}&page='+ '{0}'
                
            order_by_href = f'/arquivonc/categoria?c={categoria}&page=1&order_by='
            
            pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_big, next_label = arrow_right_big, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>")
            small_pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5', href=href, prev_label = arrow_left_small, next_label = arrow_right_small, display_msg="<p class='font-oswald text-uppercase fw-light'>A mostrar <span class='fw-normal border-bottom border-1 border-danger'>{start}</span> - <span class='fw-normal border-bottom border-1 border-danger'>{end}</span> de <span class='fw-normal border-bottom border-1 border-danger'>{total}</span> notícias</p>", link_size='sm')
            
            current_page = request.args.get('page')
            if current_page:
                return render_template('categoria.html', news=paginated_news, pagination=pagination, small_pagination=small_pagination, categoria=categoria, total=total, minimal_content=minimal_content, current_page=current_page, order_by_href=order_by_href, order_by=order_by)
            else:
                return render_template('categoria.html', news=paginated_news, pagination=pagination, small_pagination=small_pagination, categoria=categoria, total=total, minimal_content=minimal_content, current_page=1, order_by_href=order_by_href, order_by=order_by)
        else:
            return render_template('notfound.html')
        

# PARA MAIN NEWS DATE
def format_date_description(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    current_year = datetime.now().year
    current_date = datetime.now().date()
    current_day = datetime.now().day
    years_ago = current_year - date_obj.year

    day = date_obj.day
    month_names_pt = [
        'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
    ]

    if years_ago == 0:
        if day == current_day:
            return f"Hoje"
        return f"No dia {day} de {month_names_pt[date_obj.month - 1]}"
    elif years_ago == 1:
        if day == current_day:
            return f"Hoje"
        return f"Há 1 ano atrás, no dia {day} de {month_names_pt[date_obj.month - 1]}"
    else:
        if day == current_day:
            return f"Hoje, há {years_ago} anos"
        elif day == current_day - 1:
            return f"Ontem, há {years_ago} anos"
        return f"Há {years_ago} anos atrás, no dia {day} de {month_names_pt[date_obj.month - 1]}"

app.jinja_env.filters['format_date_description'] = format_date_description

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html', error=error), 500


def string_to_list(input_string):
    # Split the input string by spaces
    items = input_string.split()
    
    print(items)
    # Return the list of items
    return items

app.jinja_env.filters['string_to_list'] = string_to_list