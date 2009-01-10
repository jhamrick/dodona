import site
site.addsitedir('/mit/broder/lib/python2.5/site-packages')
import zephyr
from textwrap import fill

#from pysqlite2 import dbapi2 as sqlite
# uses a basic parsing method:
#   BEGINSECTION begins a section, can contain multiple answers.
#                must end with ENDSECTION, and must be followed
#                by a section name
#   BEGINANSWER  begins an answer, may only contain one answer.
#                it must end with ENDANSWER, and must be followed
#                by an answer name
def load_answers(file):
    topics = {}
    t = open(file)
    section = None
    answer = None
    for line in t:
        if line.startswith("BEGINSECTION"):
            section = line.partition("SECTION ")[2].strip()
            topics[section] = {}
        elif line.startswith("BEGINANSWER"):
            answer = line.partition("BEGINANSWER ")[2].strip()
            if section != None:
                topics[section][answer] = ""
            else:
                topics[answer] = ""
        elif line.startswith("ENDANSWER"):
            answer = None
        elif line.startswith("ENDSECTION"):
            section = None
        elif line.startswith("#"):
            pass
        else:
            if section != None:
                if topics[section][answer] == "":
                    topics[section][answer] = line
                else:
                    topics[section][answer] += "\n" + line
            else:
                if topics[answer] == "":
                    topics[answer] = line
                else:
                    topics[answer] += "\n" + line
    print topics
    return topics

topics = load_answers("topics")

def send(mess):
    try:
        #zephyr.ZNotice(cls='dodona-test', fields=["", mess], sender='dodona@ATHENA.MIT.EDU').send()
        print "dodona: " + mess
    except:
        print "There was an error sending the last message."

#init
zephyr.init()
zephyr.Subscriptions().add(('dodona-test', '*', '*'))
send(fill('Dodona is now running.  If you find that a topic you wish answered is not accounted for, please send mail to dodona AT mit DOT edu'))

#receive a zephyr not from yourself
def receive_from_subs():
    # try:
#         m = zephyr.receive(True)
#     except:
#         return receive_from_subs()

#     while m.sender == 'dodona@ATHENA.MIT.EDU':
#         m = zephyr.receive(True)
#     print "From: ", m.sender
#     print "Class: ", m.cls
#     print "Instance: ", m.instance
#     print "Message: ", m.__dict__['fields'][1]
#     return m
    return raw_input("--> ")

#same as fill, except it preserves newlines
def custom_fill(s):
    news = ""
    while s.partition("\n")[2] != "":
        news += fill(s.partition("\n")[0]) + "\n"
        s = s.partition("\n")[2]
    news += fill(s.partition("\n")[0])
    return news

#get and answer a question
def question():
    mess = receive_from_subs()
    #mess = m.__dict__['fields'][1]
    #mess = mess.strip()
    if topics.has_key(mess):
        if isinstance(topics[mess], dict):
            send('There are multiple topics under ' + mess + '.\nWhich of the following would you like to know about?\n\n' + str(topics[mess].keys()))
            mess2 = receive_from_subs()
            #mess2 = m2.__dict__['fields'][1]
            #mess2 = mess2.strip()
            if topics[mess].has_key(mess2):
                send(custom_fill(topics[mess][mess2]))
            else:
                send('Sorry, I don\'t understand what you are asking me.')
        else:
            send(custom_fill(topics[mess]))
    else:
        send('Sorry, I don\'t understand what you are asking me.')

#keep-alive loop
send('Welcome, I am dodona!  What would you like to ask me about?')
while True:
    question()
    send('Please ask me another question, or type \"exit\" to leave.')
    m = receive_from_subs()#.__dict__['fields'][1].strip()
    print m
    if m.lower() == 'exit':
        send('Goodbye, then.')
        break
    else:
        continue
