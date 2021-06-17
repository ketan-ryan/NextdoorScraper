import logging
import getpass
import random
import time
import re
import os

import db_manager
import navigation
import scraper

# Valid carrier inputs
valid = ['Alltell', 'ATT', 'Boost', 'Cricket', 'Firstnet', 'GoogleFi', 'MetroPCS', 'Republic', 'Sprint', 'TMobile',
         'USCellular', 'Verizon', 'Virgin']

# Ensure email is valid
email_regex = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

# Possible SMS gateways
domains = ['sms.alltelwireless.com', 'txt.att.net', 'sms.myboostmobile.com', 'mms.cricketwireless.net', 'txt.att.net',
           'msg.fi.google.com', 'mymetropcs.com', 'textrepublicwireless.com', 'messaging.sprintpcs.com', 'tmomail.net',
           'email.uscc.net', 'vtext.com', 'vmobl.com']

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')

email, password, carr, num = '', '', '', 0


# Make sure input read in from secrets.txt is valid
def validate_input(param, mode):
    if mode == 0:  # Check phone number
        try:
            if len(param.strip()) != 10:
                raise ValueError
            param = int(param)
        except ValueError as ex:
            logging.fatal('Invalid phone number in secrets.txt.')
            exit(1)
    elif mode == 1:  # Check carrier
        if not any(carrier.lower() in param.strip().lower() for carrier in valid):
            logging.fatal('Invalid carrier in secrets.txt.')
            exit(1)
    elif mode == 2:  # Check email
        if re.fullmatch(email_regex, email.strip()) is None or len(email) == 0 or len(email.split('@')[0]) > 64 or \
                len(email.split('@')[1]) > 255:
            logging.fatal('Invalid email in secrets.txt.')
            exit(1)


flag = input('Use secrets file? (Y/N/help) ')
use_secret = False
while True:
    if flag == 'help':
        print("""Whether or not you are reading in variables from a file called "secrets.txt". If true, the file will
              need to look like this, with one element per line:
              phone number (in the form 0123456789)
              phone carrier (must be a valid carrier. if unsure, do not use a secrets file)
              email
              password""")
        flag = input('Use secrets file? (Y/N/help) ')
    elif flag.upper() == 'Y':
        use_secret = True
        break
    elif flag.upper() == 'N':
        use_secret = False
        break
    else:
        print('Invalid input.')
        flag = input('Use secrets file? (Y/N/help) ')

# User is not using a secrets file - get input from command line, make sure it is valid
if not use_secret:
    # Phone number
    num = input('Enter phone number: (in the form 0123456789): ')
    while True:
        try:
            if len(num) != 10:
                raise ValueError
            num = int(num)
            break
        except ValueError as e:
            print('Please enter a valid number.')
            num = input('Enter phone number: (in the form 0123456789): ')

    carr = input('What phone provider do you have? Enter "help" to see a list of valid carriers: ')

    # Phone carrier
    while True:
        if not any(carrier.lower() in carr.lower() for carrier in valid) and carr != 'help':
            print('Please enter a valid carrier.')
            carr = input('What phone provider do you have? Enter "help" to see a list of valid carriers: ')
        elif carr == 'help':
            print(valid)
            print("Carrier not listed? Create an issue at "
                  "https://github.com/TheMinecraftOverlordYT/NextdoorScraper/issues and I'll add support for it "
                  "in a future update.")
            carr = input('What phone provider do you have? Enter "help" to see a list of valid carriers: ')
        else:
            break

    # Email
    email = input('Please enter the email you use to log into Nextdoor: ')
    while True:
        if re.fullmatch(email_regex, email) is None or len(email) == 0 or len(email.split('@')[0]) > 64 or \
                len(email.split('@')[1]) > 255:
            print('Please enter a valid email.')
            email = input('Please enter the email you use to log into Nextdoor: ')
        else:
            break

    # Password
    password = getpass.getpass(prompt='Please enter your password: ')

# Read in from secrets file, validate input
else:
    try:
        with open('secrets.txt', 'r') as secrets:
            num = secrets.readline()
            carr = secrets.readline().strip()
            email = secrets.readline()
            password = secrets.readline()
            validate_input(num, 0)
            validate_input(carr, 1)
            validate_input(email, 2)
    except IOError as e:
        logging.fatal('There was an error opening secrets.txt. Make sure it is placed in the root directory.')
        exit(1)

valid_lower = [x.lower() for x in valid]
domain = domains[valid_lower.index(carr)]
driver_path = input('Please enter the path to your web driver: ')

while True:
    if not os.path.isfile(driver_path) and len(driver_path) != 0:
        print('Please enter a valid path.')
        driver_path = input('Please enter the path to your web driver: ')
    else:
        break

search_terms = input('[Optional] What terms would you like to be notified of? Enter values separated by a comma: ')
search_terms = search_terms.split(',')

if len(search_terms) == 0:
    scraper.load_terms()
else:
    scraper.load_terms(search_terms)

driver = None
if len(driver_path) == 0:
    driver = navigation.navigate(email, password)
else:
    try:
        driver = navigation.navigate(email, password, driver_path)

    except NameError as ex:
        logger.fatal('Invalid email or password.')
        exit(1)

scraper.scroll(driver)
db_manager.init_sms(num, domain, email)

while True:
    links, titles = scraper.scrape(driver)
    db_manager.load(links, titles)
    time.sleep(random.randrange(180, 300))
    driver.refresh()
