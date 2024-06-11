from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

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

    with smtplib.SMTP('smtp.office365.com', 587) as mailserver:
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(sender, password)
        for recipient in recipients:
            msg_root['To'] = recipient
            mailserver.sendmail(sender, recipient, msg_root.as_string())
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp} -- Email sent to {recipient}")

