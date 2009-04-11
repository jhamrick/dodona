from nltk.parse.featurechart import EarleyChartParser 
from nltk.grammar import ContextFreeGrammar, Production
from nltk.grammar import Nonterminal as NT
from nltk.tree import Tree

def find_subject(parse):
    if isinstance(parse, str):
        return None

    lhs = parse.productions()[0].lhs()
    if lhs == NT("NP") or \
       lhs == NT("NP_1st") or \
       lhs == NT("NP_2nd") or \
       lhs == NT("NP_3rd") or \
       lhs == NT("NP_3rd_Pl"):
        return parse

    for subtree in parse:
        subj = find_subject(subtree)
        if subj: return subj

    return None

def find_object(parse, subject):
    if isinstance(parse, str):
        return None

    lhs = parse.productions()[0].lhs()
    if lhs == NT("NP_Obj"):
# lhs == NT("NP") or \
#        lhs == NT("NP_1st") or \
#        lhs == NT("NP_2nd") or \
#        lhs == NT("NP_3rd") or \
#        lhs == NT("NP_3rd_Pl") or \
#        lhs == NT("NP_Obj"):
        return parse

    for subtree in parse:
        obj = find_object(subtree, subject)
        if obj and obj.leaves() != subject: return obj

    return None

def find_verb(parse):    
    if isinstance(parse, str):
        return None

    lhs = parse.productions()[0].lhs()
    if lhs.symbol().startswith("Be_") or \
       lhs.symbol().startswith("Exp_") or \
       lhs.symbol().startswith("Being_") or \
       lhs.symbol().startswith("Verbal_") or \
       lhs.symbol().startswith("V_Inf"):
        return parse

    for subtree in parse:
        verb = find_verb(subtree)
        if verb: return verb

    return None
