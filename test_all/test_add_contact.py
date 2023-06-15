# -*- coding: utf-8 -*-
from contact import Contact


def test_add_contact(app):
    app.login()
    app.create_contact(
        Contact(firstname="Sergei", middlename="Ivanovich", lastname="Smirmov", nickname="test", title="title",
                company="shop", address="Moscow", email="test@mail.com", email2="test2@mail.com",
                email3="test3@mail.com", homepage="test.com"))
    app.logout()
