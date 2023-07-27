import random
import string
from model.contact import Contact
import os.path
import getopt
import jsonpickle
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of contact", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)
n = 5
f = "data/contacts.json"

for  o, a  in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a
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
               for i in range(n)]


file = os.path.join((os.path.dirname(os.path.abspath(__file__))), "..", f)

with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))
