import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')
import zephyr
from helper import custom_fill

class = ""

def init(c = "dodona-test"):
    """
    Initializes the python-zephyr utilities.
    """
    class = c
    # initialize zephyr
    zephyr.init()
    # subscribe to the specified class
    zephyr.Subscriptions().add((class, '*', '*'))
    # send an initialization message
    send(custom_fill('Dodona is now running.  If you find that a topic you wish answered is not accounted for, please send mail to dodona AT mit DOT edu'))

def send(mess, name = None):
    """
    Sends a zephyr to the specified class, addressing
    a specific person if specified.
    """
    if name != None:
        mess = name + ": " + mess

    mess = mess.decode("utf-8") # decode the message
    mess = custom_fill(mess)
    # try to send the message
    try:
        z = zephyr.ZNotice(cls=class, fields=["", mess], sender='dodona@ATHENA.MIT.EDU')
        foo = str(z.__dict__)
        z.send()
        #print "Dodona: " + mess
    except:
        print "There was an error sending the last message."

def receive_from_subs(return_sender=False):
    """
    Receive a message from the class specified in the 
    init method, and returns the message and the sender of the
    message if return_sender is True.
    """
    received = False
    while not received: # loop until you recieve a message
        try:
            m = zephyr.receive(True)
            received = True
        except:
            continue

    # ignore messages from yourself
    while m.sender == 'dodona@ATHENA.MIT.EDU':
        try:
            m = zephyr.receive(True)
        except:
            continue

    # ignore empty messages
    while m.__dict__['fields'][1].lower().strip() == "":
        try:
            m = zephyr.receive(True)
        except:
            continue

    # ignore messages from anywhere except the specified
    # class
    while m.cls != class:
        try:
            m = zephyr.receive(True)
        except:
            continue

    print "From: ", m.sender
    print "Instance: ", m.instance
    print "Message: ", m.__dict__['fields'][1]

    sender = m.sender
    m = m.__dict__['fields'][1]
    # clean the message of trailing whitespce
    # and convert it to lowercase
    m = str(m.strip().lower())

    if return_sender:  return [m, sender]
    else:  return m
