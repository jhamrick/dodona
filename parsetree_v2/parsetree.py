import pos
from pos import *
import grammar
from grammar import *
import copy
from copy import *
import time

d = POSDict()
phrases = [Nominal, NounPhrase, VerbPhrase, Sentence, AdjectivePhrase, PrepositionalPhrase]

def tokenize(mess):
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
            #words.append(char)
        elif char == " " and not oldchars == "":
            words.append(oldchars)
            oldchars = ""
        elif char == " " and oldchars == "":
            pass
        else:
            oldchars += char
    if oldchars != "":
        words.append(oldchars)
    return words

def word_to_type(word):
    pos = d.read_all(word)
    print word, ": ", pos
    types = []
    for p in pos:
        if p == "N":
            types.append(Noun(word))
        elif p == "V":
            types.append(Verb(word))
        elif p == "A":
            types.append(Adjective(word))
        elif p == "D":
            types.append(Determiner(word))
        elif p == "v":
            types.append(Adverb(word))
        elif p == "P":
            types.append(Preposition(word))
        elif p == "C":
            types.append(Conjunction(word))
        elif p == "r":
            types.append(Pronoun(word))

    return types

def check_rule(rule, sentence):
    if len(rule) > 1:
        for i in range(len(sentence) - len(rule) + 1):
            matches = False
            temp = sentence[i:i+len(rule)]
            for t, r in zip(temp, rule):
                if not isinstance(t, r): 
                    matches = False
                    break
                else:
                    matches = True

            if matches == True:
                return True
    else:
        for t in sentence:
            if isinstance(t, rule[0]):
               return True 

    return False

def build_tree(pos):
    pos_new = []

    r = False
    matching_types = []
    matching_rules = []
    for type in phrases:
        for rule in type.getRules(type([])):
            #print type, rule, pos
            r = check_rule(rule, pos)
            if r:
                matching_rules.append(rule)
                matching_types.append(type)

    #print matching_rules, matching_types
    if len(matching_types) == 0 or len(matching_rules) == 0:
        #print "ERROR --> no matches"
        return []

    m = []
    for matching_type, matching_rule in zip(matching_types, matching_rules):
        pos_new = []
        if len(matching_rule) > 1:
            for i in range(len(pos) - len(matching_rule) + 1):
                matches = False
                temp = pos[i:i+len(matching_rule)]
                for t, r in zip(temp, matching_rule):
                    if not isinstance(t, r):
                        matches = False
                        break
                    else:
                        matches = True

                if matches == True:
                    pos_new.append(matching_type(temp))
                    for j in range(i + len(matching_rule), len(pos)):
                        pos_new.append(pos[j])
                    break
                else:
                    pos_new.append(pos[i])
        else:
            for i in range(len(pos)):
                if isinstance(pos[i], matching_rule[0]):
                    pos_new.append(matching_type([pos[i]]))
                    for j in range(i+1, len(pos)):
                        pos_new.append(pos[j])
                    break
                else:
                    pos_new.append(pos[i])

        m.append(pos_new)

    #print m
    return m

def search(pos):
    for p in pos:
        if isinstance(p[0], Sentence) and len(p) == 1: return p
        if p == []: return None
    
    #print pos
    temp = []
    for p in pos:
        #print p
        t = build_tree(p)
        #print t
        if t != []:
            temp.extend(t)

    if len(temp) == 0: 
        print "NO PARSE FOUND"
        #print pos
        return []

    #print temp
    return search(temp)

def parse(sentence):
    t0 = time.clock()
    sentence = tokenize(sentence)
    pos = [[]]
    for word in sentence:
        types = word_to_type(word)
        if len(types) == 1:
            for p in pos: p.append(types[0])
        else:
            temp = deepcopy(pos)
            #print "temp: ", temp
            for t in temp:
                t.append(types[0])
            #print "temp: ", temp
            for type in types[1:]:
                for p in pos:
                    t = p[:]
                    t.append(type)
                    temp.append(t)
                    #print "pos: ", pos
                    #print "temp2: ", temp
            pos = deepcopy(temp)          

    #print pos
    #print len(pos)
    pos = search(pos)
    t1 = time.clock()

    for p in pos: print p
    print "Parse took " + str(t1 - t0) + " seconds."

parse("your pink hair is pretty")

# for entry in d.d:
#     if d.read(entry) == "r":
#         d.replace(entry, "D")
# d.save()
