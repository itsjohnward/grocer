import os
from time import sleep

from luigi import Task
from luigi.util import inherits
from csci_utils.luigi.task import Requires, Requirement

from .targets import (
    BrowserOpenTarget,
    LoginPageTarget,
    LoggedInTarget,
    StoreFrontTarget,
    DeliveryTimesModalTarget,
)
from utils.browser_utils import get_browser

browser = get_browser()


class BrowserOpen(Task):
    output = BrowserOpenTarget(browser)

    def run(self):
        browser.get("https://instacart.com")
        sleep(5)


@inherits(BrowserOpen)
class LoginPage(Task):
    requires = Requires()
    browser_open = Requirement(BrowserOpen)
    output = LoginPageTarget(browser)

    def run(self):
        buttons = browser.find_elements_by_css_selector("button")
        login_button = buttons[0]
        login_button.click()
        sleep(5)


@inherits(LoginPage)
class LoggedIn(Task):
    requires = Requires()
    login_page = Requirement(LoginPage)
    output = LoggedInTarget(browser)

    def run(self):
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


@inherits(LoggedIn)
class StoreFront(Task):
    requires = Requires()
    logged_in = Requirement(LoggedIn)
    output = StoreFrontTarget(browser)

    def run(self):
        browser.get("https://www.instacart.com/store/wegmans/storefront")
        sleep(5)


@inherits(StoreFront)
class DeliveryTimesModal(Task):
    requires = Requires()
    main_page = Requirement(StoreFront)
    output = DeliveryTimesModalTarget(browser)

    def run(self):
        cart_button = browser.find_element_by_css_selector(
            'a[href="/wegmans/info?tab=delivery"]'
        )
        cart_button.click()
        sleep(10)


# Actions


@inherits(DeliveryTimesModal)
class DeliveryTimesModal(Task):
    requires = Requires()
    main_page = Requirement(StoreFront)
    output = TargetOutput(
        file_pattern=os.path.join("data", "delivery_times", ""),
        ext=".parquet",
        target_class=ParquetTarget,
    )

    def run(self):
        self.output().write_dask(
            average_text_length_by_something(reviews, "decade"), compression="gzip",
        )

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

    def print_results(self):
        print(self.output().read_dask().compute())
