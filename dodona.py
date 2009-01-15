import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')

import zephyr
import zephyrUI
from zephyrUI import *
import fuzzystack
from fuzzystack import *
import helper
from helper import *
import parser
from parser import *

topics = load_topics("doctopics/topics.xml")
memory = FuzzyStack(10)
memory.push("data", topics)

def AI(mess, k=""):
    mess = tokenize(mess)
    keys = []
    for key in mess:
        if k == "":
            integrate_lists(keys, find_partial_key(key, topics))
        else:
            integrate_lists(keys, find_partial_key(key, topics[k]))
    if len(keys) > 1:
	return keys
    elif len(keys) == 0:
        return "d:none"
    else:
        return keys[0]

filter = ["tell", "me", "about", ",", ".", "!", "?", "i", "would", "like", "to", "know", "what", "do", "you", "is"]

def pick_out_keyword(list, f = filter):
    pruned_list = list[:]
    for elem in list:
        if elem.lower() in filter:
            pruned_list.remove(elem)
    #print pruned_list
    
    key = ""
    for item in pruned_list:
        key += item + " "
    key = key.rstrip()

    return key       

def learn(topic, subtopic = None):
    if subtopic == None:
        newtopic = True
        topics[topic] = {}
        send(custom_fill("What subtopic under " + topic + " would you like to tell me about?"))
        subtopic = receive_from_subs()
        #mess = tokenize(mess)
        #subtopic = pick_out_keyword(mess)
    else:
        newtopic = False
    
    send(custom_fill("Ok, we are talking about " + subtopic + " under " + topic + "!  Please tell me all you know about " + subtopic + " under " + topic + "."))
    mess = receive_from_subs()
    topics[topic][subtopic] =  mess
    if newtopic: update_files(topic, topics)
    else: update_files(topic, topics, False)

    send(custom_fill("Thanks!"))
    

#get and answer a question
def question():
    d = memory.read("data")
    mess = memory.read("message")
    if mess == None:  mess = receive_from_subs()
    if mess == "exit":
        send("Glad to be of help.")
        return True

    k = memory.read("topic")
    if k == None:  key = AI(mess)
    else:  key = AI(mess, k)

    while key == "d:none":
        topic = pick_out_keyword(tokenize(mess))
        memory.push("topic", topic)
        send(custom_fill("Sorry, I don't know anything about " + topic + ".  Would you like to tell me about " + topic + "? (please answer \"yes\" or \"no\")"))
        mess = receive_from_subs()
        if mess.find("exit") != -1:
            send("Glad to be of help.")
            return True
        elif mess.find("yes") != -1:
            if k == None:  learn(topic)
            else:  learn(k, topic)
            memory.pop("topic")
            return False
        elif mess.find("no") != -1:
            send("Ok.")
            memory.pop("topic")
            t = memory.read("topic")
            if t != None:
                send(custom_fill("Are we still talking about " + k + "? (please answer \"yes\" or \"no\")"))
                mess = receive_from_subs()
                if mess.find("exit") != -1:
                    send("Glad to be of help.")
                    return True
                elif mess.find("yes") != -1:
                    send(custom_fill("Ok!"))
                    return question()
                else:
                    memory.pop("topic")
                    memory.pop("data")

            return False
        else:
            memory.pop("topic")
            if k == None:  key = AI(mess)
            else:  key = AI(mess, k)

    while isinstance(key, list):
        send(custom_fill("Multiple keywords match your query.  What did you mean to ask about?\n\n" + print_list(key)))
        shortd = {}
        for item in key:
            shortd[item] = d[item]
        memory.push("data", shortd)
        return question()
    
    if isinstance(d[key], dict):
        if len(d[key]) == 1:
            send(custom_fill(d[key].keys()[0] + "\n" + d[key][d[key].keys()[0]]))
            return False
        
        key2 = AI(mess, key)
       
        if key2 == "d:none" or isinstance(key2, list):
            send(custom_fill('There are multiple topics under ' + key + '.\nWhich of the following would you like to know about?\n\n' + print_list(d[key].keys())))
            memory.push("topic", key)
            memory.push("data", d[key])
            q = question()
            memory.pop("topic")
            memory.pop("data")
            return q
        else:
            send(custom_fill(d[key][key2]))
    else:
        send(custom_fill(d[key]))
    return False

zephyr.init()
zephyr.Subscriptions().add(('dodona-test', '*', '*'))
send(custom_fill('Dodona is now running.  If you find that a topic you wish answered is not accounted for, please send mail to dodona AT mit DOT edu'))

#keep-alive loop
while True:
    exit = question()
    if exit == False:
        send(custom_fill('Please ask me another question, or type \"exit\" to leave.'))
        d = memory.read("data")
        if d == None:  memory.push("data", topics)
    else:
        memory = FuzzyStack(10)
        memory.push("data", topics)

# -*- indent-tabs-mode: nil; tab-width: 4; -*-
# vi: set ts=4 sw=4 et:
