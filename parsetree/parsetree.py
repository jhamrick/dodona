#import x
#from x import *
import helper
from helper import *

d = {"the": "D", "man": "N", "eats": "V", "[pres]": "I", "young": "Adj", "food": "N", "strong": "Adj", "quickly": "Adv", "barn": "N", "is": "V", "red": "Adj", "very": "Adv"}

class Node:        
    def __init__(self, list, type, level):
        self.children = list
        self.level = level
        self.type = type

    def __str__(self):
        tabs = ""
        for i in range(self.level):
            tabs += "    "

        p = self.type + ": "
        for child in self.children:
            p = p + "\n" + tabs + str(child)
        return p

    def addChild(self, child):
        self.children.append(child)

    def setType(self, type):
        self.type = type

    def getChildren(self):
        return self.children

    def getType(self):
        return self.type

class Leaf:
    def __init__(self, val, type, level):
        self.val = val
        self.type = type
        self.level = level

    def getVal(self):
        return self.val

    def getType(self):
        return self.type

    def __str__(self):
        return self.type + ": " + str(self.val)

class ParseTree:
    def __init__(self, head):
        self.head = head

    def __str__(self):
        return str(self.head)


# def makeNodeTree(s, level=1):    
#     if isinstance(s, str):
#         return Leaf(s, d[s], level)

#     children = []
#     for child in s:
#         children.append(makeNodeTree(child, level + 1))

#     child = children[0]
#     if not child.getType().endswith("\'") and not child.getType().endswith("P"):
#         type = child.getType() + "\'"
#     elif child.getType().endswith("\'"):
#         if len(children) > 1:
#             t = children[1].getType()
#             if t == "AdvP" or t == "PP":
#                 type = child.getType()
#             else:
#                 type = child.getType().partition("\'")[0] + "P"
#         else:
#             type = child.getType().partition("\'")[0] + "P"
#     else:
#         type = None

#     if type == None and len(children) > 1:
#         child = children[1]
#         if not child.getType().endswith("\'") and not child.getType().endswith("P"):
#             type = child.getType() + "\'"
#         elif child.getType().endswith("\'"):
#             t = children[0].getType()
#             if t == "AdvP" or t == "PP":
#                 type = child.getType()
#             else:
#                 type = child.getType().partition("\'")[0] + "P"

#     return Node(children, type, level)

rules = {"XP": [["spec", "X'"], 
                ["X'", "spec"],
                ["X'"]],
         "X'": [["adjunct", "X'"],
                ["X'", "adjunct"],
                ["X'"],
                ["comp", "X"],
                ["X", "comp"],
                ["X"]],
         "spec": [["DP"], ["NP"], ["AdjP"]],
         "adjunct": [["AdvP"], ["AdjP"], ["PP"]],
         "comp": [["CP"], ["VP"]]}

def matchRule(currNode, children):
    if currNode.getType() != "spec" and \
            currNode.getType() != "adjunct" and \
            currNode.getType() != "comp":
        pos = currNode.getType()[:len(currNode.getType())-1]
        type = currNode.getType()[len(currNode.getType())-1:]
        all_matches = rules["X" + type]

        matches = []
        for rule in all_matches:
            if len(rule) == len(children):
                if isinstance(children[0], str):
                    if rule[0] == "X'" or rule[0] == "X":
                        matches.append(rule)
                elif isinstance(children[0], list):
                    if rule[0] == "spec" or rule[0] == "adjunct" or rule[0] == "comp":
                        matches.append(rule)

        c_matches = []
        for rule in matches:
            c_rules = []
            for node in rule:
                c_rules.append(node.replace("X", pos))
            c_matches.append(c_rules)
        return c_matches                    
    else:
        return rules[currNode.getType()]

def makeNodeTree(s, currNode, level=1):
    if isinstance(s, str):
        type = currNode.getType()[:len(currNode.getType())-1]
        if type == "":
            type = currNode.getType()
        if currNode.getType().endswith("'"):
            currNode.addChild(Leaf(s, type, level+1))
            return currNode
        else:
            return Leaf(s, type, level+1)

    rules = matchRule(currNode, s)
    if len(rules) == 1:
        rule = rules[0]
        for r, child in zip(rule, s):
            currNode.addChild(makeNodeTree(child, Node([], r, level+1), level+1))

    elif currNode.getType() == "spec" or\
            currNode.getType() == "adjunct" or\
            currNode.getType() == "comp":
        types = []
        for child in s:
            if isinstance(child, list):
                types.append("list")
            else:
                types.append(d[child])

        if "V" in types and ["VP"] in rules:
            currNode.setType("VP")
        elif "N" in types and ["NP"] in rules:
            currNode.setType("NP")
        elif "Adv" in types and ["AdvP"] in rules:
            currNode.setType("AdvP")
        elif "Adj" in types and ["AdjP"] in rules:
            currNode.setType("AdjP")
        elif "D" in types and ["DP"] in rules:
            currNode.setType("DP")
        else:
            return None

        return makeNodeTree(s, currNode, level)

    else:
        poss = []
        for rule in rules:
            if isinstance(s[0], list):
                p = makeNodeTree(s[0], Node([], rule[0], level+1), level+1)
            else:
                p = makeNodeTree(s[1], Node([], rule[1], level+1), level+1)

            if p != None:
                poss.append(rule)

        if len(poss) == 1:
            currNode.addChild(makeNodeTree(s[0], Node([], poss[0][0], level+1), level+1))
            currNode.addChild(makeNodeTree(s[1], Node([], poss[0][1], level+1), level+1))

    return currNode

def makeTree(s):
    p = makeNodeTree(s, Node([], "IP", 1))
    return ParseTree(p)

p = makeTree([[["the"], "barn"], ["[pres]", ["is", ["very", ["red"]]]]])
print p
#p = makeTree([[[["the"]], ["barn"]], ["[pres]", [["is"], [["red"]]]]])
#print p
#p = makeTree([[[["the"]], ["barn"]], ["[pres]", [[["is"], [["very"], [["red"]]]]]]])
#print p
