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

def send_email(subject, body, sender, recipients, password, html=None, logo_path=None, capa_path=None, image_list=None):
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
    msg_root['To'] = ', '.join(recipients)

    with smtplib.SMTP('smtp.office365.com', 587) as mailserver:
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(sender, password)
        for recipient in recipients:
            mailserver.sendmail(sender, recipient, msg_root.as_string())
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp} -- Email sent to {recipient}")



def main():
    subject = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
    body = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
    sender = "rd.silva@ubi.pt"
    recipients = ["rodriddsilva@gmail.com", "rd.silva@ubi.pt"]
    #with open("emails.txt", "r") as f:
    #    recipients = f.read().splitlines()
    password = "bfbjcwzhqfwtchyc"
    logo_path = "./LOGO.png"
    
    
    # get a pool of capas that are in the current week
    total, capas = get_capas_same_week()
    random_index = randint(0, len(capas) - 1)
    data = capas[random_index]['data']
    year = capas[random_index]['data'][0:4]
    capas_path = f"./static/img/capas/{data}.jpg"
    
    current_date_time = datetime.now()
    current_year = current_date_time.year
    year_dif = current_year - int(year)
    year_formatted = f"{year_dif} anos" if year != current_date_time.year else "1 ano"
    
    month_list = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    month_formatted = month_list[int(data[5:7]) - 1]
    data_text_formatted = "dia " + data[8:] + " de " + month_formatted + " de " + data[0:4]
    
    
    # get the news
    news = get_news_from_period_redis()
    image_list = []
    for n in news:
        print(n['date'], n['title'])
        image_list.append(f"./static/img/news_images/{n['nid']}.jpg")
    
    html_content = f"""
        <html>
        <head>
              <style>
                .font-oswald {{
                    font-family: "Oswald", sans-serif;
                }}

                .font-guerrilla {{
                    font-family: 'Protest Guerrilla', sans-serif;
                }}

                .font-montserrat {{
                    font-family: 'Montserrat', sans-serif;;
                }}
                
                .font-staatliches{{
                    font-family: "Staatliches", sans-serif;
                }}
                
                .dark {{
                    background-color: #212529;
                }}
                
                .text-dark {{
                    color: #212529;
                }}
                
                .light {{
                    background-color: #F8F9FA;
                }}
                
                .text-light {{
                    color: #F8F9FA;
                }}
                
                .primary {{
                    background-color: #DC3545;
                }}
                
                .text-primary {{
                    color: #DC3545;
                }}
                
                .bg-primary {{
                    background-color: #DC3545;
                }}
                
                .w-100 {{
                    width: 100%;
                }}
                
                body {{
                    font-family: Arial, sans-serif;
                }}
                h1, h2, h3 {{
                    font-family: 'Trebuchet MS', sans-serif;
                }}
                img {{
                    border-radius: 5px;
                }}
                
                .text-uppercase {{
                    text-transform: uppercase;
                }}
                
                .font-paragraph {{
                    font-size: 1.2em;
                    font-family: 'Trebuchet MS', sans-serif;
                }}
                
                .font-light {{
                    font-weight: lighter;
                }}
                
                .font-bold {{
                    font-weight: bold;
                }}
                
                .fs-1 {{
                    font-size: 2.5em;
                }}
                
                .fs-2 {{
                    font-size: 2em;
                }}
                
                .fs-3 {{
                    font-size: 1.5em;
                }}
                
                .fs-4 {{
                    font-size: 1.2em;
                }}
                
                .fs-5 {{
                    font-size: 1em;
                }}
                
                .fs-6 {{
                    font-size: 0.8em;
                }}
                
                .square-image {{
                    width: 200px; /* Adjust the width as needed */
                    height: 200px; /* Set the same height as width to make the image square */
                    object-fit: cover; /* Ensure the entire image is visible within the fixed dimensions */
                }}
                
                .border-light {{
                    margin-top: 10px;
                    border: 1px solid #F8F9FA;
                    border-radius: 10px;
                    padding: 10px;
                    width: 60%;
                }}
                
                .underline-primary {{
                    text-decoration: underline;
                    text-decoration-color: #DC3545;
                }}
                
            </style>
        </head>
        <body class="dark">
            <center>
                <div>
                    <p><img src="cid:image1" alt="Example Image" style="width: 200px; margin-top: 30px"></p> <!-- Reference the image using 'cid' -->
                    <h1 class="text-light font-bold bg-primary w-100 text-uppercase">Esta semana, há {year_formatted}</h1>
                    <p><img src="cid:image2" alt="Example Image" style="width: 450px;"></p> <!-- Reference the image using 'cid' -->
                    <span class="text-light font-paragraph fs-3">Capa do {data_text_formatted}</span>
                    </div>
                <div class="">
                     <h1 class="bg-primary w-100">&nbsp;</h1>
                    """
    for i,n in enumerate(news):
        if i == 0:
           html_content += f"<div class='' style='margin-top: 15px'>"
        else:
            html_content += f"<div class='' style='margin-top: 30px'>"  
        html_content += f"<span><img src='cid:news{i}' alt='Example Image' class='square-image'></span><br>"
        html_content += f"<span class='text-light underline-primary'>{n['date']}</span><br>" 
        html_content += f"<span class='text-light'>{n['title']}</span>" 
        html_content += "</div>"
    html_content += f"""
                </div>
            </center>
        </body>
        </html>
    """

    send_email(subject, body, sender, recipients, password, html_content, logo_path, capas_path, image_list)


if __name__ == "__main__":
    main()


    # Send email
    # subject = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
