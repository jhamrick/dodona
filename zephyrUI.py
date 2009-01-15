import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')
import zephyr
import time

def send(mess):
    mess = mess.decode("utf-8")
    try:
        z = zephyr.ZNotice(cls='dodona-test', fields=["", mess], sender='dodona@ATHENA.MIT.EDU')
        foo = str(z.__dict__)
        z.send()
        print "Dodona: " + mess
    except:
        print "There was an error sending the last message."

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

    while m.__dict__['fields'][1].lower().strip() == "":
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
    #if mess.lower().find("dodona") != -1:
#    return mess.lower()
