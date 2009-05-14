import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')
import zephyr
from zephyrUI import IO
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
parser.add_option("-c", "--class", dest="cls", default="dodona-test", help="set the class which Dodona listens on")

(options, args) = parser.parse_args()
cls = options.cls

sessions = {}
# load the data the Dodona pulls from
topics = load_topics("doctopics/topics.xml")
bot = IO(cls)
print "\nDodona successfully started!\n"

while True:
    # recieve a message and return the sender as well
    m = bot.receive_from_subs(True)
    (mess, sender) = m
    sender = sender.partition("@")[0]
    # if the session with this sender does not
    # already exist, then create it
    if not sessions.has_key(sender):
        sessions[sender] = Session(sender, topics, bot)
    # add the message to the memory
    sessions[sender].memory.push("message", mess)
    
    # parse the message
    try:
        exit = sessions[sender].question()
    except KeyboardInterrupt:
        bot.send("Dodona is no longer running.")
        raise
    except:
        print traceback.format_exc()
    else:
        print "status:", sessions[sender].memory.read("status")
        print "exit:", exit
        # reset the session and prompt the user to
        # ask another question
        if exit == "reset":
            sessions[sender].clear()
        # if the user wants to exit, then delete
        # the session
        elif exit == "exit":
            del sessions[sender]
