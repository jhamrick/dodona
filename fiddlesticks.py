##        if tree.lhs() == NT("Interrog_Clause"):
##            for i in xrange(len(tree)):
##                if re.match("^NP_.*$", tree[i].node):
##                    return tree[i],i
##            return [None, None]
##            rhs = tree.rhs()
##            if str(rhs[-1]).startswith("NP_"):
##                print "hi!"
##                #return " ".join(parse[-1][-1].leaves())                
##
##            if rhs[-1] == NT("Passive_Interrog_In"):
##                return parse
##                if parse[-1].contains(NT("NP_2nd")):
##                    return " ".join(parse[-1][-1].leaves())
##            #if rhs[-1] == NT("Passive_Interrog_Tr"):
##                return find_topic(rhs[-1], type)
##            elif \
##                rhs[-1] == NT("After_Verb_Tr") or \
##                rhs[-1] == NT("After_Verb_In"):
##                return find_topic(rhs[-1], type)
##        else:
##            print 'hi2'
##            print parse
##            for subtree in parse:
##                subj = find_topic(subtree, type)
##                if subj: return subj

        tree = parse[0]

        for i in xrange(len(tree)):
            if tree[i].node = "Passive_Interrog_In":
                for j in xrange(len(tree[i])):
                    if re.math("^NP_.*S", tree[i][j].node):
                        return tree[i][j].leaves()[0]
            if tree[i].node = "Passive_Interrog_Tr":
                for j in xrange(len(tree[i])):
                    if re.math("^NP_.*S", tree[i][j].node):
                        return tree[i][j].leaves()[0]

            

        for i in xrange(len(tree)):
            if tree[i].node == "Interrog_Clause":
                for j in xrange(len(tree[i])):
                    print tree[i][j].node
                    if tree[i][j].node == "Passive_Interrog_In":
                        for k in xrange(len(tree[i][j])):
                           if re.match("^NP_.*$", tree[i][j][k].node):
                                return tree[i][j][k].leaves()[0]
                    if tree[i][j].node == "Passive_Interrog_Tr":
                        
                        for k in xrange(len(tree[i][j])):
                           if re.match("^NP_.*$", tree[i][j][k].node):
                                return tree[i][j][k].leaves()[0]

            if tree[i].node == "Ind_Clause_Ques_Aux":
                for j in xrange(len(tree[i])):
                    if tree[i][j].node == "Ind_Clause_Inf":
                        
                        for k in xrange(len(tree[i][j])):
                           if re.match("^NP_.*$", tree[i][j][k].node):
                                return tree[i][j][k].leaves()[0]
                    if tree[i][j].node == "Passive_Interrog_Tr":
                        print "here"
                        for k in xrange(len(tree[i][j])):
                           if re.match("^NP_.*$", tree[i][j][k].node):
                                return tree[i][j][k].leaves()[0]

