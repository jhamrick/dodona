#!/usr/bin/env python2.5
#
# A utility class to compute the span (constituent)
# intersection between two parse trees.
# Example:
#
#  intersection_spans = spans_intersection_from_sexp(reference, parsed)
#
# where reference and parsed are s-expressions like (S (NP ...)).
# The returned intersection_spans is a list strings of the form:
#      <non-terminal>:[leaf words]
#
# - yks 2/19/2009
#
import nltk
import sys
import re
from nltk.util import *
from optparse import OptionParser

def tree_from_sexp(sexp):
    """
    parses an s-expression into a tree
    """
    return nltk.bracket_parse(sexp)

def train(training):
    """
    Generate maximum likelihood estimates of
    productions from a training file of s-expression trees.
    """
    tfd = open(options.training)
    parses = tfd.readlines()
    parses = [parse.strip() for parse in parses]
    
    counts = {}
    for parse in parses:
	if parse != "failure":
	    tree = tree_from_sexp(parse)
	    productions = tree.productions()
	    for production in productions:
		if not counts.has_key(production):
		    counts[production] = 0
		counts[production] += 1

    lhs_map = {}
    for production in counts.keys():
	if not lhs_map.has_key(production.lhs()):
	    lhs_map[production.lhs()] = []
	lhs_map[production.lhs()].append(production)

    keys = lhs_map.keys()
    keys.sort()

    weights = {}
    for key, productions in lhs_map.items():
	total = 0;
	for production in productions:
	    total += counts[production]

	for production in productions:
	    weights[production] = max(1,
				      int(counts[production]/float(total)*100))
    regexp_hash = {}
    for key in keys:
	productions = lhs_map[key]
	for production in productions:
	    rhs_symbols = [str(nt) for nt in production.rhs()]
	    string_symbols = ' '.join(rhs_symbols)
	    string_symbols = re.escape(string_symbols)
	    regexp = "^\\d+\\s+%s\\s+%s$" %(production.lhs(), string_symbols)
					    
	    regexp_hash[regexp] = production
    return weights, regexp_hash, lhs_map

def replace_weights(regexp_hash, weights, input_file, output_file):
    ifd = open(input_file)
    lines = ifd.readlines()
    lines = [line.strip() for line in lines]
    ifd.close()

    ofd = open(output_file, "w")

    for line in lines:
	if re.match("^\s*#", line) or re.match("^\s*$", line):
	    ofd.write(line + "\n")
	else:
	    replaced = False
	    for regexp, production in regexp_hash.items():
		if re.match(regexp, line):
		    rhs_symbols = [str(nt) for nt in production.rhs()]
		    replacement = "%d\t%s\t%s" %(weights[production],
						   production.lhs(),
						   ' '.join(rhs_symbols))
		    ofd.write(replacement)
		    ofd.write("\n")
		    print "Replaced: [%s] with [%s]" %(line, replacement)
		    replaced = True
		    break

	    if not replaced:
		print "WARNING: missing training data for: %s" %(line)
		ofd.write(line)
		ofd.write("\n")
    ofd.close()
		
def print_weights(lhs_map, weights):
    keys = lhs_map.keys()
    keys.sort()
    for key in keys:
	productions = lhs_map[key]
	print "#"
	for production in productions:
	    rhs_symbols = [str(nt) for nt in production.rhs()]
	    print "%d\t%s\t%s" %(weights[production],
				      production.lhs(),
				      ' '.join(rhs_symbols))
	    
if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
		      help="input grammar filename", metavar="file")
    parser.add_option("-o", "--output", dest="output",
		      help="output grammar filename", metavar="file")
    parser.add_option("-t", "--training", dest="training",
		      help="s-expression training filename",metavar="file")
      
    (options, args) = parser.parse_args()

    if options.training is None:
	parser.print_help()
	exit(1)

    weights, regexp_hash, lhs_map = train(options.training)
    if options.input is None:
	print_weights(lhs_map, weights)
    else:
	if options.output is None:
	    options.output = options.input + ".tuned"
	print "reading grammar file: %s" %(options.input)
	print "outputting to file: %s" %(options.output)	    
	replace_weights(regexp_hash, weights,
			options.input, options.output)	
