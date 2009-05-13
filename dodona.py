import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')

import zephyr
from zephyrUI import init, send, receive_from_subs
from fuzzystack import FuzzyStack
from session import Session
from xml_parser import load_topics
import traceback

###################################
# This file runs Dodona.  It keeps
# a list of "sessions", that is,
# the conversations she is having
# with different users.
###################################

sessions = {}
# load the data the Dodona pulls from
topics = load_topics("doctopics/topics.xml")
init()

while True:
    # recieve a message and return the sender as well
    m = receive_from_subs(True)
    (mess, sender) = m
    sender = sender.partition("@")[0]
    # if the session with this sender does not
    # already exist, then create it
    if not sessions.has_key(sender):
        sessions[sender] = Session(sender, topics)
    # add the message to the memory
    sessions[sender].memory.push("message", mess)
    
    # parse the message
    try:
        exit = sessions[sender].question()
    except KeyboardInterrupt:
        send(traceback.format_exc(), sender)
        raise
    except:
        send(traceback.format_exc(), sender)
    else:
        # reset the session and prompt the user to
        # ask another question
        if exit == False:
            sessions[sender].clear()
            send('Please ask me another question, or type \"exit\" to end the session.', sender)
        # if the user wants to exit, then delete
        # the session
        elif exit == True:
            del sessions[sender]
