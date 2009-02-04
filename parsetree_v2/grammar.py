class Phrase:
    def __init__(self, children):
        self.children = children

    def __str__(self):
        s = "["
        for child in self.children: s += str(child)
        s += "] "
        return s

    def getChildren(self):
        return self.children

    def getRules(self):
        return self.rules

    def addChild(self, child):
        self.children.append(child)

class Head:
    def __init__(self, word):
        self.word = word

    def __str__(self):
        return self.word
    
    def getWord(self):
        return self.word

class NounPhrase(Phrase):
    def __init__(self, children):
        self.children = children
        self.rules = [[DefArticle, Nominal],
                      [IndefArticle, Nominal],
                      [DefArticle, AdjectivePhrase, Nominal],
                      [IndefArticle, AdjectivePhrase, Nominal],
                      [NounPhrase, Conjunction, NounPhrase],
                      [Nominal, PrepositionalPhrase],
                      [Nominal]]

    def __str__(self):
        s = "[NounPhrase: "
        for child in self.children: s += str(child)
        s += "] "
        return s    

class Noun(Head):
    def __str__(self):
        return "Noun: " + self.word + " "

class VerbPhrase(Phrase):
    def __init__(self, children):
        self.children = children
        self.rules = [[Verb, NounPhrase],
                      [Verb, NounPhrase, PrepositionalPhrase],
                      [Verb, PrepositionalPhrase],
                      [Verb, Sentence],
                      [VerbPhrase, PrepositionalPhrase],
                      [Verb, AdjectivePhrase]]

    def __str__(self):
        s = "[VerbPhrase: "
        for child in self.children: s += str(child)
        s += "] "
        return s

class Verb(Head):
    def __str__(self):
        return "Verb: " + self.word + " "

class TransVerbPhrase(VerbPhrase):
    def __str__(self):
        s = "[TransVerbPhrase"
        for child in self.children: s += str(child)
        s += "] "
        return s

class TransVerb(Head):
    def __str__(self):
        return "TransVerb: " + self.word + " "

class IntransVerbPhrase(VerbPhrase):
    def __str__(self):
        s = "[IntransVerbPhrase"
        for child in self.children: s += str(child)
        s += "] "
        return s

class IntransVerb(Head):
    def __str__(self):
        return "IntransVerb: " + self.word + " "

class Sentence(Phrase):
    def __init__(self, children):
        self.children = children
        self.rules = [[NounPhrase, VerbPhrase],
                      [Verb, NounPhrase, VerbPhrase],
                      [VerbPhrase]]

    def __str__(self):
        s = "[Sentence: "
        for child in self.children: s += str(child)
        s += "] "
        return s

class AdjectivePhrase(Phrase):
    def __init__(self, children):
        self.children = children
        self.rules = [[Adjective],
                      [Adverb, Adjective]]

    def __str__(self):
        s = "[AdjectivePhrase: "
        for child in self.children: s += str(child)
        s += "] "
        return s

class Adjective(Head):
    def __str__(self):
        return "Adjective: " + self.word + " "

class Adverb(Head):
    def __str__(self):
        return "Adverb: " + self.word + " "

class Conjunction(Head):
    def __str__(self):
        return "Conjunction: " + self.word + " "

class PrepositionalPhrase(Phrase):
    def __init__(self, children):
        self.children = children
        self.rules = [[Preposition, NounPhrase],
                      [Preposition]]

    def __str__(self):
        s = "[PrepositionalPhrase: "
        for child in self.children: s += str(child)
        s += "] "
        return s

class Preposition(Head):
    def __str__(self):
        return "Prepositional: " + self.word + " "

class Pronoun(Head):
    def __str__(self):
        return "Pronoun: " + self.word + " "

class DefArticle(Head):
    def __str__(self):
        return "DefArticle: " + self.word + " "

class IndefArticle(Head):
    def __str__(self):
        return "IndefArticle: " + self.word + " "

class Nominal(Phrase):
    def __init__(self, children):
        self.children = children
        self.rules = [[Noun],
                      [Nominal, Noun],
                      [Nominal, PrepositionalPhrase]]

    def __str__(self):
        s = "[Nominal: "
        for child in self.children: s += str(child)
        s += "] "
        return s
