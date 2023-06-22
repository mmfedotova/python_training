# -*- coding: utf-8 -*-
import time

from model.contact import Contact


def test_add_contact(app):
    time.sleep(1)
    app.contact.create_contact(
        Contact(firstname="Sergei", middlename="Ivanovich", lastname="Smirmov", nickname="test", title="title",
                company="shop", address="Moscow", email="test@mail.com", email2="test2@mail.com",
                email3="test3@mail.com", homepage="test.com"))


def test_edit_first_contact(app):
    time.sleep(1)
    app.open_home_page()
    app.contact.edit_first_contact(
        Contact(firstname="Ivan", middlename="Semenovich", lastname="Ivanov", nickname="tester", title="title1",
                company="shop1", address="NY", email="test@gmail.com", email2="test2@gmail.com",
                email3="test3@gmail.com", homepage="tester.com"))


def test_delete_first_contact(app):
    time.sleep(1)
    app.open_home_page()
    app.contact.delete_first_contact()