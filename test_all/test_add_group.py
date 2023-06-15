# -*- coding: utf-8 -*-
from group import Group

def test_add_group(app):
    app.login()
    app.create_group(Group(name="testName", header="test", footer="test"))
    app.logout()
