from nltk.parse.featurechart import EarleyChartParser 
from nltk.grammar import ContextFreeGrammar, Production
from nltk.grammar import Nonterminal as NT
import random

rules = []
test_sentences = []

grammar = open("rules.gr", "r")
line = grammar.readline()
while line:
    if line.strip() != "" and not line.strip().startswith("#"):
        line = line[2:]
        parts = line.partition("\t")
        lhs = parts[0].strip()
        rhs = [NT(x) for x in parts[2].strip().split(" ")]
        rules.append(Production(NT(lhs), rhs))
    line = grammar.readline()
grammar.close()

vocab = open("vocabulary.gr", "r")
line = vocab.readline()
while line:
    if line.strip() != "" and not line.strip().startswith("#"):
        line = line[2:]
        parts = line.partition("\t")
        lhs = parts[0].strip()
        rhs = parts[2].strip().split(" ")
        rules.append(Production(NT(lhs), rhs))
    line = vocab.readline()
vocab.close()

cfg = ContextFreeGrammar(NT("S"), rules)
parser = EarleyChartParser(cfg, trace=0)

def parse_file():
    sens = open("parseable.sen", "r")
    line = sens.readline()
    while line:
        test_sentences.append(line.strip().split(" "))
        line = sens.readline()
    sens.close()

    for sen in test_sentences:
        parse = parser.nbest_parse(sen)
        if parse: print parse[0]
        else: print "failure"

def parse_sent(sen):
    foreign = []
    try:
        parse = parser.nbest_parse(sen.strip().split(" "))
    except:
        sen = sen.strip().split(" ")
        for word in sen:
            if not cfg.covers([word]): foreign.append(word)
        parse = None

    if parse: 
        print parse[0]
        return parse[0]
    else: 
        print "failure"
        return None, foreign

def rand_sent(left=None):
    if left == None: left = NT("S")
    poss = cfg.productions(lhs=left)
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
        
