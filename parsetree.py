from nltk.parse.featurechart import EarleyChartParser 
from nltk.grammar import ContextFreeGrammar, Production
from nltk.grammar import Nonterminal as NT

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

sens = open("examples.sen", "r")
line = sens.readline()
while line:
    test_sentences.append(line.strip().split(" "))
    line = sens.readline()
sens.close()

cfg = ContextFreeGrammar(NT("S"), rules)
parser = EarleyChartParser(cfg, trace=3)

for sen in test_sentences:
    parse = parser.nbest_parse(sen)
    if parse: print parse
    else: print "failure"
