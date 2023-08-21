from model.group import Group
from model.contact import Contact


def test_group_list(app, db):
    ui_list = app.group.get_group_list()

    def clean(group):
        return Group(id=group.id, name=group.name.strip())

    db_list = map(clean, db.get_group_list())
    assert sorted(ui_list, key=Group.id_or_max) == sorted(db_list, key=Group.id_or_max)


def test_contact_list(app, db):
    def clean(contact):
        return Contact(id=contact.id, firstname=contact.firstname.replace(" ", ""),
                       lastname=contact.lastname.replace(" ", ""))

    ui_list = map(clean, app.contact.get_contact_list())

    db_list = map(clean, db.get_contact_list())

    assert sorted(ui_list, key=Contact.id_or_max) == sorted(db_list, key=Contact.id_or_max)
