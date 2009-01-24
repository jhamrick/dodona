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

# np = XPhrase([XBarComp([X("I", "N"), None], "N"), None], "N")
# vp = XPhrase([XBarComp([X("am", "V"), None], "V"), None], "V")
# ip = XPhrase([np, XBarComp([X("pres", "I"), vp], "I")], "I")
# p = ParseTree(ip)
# print p


def makeNodeTree(s, level=1):    
    if isinstance(s, str):
        return Leaf(s, d[s], level)

    children = []
    for child in s:
        children.append(makeNodeTree(child, level + 1))

    child = children[0]
    if not child.getType().endswith("\'") and not child.getType().endswith("P"):
        type = child.getType() + "\'"
    elif child.getType().endswith("\'"):
        if len(children) > 1:
            t = children[1].getType()
            if t == "AdvP" or t == "PP":
                type = child.getType()
            else:
                type = child.getType().partition("\'")[0] + "P"
        else:
            type = child.getType().partition("\'")[0] + "P"
    else:
        type = None

    if type == None and len(children) > 1:
        child = children[1]
        if not child.getType().endswith("\'") and not child.getType().endswith("P"):
            type = child.getType() + "\'"
        elif child.getType().endswith("\'"):
            t = children[0].getType()
            if t == "AdvP" or t == "PP":
                type = child.getType()
            else:
                type = child.getType().partition("\'")[0] + "P"

    return Node(children, type, level)

def makeTree(s):
    p = makeNodeTree(s)
    return ParseTree(p)

p = makeTree([[[["the"]], ["barn"]], ["[pres]", [["is"], [["red"]]]]])
print p
p = makeTree([[[["the"]], ["barn"]], ["[pres]", [[["is"], [["very"], [["red"]]]]]]])
print p
