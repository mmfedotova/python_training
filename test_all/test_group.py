# -*- coding: utf-8 -*-
from model.group import Group
import time


def test_add_group(app):
    time.sleep(1)
    old_groups = app.group.get_group_list()
    group = Group(name="testName", header="test", footer="test")
    app.group.create_group(group)
    new_groups = app.group.get_group_list()
    assert len(old_groups) + 1 == len(new_groups)
    old_groups.append(group)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)


def test_edit_first_group(app):
    time.sleep(1)
    app.group.open_groups_page()
    if app.group.count_groups() == 0:
        app.group.create_group(Group(name="testName", header="test", footer="test"))
    old_groups = app.group.get_group_list()
    group = Group(name="testName1", header="test1", footer="test1")
    group.id = old_groups[0].id
    app.group.edit_first_group(group)
    new_groups = app.group.get_group_list()
    assert len(old_groups) == len(new_groups)
    old_groups[0] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)


def test_delete_first_group(app):
    time.sleep(1)
    app.group.open_groups_page()
    if app.group.count_groups() == 0:
        app.group.create_group(Group(name="testName2", header="test2", footer="test2"))
    old_groups = app.group.get_group_list()
    app.group.delete_first_group()
    time.sleep(5)
    new_groups = app.group.get_group_list()
    assert len(old_groups) - 1 == len(new_groups)
    old_groups[0:1] = []
    assert old_groups == new_groups
