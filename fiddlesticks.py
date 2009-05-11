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
