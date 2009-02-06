################################
# A dictionary containing words
# and their associated part(s)
# of speech.  Reads the data
# in from a file and saves to
# the same file when changes
# are made.
################################

class POSDict:
    def __init__(self, file="part-of-speech"):
        self.file = file

        # Open and read from the file specified
        self.d = {}
        pos = open(file, "r")
        line = pos.readline()
        while line != "":
            l = line.partition("\t")
            self.d[l[0]] = []
            for p in l[2].strip():
                self.d[l[0]].append(p)
            line = pos.readline()
        pos.close()

        # Set the dictionary for translations,
        # used in the functions read_and_translate
        # and read_all_and_translate
        self.translations = {"N": "Noun",
                             "V": "Verb",
                             "A": "Adjective",
                             "v": "Adverb",
                             "C": "Conjunction",
                             "P": "Preposition",
                             "r": "Pronoun",
                             "D": "Determiner",
                             "p": "Punctuation"}

    def read(self, key):
        """
        Returns the first part of speech associated
        with the word.
        """
        return self.d[key][0]

    def read_and_translate(self, key):
        """
        Returns the first part of speech associated
        with the word, translated to an actual word
        using self.translations, defined in __init__
        """
        return self.translations[self.read(key)]

    def read_all(self, key):
        """
        Returns a list of all the parts of
        speech associated with the word.
        """
        return self.d[key]

    def read_all_and_translate(self, key):
        """
        Returns a list of all the parts of speech
        associated with the word, translated to an
        actual word using self.translations,
        defined in __init__
        """
        pos = []
        for p in self.read_all(key):
            pos.append(self.translations[p])
        return pos

    def add(self, key, pos):
        """
        Adds a new part of speech to an existing word,
        or adds a word and the part of speech associated
        with it.  Saves the data to file afterwards.
        """
        if not self.d.has_key(key): self.d[key] = [pos]
        else: self.d[key].append(pos)
        self.save()

    def remove(self, key):
        """
        Removes a word from the dictionary, and saves
        the data to file.
        """
        del self.d[key]
        self.save()

    def replace(self, key, pos):
        """
        Replaces the parts of speech associated with a
        word with a new part of speech, and then saves
        the data to file.
        """
        self.d[key] = [pos]
        self.save()

    def save(self):
        """
        Saves the data to file.
        """
        pos = open("part-of-speech", "w")
        for d in self.d.keys():
            p = ""
            for i in self.d[d]: p += i
            pos.write(d + "\t" + p + "\n")
        pos.close()
