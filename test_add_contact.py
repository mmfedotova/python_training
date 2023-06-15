# -*- coding: utf-8 -*-
import pytest
from contact import Contact
from application import Application

@pytest.fixture
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture

def test_add_contact(app):
    app.login()
    app.create_contact(Contact(firstname= "Sergei", middlename="Ivanovich", lastname="Smirmov", nickname= "test", title="title", company="shop", address="Moscow", email="test@mail.com", email2= "test2@mail.com", email3="test3@mail.com", homepage= "test.com"))
    app.logout()

