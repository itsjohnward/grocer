import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


BROWSER_REGISTRY = {}


def get_browser(merchant, headless=False, no_sandbox=False):
    # TODO support multiple concurrent users
    if merchant in BROWSER_REGISTRY:
        return BROWSER_REGISTRY[merchant]
    opts = Options()
    if headless:
        opts.set_headless()
    if no_sandbox:
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
    browser = Chrome(os.environ["CHROMEDRIVER_PATH"], options=opts)
    # save the browser instance in a registry so it can be re-used
    BROWSER_REGISTRY[merchant] = browser
    return browser


def find_by_text(browser, text):
    return browser.find_elements_by_xpath("//*[text()='{}']".format(text))


def get_children(element):
    for elem in element.find_elements_by_xpath(".//*"):
        yield elem


def get_parent(element):
    return element.find_elements_by_xpath("..")[0]


def get_siblings(element):
    for elem in element.find_elements_by_xpath("../*"):
        yield elem
