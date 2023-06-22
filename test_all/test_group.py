# -*- coding: utf-8 -*-
from model.group import Group
import time


def test_add_group(app):
    time.sleep(1)
    app.group.create_group(Group(name="testName", header="test", footer="test"))


def test_edit_first_group(app):
    time.sleep(1)
    app.group.open_groups_page()
    if app.group.count_groups() == 0:
        app.group.create_group(Group(name="testName", header="test", footer="test"))
    app.group.edit_first_group(Group(name="testName1", header="test1", footer="test1"))


def test_delete_first_group(app):
    time.sleep(1)
    app.group.open_groups_page()
    if app.group.count_groups() == 0:
        app.group.create_group(Group(name="testName2", header="test2", footer="test2"))
    app.group.delete_first_group()
