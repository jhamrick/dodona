import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')
import zephyr
import helper
from helper import *

def send(mess, name = None):
    if name != None:
        mess = name + ": " + mess
    mess = mess.decode("utf-8")
    mess = custom_fill(mess)
    try:
        z = zephyr.ZNotice(cls='dodona-test', fields=["", mess], sender='dodona@ATHENA.MIT.EDU')
        foo = str(z.__dict__)
        z.send()
        print "Dodona: " + mess
    except:
        print "There was an error sending the last message."

#receive a zephyr not from yourself
def receive_from_subs(return_sender=False):
    try:
        m = zephyr.receive(True)
    except:
        return receive_from_subs()

    while m.sender == 'dodona@ATHENA.MIT.EDU':
        try:
            m = zephyr.receive(True)
        except:
            continue

    while m.__dict__['fields'][1].lower().strip() == "":
        try:
            m = zephyr.receive(True)
        except:
            continue

    while m.cls != "dodona-test":
        try:
            m = zephyr.receive(True)
        except:
            continue

    print "From: ", m.sender
    print "Class: ", m.cls
    print "Instance: ", m.instance
    print "Message: ", m.__dict__['fields'][1]
    sender = m.sender
    m = m.__dict__['fields'][1]
    m = str(m.strip().lower())
    if m.find("dodona, ") != -1:
        m = m.partition("dodona, ")[2]
    if return_sender:  return [m, sender]
    else:  return m
