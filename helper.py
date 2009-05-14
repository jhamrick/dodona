from textwrap import fill

def print_list(list):
    """
    Return a nicely formatted list
    (of topics, for example)
    """
    list.sort()
    printed = ""
    for item in list:
        
        if str(item).startswith("default"): continue
        printed = printed + " - " + str(item) + "\n"
    return printed

def custom_fill(s):
    """
    Perfoms the same function as fill, except
    that custom_fill preserves newlines.
    """
    news = ""
    while s.partition("\n")[2] != "":
        news += fill(s.partition("\n")[0]) + "\n"
        s = s.partition("\n")[2]
    news += fill(s.partition("\n")[0])
    return news

def tokenize(mess):
    """
    Split the sentence into a list, which contains words and some
    punctuation, but no whitespace.
    """
    mess = mess.replace(",", " , ")
    mess = mess.replace(".", " . ")
    mess = mess.replace("?", " ? ")
    mess = mess.replace("!", " ! ")
    mess = mess.replace("\'s ", " \'s ")
    mess = mess.split(" ")
    temp = mess
    offset = 0

    for w in xrange(len(temp)):
        if mess[w-offset] == "": 
            del mess[w-offset]
            offset += 1

    return mess

def integrate_lists(list1, list2):
    """
    Combines two lists, such that there are no
    repeat items.
    """
    for item in list2:
        if list1.count(item) == 0:
            list1.append(item)
    return list1

def find_partial_key(word, dict):
    """
    Searches a dictionary of keys, some of which
    are multiple words (in a single string), for a
    given word, and returns all keys in which the
    word appears.
    """
    keys = []
    for key in dict.keys():
        key2 = tokenize(key)
        for k in key2:
            if k == word:
                keys.append(key)
                break
    return keys
