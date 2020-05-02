def find_by_text(browser, text):
    return browser.find_elements_by_xpath("//*[text()='{}']".format(text))


def get_browser(headless=False):
    opts = Options()
    if headless:
        opts.set_headless()
    return Chrome("/Users/john/csci-e-29/grocer/chromedriver", options=opts)


def get_child_text(element):
    for elem in element.find_elements_by_xpath(".//*"):
        yield elem.text


def get_parent(element):
    return element.find_elements_by_xpath("..")[0]
