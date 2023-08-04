# -*- coding: utf-8 -*-
import time
import pytest

from model.contact import Contact
import random
import re
from fixture.orm import ORMFixture


def test_add_contact(app, db, json_contacts, check_ui):
    contact = json_contacts
    time.sleep(1)
    old_contacts = db.get_contact_list()
    app.contact.create_contact(contact)
    assert len(old_contacts) + 1 == app.contact.count_contacts()
    new_contacts = db.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(),
                                                                     key=Contact.id_or_max)


def test_add_contact_to_group(app, db):
    orm = ORMFixture(host="127.0.0.1", name="addressbook", user="root", password="")
    app.open_home_page()
    old_contacts = db.get_contact_list()
    old_groups = db.get_group_list()
    group = random.choice(old_groups)
    contact = random.choice(old_contacts)
    app.contact.add_contact_to_group_by_id(group, contact)
    assert contact in orm.get_contacts_in_group(group)


def test_edit_some_contact(app, db, check_ui):
    time.sleep(1)
    app.open_home_page()
    if app.contact.count_contacts() == 0:
        app.contact.create_contact(
            Contact(firstname="Sergei", middlename="Ivanovich", lastname="Smirmov", nickname="test", homephone="12132",
                    mobilephone="22122",
                    workphone="21223", secondaryphone="1121222", title="title",
                    company="shop", address="Moscow", email="test@mail.com", email2="test2@mail.com",
                    email3="test3@mail.com", homepage="test.com"))
    old_contacts = db.get_contact_list()
    edit_contact = random.choice(old_contacts)
    contact = Contact(firstname="Ivan", middlename="Semenovich", lastname="Ivanov", nickname="tester",
                      homephone="12132", mobilephone="22122",
                      workphone="21223", secondaryphone="1121222", title="title1",
                      company="shop1", address="NY", email="test@gmail.com", email2="test2@gmail.com",
                      email3="test3@gmail.com", homepage="tester.com")
    contact.id = edit_contact.id
    index = old_contacts.index(edit_contact)
    app.contact.edit_contact_by_id(contact)
    assert len(old_contacts) == len(db.get_contact_list())
    old_contacts[index] = contact
    new_contacts = db.get_contact_list()
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(),
                                                                     key=Contact.id_or_max)


def test_delete_some_contact(app, db, check_ui):
    time.sleep(1)
    app.open_home_page()
    if len(db.get_contact_list()) == 0:
        app.contact.create_contact(
            Contact(firstname="Sergei", middlename="Ivanovich", lastname="Smirmov", nickname="test", homephone="12132",
                    mobilephone="22122",
                    workphone="21223", secondaryphone="1121222", title="title",
                    company="shop", address="Moscow", email="test@mail.com", email2="test2@mail.com",
                    email3="test3@mail.com", homepage="test.com"))
    old_contacts = db.get_contact_list()
    contact = random.choice(old_contacts)
    app.contact.delete_contact_by_id(contact.id)
    time.sleep(1)
    assert len(old_contacts) - 1 == app.contact.count_contacts()
    new_contacts = db.get_contact_list()
    old_contacts.remove(contact)
    assert old_contacts == new_contacts
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(),
                                                                     key=Contact.id_or_max)


def test_contact_on_home_page(app, db):
    contacts_from_db = sorted(db.get_contact_list(), key=Contact.id_or_max)
    contacts_from_home_page = sorted(app.contact.get_contact_list(), key=Contact.id_or_max)
    for i in range(len(contacts_from_db)):
        assert contacts_from_home_page[i].lastname == contacts_from_db[i].lastname
        assert contacts_from_home_page[i].firstname == contacts_from_db[i].firstname
        assert contacts_from_home_page[i].all_emails_from_home_page == merge_emails_like_on_home_page(
            contacts_from_db[i])
        assert contacts_from_home_page[i].all_phones_from_home_page == merge_phones_like_on_home_page(
            contacts_from_db[i])


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
