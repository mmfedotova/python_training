# -*- coding: utf-8 -*-
import time
import pytest

from model.contact import Contact
from random import randrange
import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " " * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [Contact(firstname="", middlename="",
                    lastname="",
                    nickname="",
                    homephone="", mobilephone="",
                    workphone="", secondaryphone="",
                    title="",
                    company="", address="", email="", email2="",
                    email3="", homepage="")] + [
               Contact(firstname=random_string("firstname", 10), middlename=random_string("middlename", 10),
                       lastname=random_string("lastname", 10),
                       nickname=random_string("nickname", 10),
                       homephone=random_string("homephone", 10), mobilephone=random_string("mobilephone", 10),
                       workphone=random_string("workphone", 10), secondaryphone=random_string("secondaryphone", 10),
                       title=random_string("title", 10),
                       company="shop", address="Moscow", email="test@mail.com", email2="test2@mail.com",
                       email3="test3@mail.com", homepage="test.com")
               for i in range(5)]


@pytest.mark.parametrize("contact", testdata, ids=[repr(x) for x in testdata])
def test_add_contact(app, contact):
    time.sleep(1)
    old_contacts = app.contact.get_contact_list()
    app.contact.create_contact(contact)
    assert len(old_contacts) + 1 == app.contact.count_contacts()
    new_contacts = app.contact.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)


def test_edit_some_contact(app):
    time.sleep(1)
    app.open_home_page()
    if app.contact.count_contacts() == 0:
        app.contact.create_contact(
            Contact(firstname="Sergei", middlename="Ivanovich", lastname="Smirmov", nickname="test", homephone="12132",
                    mobilephone="22122",
                    workphone="21223", secondaryphone="1121222", title="title",
                    company="shop", address="Moscow", email="test@mail.com", email2="test2@mail.com",
                    email3="test3@mail.com", homepage="test.com"))
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact = Contact(firstname="Ivan", middlename="Semenovich", lastname="Ivanov", nickname="tester",
                      homephone="12132", mobilephone="22122",
                      workphone="21223", secondaryphone="1121222", title="title1",
                      company="shop1", address="NY", email="test@gmail.com", email2="test2@gmail.com",
                      email3="test3@gmail.com", homepage="tester.com")
    contact.id = old_contacts[index].id
    app.contact.edit_contact_by_index(contact, index)
    assert len(old_contacts) == app.contact.count_contacts()
    new_contacts = app.contact.get_contact_list()
    old_contacts[index] = contact
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)


def test_delete_some_contact(app):
    time.sleep(1)
    app.open_home_page()
    if app.contact.count_contacts() == 0:
        app.contact.create_contact(
            Contact(firstname="Sergei", middlename="Ivanovich", lastname="Smirmov", nickname="test", homephone="12132",
                    mobilephone="22122",
                    workphone="21223", secondaryphone="1121222", title="title",
                    company="shop", address="Moscow", email="test@mail.com", email2="test2@mail.com",
                    email3="test3@mail.com", homepage="test.com"))
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    app.contact.delete_contact_by_index(index)
    time.sleep(1)
    assert len(old_contacts) - 1 == app.contact.count_contacts()
    new_contacts = app.contact.get_contact_list()
    old_contacts[index:index + 1] = []
    assert old_contacts == new_contacts
