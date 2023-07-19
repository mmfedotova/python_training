# -*- coding: utf-8 -*-
import time
import pytest

from model.contact import Contact
from random import randrange
import random
import string
import re


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


def test_contact_on_home_page(app):
    contact_from_home_page = app.contact.get_contact_list()[0]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    assert contact_from_home_page.all_phones_from_home_page == merge_phones_like_on_home_page(contact_from_edit_page)
    assert contact_from_home_page.all_emails_from_home_page == merge_emails_like_on_home_page(contact_from_edit_page)
    assert contact_from_home_page.firstname == contact_from_edit_page.firstname
    assert contact_from_home_page.lastname == contact_from_edit_page.lastname


def test_contact_on_contact_view_page(app):
    contact_from_view_page = app.contact.get_contact_from_view_page(0)
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(0)
    assert merge_fullname_like_on_home_page(contact_from_edit_page) == contact_from_view_page.fullname
    assert contact_from_view_page.homephone == contact_from_edit_page.homephone
    assert contact_from_view_page.workphone == contact_from_edit_page.workphone
    assert contact_from_view_page.mobilephone == contact_from_edit_page.mobilephone
    assert contact_from_view_page.secondaryphone == contact_from_edit_page.secondaryphone
    assert contact_from_view_page.email == contact_from_edit_page.email
    assert contact_from_view_page.email2 == contact_from_edit_page.email2
    assert contact_from_view_page.email3 == contact_from_edit_page.email3


def clear(s):
    return re.sub("[() -]", "", s)


def merge_phones_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "",
                            map(lambda x: clear(x),
                                filter(lambda x: x is not None,
                                       [contact.homephone, contact.mobilephone, contact.workphone,
                                        contact.secondaryphone]))))


def merge_emails_like_on_home_page(contact):
    return "\n".join(filter(lambda x: (x != "" and (x is not None)),
                            [contact.email, contact.email2, contact.email3]))


def merge_fullname_like_on_home_page(contact):
    return " ".join(filter(lambda x: (x != "" and (x is not None)),
                           [contact.firstname, contact.middlename, contact.lastname]))
