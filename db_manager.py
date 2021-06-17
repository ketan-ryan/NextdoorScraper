import json
import logging
import os
import smtplib
from urllib.parse import unquote
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup logger - might need to remove if it gets annoying
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')
number, domain, email = 0, '', ''


# Set up fields needed to send sms
def init_sms(num, dom, e):
    global number, domain, email
    number = num
    domain = dom
    email = e


# Send sms message
def send_message(body):
    server = smtplib.SMTP_SSL("smtp.gmail.com", port=465)

    with open('secrets.txt', 'r') as file:
        for i in range(4):
            _ = file.readline()
        pw = file.readline()

    server.login(email, pw)
    dom = f'1{str(number).strip()}@{domain.strip()}'
    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = dom.strip()
    msg["Subject"] = 'New nextdoor notification!'

    mime_image = MIMEText(body)
    msg.attach(mime_image)
    sms = msg.as_string()
    server.sendmail(email, dom, sms)
    server.quit()


# Loads the database file and checks to see if item already exists
def load(links, titles):
    # Open the file for reading and load the data into a dict
    if not os.path.isfile('db.json') or os.stat('db.json').st_size == 0:
        empty = {}
        with open('db.json', 'w') as file:
            json.dump(empty, file, indent=4)
            print('bro')

    with open('db.json', 'r') as file:
        data = json.load(file)

    # Open the file for writing and log any new entries
    with open('db.json', 'w') as file:
        body = []
        flag = False
        for idx, _ in enumerate(links):
            # If this is not in the database, send a notification
            if not links[idx] in data:
                data[links[idx]] = str(titles[idx])
                body.append(f"{str(titles[idx])} https://nextdoor.com{str(unquote(links[idx]))}\n")
                flag = True
            else:
                logger.info(f'Item with key "{links[idx]}" already exists')

        # Turn list of items into string
        body = ''.join(body)
        json.dump(data, file, indent=4)
        if flag:
            send_message(body)
