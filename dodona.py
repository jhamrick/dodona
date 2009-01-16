import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')

import zephyr
import zephyrUI
from zephyrUI import *
import fuzzystack
from fuzzystack import *
import helper
from helper import *
import session
from session import *

zephyr.init()
zephyr.Subscriptions().add(('dodona-test', '*', '*'))
send(custom_fill('Dodona is now running.  If you find that a topic you wish answered is not accounted for, please send mail to dodona AT mit DOT edu'))

sessions = {}

while True:
    m = receive_from_subs(True)
    (mess, sender) = m
    sender = sender.partition("@")[0]
    print mess
    mess = mess.lower()
    if not sessions.has_key(sender):
        sessions[sender] = Session(sender)
    sessions[sender].memory.push("message", mess)
    exit = sessions[sender].question()
    if exit == False:
        sessions[sender].clear()
        send('Please ask me another question, or type \"exit\" to end the session.', sender)
    elif exit == True:
        del sessions[sender]
