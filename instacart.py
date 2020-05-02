import os
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# TODO: Refactor into class with features and capabilities
# class Instacart:
#     def __init__(self):
#         self.


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
    email_form.send_keys(os.environ["EMAIL"])
    sleep(5)
    password_form = browser.find_element_by_id(
        "nextgen-authenticate.all.log_in_password"
    )
    password_form.send_keys(os.environ["PASSWORD"])
    sleep(5)
    buttons = browser.find_elements_by_css_selector("button")
    login_button = buttons[2]
    login_button.click()
    sleep(15)  # TODO: random delays


def detect_login_error(browser):
    error_msg = browser.find_element_by_id(
        "error_nextgen-authenticate.all.log_in_password"
    )
    print(error_msg)
    print(error_msg.text)


def view_cart(browser):
    cart_button = browser.find_element_by_css_selector(
        'a[href="/wegmans/info?tab=delivery"]'
    )
    cart_button.click()
    sleep(10)


def detect_load_more_times_button(browser):
    while True:
        try:
            button = browser.find_element_by_xpath('//button[text()="More times"]')
            print(button)
            button.click()
            sleep(5)
        except NoSuchElementException:
            return


def detect_no_deliveries(browser):
    try:
        browser.find_element_by_css_selector('img[alt="All delivery windows are full"]')
        return True
    except:
        return False


def detect_delivery_times(browser):
    header = find_by_text(browser, "Available Scheduled Times")[0]
    section = get_parent(get_parent(header))
    return parse_delivery_times(section.text)


def parse_delivery_times(text):
    delivery_times = {}
    for line in text.splitlines():
        if is_date(line):
            delivery_times[line] = {}
            date = line
        if is_time(line):
            delivery_times[date][line] = None
            time = line
        if is_money(line):
            delivery_times[date][time] = line
    return delivery_times


browser = get_browser()  # TODO: context manager open

load_site(browser)
open_login(browser)
login(browser)
# detect_login_error(browser)
view_cart(browser)
no_deliveries = detect_no_deliveries(browser)
if no_deliveries:
    print("No deliveries available")
else:
    detect_load_more_times_button(browser)
    print("Delivery times:", detect_delivery_times(browser))

# TODO: context manager close
browser.close()
quit()
