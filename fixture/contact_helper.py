from selenium.webdriver.support.ui import Select
from model.contact import Contact
import re


class ContactHelper:
    def __init__(self, app):
        self.app = app
        self.wd = self.app.wd

    def create_contact(self, contact):
        wd = self.wd
        self.open_add_contact_page()
        self.fill_contact_form(contact)
        self.app.return_to_home_page()
        self.contact_cache = None

    def open_add_contact_page(self):
        wd = self.wd
        if not wd.current_url.endswith("/edit.php"):
            wd.find_element_by_link_text("add new").click()

    def delete_first_contact(self):
        self.delete_contact_by_index(0)

    def delete_contact_by_index(self, index):
        wd = self.wd
        wd.find_elements_by_name("selected[]")[index].click()
        wd.find_element_by_xpath("//input[@type='button' and @value='Delete']").click()
        wd.switch_to.alert.accept()
        # self.app.return_to_home_page()
        self.app.open_home_page()
        self.contact_cache = None

    def select_contact_by_id(self, id):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_css_selector("input[value='%s']" % id).click()

    def select_contact_for_add_by_id(self, contact):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_css_selector("input[value='%s']" % contact.id).click()

    def add_contact_to_group_by_id(self, contact, group):
        wd = self.app.wd
        self.select_contact_for_add_by_id(contact)
        wd.find_element_by_xpath("//select[@name='to_group']/option[@value='%s']" % group.id).click()
        wd.find_element_by_xpath("//input[@type='submit' and @name='add']").click()

    def delete_contact_from_group_by_id(self, contact, group):
        wd = self.app.wd
        self.select_contact_by_id(contact.id)
        # TODO поправить на нужный select
        wd.find_element_by_xpath("//select[@name='to_group']/option[@value='%s']" % group.id).click()
        wd.find_element_by_xpath("//input[@type='submit' and @name='remove']").click()

    def delete_contact_by_id(self, id):
        wd = self.wd
        self.select_contact_by_id(id)
        wd.find_element_by_xpath("//input[@type='button' and @value='Delete']").click()
        wd.switch_to.alert.accept()
        # self.app.return_to_home_page()
        self.app.open_home_page()
        self.contact_cache = None

    def edit_first_contact(self):
        self.edit_contact_by_index(0)

    def open_contact_to_edit_by_index(self, index):
        wd = self.wd
        self.app.open_home_page()
        wd.find_elements_by_css_selector("img[title = 'Edit']")[index].click()

    def open_contact_to_edit_by_id(self, id):
        wd = self.wd
        self.app.open_home_page()
        wd.find_element_by_xpath("//*[@id='%s']/../..//*[@title='Edit']" % id).click()

    def open_contact_view_by_index(self, index):
        wd = self.wd
        self.app.open_home_page()
        wd.find_elements_by_css_selector("img[title = 'Details']")[index].click()

    def select_group_of_contact_by_id(self, group):
        wd = self.wd
        self.app.open_home_page()
        wd.find_element_by_xpath("//select[@name='group']/option[@value='%s']" % group.id).click()

    def edit_contact_by_index(self, contact, index):
        wd = self.wd
        self.open_contact_to_edit_by_index(index)
        self.fill_contact_form(contact)
        wd.find_element_by_name("update").click()
        self.app.return_to_home_page()
        self.contact_cache = None

    def edit_contact_by_id(self, contact):
        wd = self.wd
        self.open_contact_to_edit_by_id(contact.id)
        self.fill_contact_form(contact)
        wd.find_element_by_name("update").click()
        self.app.return_to_home_page()
        self.contact_cache = None

    def fill_contact_form(self, contact):
        wd = self.wd
        wd.find_element_by_name("firstname").click()
        wd.find_element_by_name("firstname").clear()
        wd.find_element_by_name("firstname").send_keys(contact.firstname)
        wd.find_element_by_name("middlename").click()
        wd.find_element_by_name("middlename").clear()
        wd.find_element_by_name("middlename").send_keys(contact.middlename)
        # wd.find_element_by_name("theform").click()
        wd.find_element_by_name("lastname").click()
        wd.find_element_by_name("lastname").clear()
        wd.find_element_by_name("lastname").send_keys(contact.lastname)
        wd.find_element_by_name("nickname").click()
        wd.find_element_by_name("nickname").clear()
        wd.find_element_by_name("nickname").send_keys(contact.nickname)
        # wd.find_element_by_name("photo").click()
        # wd.find_element_by_name("photo").clear()
        # wd.find_element_by_name("photo").send_keys("C:\\fakepath\\test_photo.png")
        wd.find_element_by_name("title").click()
        wd.find_element_by_name("title").clear()
        wd.find_element_by_name("title").send_keys(contact.title)
        wd.find_element_by_name("company").click()
        wd.find_element_by_name("company").clear()
        wd.find_element_by_name("company").send_keys(contact.company)
        wd.find_element_by_name("address").click()
        wd.find_element_by_name("address").clear()
        wd.find_element_by_name("address").send_keys(contact.address)
        wd.find_element_by_name("home").click()
        wd.find_element_by_name("home").clear()
        wd.find_element_by_name("home").send_keys(contact.homephone)
        wd.find_element_by_name("mobile").click()
        wd.find_element_by_name("mobile").clear()
        wd.find_element_by_name("mobile").send_keys(contact.mobilephone)
        wd.find_element_by_name("work").click()
        wd.find_element_by_name("work").clear()
        wd.find_element_by_name("work").send_keys(contact.workphone)
        wd.find_element_by_name("fax").click()
        wd.find_element_by_name("fax").clear()
        wd.find_element_by_name("fax").send_keys("09992")
        wd.find_element_by_name("email").click()
        wd.find_element_by_name("email").clear()
        wd.find_element_by_name("email").send_keys(contact.email)
        wd.find_element_by_name("email2").click()
        wd.find_element_by_name("email2").clear()
        wd.find_element_by_name("email2").send_keys(contact.email2)
        wd.find_element_by_name("email3").click()
        wd.find_element_by_name("email3").clear()
        wd.find_element_by_name("email3").send_keys(contact.email3)
        wd.find_element_by_name("homepage").click()
        wd.find_element_by_name("homepage").clear()
        wd.find_element_by_name("homepage").send_keys(contact.homepage)
        wd.find_element_by_name("bday").click()
        Select(wd.find_element_by_name("bday")).select_by_visible_text("10")
        wd.find_element_by_xpath("//option[@value='10']").click()
        wd.find_element_by_name("bmonth").click()
        Select(wd.find_element_by_name("bmonth")).select_by_visible_text("January")
        wd.find_element_by_xpath("//option[@value='January']").click()
        wd.find_element_by_name("byear").click()
        wd.find_element_by_name("byear").clear()
        wd.find_element_by_name("byear").send_keys("1998")
        wd.find_element_by_name("aday").click()
        Select(wd.find_element_by_name("aday")).select_by_visible_text("14")
        wd.find_element_by_xpath("//div[@id='content']/form/select[3]/option[15]").click()
        wd.find_element_by_name("amonth").click()
        Select(wd.find_element_by_name("amonth")).select_by_visible_text("February")
        wd.find_element_by_xpath("//div[@id='content']/form/select[4]/option[3]").click()
        wd.find_element_by_name("ayear").click()
        wd.find_element_by_name("ayear").clear()
        wd.find_element_by_name("ayear").send_keys("2013")
        wd.find_element_by_name("address2").send_keys("none")
        wd.find_element_by_name("phone2").click()
        wd.find_element_by_name("phone2").clear()
        wd.find_element_by_name("phone2").send_keys(contact.secondaryphone)
        wd.find_element_by_name("notes").click()
        wd.find_element_by_name("notes").clear()
        wd.find_element_by_name("notes").send_keys("call after")
        wd.find_element_by_xpath("//div[@id='content']/form/input[21]").click()

    def count_contacts(self):
        wd = self.wd
        self.app.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.app.open_home_page()
            self.contact_cache = []
            for row in wd.find_elements_by_xpath("//tr[@name='entry']"):
                cells = row.find_elements_by_tag_name("td")
                lastname = cells[1].text
                firstname = cells[2].text
                id = cells[0].find_element_by_name("a").get_attribute("value")
                all_phones = cells[5].text
                all_emails = cells[4].text
                self.contact_cache.append(
                    Contact(firstname=firstname, lastname=lastname, id=id,
                            all_phones_from_home_page=all_phones,
                            all_emails_from_home_page=all_emails))
        return list(self.contact_cache)

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_contact_to_edit_by_index(index)
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        middlename = wd.find_element_by_name("middlename").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        id = wd.find_element_by_name("id").get_attribute("value")
        homephone = wd.find_element_by_name("home").get_attribute("value")
        mobilephone = wd.find_element_by_name("mobile").get_attribute("value")
        workphone = wd.find_element_by_name("work").get_attribute("value")
        secondaryphone = wd.find_element_by_name("phone2").get_attribute("value")
        email = wd.find_element_by_name("email").get_attribute("value")
        email2 = wd.find_element_by_name("email2").get_attribute("value")
        email3 = wd.find_element_by_name("email3").get_attribute("value")
        return Contact(firstname=firstname, middlename=middlename, lastname=lastname,
                       homephone=homephone, mobilephone=mobilephone,
                       workphone=workphone, secondaryphone=secondaryphone, email=email, email2=email2, email3=email3,
                       id=id)

    def get_contact_from_view_page(self, index):
        wd = self.app.wd
        self.open_contact_view_by_index(index)
        text = wd.find_element_by_id("content").text
        fullname = wd.find_element_by_xpath("//div[@id='content']/b").text
        homephone = re.search("H: (.*)", text).group(1)
        mobilephone = re.search("M: (.*)", text).group(1)
        workphone = re.search("W: (.*)", text).group(1)
        secondaryphone = re.search("P: (.*)", text).group(1)
        email = wd.find_elements_by_xpath("//a[contains (@href,'mailto:')]")[0].text
        email2 = wd.find_elements_by_xpath("//a[contains (@href,'mailto:')]")[1].text
        email3 = wd.find_elements_by_xpath("//a[contains (@href,'mailto:')]")[2].text
        return Contact(fullname=fullname, homephone=homephone, mobilephone=mobilephone,
                       workphone=workphone, secondaryphone=secondaryphone, email=email, email2=email2, email3=email3)
