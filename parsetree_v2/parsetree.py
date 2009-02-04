import pos
from pos import *
import grammar
from grammar import *

#d = POSDict()
d = {"the": "D", "barn": "N", "is": "V", "red": "A", "very": "v"}
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
    if d[word] == "N":
        return Noun(word)
    elif d[word] == "V":
        return Verb(word)
    elif d[word] == "A":
        return Adjective(word)
    elif d[word] == "D":
        return DefArticle(word)
    elif d[word] == "v":
        return Adverb(word)

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
        #print type
        for rule in type.getRules(type([])):
            r = check_rule(rule, pos)
            if r:
                matching_rules.append(rule)
                matching_types.append(type)

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
            for t in pos:
                if isinstance(t, matching_rule[0]):
                    pos_new.append(matching_type([t]))
                else:
                    pos_new.append(t)

        m.append(pos_new)

    #print m
    return m

def search(pos):
    for p in pos:
        if isinstance(p[0], Sentence): return p
        if p == []: return None
    
    for p in pos:
        temp = search(build_tree(p))
        if temp != None:
            return temp

def parse(sentence):
    sentence = tokenize(sentence)
    pos = []
    for word in sentence:
        pos.append(word_to_type(word))

    pos = build_tree(pos)
    #for p in pos: print p
    pos = search(pos)

    for p in pos: print p

parse("the barn is very red")
