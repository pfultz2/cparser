#!/usr/bin/python

import sys, re

def print_ln(n):
   sys.stdout.write("\n")
   for i in range(n): sys.stdout.write(' ')
tab = 0
for line in sys.stdin.readlines():
    for word in re.findall('[\w]+|\S', line):
        word = word.strip()
        if (word is "{"):
            print_ln(tab)
            tab = tab + 4
        elif (word is "}"):
            tab = tab - 4
            print_ln(tab)
        sys.stdout.write(word)
        if (word in ['{', '}', ';']):
            print_ln(tab)
        else: sys.stdout.write(' ')
