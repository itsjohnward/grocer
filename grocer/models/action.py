

@inherits(BrowserOpen)
class Navigate(Task):
    requires = Requires()
    browser_open = Requirement(BrowserOpen)
    output = LoginPageTarget(browser)

    def run(self):
        buttons = browser.find_elements_by_css_selector("button")
        login_button = buttons[0]
        login_button.click()
        sleep(5)


@inherits(Prereq)
class Action(Task):
    def __init__(self, data_name, browser, page, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.requires = Requires()
        Requirement(page)
        output = TargetOutput(
            file_pattern=os.path.join("data", data_name, ""),
            ext=".parquet",
            target_class=ParquetTarget,
        )

    def run(self):
        self.output().write_dask(
            dd.from_pandas(self.detect_delivery_times(), chunksize=1)
        )