import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def navigate():
    with open('secrets.txt') as file:
        username = file.readline()
        password = file.readline()

    driver = webdriver.Edge(executable_path='G:\Program Files\msedgedriver.exe')

    driver.get('https://nextdoor.com/login/')

    time.sleep(2)

    email_field = driver.find_element_by_id('id_email')
    email_field.send_keys(str(username))

    time.sleep(2)

    password_field = driver.find_element_by_id('id_password')
    password_field.send_keys(str(password))
    password_field.send_keys(Keys.ENTER)

    time.sleep(2)

    driver.get('https://nextdoor.com/for_sale_and_free/?init_source=more_menu')

    time.sleep(5)


if __name__ == '__main__':
    navigate()
