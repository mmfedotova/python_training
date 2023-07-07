# -*- coding: utf-8 -*-
import time

from model.contact import Contact
from random import randrange


def test_add_contact(app):
    time.sleep(1)
    old_contacts = app.contact.get_contact_list()
    contact = Contact(firstname="Sergei", middlename="Ivanovich", lastname="Smirmov", nickname="test",
                      homephone="12132", mobilephone="22122",
                      workphone="21223", secondaryphone="1121222", title="title",
                      company="shop", address="Moscow", email="test@mail.com", email2="test2@mail.com",
                      email3="test3@mail.com", homepage="test.com")
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
