# -*- coding: utf-8 -*-
import pytest

from model.group import Group
import time
from random import randrange
import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [Group(name="", header="", footer="")] + [
    Group(name=random_string("name", 10), header=random_string("header", 20), footer=random_string("footer", 20))
    for i in range(5)]


@pytest.mark.parametrize("group", testdata, ids=[repr(x) for x in testdata])
def test_add_group(app, group):
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
