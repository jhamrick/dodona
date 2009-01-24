from textwrap import fill

def print_list(list):
    list.sort()
    printed = ""
    for item in list:
        printed = printed + " - " + str(item) + "\n"
    return printed

#same as fill, except it preserves newlines
def custom_fill(s):
    news = ""
    while s.partition("\n")[2] != "":
        news += fill(s.partition("\n")[0]) + "\n"
        s = s.partition("\n")[2]
    news += fill(s.partition("\n")[0])
    return news

def tokenize(mess):
    words = []
    #print mess
    oldchars = ""
    for char in mess:
        #print char
        if char == "," or \
           char == "." or \
           char == "?" or \
           char == "!" or \
           char == "\'" or \
           char == "\"":
            if not oldchars == "":
                words.append(oldchars)
                oldchars = ""
            words.append(char)
        elif char == " " and not oldchars == "":
            words.append(oldchars)
            oldchars = ""
        elif char == " " and oldchars == "":
            pass
        else:
            oldchars += char
    if oldchars != "":
        words.append(oldchars)
    #print words
    return words

def integrate_lists(list1, list2):
    for item in list2:
        if list1.count(item) == 0:
            list1.append(item)
    return list1

def find_partial_key(word, list):
    keys = []
    for key in list.keys():
        key2 = tokenize(key)
        for k in key2:
            if k == word:
                keys.append(key)
                break
    return keys
