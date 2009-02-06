class POSDict:
    def __init__(self):
#         pos = open("wordnet/data.adj", "r")

#         self.d = {}
#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[4] = l[4].replace("_", " ")
#             if not self.d.has_key(l[4]): self.d[l[4]] = []
#             if not "A" in self.d[l[4]]: self.d[l[4]].append("A")
#             #print l[4]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/adj.exc", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[0] = l[0].replace("_", " ")
#             l[1] = l[1].replace("_", " ")
#             if not self.d.has_key(l[0]): self.d[l[0]] = []
#             if not self.d.has_key(l[1]): self.d[l[1]] = []
#             if not "A" in self.d[l[0]]: self.d[l[0]].append("A")
#             if not "A" in self.d[l[1]]: self.d[l[1]].append("A")
#             #print l[4]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/adv.exc", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[0] = l[0].replace("_", " ")
#             l[1] = l[1].replace("_", " ")
#             if not self.d.has_key(l[0]): self.d[l[0]] = []
#             if not self.d.has_key(l[1]): self.d[l[1]] = []
#             if not "v" in self.d[l[0]]: self.d[l[0]].append("v")
#             if not "v" in self.d[l[1]]: self.d[l[1]].append("v")
#             #print l[4]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/noun.exc", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[0] = l[0].replace("_", " ")
#             l[1] = l[1].replace("_", " ")
#             if not self.d.has_key(l[0]): self.d[l[0]] = []
#             if not self.d.has_key(l[1]): self.d[l[1]] = []
#             if not "N" in self.d[l[0]]: self.d[l[0]].append("N")
#             if not "N" in self.d[l[1]]: self.d[l[1]].append("N")
#             #print l[4]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/verb.exc", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[0] = l[0].replace("_", " ")
#             l[1] = l[1].replace("_", " ")
#             if not self.d.has_key(l[0]): self.d[l[0]] = []
#             if not self.d.has_key(l[1]): self.d[l[1]] = []
#             if not "V" in self.d[l[0]]: self.d[l[0]].append("V")
#             if not "V" in self.d[l[1]]: self.d[l[1]].append("V")            #print l[4]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/data.adv", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[4] = l[4].replace("_", " ")
#             if not self.d.has_key(l[4]): self.d[l[4]] = []
#             if not "v" in self.d[l[4]]: self.d[l[4]].append("v")
#             #print l[4]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/data.noun", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[4] = l[4].replace("_", " ")
#             if not self.d.has_key(l[4]): self.d[l[4]] = []
#             if not "N" in self.d[l[4]]: self.d[l[4]].append("N")
#             #print l[4]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/data.verb", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[4] = l[4].replace("_", " ")
#             if not self.d.has_key(l[4]): self.d[l[4]] = []
#             if not "V" in self.d[l[4]]: self.d[l[4]].append("V")
#             #print l[4]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/data.conj", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[0] = l[0].replace("_", " ")
#             if not self.d.has_key(l[0]): self.d[l[0]] = []
#             if not "C" in self.d[l[0]]: self.d[l[0]].append("C")
#             #print l[0]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/data.prep", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[1] = l[1].replace("_", " ")
#             if not self.d.has_key(l[1]): self.d[l[1]] = []
#             if not "P" in self.d[l[1]]: self.d[l[1]].append("P")
#             #print l[1]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/data.pro", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[0] = l[0].replace("_", " ")
#             if not self.d.has_key(l[0]): self.d[l[0]] = []
#             if not "r" in self.d[l[0]]: self.d[l[0]].append("r")
#             #print l[0]
#             line = pos.readline()

#         pos.close()
#         pos = open("wordnet/data.det", "r")

#         line = pos.readline()
#         while line != "":
#             l = line.split()
#             l[0] = l[0].replace("_", " ")
#             if not self.d.has_key(l[0]): self.d[l[0]] = []
#             if not "D" in self.d[l[0]]: self.d[l[0]].append("D")
#             #print l[0]
#             line = pos.readline()

#         pos.close()

        self.d = {}
        pos = open("part-of-speech", "r")
        line = pos.readline()
        while line != "":
            l = line.partition("\t")
            self.d[l[0]] = []
            for p in l[2].strip():
                self.d[l[0]].append(p)
            line = pos.readline()
        pos.close()

        self.translations = {"N": "Noun",
                             "V": "Verb",
                             "A": "Adjective",
                             "v": "Adverb",
                             "C": "Conjunction",
                             "P": "Preposition",
                             "r": "Pronoun",
                             "D": "Determiner"}

    def read(self, key):
        return self.d[key][0]

    def read_and_translate(self, key):
        return self.translations[self.read(key)]

    def read_all(self, key):
        return self.d[key]

    def read_all_and_translate(self, key):
        pos = []
        for p in self.read_all(key):
            pos.append(self.translations[p])
        return pos

    def add(self, key, pos):
        if not self.d.has_key(key): self.d[key] = [pos]
        else: self.d[key].append(pos)

    def remove(self, key):
        del self.d[key]

    def replace(self, key, pos):
        self.d[key] = [pos]

    def save(self):
        pos = open("part-of-speech", "w")
        for d in self.d.keys():
            p = ""
            for i in self.d[d]: p += i
            pos.write(d + "\t" + p + "\n")
        pos.close()

d = POSDict()
