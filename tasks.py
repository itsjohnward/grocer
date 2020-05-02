

class Page(Task):
    def requires(self):
        pass

    def output(self):
        pass

    def run(self):
        pass

class LoginPage(Task):
    Requires(BrowserOpenTarget)
    Outputs(LoginPageTarget)

    def run(self):
        # Open browser to login page

class Login(Task):
    Requires(LoginPageTarget)
    Outputs(LoggedInTarget)

    def run(self):
        # fill in form and click login

class MainPage(Task):
    Requires(LoggedInTarget)
    Outputs(MainPageTarget) # so if Login already brought me here, I'm fine. Skip

    def run(self):
        # find header button and click it

class DeliveryTimesModal(Task):
    Requires(MainPageTarget)
    Outputs(DeliveryTimesModalTarget)

    def run(self):
        # find delivery times button and click it