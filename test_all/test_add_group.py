# -*- coding: utf-8 -*-
from model.group import Group


def test_add_group(app):
    app.session.login()
    app.create_group(Group(name="testName", header="test", footer="test"))
    app.session.logout()
