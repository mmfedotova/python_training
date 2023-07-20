from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import IEDriverManager
from fixture.session import SessionHelper
from fixture.group_helper import GroupHelper
from fixture.contact_helper import ContactHelper


class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        elif browser == "chrome":
            self.wd = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        elif browser == "ie":
            self.wd = webdriver.Ie(executable_path=IEDriverManager().install())
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.wd.implicitly_wait(2)
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)
        self.contact = ContactHelper(self)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        if not wd.current_url.endswith("/addressbook/"):
            wd.get(self.base_url)

    def return_to_home_page(self):
        wd = self.wd
        if not wd.current_url.endswith("/addressbook/"):
            wd.find_element_by_link_text("home page").click()

    def destroy(self):
        self.wd.quit()
