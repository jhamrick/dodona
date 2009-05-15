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
