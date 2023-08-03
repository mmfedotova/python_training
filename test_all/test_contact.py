# -*- coding: utf-8 -*-
import time
import pytest

from model.contact import Contact
import random
import re


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
    contact = random.choice(old_contacts)
    contact.firstname = Contact(firstname="Ivan").firstname
    app.contact.edit_contact_by_id(contact)
    assert len(old_contacts) == len(db.get_contact_list())
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
