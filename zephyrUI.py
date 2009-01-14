import bot
from bot import *

def send(mess):
    try:
        zephyr.ZNotice(cls='dodona-test', fields=["", mess], sender='dodona@ATHENA.MIT.EDU').send()
        print "dodona: " + mess
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
        m = zephyr.receive(True)
    print "From: ", m.sender
    print "Class: ", m.cls
    print "Instance: ", m.instance
    print "Message: ", m.__dict__['fields'][1]
    m = m.__dict__['fields'][1]
    m = m.strip()
    return m
    #return raw_input("--> ")
