from luigi import Target


class PageAnchor(Target):
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
