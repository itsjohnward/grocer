from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def find_by_text(browser, text):
    return browser.find_elements_by_xpath("//*[text()='{}']".format(text))


def get_browser(headless=False):
    opts = Options()
    if headless:
        opts.set_headless()
    return Chrome("/Users/john/csci-e-29/grocer/chromedriver", options=opts)


def get_children(element):
    for elem in element.find_elements_by_xpath(".//*"):
        yield elem


def get_parent(element):
    return element.find_elements_by_xpath("..")[0]


def get_siblings(element):
    for elem in element.find_elements_by_xpath("../*"):
        yield elem
