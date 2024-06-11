from datetime import datetime, timedelta
import json
from random import randint

import redis
from redis.commands.search.query import Query

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def connect_redis():    
    r = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True,
        )

    return r

r = connect_redis()

def save_newsletter_item(date, nids, capaId):
    today = datetime.now()
    # today date as YYYY-MM-DD and a string
    date_today = today.strftime('%Y-%m-%d')
    
    key_prefix = "newsletter_item"
    key = f"{key_prefix}:{date_today}"
    data = {
        "date": date,
        "nids": nids,
        "capaId": capaId
    }
    flat_data = {k: str(v) for k, v in data.items()}  # Convert all values to strings
    r.hset(key, mapping=flat_data)


def get_email_redis(email):
    key = f"newsletter_email:{email}"
    email_data = r.hgetall(key)
    return email_data

def get_all_emails_redis():
    keys = r.keys("newsletter_email:*")
    emails = []
    for key in keys:
        email_data = r.hgetall(key)
        if email_data['active'] == '0':
            continue
        else:
            #print(email_data)
            emails.append(email_data)
    return emails

def get_news_year(year):
    index_name = 'idx:news'
    query = f'@date:{year}'

    try:
        results = r.ft(index_name).search(Query(query).paging(0, 3000))
    except redis.exceptions.ResponseError as e:
        print("Error executing RediSearch query:", e)
        return [] 

    #print(f"Results from year {year}:", results.total) 
        
    return results.docs


def get_news_from_period_redis(week=True):
    current_date = datetime.now()
    yesterday_date = current_date - timedelta(days=1)
    current_month, current_day, current_year = current_date.month, current_date.day, current_date.year
    yesterday_month, yesterday_day, yesterday_year = yesterday_date.month, yesterday_date.day, yesterday_date.year

    max_articles_per_year = 1
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
                        if article not in news_from_period:
                            news_from_period.append(article)
                            articles_loaded_per_year[year] += 1

        # Sort news articles by date
        news_from_period.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

        return news_from_period


def get_capas_same_week():
    current_date_time = datetime.now()
    
    total_capas = 0
    capas_per_day = []

    for year in range(2009, 2020):
        per_year = 0
        tmp_total_capas, tmp_capas_per_day = get_capas_per_year(year)  # Assuming this function exists
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
                    break # Found news for this date, move to next year
                current_date -= timedelta(days=1)
                
    return total_capas, capas_per_day

def get_capas_per_year(year):
    query_string = f"@data:{year}"
    
    results = r.ft("idx:capas").search(Query(query_string).paging(0, 3500))
    
    # Filter documents to include only those with the "nc_capas" prefix
    nc_capas_documents = [doc for doc in results.docs if doc['id'].startswith('nc_capas')]
    
    # after filtering, sort by data (that is date)
    nc_filtered_docs = sorted(nc_capas_documents, key=lambda x: x['data'])

    total = len(nc_filtered_docs)
    return total, nc_filtered_docs

def send_email(subject, body, sender, recipient, password, html=None, logo_path=None, capa_path=None, image_list=None):
    if html:
        # Create a multipart message
        msg_root = MIMEMultipart('related')
        msg_alternative = MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)
        
        # Attach plain text and HTML versions of the message body
        msg_text = MIMEText(body)
        msg_alternative.attach(msg_text)
        
        msg_html = MIMEText(html, 'html')
        msg_alternative.attach(msg_html)
        
        # Attach the image if provided
        if logo_path:
            with open(logo_path, 'rb') as img_file:
                msg_image = MIMEImage(img_file.read())
                msg_image.add_header('Content-ID', '<image1>')
                msg_root.attach(msg_image)
        if capa_path:
            with open(capa_path, 'rb') as img_file:
                msg_image = MIMEImage(img_file.read())
                msg_image.add_header('Content-ID', '<image2>')
                msg_root.attach(msg_image)
                
        if image_list:
            for i,image in enumerate(image_list):
                with open(image, 'rb') as img_file:
                    msg_image = MIMEImage(img_file.read())
                    msg_image.add_header('Content-ID', f'<news{i}>')
                    msg_root.attach(msg_image)
    else:
        msg_root = MIMEText(body)

    msg_root['Subject'] = subject
    msg_root['From'] = sender

    with smtplib.SMTP('smtp.office365.com', 587) as mailserver:
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(sender, password)
        msg_root['To'] = recipient
        mailserver.sendmail(sender, recipient, msg_root.as_string())
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #print(f"{timestamp} -- Email sent to {recipient}")



def main():
    sender = "newsletter.arquivonc@ubi.pt"
    all_emails = get_all_emails_redis()
    recipients = [email['email'] for email in all_emails]
    password = "tphlrnczbyryrntn"
    logo_path = "./OLD_LOGO.png"
    
    # get a pool of capas that are in the current week
    total, capas = get_capas_same_week()
    random_index = randint(0, len(capas) - 1)
    data = capas[random_index]['data']
    year = capas[random_index]['data'][0:4]
    capas_path = f"../static/img/capas/{data}.jpg"
    
    current_date_time = datetime.now()
    current_year = current_date_time.year
    year_dif = current_year - int(year)
    year_formatted = f"{year_dif} anos" if year != current_date_time.year else "1 ano"
    
    month_list = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    month_formatted = month_list[int(data[5:7]) - 1]
    data_text_formatted = "Dia " + data[8:] + " de " + month_formatted + " de " + data[0:4]
    
    
    # get the news
    news = get_news_from_period_redis()
    news_nids = ""
    image_list = []
    for i,n in enumerate(news):
        #print(n['date'], n['title'])
        if i == len(news) - 1:
            news_nids += f"{n['nid']}"
        else:
            news_nids += f"{n['nid']},"
        
        if n['image_url'].startswith("http") or n['image_url'] == "" or n['image_url'] == "None":
            image_list.append("../static/img/LOGO2.png")
        else:
            image_list.append(f"../static/img/news_images/{n['nid']}.jpg")
        
    save_newsletter_item(data, news_nids, capas[random_index]['data'])
    

    for i, recipient in enumerate(recipients):
        curr_email = recipient
        curr_token = all_emails[i]['token']
        
        subject = f"Esta semana há {year_formatted}! 📰"
        body = f"Esta semana, há {year_formatted}! 📰\n\n"

        html_content = f"""
        <html>
        <head>
             <style>
                   body {{
                        font-family: Arial, sans-serif;
                    }}
                    .title {{
                        font-family: 'Trebuchet MS', sans-serif;
                        text-transform: uppercase;
                    }}
                    
                    .content {{
                        font-family: Helvetica, sans-serif;
                    }}
                    
                    .container {{
                        width: 90%;
                        max-width: 600px;
                    }}
                    
                    .row {{
                        display: table;
                        width: 95%;
                    }}
                    
                    .column {{
                        display: table-cell;
                        vertical-align: top;
                    }}
                    
                    .text {{
                        width: 69%;
                    }}
                    
                    .image {{
                        padding-left: 10px;
                        padding-right: 10px;
                        width: 29%;
                        max-width: 200px;
                        max-height: 200px;
                        text-align: center;
                    }}
                    
                    .image img {{
                        width: 200px;
                        height: 200px;
                        max-width: 200px;
                        max-height: 200px;
                        border-radius: 5px;
                        object-fit: cover;
                    }}

                    @media only screen and (max-width: 450px) {{
                        .row {{
                            display: block;
                            width: 99%;
                        }}
                        .column {{
                            width: 99%;
                            display: block;
                            text-align: center;
                        }}
                        .image {{
                            max-width: 250px;
                            max-height: 250px;
                            padding: 0;
                        }}
                        
                        .image img {{
                            max-width: 200px;
                            max-height: 200px;
                        }}
                    }}
            </style>
        </head>
        <body class="" style="font-family: Arial, sans-serif; background-color: #F8F9FA;">
            <center>
                <div style="width: 90%; max-width: 600px;">
                    <center style='width: 100%; background-color: #212529 margin-top: 30px; margin-bottom: 0px;'>
                        <div style='width: 100%; background-color: #212529; padding-bottom: 20px; padding-top: 20px;'>
                            <img src="cid:image1" alt="ArquivoNC" style="width: 200px;"><br>
                            <span class='title' style='color: white; text-transform: none; font-size: 1.8em;'><em>Newsletter</em> Semanal</span><br>
                            <span class='title' style='color: white; text-transform: none; font-size: 1em;'><em>Todas as quintas-feiras</em></span>
                            
                        </div>
                    </center>
                    <div style='background-color: #DC3545'>
                        <div style='padding-bottom: 5px; padding-top: 10px;'>
                            <center>
                            <h2 class="title" style='color: white; height: 10px;'>Nesta semana, há {year_formatted}</h2>
                            </center>
                        </div>
                        <br><span style='padding-left: 10px; padding-right: 10px; margin-bottom: 0px; margin-top: 0px;'><img src="cid:image2" alt="{data_text_formatted}" class='' style="max-width: 300px; width: 85%"><span><br>
                        <div style="padding-bottom: 10px; ">
                            <center>
                                <h2 class="title" style='color: white; text-decoration: underline; text-decoration-color: #DC3545; height: 10px;'>{data_text_formatted}</h2>
                            </center>
                        </div>
                    </div>
                </div>
            </center>
            <div class="" style="padding-bottom: 40px;">
        """
        for i, n in enumerate(news):
            html_content += f"<center><hr style='max-width: 600px; width: 90%; color: #797270; margin-top: 30px; margin-bottom: 30px;'><div class='container' style='width: 90%; max-width: 600px;'><div class='row'>" if i != 0 else "<center><hr style='margin-top: 15px; margin-bottom: 30px; max-width: 600px; width: 90%; color: #797270;'><div class='container' style='width: 90%; max-width: 600px;'><div class='row'>"
            html_content += f"<div class='column image'><img src='https://arquivonc.ubi.pt/arquivonc/static/img/news_images/{n['nid']}.jpg' alt='{n['title']}' class='square-image' style='object-fit: cover; max-height: 200px'></div>"
            html_content += f"<div class='column text'>"
            html_content += f"<span class='title' style='font-weight: bold; font-size: 1.9em; color: #212529; text-decoration: underline; text-decoration-color: #DC3545;'>{n['date']}</span><br>"
            html_content += f"<span class='title' style='color: #212529; font-size: 1.3em;'><a href='https://arquivonc.ubi.pt/arquivonc/noticias?nid={n['nid']}' class='' style='color: #212529; text-decoration: none; font-size: 1.2em; font-weight: bold;'>{n['title']}</a></span><br>"
            html_content += f"<span class='content' style='color: #212529;'><a href='https://arquivonc.ubi.pt/arquivonc/noticias?nid={n['nid']}' class='' style='color: #212529; text-decoration: none;'>{n['content'][:300]}...</a></span><br>"
            html_content += f"</div>"
            html_content += "</div></div></center>"

        html_content += f"""
            <center>
                <div style="padding-top: 10px; padding-bottom: 20px; background:#DC3545; margin-top: 30px; width: 90%; max-width: 600px;">
                    <center>
                    <h2 class="title" style='color: white; font-size: 1.2em; font-weight: bold; background-color: #DC3545;'>Obrigado por subscrever a <em>newsletter</em> do ArquivoNC!</h2>
                    </center>
                </div>
                <div style="width: 90%; max-width: 600px;">
                    <hr style="max-width: 100%; color: #9F9FAD; ">
                    <p class="" style='color: #212529; font-family: 'Trebuchet MS', sans-serif;'>Caso este email lhe tenha sido reencaminhado, <a href="https://arquivonc.ubi.pt/arquivonc/newsletter" class="" style="text-decoration: underline; text-decoration-color: #212529; color: #212529; font-weight: bold;">subscreva aqui!</a> </p>
                </div>
                <div style="width: 90%; max-width: 600px;">
                    <p class="" style='color: #212529; font-family: 'Trebuchet MS', sans-serif;'>Para cancelar a subscrição, <a href="https://arquivonc.ubi.pt/arquivonc/remover?token={curr_token}" class="" style='text-decoration: underline; text-decoration-color: #212529; color: #212529; font-weight: bold;'>clique aqui</a></p>
                </div>
            </center>
            </div>
        </body>
        </html> 
        """

        send_email(subject, body, sender, curr_email, password, html_content, logo_path, capas_path)



main()


    # Send email
    # subject = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
