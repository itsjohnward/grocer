import os
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

# class Instacart:
#     def __init__(self):
#         self.


def get_browser(headless=False):
    opts = Options()
    if headless:
        opts.set_headless()
    return Chrome("/Users/john/csci-e-29/grocer/chromedriver", options=opts)


def load_site(browser):
    browser.get("https://instacart.com")
    sleep(5)


def open_login(browser):
    buttons = browser.find_elements_by_css_selector("button")
    login_button = buttons[0]
    login_button.click()
    sleep(5)


def login(browser):
    email_form = browser.find_element_by_id("nextgen-authenticate.all.log_in_email")
    email_form.send_keys("test")
    sleep(5)
    password_form = browser.find_element_by_id(
        "nextgen-authenticate.all.log_in_password"
    )
    password_form.send_keys("test")
    sleep(5)
    buttons = browser.find_elements_by_css_selector("button")
    login_button = buttons[2]
    login_button.click()
    sleep(5)


def detect_login_error(browser):
    error_msg = browser.find_element_by_id(
        "error_nextgen-authenticate.all.log_in_password"
    )
    print(error_msg)
    print(error_msg.text)


browser = get_browser()
load_site(browser)
open_login(browser)
login(browser)
detect_login_error(browser)

browser.close()
quit()
