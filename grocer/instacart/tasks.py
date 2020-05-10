import os
from time import sleep

from luigi import Task
from luigi.util import inherits
from csci_utils.luigi.dask.target import ParquetTarget
from csci_utils.luigi.task import Requires, Requirement, TargetOutput
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import dask.dataframe as dd

from .targets import (
    BrowserOpenTarget,
    LoginPageTarget,
    LoggedInTarget,
    StoreFrontTarget,
    DeliveryTimesModalTarget,
)
from grocer.utils.browser_utils import get_browser, find_by_text, get_parent
from grocer.utils.str_utils import is_date, is_time, is_money

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
class GetDeliveryTimes(Task):
    requires = Requires()
    main_page = Requirement(DeliveryTimesModal)
    output = TargetOutput(
        file_pattern=os.path.join("data", "delivery_times", ""),
        ext=".parquet",
        target_class=ParquetTarget,
    )

    def run(self):
        # self.detect_load_more_times_button()
        if self.detect_no_deliveries():
            self.output().write_dask(dd.from_pandas(pd.DataFrame([]), chunksize=1))
        else:
            self.output().write_dask(
                dd.from_pandas(self.detect_delivery_times(), chunksize=1)
            )

    def detect_delivery_times(self):
        header = find_by_text(browser, "Available Scheduled Times")[0]
        section = get_parent(get_parent(header))
        return pd.DataFrame(self.parse_delivery_times(section.text))

    def parse_delivery_times(self, text):
        delivery_times = []
        for line in text.splitlines():
            if is_date(line):
                date = line
            if is_time(line):
                delivery_times.append({"date": date, "time": line})
            if is_money(line):
                delivery_times[-1]["price"] = line
        return delivery_times

    def detect_load_more_times_button(self):
        while True:
            try:
                button = browser.find_element_by_xpath('//button[text()="More times"]')
                print(button)
                button.click()
                sleep(5)
            except NoSuchElementException:
                return

    def detect_no_deliveries(self):
        try:
            browser.find_element_by_css_selector(
                'img[alt="All delivery windows are full"]'
            )
            return True
        except:
            return False

    def print_results(self):
        print(self.output().read_dask().compute())
