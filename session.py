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

class Session:
    def __init__(self, name):
        self.memory = FuzzyStack(20)
        self.memory.push("data", topics)
        self.memory.push("name", name)
        self.filter = ["tell", "me", "about", ",", ".", "!", "?", "i", "would", "like", "to", "know", "what", "do", "you", "is"]
        self.name = name

    def AI(self, mess, d = topics):
        mess = tokenize(mess)
        keys = []
        for key in mess:
            integrate_lists(keys, find_partial_key(key, d))
        if len(keys) > 1:
            return keys
        elif len(keys) == 0:
            return "d:none"
        else:
            return keys[0]
    
    def pick_out_keyword(self, list, f = ""):
        if f == "":  f = self.filter
        pruned_list = list[:]
        for elem in list:
            if elem.lower() in f:
                pruned_list.remove(elem)
        #print pruned_list

        key = ""
        for item in pruned_list:
            key += item + " "
        key = key.rstrip()

        return key     

    def add_data(self, mess, newtopic):
        subtopic = self.memory.pop("topic")[1]
        topic = self.memory.pop("topic")[1]
        print topics[topic]
        topics[topic][subtopic] =  mess
        if newtopic: update_files(topic, topics)
        else: update_files(topic, topics, False)
        send("Thanks!", self.name)
        return False

    def sub_topic(self, mess, subtopic = None):
        topic = self.memory.read("topic")
        if subtopic == None:
            subtopic = mess
            newtopic = True
        else:
            newtopic = False
        print topic, subtopic
        send("Ok, we are talking about " + subtopic + " under " + topic + "!  Please tell me all you know about " + subtopic + " under " + topic + ".", self.name)
        self.memory.push("topic", subtopic)
        if newtopic:  self.memory.push("status", "add_data_true")
        else:  self.memory.push("status", "add_data_false")
        return None

    def learn(self):
        name = self.name
        subtopic = self.memory.pop("topic")[1]
        topic = self.memory.pop("topic")
        if topic == False:
            topic = subtopic
            topics[subtopic] = {}
            send("What subtopic under " + topic + " would you like to tell me about?", name)
            self.memory.push("topic", topic)
            self.memory.pop("status")
            self.memory.push("status", "subtopic")
            return None
        else:
            self.memory.push("topic", topic[1])
            return self.sub_topic("", subtopic)

    def unknown(self, mess):
        name = self.name
        if mess.find("yes") != -1:
            self.learn()
            return None
        
        if mess.find("no") != -1:
            send("Ok.", name)
            self.memory.pop("topic")
            t = self.memory.read("topic")
            self.memory.pop("status")
            if t == None:  return False

            send("Are we still talking about " + t + "?  (Please answer \"yes\" or \"no\")")
            self.memory.push("status", "conv_topic")
            return None

        return None

    def conv_topic(self, mess):
        name = self.name
        if mess.find("yes") != -1:
            send("Ok!", name)
            return None
        
        if mess.find("no") != -1:
            send("Duly noted.", name)
            self.memory.pop("topic")
            self.memory.pop("status")
            return False

        return None

    def clear(self):
        self.memory = FuzzyStack(20)
        self.memory.push("data", topics)        

    #get and answer a question
    def question(self):
        name = self.name
        mess = self.memory.read("message")
        if mess == None: return False
        if mess == "exit":
            send("Glad to be of help", name)
            return True

        if mess.find("nevermind") != -1:
            send("Ok.", name)
            self.clear()
            return False

        m = tokenize(mess)
        if "hi" in m or \
                "hey" in m or \
                "hello" in m != -1:
            send("Hello, " + name + "!")
            return None
        
        s = self.memory.read("status")
        print "s: ", s
        if s == "unknown":  return self.unknown(mess)
        if s == "conv_topic":  return self.conv_topic(mess)
        if s == "subtopic":  return self.sub_topic(mess)
        if s == "add_data_true":  return self.add_data(mess, True)
        if s == "add_data_false":  return self.add_data(mess, False)

        d = self.memory.read("data")
        k = self.memory.read("topic")
        if k == None:  key = self.AI(mess)
        else:  key = self.AI(mess, d)

        if key == "d:none":
            topic = self.pick_out_keyword(tokenize(mess))
            self.memory.push("topic", topic)
            send("Sorry, I don't know anything about " + topic + ".  Would you like to tell me about " + topic + "?  (Please answer \"yes\" or \"no\")", name)
            self.memory.push("status", "unknown")
            return None

        if isinstance(key, list):
            send("Multiple keywords match your query.  What did you mean to ask about?\n\n" + print_list(key), name)
            shortd = {}
            for item in key:
                shortd[item] = d[item]
            self.memory.push("data", shortd)
            while(self.memory.read("message") != None):
                self.memory.pop("message")
            return None

        if isinstance(d[key], dict):
            #if len(d[key]) == 1:
            #    send(d[key].keys()[0] + "\n" + d[key][d[key].keys()[0]], name)
            #    return False

            key2 = self.AI(mess, d[key])

            if key2 == "d:none" or isinstance(key2, list):
                send("Please pick a topic below, or tell me a new one! (in relation to " + topic + ")\n\n" + print_list(d[key].keys()), name)
                self.memory.push("topic", key)
                self.memory.push("data", d[key])
                return None

            else:
                send(d[key][key2], name)
                return False

        send(custom_fill(d[key]), name)
        return False
 
# -*- indent-tabs-mode: nil; tab-width: 4; -*-
# vi: set ts=4 sw=4 et:
