# -*- coding: utf-8 -*-
import random

from model.group import Group
import time
from random import randrange


def test_add_group(app, db, json_groups, check_ui):
    group = json_groups
    time.sleep(1)
    old_groups = db.get_group_list()
    app.group.create_group(group)
    new_groups = db.get_group_list()
    old_groups.append(group)
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)


def test_edit_some_group(db, app, check_ui):
    time.sleep(1)
    app.group.open_groups_page()
    if len(db.get_group_list()) == 0:
        app.group.create_group(Group(name="testName", header="test", footer="test"))
    old_groups = db.get_group_list()
    group = random.choice(old_groups)
    group.name = Group(name="testName1").name
    app.group.edit_group_by_id(group)
    assert len(old_groups) == app.group.count_groups()
    new_groups = db.get_group_list()
    assert sorted(old_groups, key=Group.id_or_max) == sorted(new_groups, key=Group.id_or_max)
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)


def test_delete_some_group(db, app, check_ui):
    time.sleep(1)
    app.group.open_groups_page()
    if len(db.get_group_list()) == 0:
        app.group.create_group(Group(name="testName2", header="test2", footer="test2"))
    old_groups = db.get_group_list()
    group = random.choice(old_groups)
    app.group.delete_group_by_id(group.id)
    time.sleep(5)
    new_groups = db.get_group_list()
    assert len(old_groups) - 1 == app.group.count_groups()
    old_groups.remove(group)
    assert old_groups == new_groups
    if check_ui:
        assert sorted(new_groups, key=Group.id_or_max) == sorted(app.group.get_group_list(), key=Group.id_or_max)
