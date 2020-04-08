# -*- coding: UTF-8 -*-
# Date   : 2019/12/23 9:31
# Editor : gmj
# Desc   : 模拟登陆获取cookie
import random
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains

options = ChromeOptions()
options.headless = True


# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# google = Chrome(r'D:\pyth\chromedriver.exe', options=options)
class MyDriver(object):
    def __init__(self, options):
        self.driver = webdriver.Chrome(options=options)

    def get(self, url):
        self.driver.get(url)

    def max_window(self):
        self.driver.maximize_window()

    def click_by_id(self, id: str):
        self.driver.find_element_by_id(id).click()

    def click_by_class_name(self, class_name: str):
        self.driver.find_element_by_class_name(class_name).click()

    def input(self, id, txt: str):
        self.driver.find_element_by_id(id).send_keys(txt)

    def wait(self, sec):
        time.sleep(sec)

    def find_by_xpath(self, xpath_):
        self.driver.find_element_by_xpath(xpath_)

    def get_cookies(self):
        self.driver.get_cookies()

    def move(self, ele):
        ActionChains(self.driver).move_to_element(ele).perform()


def login_wanmei(tel, pwd):
    google = webdriver.Chrome(options=options)
    google.get('https://www.wmzy.com/api/school')
    google.maximize_window()
    try:
        login = google.find_element_by_id('login_link')
        login.click()
        login2 = google.find_element_by_id('switchForm')
        login2.click()
        phone = google.find_element_by_id('mobile')
        phone.send_keys(tel)
        time.sleep(1)
        password = google.find_element_by_id('password')
        password.send_keys(pwd)
        time.sleep(1)
        agree = google.find_element_by_class_name('ag-ch ')
        agree.click()
        time.sleep(random.random())
        submit = google.find_element_by_xpath('//a[@class="btn btn-submitFrom"]')
        submit.click()
        time.sleep(0.5)
        mouse = google.find_element_by_xpath("//span[@class='nick-name-mask']")
        ActionChains(google).move_to_element(mouse).perform()
        time.sleep(0.2)
        cookies = google.get_cookies()
    except Exception as e:
        raise e
    finally:
        google.quit()
    return cookies
