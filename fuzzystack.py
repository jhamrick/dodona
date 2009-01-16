# Fuzzy stack
# 10 Jan 2009 kmill
# Something between a stack, a priority queue, and a dictionary
# Hopefully useful for NLP

class FuzzyStack :
    def __init__(self, depth=4) :
        self.data = list()
        self.depth = depth

    def __str__(self):
        d = self.get()
        p = ""
        for key in d.keys():
            p = p + str(key) + ": "
            if isinstance(d[key], dict):
                p = p + str(d[key].keys()) + "\n"
            else:
                p = p + str(d[key]) + "\n"
        return p

    # Pushes a new key/value pair onto the dictionary
    def push(self, symbol, value) :
        # Truncate the stack to the desired length if necessary
        if len(self.data) == self.depth :
            self.rpop(symbol)
        if len(self.data) == self.depth :
            self.popoldest()
        self.data.insert(0, (symbol, value));

    # Returns a dictionary of the most relevant keys
    def get(self) :
        output = dict()
        for d in reversed(self.data) :
            output[d[0]] = d[1]
        return output

    # Retrieve a key
    def read(self, symbol) :
        d = self.get()
        if d.has_key(symbol): return d[symbol]
        return None

    # Count the number of records with the given key
    def countSymbols(self, symbol) :
        return len([0 for d in self.data if d[0] == symbol])

    # get index^th record with a given key
    def readIndex(self, symbol, index) :
        return [d[1] for d in self.data if d[0] == symbol][index]

    # An iterator to do the previous function
    def values(self, symbol) :
        return [d[1] for d in self.data if d[0] == symbol].__iter__()

    # Sees what's on top of the stack
    def peek(self) :
        return self.data[0];

    # Pop off the data of a given key
    def pop(self, symbol) :
        for d in self.data :
            if(symbol == d[0]) :
                self.data.remove(d)
                return d
        return False

    # Pop off the oldest occurrance of a key
    def rpop(self, symbol) :
        index = -1
        for i in range(0, len(self.data)) :
            if(symbol == self.data[i][0]) :
                index = i
        if index >= 0 :
            return self.data.pop(index)
        else :
            return None

    # Pop off the key which is farthest down and has the most siblings
    def popoldest(self) :
        index = -1
        maxnum = 0
        keys = dict()
        for i in range(0, len(self.data)) :
            if not keys.has_key(self.data[i][0]) :
                keys[self.data[i][0]] = 0
            else :
                keys[self.data[i][0]] += 1
            if keys[self.data[i][0]] >= maxnum :
                maxnum = keys[self.data[i][0]]
                index = i
        if index >= 0 :
            return self.data.pop(index)
        else :
            return None

