from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import unquote
import smtplib
import logging
import json
import arg_handler
import os

os.system('color')
# yellow, bright yellow, reset, red, green, bold, blue
y, yb, r, d, g, b, bl = '\u001b[33m', '\u001b[33;1m', '\u001b[0m', '\u001b[31m', '\u001b[32m', '\u001b[1m', '\u001b[34m'

# Setup logger - might need to remove if it gets annoying
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG if arg_handler.is_debug() else logging.INFO, format=f'\u001b[37;1m{b}%(asctime)s - %(name)s - %(levelname)s - %(message)s{r}',
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
    logger.debug('SMTP connection established')
    with open('token.txt', 'r') as file:
        pw = file.readline()

    server.login(email, pw)
    logger.debug('Logged in')
    dom = f'1{str(number).strip()}@{domain.strip()}'
    logger.debug(dom)
    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = dom.strip()
    msg["Subject"] = 'New nextdoor notification!'

    mime_text = MIMEText(body)
    msg.attach(mime_text)
    sms = msg.as_string()
    server.sendmail(email, dom, sms)
    server.quit()
    logger.info(f'{g}Message delivery successful.{r}')


# Loads the database file and checks to see if item already exists
def load(links, titles, path):
    # Open the file for reading and load the data into a dict
    if not os.path.isfile(path) or os.stat(path).st_size == 0:
        logger.debug(f'Writing new file {path}')
        empty = {}
        with open(path, 'w') as file:
            json.dump(empty, file, indent=4)

    with open(path, 'r') as file:
        data = json.load(file)

    # Open the file for writing and log any new entries
    with open(path, 'w') as file:
        logger.debug(f'Opened {path} for writing')
        body = []
        flag = False
        for idx, _ in enumerate(links):
            # If this is not in the database, send a notification
            if not links[idx] in data:
                data[links[idx]] = str(titles[idx])
                body.append(f"{str(titles[idx])} https://nextdoor.com{str(unquote(links[idx]))}\n")
                logger.debug(f'Added {titles[idx]} to database file')
                flag = True
            else:
                logger.info(f'{y}Item with value "{titles[idx]}" already exists{r}')

        # Turn list of items into string
        body = ''.join(body)
        json.dump(data, file, indent=4)
        if flag:
            logger.info(f'{g}Database updated successfully.{r}')
            try:
                send_message(body)
            except TimeoutError:
                logger.warning(f'{y}There was an error sending the NextDoor notification. Please try again later.{r}')
