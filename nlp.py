from nltk.parse.featurechart import EarleyChartParser 
from nltk.grammar import ContextFreeGrammar, Production
from nltk.grammar import Nonterminal as NT
from nltk.tree import Tree
from parsetree import *
import re

QUESTION = 1
STATEMENT = 2
COMMAND = 3

def get_sentence_type(parse):
    if isinstance(parse, str):
        return None

    lhs = parse.productions()[0].lhs()
    if lhs == NT("Ind_Clause_Ques") or \
       lhs == NT("Ind_Clause_Ques_Aux"):
        return QUESTION
    elif lhs == NT("Ind_Clause") or \
         lhs == NT("Ind_Clause_Pl"):
        if parse.productions()[0].rhs()[0] == NT("VP_Inf"):
            return COMMAND
        else:
            return STATEMENT

    for subtree in parse:
        type = get_sentence_type(subtree)
        if type: return type

    return None

def find_topic(parse, type=None):
    if type == None: type = get_sentence_type(parse)
    if isinstance(parse, str): return None
    #print parse
    #tree = parse.productions()[0]
    tree = parse[0]


    if type == QUESTION:
        
        for i in xrange(len(tree)):
            if tree[i].node == "Interrog_Clause":
                for j in xrange(len(tree[i])):
                    if tree[i][j].node == "Passive_Interrog_In":
                        for k in xrange(len(tree[i][j])):
                           if re.match("^NP_.*$", tree[i][j][k].node)
                                return tree[i][j][k].leaves()[0]


    elif type == STATEMENT:
        pass

    elif type == COMMAND:
        if tree.lhs() == NT("VP_Inf"):
            print "command!"
            rhs = tree.rhs()
            if rhs[-1] == NT("PP"):
                return " ".join(parse[-2][-1].leaves())
            elif \
               rhs[-1] == NT("After_Verb_Tr") or \
               rhs[-1] == NT("After_Verb_In") or \
               rhs[-1] == NT("V_Inf_In_Neg") or \
               rhs[-1] == NT("VP_Inf"):
                return find_topic(rhs[-1], type)                
        else:
            for subtree in parse:
                subj = find_topic(subtree, type)
                if subj: return subj

    return None



# def find_subject(parse, is_question=None):
#     if is_question == None and parse.productions()[-1].lhs() == NT("PuncQ"): is_question = True
#     elif is_question == None: is_question = False
#     print "Is a question?", is_question
#     if isinstance(parse, str):
#         return None

#     lhs = parse.productions()[0].lhs()
#     if lhs == NT("NP") or \
#        lhs == NT("NP_1st") or \
#        lhs == NT("NP_2nd") or \
#        lhs == NT("NP_3rd") or \
#        lhs == NT("NP_3rd_Pl"):
#         return parse

#     for subtree in parse:
#         subj = find_subject(subtree, is_question)
#         if subj: return subj

#     return None

# def find_object(parse, subject, is_question=None):
#     if is_question == None and parse.productions()[-1].lhs() == NT("PuncQ"): is_question = True
#     elif is_question == None: is_question = False
#     print "Is a question?", is_question
#     if isinstance(parse, str):
#         return None

#     lhs = parse.productions()[0].lhs()
#     if lhs == NT("NP") or \
#        lhs == NT("NP_1st") or \
#        lhs == NT("NP_2nd") or \
#        lhs == NT("NP_3rd") or \
#        lhs == NT("NP_3rd_Pl") or \
#        lhs == NT("NP_Obj"):
#         return parse

#     for subtree in parse:
#         obj = find_object(subtree, subject, is_question)
#         if obj and obj.leaves() != subject: return obj

#     return None

# def find_verb(parse, is_question=None):   
#     if is_question == None and parse.productions()[-1].lhs() == NT("PuncQ"): is_question = True
#     elif is_question == None: is_question = False
#     print "Is a question?", is_question 
#     if isinstance(parse, str):
#         return None

#     lhs = parse.productions()[0].lhs()
#     if lhs.symbol().startswith("Be_") or \
#        lhs.symbol().startswith("Exp_") or \
#        lhs.symbol().startswith("Being_") or \
#        lhs.symbol().startswith("Verbal_") or \
#        lhs.symbol().startswith("V_Inf"):
#         return parse

#     for subtree in parse:
#         verb = find_verb(subtree, is_question)
#         if verb: return verb

#     return None
