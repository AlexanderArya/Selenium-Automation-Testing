from pages.base_page import BasePage


class GooglePage(BasePage):

    URL = "https://www.google.com"

    def open(self):
        self.driver.get(self.URL)
