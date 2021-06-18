from sys import exit
import logging
import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')


def navigate(email, password, path='msedgedriver.exe'):
    # We need the driver for selenium to work
    driver = None

    try:
        driver = webdriver.Edge(executable_path=path)
    except selenium.common.exceptions.WebDriverException:
        logger.fatal('Could not find your webdriver. Please make sure the path is valid.')
        exit(1)
    driver.get('https://nextdoor.com/login/')

    time.sleep(2)

    # Login
    try:
        email_field = driver.find_element_by_id('id_email')
        email_field.send_keys(str(email))

        time.sleep(2)

        password_field = driver.find_element_by_id('id_password')
        password_field.send_keys(str(password))
        password_field.send_keys(Keys.ENTER)
    except selenium.common.exceptions:
        logger.fatal('Could not log in to NextDoor. Please check your email and password and try again.')
        exit(1)
    time.sleep(3)

    # Navigate to 'finds' section
    driver.get('https://nextdoor.com/for_sale_and_free/?init_source=more_menu&is_free=true')

    if 'https://nextdoor.com/login' in driver.page_source:
        logger.fatal('Unable to log in to NextDoor. Please check your email and password and try again.')
        exit(1)

    return driver
