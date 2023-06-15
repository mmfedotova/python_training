from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from fixture.session import SessionHelper
from fixture.group_helper import GroupHelper
from fixture.contact_helper import ContactHelper


class Application:
    def __init__(self):
        self.wd = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        self.wd.implicitly_wait(30)
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)
        self.contact = ContactHelper(self)

    def open_home_page(self):
        wd = self.wd
        wd.get("http://localhost/addressbook/")

    def return_to_home_page(self):
        wd = self.wd
        wd.find_element_by_link_text("home page").click()

    def destroy(self):
        self.wd.quit()
