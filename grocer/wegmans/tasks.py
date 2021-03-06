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
    TrialPromptClosedTarget,
    InfoModalTarget,
    InfoModalDeliveryTimesTarget,
)
from grocer.utils.browser_utils import get_browser, find_by_text, get_parent
from grocer.utils.str_utils import is_date, is_time, is_money, get_time_window

# TODO Remove hard-coding:
MERCHANT_NAME = "wegmans"


class BrowserOpen(Task):
    output = BrowserOpenTarget(merchant=MERCHANT_NAME)

    def run(self):
        get_browser(merchant=MERCHANT_NAME).get("https://instacart.com")
        sleep(5)


@inherits(BrowserOpen)
class LoginPage(Task):
    requires = Requires()
    browser_open = Requirement(BrowserOpen)
    output = LoginPageTarget(merchant=MERCHANT_NAME)

    def run(self):
        buttons = get_browser(merchant=MERCHANT_NAME).find_elements_by_css_selector(
            "button"
        )
        login_button = buttons[0]
        login_button.click()
        sleep(5)


@inherits(LoginPage)
class LoggedIn(Task):
    requires = Requires()
    login_page = Requirement(LoginPage)
    output = LoggedInTarget(merchant=MERCHANT_NAME)

    def run(self):
        browser = get_browser(merchant=MERCHANT_NAME)
        email_form = browser.find_element_by_id("nextgen-authenticate.all.log_in_email")
        # TODO: get email from task param
        email_form.send_keys(os.environ["EMAIL"])
        sleep(5)
        password_form = browser.find_element_by_id(
            "nextgen-authenticate.all.log_in_password"
        )
        # TODO: get password from task param
        password_form.send_keys(os.environ["PASSWORD"])
        sleep(5)
        buttons = browser.find_elements_by_css_selector("button")
        login_button = buttons[2]
        login_button.click()
        sleep(14)  # TODO: random delays


@inherits(LoggedIn)
class StoreFront(Task):
    requires = Requires()
    logged_in = Requirement(LoggedIn)
    output = StoreFrontTarget(merchant=MERCHANT_NAME)

    def run(self):
        get_browser(merchant=MERCHANT_NAME).get(
            "https://www.instacart.com/store/wegmans/storefront"
        )
        sleep(14)


@inherits(StoreFront)
class CloseTrialPrompt(Task):
    requires = Requires()
    store_front = Requirement(StoreFront)
    output = TrialPromptClosedTarget(merchant=MERCHANT_NAME)

    def run(self):
        buttons = find_by_text(get_browser(merchant=MERCHANT_NAME), "Got it, Thanks",)
        if len(buttons) > 0:
            buttons[0].click()
            sleep(2)


@inherits(StoreFront)
@inherits(CloseTrialPrompt)
class InfoModal(Task):
    requires = Requires()
    main_page = Requirement(StoreFront)
    trial_prompt_closed = Requirement(CloseTrialPrompt)
    output = InfoModalTarget(merchant=MERCHANT_NAME)

    def run(self):
        cart_button = get_browser(merchant=MERCHANT_NAME).find_element_by_css_selector(
            'a[href="/wegmans/info?tab=info"]'
        )
        cart_button.click()
        sleep(7)


@inherits(InfoModal)
class InfoModalDeliveryTimes(Task):
    requires = Requires()
    info_modal = Requirement(InfoModal)
    output = InfoModalDeliveryTimesTarget(merchant=MERCHANT_NAME)

    def run(self):
        find_by_text(get_browser(merchant=MERCHANT_NAME), "Delivery times",)[0].click()
        sleep(8)


# Actions


@inherits(InfoModalDeliveryTimes)
class GetDeliveryTimes(Task):
    requires = Requires()
    main_page = Requirement(InfoModalDeliveryTimes)

    # get_time_window() makes sure we don't run this more than once every 5 minutes
    output = TargetOutput(
        file_pattern=os.path.join(
            "data", "delivery_times_{}".format(get_time_window()), ""
        ),
        ext=".parquet",
        target_class=ParquetTarget,
    )

    def run(self):
        # Commented out because it significantly increases run time
        # self.detect_load_more_times_button()
        if self.detect_no_deliveries():
            self.output().write_dask(dd.from_pandas(pd.DataFrame([]), chunksize=1))
        else:
            self.output().write_dask(
                dd.from_pandas(self.detect_delivery_times(), chunksize=1)
            )

    def detect_delivery_times(self):
        header = find_by_text(
            get_browser(merchant=MERCHANT_NAME), "Available Scheduled Times",
        )[0]
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
                button = get_browser(merchant=MERCHANT_NAME).find_element_by_xpath(
                    '//button[text()="More times"]'
                )
                button.click()
                sleep(5)
            except NoSuchElementException:
                return

    def detect_no_deliveries(self):
        try:
            get_browser(merchant=MERCHANT_NAME).find_element_by_css_selector(
                'img[alt="All delivery windows are full"]'
            )
            return True
        except:
            return False

    def print_results(self):
        print(self.get_results())

    def get_results(self):
        return self.output().read_dask().compute()
