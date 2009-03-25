cat rules.gr vocabulary.gr > grammar.gr
./randsent -n 1 -s START -g grammar.gr

#./randsent -t -n 10 -s START -g grammar.gr | ./prettyprint