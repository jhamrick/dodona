from pos import POSDict
from grammar import Sentence, NounPhrase, VerbPhrase, AdjectivePhrase, PrepositionalPhrase, Nominal, Noun, Verb, Adjective, Adverb, Conjunction, Preposition, Pronoun, Determiner, Punctuation
from copy import deepcopy
import time

#########################################
# This file contains all the functions
# needed to parse a sentence.  There is:
#    tokenize(mess)
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

def tokenize(mess):
    """
    Split the sentence into a list, which contains words and some
    punctuation, but no whitespace.
    """
    words = []
    oldchars = ""
    for char in mess:
        if char == "," or \
           char == "." or \
           char == "?" or \
           char == "!":
            # if the previous characters are not whitespace,
            # then make them a new entry in the list
            if not oldchars == "":
                words.append(oldchars)
                oldchars = ""
            # if the current character is punctuation,
            # then make it a new entry in the list
            words.append(char)
        # if the current character is a space and the
        # previous characters are not whitespace, then
        # make the previous characters into an entry in
        # the list
        elif char == " " and not oldchars == "":
            words.append(oldchars)
            oldchars = ""
        # if the current character is a space and the
        # previous characters are whitespace, then do
        # nothing.
        elif char == " " and oldchars == "":
            pass
        # otherwise, add the current character to the string
        # of previous characters
        else:
            oldchars += char
    
    # once you're at the end of the word, make any
    # previous characters which are not whitespace
    # to the list
    if oldchars != "":
        words.append(oldchars)

    return words

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
        # if the tree begins with a single node which is of type
        # Sentence, then we've successfully parsed the sentence!
        if isinstance(p[0], Sentence) and len(p) == 1: return p
        # if the tree is empty, return an empty list
        if p == []: return p
    
    temp = []
    # for each possible tree, find all possible chilren
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
    t0 = time.clock() # record the starting time
    sentence = tokenize(sentence) # split the sentence into a list
    
    # make a list of all possible sentences, given the type(s) of
    # speech for each word
    pos = [[]]
    for word in sentence:
        types = word_to_type(word)
        if len(types) == 1:
            for p in pos: p.append(types[0])
        else:
            temp = deepcopy(pos)
            for t in temp:
                t.append(types[0])
            for type in types[1:]:
                for p in pos:
                    t = p[:]
                    t.append(type)
                    temp.append(t)
            pos = deepcopy(temp)          

    # perform the search on the possible sentences
    pos = search(pos)
    t1 = time.clock() # record the end time

    for p in pos: print p
    print "Parse took " + str(t1 - t0) + " seconds."

    return pos
