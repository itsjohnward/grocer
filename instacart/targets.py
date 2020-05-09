from functools import partial

from luigi import Target
from utils.browser_utils import get_browser, find_by_text
from selenium.common.exceptions import NoSuchElementException


class InstacartTarget(Target):
    def __init__(self, browser, *args, **kwargs):
        self.browser = browser
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
        print("BrowserOpenTarget", self.browser.current_url)
        return self.browser.current_url == "https://www.instacart.com/"


class WelcomePageTarget(InstacartTarget):
    def exists(self):
        return (
            len(find_by_text(self.browser, "Already have an account?")) > 0
            and len(find_by_text(self.browser, "Log in")) > 0
        )


class LoginPageTarget(InstacartTarget):
    def exists(self):
        return (
            len(find_by_text(self.browser, "Welcome back")) > 0
            and len(find_by_text(self.browser, "Log in")) > 0
        )


class LoggedInTarget(InstacartTarget):
    def exists(self):
        # A log out button exists
        return len(find_by_text(self.browser, "Log out")) > 0


class StoreFrontTarget(InstacartTarget):
    def exists(self):
        return (
            self.browser.current_url
            == "https://www.instacart.com/store/wegmans/storefront"
        )


class DeliveryTimesModalTarget(InstacartTarget):
    def exists(self):
        return len(find_by_text(browser, "Available Scheduled Times") > 0)
