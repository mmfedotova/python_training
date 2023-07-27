# -*- coding: utf-8 -*-

from model.group import Group
import time
from random import randrange


def test_add_group(app, json_groups):
    group = json_groups
    time.sleep(1)
    old_groups = app.group.get_group_list()
    app.group.create_group(group)
    assert len(old_groups) + 1 == app.group.count_groups()
    new_groups = app.group.get_group_list()
    old_groups.append(group)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)


def test_edit_some_group(app):
    time.sleep(1)
    app.group.open_groups_page()
    if app.group.count_groups() == 0:
        app.group.create_group(Group(name="testName", header="test", footer="test"))
    old_groups = app.group.get_group_list()
    index = randrange(len(old_groups))
    group = Group(name="testName1", header="test1", footer="test1")
    group.id = old_groups[index].id
    app.group.edit_group_by_index(group, index)
    assert len(old_groups) == app.group.count_groups()
    new_groups = app.group.get_group_list()
    old_groups[index] = group
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)


def test_delete_some_group(app):
    time.sleep(1)
    app.group.open_groups_page()
    if app.group.count_groups() == 0:
        app.group.create_group(Group(name="testName2", header="test2", footer="test2"))
    old_groups = app.group.get_group_list()
    index = randrange(len(old_groups))
    app.group.delete_group_by_index(index)
    time.sleep(5)
    assert len(old_groups) - 1 == app.group.count_groups()
    new_groups = app.group.get_group_list()
    old_groups[index:index + 1] = []
    assert old_groups == new_groups
