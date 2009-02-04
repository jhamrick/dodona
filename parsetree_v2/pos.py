class POSDict:
    def __init__(self):
        pos = open("part-of-speech", "r")

        self.d = {}
        line = pos.readline()
        while line != "":
            line = pos.readline()
            l = line.partition("\t")
            self.d[l[0]] = []
            parts = l[2].strip()
            for part in parts:
                if part != "|": self.d[l[0]].append(part)
            print l[0]

        pos.close()

        self.translations = {"N": "Noun",
                             "P": "Plural",
                             "h": "Noun Phrase",
                             "V": "Verb",
                             "t": "Transitive Verb",
                             "i": "Intransitive Verb",
                             "A": "Adjective",
                             "v": "Adverb",
                             "C": "Conjunction",
                             "P": "Preposition",
                             "!": "Interjection",
                             "r": "Pronoun",
                             "D": "Definite Article",
                             "I": "Indefinite Article",
                             "o": "Nominative"}

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
