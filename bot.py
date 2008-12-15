import site
site.addsitedir('/mit/broder/lib/python2.5/site-packages')
import zephyr
from textwrap import fill


topics = {}
t = open("topics")
for line in t:
    if line.startswith("NEWTOPIC "):
        line = line.partition("NEWTOPIC ")[2]
        part = line.partition(": ")
        topics[part[0]] = part[2]

#print topics
def send(mess):
    zephyr.ZNotice(cls='dodona-test', fields=["", mess], sender='dodona@ATHENA.MIT.EDU').send()

#init
zephyr.init()
zephyr.Subscriptions().add(('dodona-test', '*', '*'))
send('dodona is now running.  If you find\nthat a topic you wish answered is not accounted for, please send mail\nto dodona AT mit DOT edu')

#receive a zephyr not from yourself
def receive_from_subs():
    m = zephyr.receive(True)
    while m.sender == 'dodona@ATHENA.MIT.EDU':
        m = zephyr.receive(True)
    print "From: ", m.sender
    print "Class: ", m.cls
    print "Instance: ", m.instance
    print "Message: ", m.__dict__['fields'][1]
    return m

#get and answer a question
def question():
    m = receive_from_subs()
    mess = m.__dict__['fields'][1]
    mess = mess.strip()
    #send('You asked me about: ' + mess)
    #print topics.keys()
    if topics.has_key(mess):
        send(fill(topics[mess]))
    else:
        send('Sorry, I don\'t understand what you are asking me.')

#keep-alive loop
send('Welcome, I am dodonab-bot!  What would you like to ask me about?')
while True:
    question()
    send('Would you like to ask me another question?')
    m = receive_from_subs().__dict__['fields'][1].strip()
    print m
    if m.lower() == 'no' or m.lower() == 'n':
        send('Goodbye, then.')
        break
    elif m.lower() == 'yes' or m.lower() == 'y':
        send('Well, ask me, then!')
    else:
        send('Please ask me your question again.')
