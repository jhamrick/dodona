class XPhrase:
    def __init__(self, list, type):
        if isinstance(list[0], XBar):
            self.xbar = list[0]
            self.spec = list[1]
        else:
            self.xbar = list[1]
            self.spec = list[0]
        
        self.type = type
        self.children = (list[0], list[1])

    def __str__(self):
        return self.type + "P\n" + str(self.children[0]) + "\n" + str(self.children[1])

    def getChildren(self):
        return self.children

    def getXBar(self):
        return self.xbar

    def getSpec(self):
        return self.spec

    def getType(self):
        return self.type

class XBar:
    def getType(self):
        return self.type

    def getChildren(self):
        return self.children

    def __str__(self):
        return self.type + "\'\n" + str(self.children[0]) + "\n" + str(self.children[1])

class XBarAdj(XBar):
    def __init__(self, list, type):
        if isinstance(list[0], XBar):
            self.xbar = list[0]
            self.adj = list[1]
        else:
            self.xbar = list[1]
            self.adj = list[0]
            
        self.type = type
        self.children = (list[0], list[1])

    def getXBar(self):
        return self.xbar

    def getAdj(self):
        return self.adj

class XBarComp(XBar):
    def __init__(self, list, type):
        if isinstance(list[0], X):
            self.x = list[0]
            self.comp = list[1]
        else:
            self.x = list[1]
            self.comp = list[0]
            
        self.type = type
        self.children = (list[0], list[1])

    def getX(self):
        return self.x

    def getComp(self):
        return self.comp

class X:
    def __init__(self, val, type):
        self.val = val
        self.type = type

    def getVal(self):
        return self.val

    def getType(self):
        return self.type

    def __str__(self):
        return self.type + "\n\"" + str(self.val) + "\""
