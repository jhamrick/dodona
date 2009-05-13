import site
site.addsitedir('/afs/athena.mit.edu/user/b/r/broder/lib/python2.5/site-packages')

import zephyr
from zephyrUI import send
from fuzzystack import FuzzyStack
from helper import print_list, tokenize, integrate_lists, find_partial_key
from nlp import get_sentence_type, find_topic, find_compound_noun, find_PP, find_noun, QUESTION, STATEMENT, COMMAND
from xml_parser import update_files
from parsetree import Parser

#######################################
# The Session class stores a "session",
# or conversation, between Dodona and
# the user.
#######################################

class Session:
    def __init__(self, name, topics):
        self.memory = FuzzyStack(20)
        self.memory.push("data", topics)
        self.memory.push("name", name)
        self.name = name
        self.topics = topics
        self.parser = Parser()

    def AI(self, mess, d = None, k = None):
        """

        """
        if d == None: d = self.topics
        parse = self.parser.parse_sent(mess)
        print "PARSE:\n", parse
        ans = None
        if isinstance(parse, tuple):
            if parse[1]:
                foreign = ", ".join(parse[1])
                send("Sorry, I don't understand the following words: " + foreign + ".", self.name)
                self.memory.push("topic", list(parse[1]))
                self.learn()
                return
            else:
                ans = "Sorry, I don't understand what you are saying."
        else:
            type = get_sentence_type(parse)
            top = find_topic(parse, type)
            subtop = None

            if type == QUESTION and top:
                ques_word = top[1]
                top = top[0]

            if top:
                pp = find_PP(top)
                if pp:
                    b_pp = find_noun(top)
                    pp_noun = find_noun(top, exceptions=[" ".join(b_pp.leaves())])
                    if pp_noun: top = pp_noun
                    if b_pp: subtop = b_pp

            if top and subtop:
                topic = " ".join(top.leaves())
                subtopic = " ".join(subtop.leaves())
                print "TOPIC:", topic
                print "SUBTOPIC:", subtopic

                if d.has_key(topic) and isinstance(d[topic], dict):
                    if d[topic].has_key(subtopic):
                        ans = d[topic][subtopic]
                    else:
                        ans = "Sorry, I know about " + topic + ", but I don't know about " + subtopic + "."
                elif topic == k:
                    if d.has_key(subtopic):
                        ans = d[subtopic]
                    else:
                        ans = "Sorry, I know about " + topic + ", but I don't know about " + subtopic + "."

                if not ans and d.has_key(topic):
                        ans = "Multiple keywords match your query.  What did you mean to ask about?\n\n" + print_list(d[topic].keys())
                        self.memory.push("topic", topic)
                        self.memory.push("data", d[topic])

                elif not ans:
                    if type == QUESTION:
                        ans = "Sorry, I don't know what you are asking me."
                    else:
                        ans = "Sorry, I don't know what you are saying." 

            elif top:
                compound = find_compound_noun(top)
                print "TOPIC:", " ".join(top.leaves())
                if compound:
                    c = compound.leaves()
                    ans = ""
                    t = None
                    for i in xrange(1, len(c)):
                        topic = " ".join(c[:i])
                        subtopic = " ".join(c[i:])
                        print "topic:", topic
                        print "subtopic:", subtopic

                        if d.has_key(topic) and isinstance(d[topic], dict):
                            if d[topic].has_key(subtopic):
                                ans = d[topic][subtopic]
                            else:
                                ans = "Sorry, I know about " + topic + ", but I don't know about " + subtopic + "."
                        elif topic == k:
                            if d.has_key(subtopic):
                                ans = d[subtopic]
                            else:
                                ans = "Sorry, I know about " + topic + ", but I don't know about " + subtopic + "."
                        if not ans:
                            if d.has_key(topic):
                                ans = "Multiple keywords match your query.  What did you mean to ask about?\n\n" + print_list(d[topic].keys())
                                t = topic

                    if t:
                        self.memory.push("topic", t)
                        self.memory.push("data", d[t])

                    if not ans:
                        ans = "Sorry, I don't know about " + " ".join(top.leaves()) + "."
 
                if (compound and ans.startswith("Sorry")) or not compound:
                    top = " ".join(top.leaves())
                    if d.has_key(top):
                        if isinstance(d[top], dict):
                            ans = "Multiple keywords match your query.  What did you mean to ask about?\n\n" + print_list(d[top].keys())
                            self.memory.push("topic", top)
                            self.memory.push("data", d[top])
                        elif top == k:
                            ans = "Multiple keywords match your query.  What did you mean to ask about?\n\n" + print_list(d.keys())
                        else:
                            ans = d[top]
                    else:
                        ans = "Sorry, I don't know about " + top + "."
            else:
                print "TOPIC: None found"
                if type == QUESTION:
                    ans = "Sorry, I don't understand what you are asking me."
                else:
                    ans = "Sorry, I don't understand what you are saying."

        print ans
        send(ans, self.name)


    def add_data(self, mess, newtopic):
        """
        Adds a piece of new data to Dodona's 
        knowledge, after having ascertained the 
        subtopic and topic.

        Corresponds to the status add_data_true or
        add_data_false, depending on whether the
        topic is brand new or not, respectively.
        """
#         subtopic = self.memory.pop("topic")[1]
#         topic = self.memory.pop("topic")[1]
#         print topics[topic]
#         topics[topic][subtopic] =  mess
#         if newtopic: update_files(topic, topics)
#         else: update_files(topic, topics, False)
#         send("Thanks!", self.name)
#         return False

    def sub_topic(self, mess, subtopic = None):
        """
        Part of Dodona's learning algorithm.
        Determines the subtopic, and waits for
        the user to give it information about
        that subtopic and topic.

        Corresponds to the status subtopic.
        """
        topic = self.memory.read("topic")
        # if the subtopic is not already known, then
        # read it from the current message.  This is
        # an indicator that the topic is new or not.
        if subtopic == None:
            subtopic = mess
            newtopic = True
        else:
            newtopic = False

        send("Ok, we are talking about " + subtopic + " under " + topic + "!  Please tell me all you know about " + subtopic + " under " + topic + ".", self.name)
        self.memory.push("topic", subtopic)

        # if the topic is new, then set the status to add_data_true
        if newtopic:  self.memory.push("status", "add_data_true")
        # if it's not, then set the status to add_data_false
        else:  self.memory.push("status", "add_data_false")

        return None

    def add_new_word(self, word, pos):
        vocab = open("vocabulary.gr", "a")
        vocab.write("\n1\t" + pos + "\t" + word)
        vocab.close()
        self.parser.add_new_vocab_rule([pos, [word]])

    def part_of_speech(self, mess, step):
        word = self.memory.pop("topic")[1]
        name = self.name

        if step == "first":
            if mess.find("plural noun") != -1:
                self.add_new_word(word, "Noun_Pl")
                self.memory.pop("status")
                return self.learn()

            elif mess.find("noun") != -1:
                self.add_new_word(word, "Noun")
                self.memory.pop("status")
                return self.learn()

            elif mess.find("adjective") != -1:
                self.add_new_word(word, "Adj_State")
                self.memory.pop("status")
                return self.learn()

            elif mess.find("adverb") != -1:
                self.add_new_word(word, "Adv")
                self.memory.pop("status")
                return self.learn()

            elif mess.find("intransitive verb") != -1:
                send("What is the infinitive for the verb " + word + "?", name)
                self.memory.pop("status")
                self.memory.push("status", "pos_verb1in")
                self.memory.push("topic", word)

            elif mess.find("transitive verb") != -1:
                send("What is the infinitive for the verb " + word + "?", name)
                self.memory.pop("status")
                self.memory.push("status", "pos_verb1tr")
                self.memory.push("topic", word)

            elif mess.find("preposition") != -1:
                self.add_new_word(word, "Prep")
                self.memory.pop("status")
                return self.learn()

            else:
                self.memory.pop("topic")
                self.memory.pop("status")
                return False
        
        elif step.startswith("verb1"):
            if step.endswith("in"):
                self.add_new_word(mess, "V_Inf_In")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb2in")
            elif step.endswith("tr"):
                self.add_new_word(mess, "V_Inf_Tr")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb2tr")

            self.memory.push("topic", word)
            send("What is the present participle for the verb " + word + "?", name)
            return None

        elif step.startswith("verb2"):
            if step.endswith("in"):
                self.add_new_word(mess, "V_Pres_Part_In")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb3in")
            elif step.endswith("tr"):
                self.add_new_word(mess, "V_Pres_Part_Tr")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb3tr")

            self.memory.push("topic", word)
            send("What is the past participle for the verb " + word + "?", name)
            return None

        elif step.startswith("verb3"):
            if step.endswith("in"):
                self.add_new_word(mess, "V_Past_Part_In")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb4in")
            elif step.endswith("tr"):
                self.add_new_word(mess, "V_Past_Part_Tr")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb4tr")

            self.memory.push("topic", word)
            send("What is the 1st person singular present for the verb " + word + "?", name)
            return None

        elif step.startswith("verb4"):
            if step.endswith("in"):
                self.add_new_word(mess, "V_Base_Pres_In")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb5in")
            elif step.endswith("tr"):
                self.add_new_word(mess, "V_Base_Pres_Tr")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb5tr")

            self.memory.push("topic", word)
            send("What is the 3rd person singular present for the verb " + word + "?", name)
            return None

        elif step.startswith("verb5"):
            if step.endswith("in"):
                self.add_new_word(mess, "V_3rdSing_Pres_In")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb6in")
            elif step.endswith("tr"):
                self.add_new_word(mess, "V_3rdSing_Pres_Tr")
                self.memory.pop("status")
                self.memory.push("status", "pos_verb6tr")

            self.memory.push("topic", word)
            send("What is the 1st person singular past for the verb " + word + "?", name)
            return None

        elif step.startswith("verb6"):
            if step.endswith("in"):
                self.add_new_word(mess, "V_Base_Past_In")
            elif step.endswith("tr"):
                self.add_new_word(mess, "V_Base_Past_Tr")

            self.memory.pop("status")
            return self.learn()

    def learn(self):
        """
        Begins the learning process.  Determines the topic
        to which new information will be added.  If the user
        is already talking about a topic, and tells Dodona
        something she doesn't understand, then this will be
        the subtopic.  If not, then she prompts the user to
        enter a subtopic.
        """
        name = self.name
        unknown_all = list(self.memory.pop("topic"))[1]
        if unknown_all != []:
            unknown = unknown_all[0]
            del unknown_all[0]
            pos = ["Noun", "Plural Noun", "Adjective", "Adverb", "Transitive Verb", "Intransitive Verb", "Preposition", "Other"]

            send("Which of the following parts of speech is \'" + unknown + "\'?\n" + print_list(pos), name)
            self.memory.push("topic", unknown_all)
            self.memory.push("topic", unknown)
            self.memory.pop("status")
            self.memory.push("status", "pos_first")
            return None
        else:
            self.memory.pop("status")            
            return False

#         subtopic = self.memory.pop("topic")[1]
#         topic = self.memory.pop("topic")
#         # if the topic is foreign, then prompt the user
#         # for a subtopic and set the status to subtopic
#         if topic == False:
#             topic = subtopic
#             topics[subtopic] = {}
#             send("What subtopic under " + topic + " would you like to tell me about?", name)
#             self.memory.push("topic", topic)
#             self.memory.pop("status")
#             self.memory.push("status", "subtopic")
#             return None
#         # if not, then go directly to sub_topic
#         else:
#             self.memory.push("topic", topic[1])
#             return self.sub_topic("", subtopic)

    def unknown(self, mess):
        """
        Called when Dodona encounters something she does
        not understand.  Asks the user if he/she would
        like to tell Dodona about the subject.

        Corresponds to the status unknown.
        """
        name = self.name
        # if the user says yes, then call learn
        if mess.find("yes") != -1:
            self.learn()
            return None
        
        # if the user says no, and you're already
        # talking about a specific topic, then ask if
        # the user wants to continue talking about it,
        # and sets the status to conv_topic
        # if not, then return False (reset the session)
        if mess.find("no") != -1:
            send("Ok.", name)
            self.memory.pop("topic")
            t = self.memory.read("topic")
            self.memory.pop("status")
            if t == None:  return False

            send("Are we still talking about " + t + "?  (Please answer \"yes\" or \"no\")")
            self.memory.push("status", "conv_topic")

        return None

    def conv_topic(self, mess):
        """
        Called when the user responds to Dodona's
        question of whether they are talking about
        a certain topic, and processes the users's
        answer.

        Corresponds to the status conv_topic.
        """
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
        """
        Clears (resets) the session and the
        memory, but does not kill it.
        """
        self.memory = FuzzyStack(20)
        self.memory.push("data", self.topics)        

    def question(self):
        """
        Parses the user's most recent message,
        and decides what to do based on the
        content and the current status.
        """
        name = self.name
        mess = self.memory.read("message")
        m = tokenize(mess)
        mess = " ".join(m)

        if mess == None: return False

        # if the user wants to exit, then
        # return True (kill the session)
        if mess.startswith("exit") or \
                "bye" in m or \
                "goodbye" in m:
            send("Glad to be of help :)", name)
            return True

        # if the user says "nevermind", then
        # clear the session
        if mess.find("nevermind") != -1:
            send("Ok.", name)
            self.clear()
            return False

        # if the user greets Dodona, then respond
        # in kind.
        if "hi" in m or \
                "hey" in m or \
                "hello" in m != -1:
            send("hello, " + name + "!")
            return None
        
        # check the status, and return the corresponding
        # function if necessary
        s = self.memory.read("status")
        #if s == "unknown":  return self.unknown(mess)
        if s == "learn":  return self.learn()
        if s:
            if s.startswith("pos"):  return self.part_of_speech(mess, s.split("_")[1])
        if s == "conv_topic":  return self.conv_topic(mess)
        if s == "subtopic":  return self.sub_topic(mess)
        if s == "add_data_true":  return self.add_data(mess, True)
        if s == "add_data_false":  return self.add_data(mess, False)

        d = self.memory.read("data")
        k = self.memory.read("topic")
        # if there is no current topic, then decipher one
        # from the most recent message.
        if k == None:
            self.AI(mess)
            if self.memory.read("topic"):
                return None
            else:
                return False

        # if there is a current topic, search for a subtopic
        else:
            self.AI(mess, d, k)
            self.memory.pop("topic")
            self.memory.pop("data")
            return False
        
        # missing = None
#         if isinstance(key, tuple):
#             missing = key[1]
#             key = key[0]

#         # if there is no matching key, then ask the user to
#         # tell Dodona about the topic.
#         if key == "d:none":
#             if missing: 
#                 topic = ", ".join(missing)
#                 #self.memory.push("topic", topic)
#                 send("Sorry, I don't know understand the following words: " + topic)
#                 #self.memory.push("status", "unknown")
#                 return False
#             else:
#                 send("Sorry, I don't understand what you are asking me.")
#                 return False
        
#         # if the key is a list, this means that there are
#         # multiple matching keywords.  Prompt the user as to
#         # which one they want.
#         if isinstance(key, list):
#             send("Multiple keywords match your query.  What did you mean to ask about?\n\n" + print_list(key), name)
#             shortd = {}
#             for item in key:
#                 shortd[item] = d[item]
#             self.memory.push("data", shortd)
#             while(self.memory.read("message") != None):
#                 self.memory.pop("message")
#             return None

#         # if the key is a dictionary, then you know it is a
#         # topic, and has subtopics.  Ask the user which subtopic
#         # they would like to know about.
#         try:
#             if isinstance(d[key], dict):
#                 #key2 = self.AI(mess, d[key])
#                 key2 = "d:none"

#                 if key2 == "d:none" or isinstance(key2, list):
#                     send("Please pick a topic below, or tell me a new one! (in relation to " + key + ")\n\n" + print_list(d[key].keys()), name)
#                     self.memory.push("topic", key)
#                     self.memory.push("data", d[key])
#                     return None

#                 else:
#                     send(d[key][key2], name)
#                     return False
#         except:
#             send("Sorry, I don't understand what you are asking me.")
#             return False
            

#         # if there is just a single key, then respond with
#         # the knowledge which Dodona has about the topic
#         send(custom_fill(d[key]), name)
#         return False
 
# -*- indent-tabs-mode: nil; tab-width: 4; -*-
# vi: set ts=4 sw=4 et:
