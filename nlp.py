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

def find_PP(parse):
    if isinstance(parse, str): return None
    tree = parse.productions()[0]

    if tree.lhs() == NT("PP"):
        return parse[-1]
    else:
        for subtree in parse:
            pp = find_PP(subtree)
            if pp: return pp

    return None

def find_noun(parse, exceptions=[]):
    if isinstance(parse, str): return None
    tree = parse.productions()[0]

    if tree.lhs() == NT("Name") or \
       tree.lhs() == NT("Place") or \
       tree.lhs() == NT("Program") or \
       tree.lhs() == NT("Org") or \
       tree.lhs() == NT("Field") or \
       tree.lhs() == NT("Nominal") or \
       tree.lhs() == NT("Command") or \
       tree.lhs() == NT("File_Addr") or \
       tree.lhs() == NT("Web_Addr") or \
       tree.lhs() == NT("Nominal") or \
       tree.lhs() == NT("Nominal_Pl"):
        if " ".join(parse.leaves()) not in exceptions: return parse
    else:
        for subtree in parse:
            n = find_noun(subtree, exceptions)
            if n: return n

    return None

def find_compound_noun(parse):
    if isinstance(parse, str): return None
    tree = parse.productions()[0]

    if tree.lhs() == NT("CompoundNoun") or \
       tree.lhs() == NT("CompoundNoun_Pl"):
        return parse
    else:
        for subtree in parse:
            c = find_compound_noun(subtree)
            if c: return c
    
    return None

def find_after_verb(parse):
    if isinstance(parse, str): return None
    tree = parse.productions()[0]
    
    if tree.lhs() == NT("After_Verb_Tr") or \
       tree.lhs() == NT("After_Verb_In"):
        return parse
    else:
        for subtree in parse:
            subj = find_after_verb(subtree)
            if subj: return subj

def find_topic(parse, type=None, qword=None):
    if type == None: type = get_sentence_type(parse)
    if isinstance(parse, str): return None
    tree = parse.productions()[0]
    print type, "- tree:", tree

    if type == QUESTION:
        if tree.lhs() == NT("Ind_Clause_Ques") or \
           tree.lhs() == NT("Ind_Clause_Ques_Aux"):
            if not qword: 
                qword = parse[0].leaves()[0]
                print "qword:", qword

            rhs = tree.rhs()
            if rhs[-1] == NT("VP_3rd"):
                print "VP_3rd"
                return parse[-1][-1], qword

            elif rhs[-1] == NT("Ind_Clause_Ques_Aux"):
                print "Ind_Clause_Ques_Aux"
                return find_topic(parse[-1][-1], type=STATEMENT), qword

            elif rhs[-1] == NT("Interrog_Clause"):
                print "Interrog_Clause"
                print parse[-1][-1]
                return find_after_verb(parse[-1][-1]), qword

            elif rhs[-1] == NT("Ind_Clause_Inf") or \
                 rhs[-1] == NT("Ind_Clause_Inf_3rd"):
                print "Ind_Clause_Inf"
                return find_topic(parse[-1], type=STATEMENT), qword
        else:
            for subtree in parse:
                subj = find_topic(subtree, type)
                if subj: return subj

    elif type == STATEMENT:
        if tree.lhs() == NT("VP_1st") or \
           tree.lhs() == NT("VP_Inf"):
            rhs = tree.rhs()
            if rhs[-1] == NT("After_Verb_Tr") or \
               rhs[-1] == NT("After_Verb_In"):
                return parse[-1]
        else:
            for subtree in parse:
                subj = find_topic(subtree, type)
                if subj: return subj

    elif type == COMMAND:
        if tree.lhs() == NT("VP_Inf"):
            rhs = tree.rhs()
            if rhs[-1] == NT("PP"):
                return parse[-1]
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
