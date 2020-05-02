class InstacartTarget(Target):
    def __init__(self, browser, *args, **kwargs):
        self.browser = browser
        super().__init__(*args, **kwargs)

    def exists(self):
        pass


class WelcomePageTarget(Target):
    def exists(self):
        # has login links
        pass


class LoginPageTarget(InstacartTarget):
    def exists(self):
        # has sign-in form
        pass


class MainPageTarget(Target):
    def exists(self):
        # has delivery times link
        pass


class DeliveryTimesModalTarget(Target):
    def exists(self):
        # has deliver times
        pass


class CartModelTarget(Target):
    def exists(self):
        # has cart items and checkout link
        pass


class CheckoutTarget(Target):
    def exists(self):
        # has payment info
        pass
