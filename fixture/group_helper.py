class GroupHelper:
    def __init__(self, app):
        self.app = app
        self.wd = self.app.wd

    def return_to_group_page(self):
        wd = self.wd
        wd.find_element_by_id("header").click()
        wd.find_element_by_link_text("groups").click()

    def create_group(self, group):
        wd = self.wd
        self.open_groups_page()
        # init group creation
        wd.find_element_by_name("new").click()
        # fill group form
        self.fill_groups_form(group)
        # submit group creation
        wd.find_element_by_name("submit").click()
        self.return_to_group_page()

    def open_groups_page(self):
        wd = self.wd
        wd.find_element_by_link_text("groups").click()

    def select_first_group(self):
        wd = self.wd
        wd.find_element_by_name("selected[]").click()

    def delete_first_group(self):
        wd = self.wd
        self.open_groups_page()
        self.select_first_group()
        wd.find_element_by_name("delete").click()
        self.return_to_group_page()

    def edit_first_group(self, group):
        wd = self.wd
        self.open_groups_page()
        self.select_first_group()
        wd.find_element_by_name("edit").click()
        self.fill_groups_form(group)
        wd.find_element_by_name("update").click()
        self.return_to_group_page()

    def fill_groups_form(self, group):
        wd = self.wd
        wd.find_element_by_name("group_name").click()
        wd.find_element_by_name("group_name").clear()
        wd.find_element_by_name("group_name").send_keys(group.name)
        wd.find_element_by_name("group_header").click()
        wd.find_element_by_name("group_header").clear()
        wd.find_element_by_name("group_header").send_keys(group.header)
        wd.find_element_by_name("group_footer").click()
        wd.find_element_by_name("group_footer").clear()
        wd.find_element_by_name("group_footer").send_keys(group.footer)

    def count_groups(self):
        wd = self.wd
        self.open_groups_page()
        return len(wd.find_elements_by_name("selected[]"))
