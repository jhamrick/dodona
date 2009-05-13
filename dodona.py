import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')
import zephyr
from zephyrUI import init, send, receive_from_subs
from fuzzystack import FuzzyStack
from session import Session
from xml_parser import load_topics
import traceback
from optparse import OptionParser

###################################
# This file runs Dodona.  It keeps
# a list of "sessions", that is,
# the conversations she is having
# with different users.
###################################

parser = OptionParser()
parser.add_option("-v", "--v", action="store_true", dest="verbose", default=False, help="send informative zephyrs about how sentences are parsed and analyzed")

(options, args) = parser.parse_args()
verbose = options.verbose

sessions = {}
# load the data the Dodona pulls from
topics = load_topics("doctopics/topics.xml")
init()

while True:
    # recieve a message and return the sender as well
    m = receive_from_subs(True, v=verbose)
    (mess, sender) = m
    sender = sender.partition("@")[0]
    # if the session with this sender does not
    # already exist, then create it
    if not sessions.has_key(sender):
        sessions[sender] = Session(sender, topics, verbose)
    # add the message to the memory
    sessions[sender].memory.push("message", mess)
    
    # parse the message
    try:
        exit = sessions[sender].question()
    except KeyboardInterrupt:
        if verbose:
            send(traceback.format_exc(), v=verbose)
        else:
            send("Dodona is no longer running.", v=verbose)
        raise
    except:
        if verbose:
            send(traceback.format_exc(), sender, v=verbose)
    else:
        # reset the session and prompt the user to
        # ask another question
        if exit == False:
            sessions[sender].clear()
            send('Please ask me another question, or type \"exit\" to end the session.', sender, v=verbose)
        # if the user wants to exit, then delete
        # the session
        elif exit == True:
            del sessions[sender]
