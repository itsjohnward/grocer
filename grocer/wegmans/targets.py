from functools import partial
import os

from luigi import Target
from grocer.utils.browser_utils import get_browser, find_by_text
from selenium.common.exceptions import NoSuchElementException

from grocer.utils.browser_utils import get_browser

# TODO: generalize GroceryTarget and Page anchors
class InstacartTarget(Target):
    def __init__(self, merchant, *args, **kwargs):
        self.merchant_name = merchant
        super().__init__(*args, **kwargs)

    def exists(self):
        raise NotImplemented()

    def __get__(self, task, cls):
        if task is None:
            return self
        return partial(self.__call__, task)

    def __call__(self, task):
        return self


class BrowserOpenTarget(InstacartTarget):
    def exists(self):
        browser = get_browser(merchant=self.merchant_name)
        return browser.current_url == "https://www.instacart.com/"


class WelcomePageTarget(InstacartTarget):
    def exists(self):
        browser = get_browser(merchant=self.merchant_name)
        return (
            len(find_by_text(browser, "Already have an account?",)) > 0
            and len(find_by_text(browser, "Log in")) > 0
        )


class LoginPageTarget(InstacartTarget):
    def exists(self):
        browser = get_browser(merchant=self.merchant_name)
        return (
            len(find_by_text(browser, "Welcome back",)) > 0
            and len(find_by_text(browser, "Log in")) > 0
        )


class LoggedInTarget(InstacartTarget):
    def exists(self):
        browser = get_browser(merchant=self.merchant_name)
        # A log out button exists
        return len(find_by_text(browser, "Log Out")) > 0


class TrialPromptClosedTarget(InstacartTarget):
    def exists(self):
        browser = get_browser(merchant=self.merchant_name)
        # The trial prompt is not displayed
        return len(find_by_text(browser, "Got it, Thanks")) == 0


class StoreFrontTarget(InstacartTarget):
    def exists(self):
        browser = get_browser(merchant=self.merchant_name)
        return (
            browser.current_url == "https://www.instacart.com/store/wegmans/storefront"
        )


class InfoModalTarget(InstacartTarget):
    def exists(self):
        browser = get_browser(merchant=self.merchant_name)
        return (
            (len(find_by_text(browser, "Info",)) > 0)
            & (len(find_by_text(browser, "Delivery times",)) > 0)
            & (len(find_by_text(browser, "Pickup times",)) > 0)
        )


class InfoModalDeliveryTimesTarget(InstacartTarget):
    def exists(self):
        browser = get_browser(merchant=self.merchant_name)
        return len(find_by_text(browser, "Available Scheduled Times",)) > 0
