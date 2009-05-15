from nltk.parse.featurechart import EarleyChartParser 
from nltk.grammar import ContextFreeGrammar, Production
from nltk.grammar import Nonterminal as NT
import random

#######################################
# The Parser class reads in grammar
# rules and vocab rules from two files,
# and creates a ContextFreeGrammar and
# EarleyChartParser.
######################################

class Parser:
    def __init__(self, rules_file="rules.gr", vocab_file="vocabulary.gr"):
        """
        Reads in grammar rules (from rules_file) and vocab rules (from
        vocab_file) and creates self.cfg (a ContextFreeGrammar) and
        self.parser (a EarleyChartParser).
        """
        self.rules = []
        test_sentences = []

        # get the rules from rules_file
        grammar = open(rules_file, "r")
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

        # get the rules from vocab_file
        vocab = open(vocab_file, "r")
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

        # create the grammar and parser
        self.cfg = ContextFreeGrammar(NT("S"), self.rules)
        self.parser = EarleyChartParser(self.cfg, trace=0)

    def add_new_vocab_rule(self, rule):
        """
        Adds a new vocabulary rule to the set of rules, and
        recreates self.cfg and self.parser.
        """
        self.rules.append(Production(NT(rule[0]), rule[1]))
        self.cfg = ContextFreeGrammar(NT("S"), self.rules)
        self.parser = EarleyChartParser(self.cfg, trace=0)

    def parse_file(self, file):
        """
        Parses sentences in a file.
        """
        sens = open(file, "r")
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
        """
        Parses a single sentence.  Returns the parse, or returns a
        tuple (None, foreign_words).
        """
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

    def parse_NP(self, sen):
        """
        Parses a partial sentence (that is, usually a noun phrase.
        Returns the parse, or returns a tuple.
        """
        try:
            cfg_temp = ContextFreeGrammar(NT("NP"), self.rules)
            parser_temp = EarleyChartParser(cfg_temp, trace=0)
            parse = parser_temp.nbest_parse(sen.strip().split(" "), trace=tr)
        except:
            print traceback.format_exc()
        
        if parse:
            return parse[0]
        else:
            print "failure"
            return None

    def rand_sent(self):
        """
        Creates a random sentence from self.cfg.
        """
        poss = self.cfg.productions(lhs=NT("S"))
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
