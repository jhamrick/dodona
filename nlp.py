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
        return 0

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

    return 0

def find_topic(parse, type=None):
    if type == None: type = get_sentence_type(parse)
    if isinstance(parse, str): return None
    tree = parse.productions()[0]

    if type == QUESTION:
        tree = parse[0]
        
        for i in xrange(len(tree)):
            if tree[i].node == "Interrog_Clause":
                for j in xrange(len(tree[i])):
                    print tree[i][j].node
                    if tree[i][j].node == "Passive_Interrog_In":
                        for k in xrange(len(tree[i][j])):
                           if re.match("^NP_.*$", tree[i][j][k].node):
                                return tree[i][j][k].leaves()[0]
                    if tree[i][j].node == "Passive_Interrog_Tr":
                        
                        for k in xrange(len(tree[i][j])):
                           if re.match("^NP_.*$", tree[i][j][k].node):
                                return tree[i][j][k].leaves()[0]

            if tree[i].node == "Ind_Clause_Ques_Aux":
                for j in xrange(len(tree[i])):
                    if tree[i][j].node == "Ind_Clause_Inf":
                        
                        for k in xrange(len(tree[i][j])):
                           if re.match("^NP_.*$", tree[i][j][k].node):
                                return tree[i][j][k].leaves()[0]
                    if tree[i][j].node == "Passive_Interrog_Tr":
                        print "here"
                        for k in xrange(len(tree[i][j])):
                           if re.match("^NP_.*$", tree[i][j][k].node):
                                return tree[i][j][k].leaves()[0]

    elif type == STATEMENT:
        if tree.lhs() == NT("VP_1st"):
            rhs = tree.rhs()
            if rhs[-1] == NT("After_Verb_Tr") or \
               rhs[-1] == NT("After_Verb_In"):
                return parse[-1][-1]
        else:
            for subtree in parse:
                subj = find_topic(subtree, type)
                if subj: return subj

    elif type == COMMAND:
        if tree.lhs() == NT("VP_Inf"):
            rhs = tree.rhs()
            if rhs[-1] == NT("PP"):
                return parse[-1][-1]
            elif \
               rhs[-1] == NT("After_Verb_Tr") or \
               rhs[-1] == NT("After_Verb_In") or \
               rhs[-1] == NT("V_Inf_In_Neg") or \
               rhs[-1] == NT("VP_Inf") or \
               rhs[-1] == NT("NP_Obj"):
                return find_topic(parse[-1][-1], type)
        elif tree.lhs() == NT("PP"):
            return parse[-1]
        else:
            for subtree in parse:
                subj = find_topic(subtree, type)
                if subj: return subj

    return None
