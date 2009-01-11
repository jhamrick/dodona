import site
site.addsitedir('/mit/broder/lib/python2.5/site-packages')
import zephyr
from textwrap import fill
from xml.dom import minidom
import zephyrUI
from zephyrUI import *

def load_topics(file):
	topics = {}  
	xmldoc = minidom.parse(file)
	topicsNode = xmldoc.firstChild
	for topic in topicsNode.childNodes:
		if topic.nodeType == topic.ELEMENT_NODE and topic.localName == "topic":
			topic_name = topic.attributes["name"].value
			topic_file = topic.attributes["file"].value			
			topics[topic_name.encode('ascii')] = load_topic(topic_file)
	for topic in topicsNode.childNodes:
		if topic.nodeType == topic.ELEMENT_NODE and topic.localName == "alias":
			topic_name = topic.attributes["name"].value
			topic_file = topic.attributes["to"].value			
			topics[topic_name.encode('ascii')] = topics[(topic_file)]

#	print topics
	return topics

def load_topic(file):
	answers = {} 
	xmldoc = minidom.parse(file)
	topicNode = xmldoc.firstChild
	for answer in topicNode.childNodes:
		if answer.nodeType == answer.ELEMENT_NODE:
			if answer.localName == "answer":
				answer_question = answer.attributes["question"].value
				answers[answer_question.encode('ascii')] = answer.firstChild.data
			elif answer.localName == "default":
				default_answer = answer.firstChild.data
				#answers["DEFAULT"] = default_answer 
	return answers

topics = load_topics("doctopics/topics.xml")

#same as fill, except it preserves newlines
def custom_fill(s):
    news = ""
    while s.partition("\n")[2] != "":
        news += fill(s.partition("\n")[0]) + "\n"
        s = s.partition("\n")[2]
    news += fill(s.partition("\n")[0])
    return news

def message_to_list(mess):
    words = []
    #print mess
    oldchars = ""
    for char in mess:
	#print char    
        if char == "," or \
           char == "." or \
           char == "?" or \
           char == "!" or \
           char == "\'" or \
           char == "\"":
            if not oldchars == "":
                words.append(oldchars)
                oldchars = ""
            words.append(char)
        elif char == " " and not oldchars == "":
            words.append(oldchars)
            oldchars = ""
        else:
            oldchars += char
    if oldchars != "":
	words.append(oldchars)    
    #print words
    return words

def find_partial_key(word, list):
    keys = []
    for key in list.keys():
        key2 = message_to_list(key)
	for k in key2:
            if k == word:
                keys.append(key)
		break
    return keys

def integrate_lists(list1, list2):
    for item in list2:
        if list1.count(item) == 0:
            list1.append(item)
    return list1

def AI(mess, k=""):
    mess = message_to_list(mess)
    keys = []
    for key in mess:
        if k == "":
	    integrate_lists(keys, find_partial_key(key, topics))
        else:
	    integrate_lists(keys, find_partial_key(key, topics[k]))
    if len(keys) > 1:
        send("Multiple keywords match your query.  Which did you mean to ask about?\n\n" + str(keys))
	return ""
	

    elif len(keys) == 0:
        #send("Sorry, I don\'t understand what you are asking me.")
	return ""
    else:
        return keys[0]

#get and answer a question
def question():
    mess = receive_from_subs()
    if mess.lower() == "exit":
        send("Goodbye, then.")
	return True
    key = AI(mess)
    #print key, mess
    if key == '':
        exit = question()
	if exit:
            #send("Goodbye, then.")
	    return True   
    elif isinstance(topics[key], dict):
        key2 = AI(mess, key)
	if key2 == "":
            send('There are multiple topics under ' + key + '.\nWhich of the following would you like to know about?\n\n' + str(topics[key].keys()))
            mess2 = receive_from_subs()
            key2 = AI(mess2, key)
	    if key2 == '':
                exit = question()
		if exit:
                    #send("Goodbye, then.")
		    return True   
	    else:
                send(custom_fill(topics[key][key2]))
	else:
            send(custom_fill(topics[key][key2]))
    else:
        send(custom_fill(topics[key]))
    return False

#keep-alive loop
send('Welcome, I am Dodona!  What would you like to ask me about?\n\n' + str(topics.keys()))
while True:
    exit = question()
    if exit == True:
	break    
    send('Please ask me another question, or type \"exit\" to leave.\n\n' + str(topics.keys()))
