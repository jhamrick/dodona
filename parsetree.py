from nltk.parse.featurechart import EarleyChartParser 
from nltk.grammar import ContextFreeGrammar, Production
from nltk.grammar import Nonterminal as NT
import random

class Parser:
    def __init__(self):
        self.rules = []
        test_sentences = []

        grammar = open("rules.gr", "r")
        line = grammar.readline()
        while line:
            if line.strip() != "" and not line.strip().startswith("#"):
                line = line[2:]
                parts = line.partition("\t")
                lhs = parts[0].strip()
                rhs = [NT(x) for x in parts[2].strip().split(" ")]
                self.rules.append(Production(NT(lhs), rhs))
            line = grammar.readline()
        grammar.close()

        vocab = open("vocabulary.gr", "r")
        line = vocab.readline()
        while line:
            if line.strip() != "" and not line.strip().startswith("#"):
                line = line[2:]
                parts = line.partition("\t")
                lhs = parts[0].strip()
                rhs = parts[2].strip().lower().split(" ")
                self.rules.append(Production(NT(lhs), rhs))
            line = vocab.readline()
        vocab.close()

        self.cfg = ContextFreeGrammar(NT("S"), self.rules)
        self.parser = EarleyChartParser(self.cfg, trace=0)

    def add_new_vocab_rule(self, rule):
        self.rules.append(Production(NT(rule[0]), rule[1]))
        self.cfg = ContextFreeGrammar(NT("S"), self.rules)
        self.parser = EarleyChartParser(self.cfg, trace=0)

    def parse_file(self):
        sens = open("examples.sen", "r")
        line = sens.readline()
        while line:
            test_sentences.append(line.strip().split(" "))
            line = sens.readline()
        sens.close()

        for sen in test_sentences:
            parse = self.parser.nbest_parse(sen, trace=0)
            if parse: print parse[0]
            else: print "failure"

    def parse_sent(self, sen):
        foreign = []
        try:
            parse = self.parser.nbest_parse(sen.strip().split(" "), trace=0)
        except:
            sen = sen.strip().split(" ")
            for word in sen:
                if not self.cfg.covers([word]): foreign.append(word)
            parse = None

        if parse: 
            #for p in parse: print p
            return parse[0]
        else: 
            print "failure"
            return None, foreign

    def rand_sent(self, left=None):
        if left == None: left = NT("S")
        poss = self.cfg.productions(lhs=left)
        if len(poss) > 1:
            index = random.randint(0,len(poss)-1)
        elif len(poss) == 1: index = 0
        else: 
            print left
            return None

        sen = []
        print poss[index]
        for nt in poss[index].rhs():
            if isinstance(nt, NT):
                sen.append(rand_sent(nt))                
            else: sen.append(nt)

        return " ".join(sen)
