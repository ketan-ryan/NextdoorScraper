from sys import exit
import traceback
import logging
import getpass
import random
import time
import re
import os

import db_manager
import navigation
import scraper

os.system('color')
# yellow, bright yellow, reset, red, green, bold, blue
y, yb, r, d, g, b, bl = '\u001b[33m', '\u001b[33;1m', '\u001b[0m', '\u001b[31m', '\u001b[32m', '\u001b[1m', '\u001b[34m'

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
logging.basicConfig(level=logging.WARN, format=f'{d}%(asctime)s - %(name)s - %(levelname)s - %(message)s{r}',
                    datefmt='%m/%d/%Y %H:%M:%S')

email, password, carr, num = '', '', '', 0


# Make sure input read in from secrets.txt is valid
def validate_input(param, mode):
    if mode == 0:  # Check phone number
        try:
            if len(param.strip()) != 10:
                raise ValueError
            param = int(param)
        except ValueError:
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
        print(f"""{yb}Whether or not you are reading in variables from a file called "secrets.txt". If true, the file 
      will need to look like this, with one element per line:
              {bl}phone number (in the form 9995554444)
              phone carrier{yb} (must be a valid carrier. if unsure, do not use a secrets file){bl}
              email
              password{r}""")
        flag = input('Use secrets file? (Y/N/help) ')
    elif flag.upper() == 'Y':
        use_secret = True
        break
    elif flag.upper() == 'N':
        use_secret = False
        break
    else:
        print(f'{y}Invalid input.{r}')
        flag = input('Use secrets file? (Y/N/help) ')

# User is not using a secrets file - get input from command line, make sure it is valid
if not use_secret:
    # Phone number
    num = input(f'Enter phone number: {bl}(in the form 9995554444){r}: ')
    while True:
        try:
            if len(num) != 10:
                raise ValueError
            num = int(num)
            break
        except ValueError as e:
            print(f'{y}Please enter a valid number.{r}')
            num = input(f'Enter phone number: {bl}(in the form 9995554444){r}: ')

    carr = input('What phone provider do you have? Enter "help" to see a list of valid carriers: ')

    # Phone carrier
    while True:
        if not any(carrier.lower() in carr.lower() for carrier in valid) and carr != 'help':
            print(f'{y}Please enter a valid carrier.{r}')
            carr = input('What phone provider do you have? Enter "help" to see a list of valid carriers: ')
        elif carr == 'help':
            print(valid)
            print(f"{yb}Carrier not listed? Create an issue at "
                  "https://github.com/TheMinecraftOverlordYT/NextdoorScraper/issues and I'll add support for it "
                  f"in a future update.{r}")
            carr = input('What phone provider do you have? Enter "help" to see a list of valid carriers: ')
        else:
            break

    # Email
    email = input('Please enter the email you use to log into Nextdoor: ')
    while True:
        if re.fullmatch(email_regex, email) is None or len(email) == 0 or len(email.split('@')[0]) > 64 or \
                len(email.split('@')[1]) > 255:
            print(f'{y}Please enter a valid email.{r}')
            email = input('Please enter the email you use to log into Nextdoor: ')
        else:
            break

    # Password
    password = getpass.getpass(prompt='Please enter your password: ')

# Read in from secrets file, validate input
else:
    secrets_file = input('Please enter the path to your secrets file, or enter "help": ')
    while True:
        if secrets_file == 'help':
            print(f"{yb}Please enter the path pointing to your secrets file. An example path might look something "
                  f"like{bl}\n "
                  r"C:\Users\John\Desktop\NextdoorScraper\secrets.txt."
                  f"{yb} The file should end in '.txt'."
                  f"{r}")
            secrets_file = input('Please enter the path to your secrets file, or enter "help": ')
        elif not os.path.isfile(secrets_file) or not secrets_file[-4:] == '.txt':
            print(f'{y}Invalid path.{r}')
            secrets_file = input('Please enter the path to your secrets file, or enter "help": ')
        else:
            break

    try:
        with open(secrets_file, 'r') as secrets:
            num = secrets.readline()
            carr = secrets.readline().strip()
            email = secrets.readline()
            password = secrets.readline()
            validate_input(num, 0)
            validate_input(carr, 1)
            validate_input(email, 2)
    except IOError:
        logging.fatal('There was an error opening secrets.txt. Make sure the path is correct and you '
                      'have appropriate permissions.')
        traceback.print_exc()
        exit(1)

valid_lower = [x.lower() for x in valid]
domain = domains[valid_lower.index(carr)]
driver_path = input('Please enter the path to your web driver: ')

while True:
    if not os.path.isfile(driver_path.strip()) or driver_path.strip()[-4:] != '.exe':
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

db_path = input('Please enter the full path to where you would like your database file to be stored, or "help": ')
while True:
    if db_path == 'help':
        print(f'{yb}Please enter a path pointing to where you want your database to be stored. An example might look '
              f'like {bl}\n' r'C:\Users\John\Desktop\NextDoorScraper\db.json''.\n'f'{yb}The path should end '
              f'with {bl}.json{yb}.  This file will keep track of notifications you have gotten so as to not '
              f'notify you twice for the same item.{r}')
        db_path = input('Please enter the path to where you would like your database file to be stored, or "help": ')
    # Strip off the file (x.json) then convert back to string and make sure directory is valid.
    # This checks that their desired db file would be valid without it actually having to already exist.
    elif not os.path.isdir("\\".join(db_path.strip().split("\\")[:-1])) or not db_path[-5:] == '.json':
        print('Please enter a valid path.')
        db_path = input('Please enter the path to where you would like your database file to be stored, or "help": ')
    else:
        break

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
    logger.debug('Page refreshed')
