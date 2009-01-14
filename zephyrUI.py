import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')
import zephyr
from textwrap import fill
from xml.dom import minidom
import zephyrUI
from zephyrUI import *
import fuzzystack
from fuzzystack import *
import time

def send(mess):
    try:
        z = zephyr.ZNotice(cls='dodona-test', fields=["", mess], sender='dodona@ATHENA.MIT.EDU')
        print z.__dict__
        foo = str(z.__dict__)
        time.sleep(1)
        z.send()
        #print "dodona: " + mess
    except:
        print "There was an error sending the last message."

#init
if __name__ != '__main__':
    zephyr.init()
    zephyr.Subscriptions().add(('dodona-test', '*', '*'))
    send(fill('Dodona is now running.  If you find that a topic you wish answered is not accounted for, please send mail to dodona AT mit DOT edu'))

#receive a zephyr not from yourself
def receive_from_subs():
    try:
        m = zephyr.receive(True)
    except:
        return receive_from_subs()

    while m.sender == 'dodona@ATHENA.MIT.EDU':
        try:
            m = zephyr.receive(True)
        except:
            return receive_from_subs()

    while m.__dict__['fields'][1].lower().find("dodona") == -1:
        try:
            m = zephyr.receive(True)
        except:
            return receive_from_subs()

    print "From: ", m.sender
    print "Class: ", m.cls
    print "Instance: ", m.instance
    print "Message: ", m.__dict__['fields'][1]
    m = m.__dict__['fields'][1]
    m = m.strip()
    return m
    
    #while True:
    #    mess = raw_input("--> ")
    #    if mess.lower().find("dodona") != -1:
    #        return mess
