#!/usr/bin/python
# -*- coding: latin1 -*-
"""
SYNOPSIS

    

DESCRIPTION

    

EXAMPLES

    

EXIT STATUS

    

AUTHOR

    luca.mella@studio.unibo.it

LICENSE

    Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)

VERSION

    0.2
"""

import scipy.stats
import numpy as np
import sys, math
from optparse import OptionParser
from collections import defaultdict


class PoV:

    def __init__(self): 
        self.pov = defaultdict (lambda: 1)
        self.length = 256
        for i in range(self.length):
            self.pov[i] = 1

    def getExpected (self):
        result = defaultdict(lambda: 1 ) #[pov.length / 2];
        for i in range(self.length/2):
            avg = (self.pov[2 * i] + self.pov[2 * i + 1]) / 2.0
            result[i] = avg
        return result

    def incPov(self, i):
        self.pov[i]+=1

    def  getPov(self):
        result = defaultdict(lambda: 1 )
        for i in range(self.length/2):
            result[i] = self.pov[2 * i + 1]
        return result
    

def dochisquare( inputfile , chunksize ):
    pov = PoV()
    i = 0
    char = inputfile.read(1)
    while char != '': 
        b = ord(char)
        pov.incPov(b)
        if  i % chunksize == 0 and i != 0:
            obs = np.array( [x for x in pov.getPov().itervalues() ])
            exp = np.array( [x for x in pov.getExpected().itervalues() ])
            (chi,pval) = scipy.stats.chisquare(obs,exp)
            print pval
        i+=1
        char = inputfile.read(1) 
    return

parser = OptionParser("usage: %prog [OPTIONS] ARGS \nWill receive experimental bitstring in STDIN")
parser.add_option("-s", "--size",dest="size", action="store", type="int",
                  default=128,help="block size considered in chi-square analysis", metavar="BLOCKSIZE")

(options, args) = parser.parse_args()

chnksz = options.size

if chnksz == 0 :
    chnksz = 128

dochisquare( sys.stdin , chnksz )

