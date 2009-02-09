from pos import POSDict
from grammar import Sentence, NounPhrase, VerbPhrase, AdjectivePhrase, PrepositionalPhrase, Nominal, Noun, Verb, Adjective, Adverb, Conjunction, Preposition, Pronoun, Determiner, Punctuation, string_to_type, Phrase, Head
from copy import deepcopy
import time
from helper import tokenize

#########################################
# This file contains all the functions
# needed to parse a sentence.  There is:
#    word_to_type(word)
#    check_rule(rule, sentence)
#    build_tree(pos)
#    search(pos)
# and most importantly:
#    parse(sentence)
########################################

d = POSDict() # initialize the dictionary containing all the words and their
              # associated part(s) of speech

# specify the phrases which will be used to build the tree
phrases = [Nominal, NounPhrase, VerbPhrase, Sentence, AdjectivePhrase, PrepositionalPhrase]
parses = {}

def word_to_type(word):
    """
    Reads the dictionary to find the part(s) of speech
    which are associated with the word, and then translates
    them into instances of the corresponding class(either
    Noun, Verb, Adjective, Determiner, Adverb, Preposition,
    Conjunction, Pronoun, or Punctuation).
    """
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
        elif p == "p":
            types.append(Punctuation(word))

    return types

def check_rule(rule, sentence):
    """
    Check a rule against the sentence to see if
    it matches.  For example,
        "The barn is red"
    has
        Determiner Noun Verb Adjective
    which would match the rule under Nominal, which is
    simply [Noun].
    """
    # if the length of the rule is > 1, then we need
    # to split the sentence up into chunks of size n:
    #    "The barn is red"
    #    "The barn", "barn is", "is red", for n=2
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
    # otherwise, we can just iterate through the 
    # sentence until we find a match
    else:
        for t in sentence:
            if isinstance(t, rule[0]):
               return True 

    return False

def build_tree(pos):
    """
    Checks the current sentence structure against
    the rules, and creates new trees based on which rules
    match.  Returns a list of all possible structures.
    """
    pos_new = []
    r = False
    matching_types = []
    matching_rules = []

    # for each phrase type, check each rule against
    # the sentence and add the matching rules and types
    # to matching_types and matching_rules, respectively
    for type in phrases:
        for rule in type.getRules(type([])):
            r = check_rule(rule, pos)
            if r:
                matching_rules.append(rule)
                matching_types.append(type)

    # if there aren't any matching rules, then return
    if len(matching_types) == 0 or len(matching_rules) == 0:
        return []

    m = []
    # find which rules match to which parts of the sentence, and replace
    # that bit of the sentence with the new type
    for matching_type, matching_rule in zip(matching_types, matching_rules):
        pos_new = []
        # if the length of the rule is > 1, then we need to split the
        # sentence up into chunks
        if len(matching_rule) > 1:
            for i in range(len(pos) - len(matching_rule) + 1):
                matches = False
                temp = pos[i:i+len(matching_rule)]
                for t, r in zip(temp, matching_rule):
                    if not isinstance(t, r):
                        # if it doesn't match, then we move on to the next
                        # chunk of sentence
                        matches = False
                        break
                    else:
                        matches = True

                # if the current rule matches the current chunk of sentence
                # then we replace the chunk with the type specified by the rule
                if matches == True:
                    pos_new.append(matching_type(temp))
                    for j in range(i + len(matching_rule), len(pos)):
                        pos_new.append(pos[j])
                    break
                # otherwise, leave the current chunk as it is
                else:
                    pos_new.append(pos[i])
        # if the rules is of length 1, then we can just iterate through it
        else:
            for i in range(len(pos)):
                # if the current rule matches the current chunk of sentence
                # then we can replace the chunk with the type specified by
                # the rule
                if isinstance(pos[i], matching_rule[0]):
                    pos_new.append(matching_type([pos[i]]))
                    for j in range(i+1, len(pos)):
                        pos_new.append(pos[j])
                    break
                # othewise, leave the current chunk as it is
                else:
                    pos_new.append(pos[i])

        # add the new, modified sentence to the list of possible trees
        m.append(pos_new)

    return m

def search(pos):
    """
    Performs a breadth-first-search with all the possible
    trees found by build_tree, and returns the final tree
    if it succeeds, or an empty list if it fails.
    """
    for p in pos:
        # if the tree begins with a single node 
        # then we've successfully parsed the sentence!
        if len(p) == 1: return p
        # if the tree is empty, return an empty list
        if p == []: return p
    
    temp = []
    # for each possible tree, find all possible children
    for p in pos:
        t = build_tree(p)
        # if there are possible children, add them to the temporary list
        if t != []:
            temp.extend(t)

    # if the temporary list is of length 0, then we've
    # failed at finding a parse
    if len(temp) == 0: 
        print "NO PARSE FOUND"
        return []

    return search(temp)

def save_parses():
    """
    Saves the known parses of various
    sentences to file.
    """
    p = open("parses", "w")
    for s in parses.keys():
        temp = s
        print temp
        for parse in parses[s]:
            temp = temp + "\t" + str(parse)
        p.write(temp + "\n")

    p.close()

def make_tree_from_parse(p):
    """
    Makes a tree from a string of format:
    [.Sentence [.NounPhrase [.Nominal [.Noun I ] ] ] [.VerbPhrase [.Verb am ] [.NounPhrase [.Nominal [.Determiner a ] [.Noun girl ] ] ] ] ] 
    """
    node = string_to_type(p[2:p.find(" ")])
    p2 = p[p.find(" ")+1:]
    left = 0
    right = 0
    chars = ""
    for char in p2:
        chars += char
        if char == "]":
            right += 1
            if isinstance(node, Head):
                node.setWord(chars.rstrip(" ]"))
                return node

        elif char == "[":
            left += 1

        if left == right and left > 0:
            if chars.strip() == "":
                chars = ""
            elif isinstance(node, Phrase):
                node.addChild(make_tree_from_parse(chars))
                chars = ""

    return node
            

def load_stored_parses():
    """
    Loads known parses into a dictionary.
    """
    p = open("parses", "r")
    line = p.readline()
    parse = {}
    while line != "":
        l = line.split("\t")
        parse[l[0]] = []
        for i in range(1, len(l)):
            t = make_tree_from_parse(l[i])
            print t
            parse[l[0]].append(t)
        line = p.readline()

    p.close()
    return parse

def parse(sentence):
    """
    Splits the sentence up into a list, matches
    each item in the list to it's corresponding class
    and creates all possible sentences if words have
    multiple parts of speech associated with them.
    Using the function search, it attempts to parse the
    sentence, and returns the result.

    Also prints out the amount of time the parse took to
    complete.
    """
    if parses.has_key(sentence):
        print("Parse already exists; no need to search.")
        for p in parses[sentence]: print p
        return parses[sentence]

    t0 = time.clock() # record the starting time
    sen = tokenize(sentence) # split the sentence into a list

    for parse in parses.keys():
        new_sen = []
        p = parse.split()
        i = 0
        while i < (len(sen) - len(p) + 1):
            curr = sen[i:i+len(p)]
            if curr == p:
                new_sen.append(parses[parse][0])
                print parses[parse][0]
                i += len(p)
            else:
                new_sen.append(sen[i])
                i += 1
        if i < len(sen):
            for j in range(i, len(sen)):
                new_sen.append(sen[j])

        sen = new_sen
    
    # make a list of all possible sentences, given the type(s) of
    # speech for each word
    pos = [[]]
    for word in sen:
        if isinstance(word, str):
            types = word_to_type(word)
            oldpos = pos
            pos = []
            for p_s in oldpos:
                pos += [p_s + [type_] for type_ in types]
        else:
            oldpos = []
            for p in pos:
                temp = p
                temp.append(word)
                oldpos.append(temp)
            pos = oldpos

    print pos

    print "There are " + str(len(pos)) + " possible sentences."

    # perform the search on the possible sentences
    for p in pos:
        print "Performing search on:"
        print p
        st0 = time.clock()
        p_temp = search([p])
        st1 = time.clock()
        print "Subsearch took " + str(st1 - st0) + " seconds."
        if p_temp != []:
            pos = p_temp
            if not parses.has_key(sentence): parses[sentence] = []
            parses[sentence].append(pos[0])
            save_parses()
            break

    t1 = time.clock() # record the end time

    for p in pos: print p
    print "Parse took " + str(t1 - t0) + " seconds."

    return pos

parses = load_stored_parses()
