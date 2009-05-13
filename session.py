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
    def __init__(self, name, topics, verbose):
        self.memory = FuzzyStack(20)
        self.memory.push("data", topics)
        self.memory.push("name", name)
        self.name = name
        self.topics = topics
        self.parser = Parser()
        self.verbose = verbose

    def AI(self, mess, d = None, k = None):
        """
        Parses the message, and attempts to locate a topic.  If it is
        able to find a topic, it tells the user about the topic,
        otherwise it prints a message saying that it can't parse the 
        sentence, or it doesn't know about the topic.
        """

        # make sure the dictionary is set to something
        if d == None: d = self.topics

        # parse the sentence, and print the parse
        parse = self.parser.parse_sent(mess)
        print "PARSE:\n", parse
        if self.verbose: send("PARSE:\n" + str(parse), self.name)
        ans = None

        # if the parse is returned as a tuple, then we know
        # that the parse failed.
        if isinstance(parse, tuple):
            # if the second value in the tuple is valid, then there were
            # words that were not in the grammar.  Tell the user about the
            # words, and then enter a function to learn the foreign words.
            if parse[1]:
                send("Sorry, I don't understand the following words: " + \
                         ", ".join(parse[1]) + ".", self.name, v=self.verbose)
                self.memory.push("topic", list(parse[1]))
                self.learn()
                return
            # otherwise, we just couldn't parse the sentence
            else:
                ans = "Sorry, I couldn't parse what you just said.."

        # otherwise, the parse succeeded
        else:
            # find the sentence type: STATEMENT, QUESTION, or COMMAND
            type = get_sentence_type(parse)
            if self.verbose: send("TYPE: " + str(type), self.name)

            # based on the sentence type, find the topic of the sentence.
            # we don't yet know what the subtopic is, so just set it to
            # None.
            top = find_topic(parse, type)
            subtop = None

            # if the sentence is a question and find_topic() found a
            # topic, then top is a tuple, and we need to store the
            # parts separately.
            if type == QUESTION and top:
                ques_word = top[1]
                top = top[0]

            # if a topic was found, then we want to look for a
            # prepositional phrase.  For example, we want to be able
            # to get TOPIC=emacs, SUBTOPIC=keys from "keys in emacs"
            if top:
                # look for a PP
                pp = find_PP(top)

                # if a PP exists, then look for the nouns:  in the most
                # common cases, there will be either one or two, for
                # example "keys in emacs" or "about emacs"
                if pp:
                    b_pp = find_noun(top)
                    pp_noun = find_noun(top, exceptions=[" ".join(b_pp.leaves())])
                    if pp_noun and b_pp: 
                        top = pp_noun
                        subtop = b_pp
                    elif b_pp:
                        top = b_pp
            
            # if we found both a topic and subtopic
            if top and subtop:
                # convert the tree structures into strings
                topic = " ".join(top.leaves())
                subtopic = " ".join(subtop.leaves())
                print "TOPIC:", topic
                print "SUBTOPIC:", subtopic
                if self.verbose:
                    send("TOPIC: " + topic + "\nSUBTOPIC: " + subtopic, self.name)

                # check to see if topic is a key in the knowledge
                # dictionary, and that the the entry corresponding
                # to topic is also a dictionary
                if d.has_key(topic) and isinstance(d[topic], dict):

                    # if subtopic is a key in the entry corresponding
                    # to topic, then set the subtopic entry as the answer.
                    # otherwise, say that we know about topic, but not
                    # subtopic.
                    if d[topic].has_key(subtopic):
                        ans = d[topic][subtopic]
                    else:
                        ans = "Sorry, I know about " + topic + \
                            ", but I don't know about " + subtopic + "."

                # check to see if the current topic stored in memory is
                # the same as the topic we found.
                elif topic == k:

                    # is the subtopic we found a key in the dictionary?
                    # if so, set it's entry as the anser.  Otherwise,
                    # say that we know about topic, but not subtopic
                    if d.has_key(subtopic):
                        ans = d[subtopic]
                    else:
                        ans = "Sorry, I know about " + topic + \
                            ", but I don't know about " + subtopic + "."

                # otherwise, we don't know what's going on
                else:
                    if type == QUESTION:
                        ans = "Sorry, I don't know what you are asking me."
                    else:
                        ans = "Sorry, I don't know what you are saying." 

            # or, if there is no subtopic
            elif top:

                # check for compound nouns.  Just because we didn't
                # find a subtopic out of prepositional phrases doesn't
                # mean that one doesn't exist.  For example, we want
                # TOPIC=emacs, SUBTOPIC=keys from "emacs keys"
                compound = find_compound_noun(top)

                if compound:
                    c = compound.leaves()
                    ans = ""
                    t = None

                    # we want to check all groupings of topics and
                    # subtopics.  So, if there are three words, A B C,
                    # we could have TOPIC=A, SUBTOPIC="B C", or TOPIC="A B",
                    # SUBTOPIC=C
                    for i in xrange(1, len(c)):

                        # convert the tree structures into strings
                        topic = " ".join(c[:i])
                        subtopic = " ".join(c[i:])
                        print "TOPIC:", topic
                        print "SUBTOPIC:", subtopic
                        if self.verbose:
                            send("TOPIC: " + topic + "\nSUBTOPIC: " + subtopic, self.name)

                        # check to see if the dictionary has topic as a key
                        # and if the entry corresponding to that is also a
                        # dictionary
                        if d.has_key(topic) and isinstance(d[topic], dict):

                            # is subtopic a key in the sub-dictionary?
                            if d[topic].has_key(subtopic):
                                ans = d[topic][subtopic]
                            else:
                                ans = "Sorry, I know about " + topic + \
                                    ", but I don't know about " + subtopic + \
                                    "."

                        # check to see if the current topic in memory
                        # is the topic that we've found
                        elif topic == k:

                            # does the dictionary have subtopic as a key?
                            if d.has_key(subtopic):
                                ans = d[subtopic]
                            else:
                                ans = "Sorry, I know about " + topic + \
                                    ", but I don't know about " + subtopic + \
                                    "."
                    
                    # if we didn't find an answer, then say we don't know
                    # about the topic
                    if not ans:
                        ans = "Sorry, I don't know about " + \
                            " ".join(top.leaves()) + "."


                # if the topic isn't a compound noun, or it is but we weren't
                # able to find a topic and subtopic (because it's possible that
                # the topic itself is multiple words, and there is no
                # subtopic):
                if (compound and ans.startswith("Sorry")) or not compound:

                    # convert the tree structure into a string
                    topic = " ".join(top.leaves())
                    print "TOPIC:", topic
                    if self.verbose: send("TOPIC: " + topic, self.name)

                    # if the topic is a key in the dictionary
                    if d.has_key(topic):
                        
                        # if the entry matching topic is a dictionary, then
                        # we should ask what subtopic they want to know about
                        if isinstance(d[topic], dict):
                            ans = "Multiple keywords match your query.  " + \
                                "What did you mean to ask about?\n\n" + \
                                print_list(d[topic].keys())
                            self.memory.push("topic", topic)
                            self.memory.push("data", d[topic])

                        # if the topic we found is the same as the topic in
                        # memory, then ask (again) which subtopic they
                        # want to ask about
                        elif topic == k:
                            ans = "Multiple keywords match your query.  " + \
                                "What did you mean to ask about?\n\n" + \
                                print_list(d.keys())

                        # otherwise, just give them the entry that corresponds
                        # to topic
                        else:
                            ans = d[topic]

                    # otherwise, we don't know what they're talking about
                    else:
                        ans = "Sorry, I don't know about " + topic + "."

            # otherwise, we couldn't find a topic from the sentence, so
            # tell them so
            else:
                print "TOPIC: None found"
                if verbose: send("TOPIC: None found", self.name)
                ans = "Sorry, I couldn't determine the topic of what you are asking me."

        # print the answer out to the terminal, and send the answer
        # to the user.
        print ans
        send(ans, self.name, v=self.verbose)

    def add_new_word(self, word, pos):
        """
        Adds a new vocabulary word and rule to vocabulary.gr and
        to the ContextFreeGrammar.
        """
        vocab = open("vocabulary.gr", "a")
        vocab.write("\n1\t" + pos + "\t" + word)
        vocab.close()
        self.parser.add_new_vocab_rule([pos, [word]])

    def part_of_speech(self, mess, step):
        """
        Part of Dodona's word-learning algorithm.  Learns the
        part of speech for the word, and either moves to the next step
        (for example, if the word is a verb, we want to know all
        conjugations of that verb) or ends the learning process.
        """
        word = self.memory.pop("topic")[1]
        name = self.name

        # first step
        if step == "first":

            # plural noun
            if mess.find("plural noun") != -1:
                self.add_new_word(word, "Noun_Pl")
                self.memory.pop("status")
                return self.learn()

            # noun
            elif mess.find("noun") != -1:
                self.add_new_word(word, "Noun")
                self.memory.pop("status")
                return self.learn()

            # adjective
            elif mess.find("adjective") != -1:
                self.add_new_word(word, "Adj_State")
                self.memory.pop("status")
                return self.learn()

            # adverb
            elif mess.find("adverb") != -1:
                self.add_new_word(word, "Adv")
                self.memory.pop("status")
                return self.learn()

            # intransitive verb
            elif mess.find("intransitive verb") != -1:
                send("What is the infinitive for the verb " + word + "?", name, v=self.verbose)
                self.memory.pop("status")
                self.memory.push("status", "pos_verb1in")
                self.memory.push("topic", word)

            # transitive verb
            elif mess.find("transitive verb") != -1:
                send("What is the infinitive for the verb " + word + "?", name, v=self.verbose)
                self.memory.pop("status")
                self.memory.push("status", "pos_verb1tr")
                self.memory.push("topic", word)

            # preposition
            elif mess.find("preposition") != -1:
                self.add_new_word(word, "Prep")
                self.memory.pop("status")
                return self.learn()

            # anything else
            else:
                self.memory.pop("status")
                return self.learn()
        
        # step 2, stores the infinitive
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
            send("What is the present participle for the verb " + word + "?", name, v=self.verbose)
            return None

        # step 3, stores the present participle
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
            send("What is the past participle for the verb " + word + "?", name, v=self.verbose)
            return None

        # step 4, stores the past participle
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
            send("What is the 1st person singular present for the verb " + word + "?", name, v=self.verbose)
            return None

        # step 5, stores the present base
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
            send("What is the 3rd person singular present for the verb " + word + "?", name, v=self.verbose)
            return None

        # step 6, stores the 3rd person singular
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
            send("What is the 1st person singular past for the verb " + word + "?", name, v=self.verbose)
            return None

        # step 7, stores the past base
        elif step.startswith("verb6"):
            if step.endswith("in"):
                self.add_new_word(mess, "V_Base_Past_In")
            elif step.endswith("tr"):
                self.add_new_word(mess, "V_Base_Past_Tr")

            self.memory.pop("status")
            return self.learn()

    def learn(self):
        """
        Begins the learning process.  Asks the user what
        part of speech the word is, and keeps track of the
        remaining words which we still need to learn about
        """
        name = self.name
        unknown_all = list(self.memory.pop("topic"))[1]
        if unknown_all != []:
            unknown = unknown_all[0]
            del unknown_all[0]
            pos = ["Noun", \
                   "Plural Noun", \
                   "Adjective", \
                   "Adverb", \
                   "Transitive Verb", \
                   "Intransitive Verb", \
                   "Preposition", \
                   "Other"]

            send("Which of the following parts of speech is \'" + \
                     unknown + "\'?\n" + print_list(pos), name, v=self.verbose)
            self.memory.push("topic", unknown_all)
            self.memory.push("topic", unknown)
            self.memory.pop("status")
            self.memory.push("status", "pos_first")
            return None
        else:
            self.memory.pop("status")            
            return False

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
            send("Glad to be of help :)", name, v=self.verbose)
            return True

        # if the user says "nevermind", then
        # clear the session
        if mess.find("nevermind") != -1:
            send("Ok.", name, v=self.verbose)
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
            if s.startswith("pos"):  
                return self.part_of_speech(mess, s.split("_")[1])
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
 
# -*- indent-tabs-mode: nil; tab-width: 4; -*-
# vi: set ts=4 sw=4 et:
