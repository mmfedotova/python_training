# -*- coding: utf-8 -*-
import pytest
from group import Group
from application import Application

@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture
def test_add_group(app):
    app.login()
    app.create_group(Group(name="testName", header="test", footer="test"))
    app.logout()
