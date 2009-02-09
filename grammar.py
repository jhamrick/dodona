def string_to_type(s):
    """
    Converts a string into it's
    corresponding type
    """
    if s == "Sentence":
        return Sentence()
    elif s == "NounPhrase":
        return NounPhrase()
    elif s == "VerbPhrase":
        return VerbPhrase()
    elif s == "AdjectivePhrase":
        return AdjectivePhrase()
    elif s == "PrepositionalPhrase":
        return PrepositionalPhrase()
    elif s == "Nominal":
        return Nominal()
    elif s == "Noun":
        return Noun()
    elif s == "Verb":
        return Verb()
    elif s == "Adjective":
        return Adjective()
    elif s == "Adverb":
        return Adverb()
    elif s == "Conjuction":
        return Conjunction()
    elif s == "Preposition":
        return Preposition()
    elif s == "Pronoun":
        return Pronoun()
    elif s == "Determiner":
        return Determiner()
    elif s == "Punctuation":
        return Punctuation()

##############################
# The basic class for all
# lexical phrases
##############################
class Phrase:
    def __init__(self, children=None):
        if children == None:
            self.children = []
        else:
            self.children = children

    def __str__(self):
        s = "["
        for child in self.children: s += str(child)
        s += "] "
        return s

    def getChildren(self):
        """
        Returns a copy of the children for the phrase.
        """
        return self.children

    def getRules(self):
        """
        Returns a copy of the rules for the phrase.
        """
        return self.rules

    def addChild(self, child):
        """
        Adds another child to the phrase.
        """
        self.children.append(child)

##############################
# The basic class for all
# lexical heads (non-phrases)
##############################
class Head:
    def __init__(self, word=None):
        if word == None:
            self.word = ""
        else:
            self.word = word

    def __str__(self):
        return self.word

    def setWord(self, word):
        self.word = word
    
    def getWord(self):
        """
        Returns the value of the Head (the word or punctuation).
        """
        return self.word

    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(self.word) + ')'

##############################
# The following classes all
# inherit from the Phrase
# class.  The only difference
# between these are the rules,
# and the type of phrase.
#############################

class Sentence(Phrase):
    def __init__(self, children=None):
        if children == None:
            self.children = []
        else:
            self.children = children
        self.rules = [[NounPhrase, VerbPhrase],
                      [Verb, NounPhrase, VerbPhrase],
                      [VerbPhrase],
                      [NounPhrase, VerbPhrase, Punctuation],
                      [Verb, NounPhrase, VerbPhrase, Punctuation],
                      [VerbPhrase, Punctuation],
                      [NounPhrase, Punctuation, Sentence],
                      [Sentence, Conjunction, Sentence]]

    def __str__(self):
        s = "[.Sentence "
        for child in self.children: s += str(child)
        s += "] "
        return s

class NounPhrase(Phrase):
    def __init__(self, children=None):
        if children == None:
            self.children = []
        else:
            self.children = children
        self.rules = [[AdjectivePhrase, Nominal],
                      [Nominal, PrepositionalPhrase],
                      [NounPhrase, Conjunction, NounPhrase],
                      [Nominal],
                      [AdjectivePhrase, Conjunction, AdjectivePhrase, Nominal],
                      [Determiner, AdjectivePhrase, Nominal]]

    def __str__(self):
        s = "[.NounPhrase "
        for child in self.children: s += str(child)
        s += "] "
        return s    

class VerbPhrase(Phrase):
    def __init__(self, children=None):
        if children == None:
            self.children = []
        else:
            self.children = children
        self.rules = [[Verb, Verb],
                      [Verb, Verb, Verb],
                      [Verb, NounPhrase],
                      [Verb, NounPhrase, PrepositionalPhrase],
                      [Verb, PrepositionalPhrase],
                      [Verb, Sentence],
                      [VerbPhrase, PrepositionalPhrase],
                      [Verb, AdjectivePhrase],
                      [Adverb, Verb, NounPhrase],
                      [Adverb, Verb],
                      [Verb, NounPhrase, Adverb],
                      [Verb, Adverb],
                      [Verb]]

    def __str__(self):
        s = "[.VerbPhrase "
        for child in self.children: s += str(child)
        s += "] "
        return s

class AdjectivePhrase(Phrase):
    def __init__(self, children=None):
        if children == None:
            self.children = []
        else:
            self.children = children
        self.rules = [[Adjective],
                      [Adverb, Adjective]]

    def __str__(self):
        s = "[.AdjectivePhrase "
        for child in self.children: s += str(child)
        s += "] "
        return s

class PrepositionalPhrase(Phrase):
    def __init__(self, children=None):
        if children == None:
            self.children = []
        else:
            self.children = children
        self.rules = [[Preposition, NounPhrase],
                      [Preposition]]

    def __str__(self):
        s = "[.PrepositionalPhrase "
        for child in self.children: s += str(child)
        s += "] "
        return s

class Nominal(Phrase):
    def __init__(self, children=None):
        if children == None:
            self.children = []
        else:
            self.children = children
        self.rules = [[Noun],
                      [Determiner, Noun],
                      [Nominal, PrepositionalPhrase]]

    def __str__(self):
        s = "[.Nominal "
        for child in self.children: s += str(child)
        s += "] "
        return s

##############################
# The following classes all
# inherit from the Head
# class.  The only difference
# between these are the type
# of head.
#############################

class Noun(Head):
    def __str__(self):
        return "[.Noun " + self.word + " ] "

class Verb(Head):
    def __str__(self):
        return "[.Verb " + self.word + " ] "

class Adjective(Head):
    def __str__(self):
        return "[.Adjective " + self.word + " ] "

class Adverb(Head):
    def __str__(self):
        return "[.Adverb " + self.word + " ] "

class Conjunction(Head):
    def __str__(self):
        return "[.Conjunction " + self.word + " ] "

class Preposition(Head):
    def __str__(self):
        return "[.Preposition " + self.word + " ] "

class Pronoun(Head):
    def __str__(self):
        return "[.Pronoun " + self.word + " ] "

class Determiner(Head):
    def __str__(self):
        return "[.Determiner " + self.word + " ] "

class Punctuation(Head):
    def __str__(self):
        return "[.Punctuation " + self.word + " ] "
