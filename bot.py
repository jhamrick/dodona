import site
site.addsitedir('/mit/broder/lib/python2.5/site-packages')
import zephyr
from textwrap import fill
from xml.dom import minidom  

def load_topics(file):
	topics = {}  
	xmldoc = minidom.parse(file)
	topicsNode = xmldoc.firstChild
	for topic in topicsNode.childNodes:
		if topic.nodeType == topic.ELEMENT_NODE and topic.localName == "topic":
			topic_name = topic.attributes["name"].value
			topic_file = topic.attributes["file"].value			
			topics[topic_name.encode('ascii')] = load_topic(topic_file)
	print topics
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

topics = load_topics("topics.xml")

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
    print words
    return words            

def AI(mess, k=""):
    mess = message_to_list(mess)
    keys = []
    for key in mess:
        if k == "":
            if topics.has_key(key):
                keys.append(key)
        else:
            if topics[k].has_key(key):
                keys.append(key)
    if len(keys) > 1:
        send("Multiple keywords match your query.  Which did you mean to ask about?\n\n" + str(keys))
        question()
    elif len(keys) == 0:
        send("Sorry, I don\'t understand what you are asking me.")
	return ""
    else:
        return keys[0]

#get and answer a question
def question():
    mess = receive_from_subs()
    if mess.lower() == "exit":
        send("Goodbye, then.")
	return True
    #mess = m.__dict__['fields'][1]
    #mess = mess.strip()
    key = AI(mess)
    #print "key: ", repr(key)
    if key == '':
	question()    
    elif isinstance(topics[key], dict):
        send('There are multiple topics under ' + key + '.\nWhich of the following would you like to know about?\n\n' + str(topics[key].keys()))
        mess2 = receive_from_subs()
        key2 = AI(mess2, key)
#             #mess2 = m2.__dict__['fields'][1]
#             #mess2 = mess2.strip()
#             if topics[mess].has_key(mess2):
	if key2 == '':
	    question()
	else:
            send(custom_fill(topics[key][key2]))
#             else:
#                 send('Sorry, I don\'t understand what you are asking me.')
    else:
        send(custom_fill(topics[key]))
    return False
#     else:
#         send('Sorry, I don\'t understand what you are asking me.')

#keep-alive loop
send('Welcome, I am Dodona!  What would you like to ask me about?')
while True:
    exit = question()
    if exit == True:
	break    
    send('Please ask me another question, or type \"exit\" to leave.')
