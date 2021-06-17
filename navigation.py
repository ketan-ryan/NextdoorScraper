import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Log into the site and go to the correct page
def navigate(email, password, path="G:\Program Files\msedgedriver.exe"):
    # We need the driver for selenium to work
    driver = webdriver.Edge(executable_path=path)

    driver.get('https://nextdoor.com/login/')

    time.sleep(2)

    # Login
    email_field = driver.find_element_by_id('id_email')
    email_field.send_keys(str(email))

    time.sleep(2)

    password_field = driver.find_element_by_id('id_password')
    password_field.send_keys(str(password))
    password_field.send_keys(Keys.ENTER)

    time.sleep(3)

    # Navigate to 'finds' section
    driver.get('https://nextdoor.com/for_sale_and_free/?init_source=more_menu&is_free=true')

    return driver
