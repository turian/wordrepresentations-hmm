#!/usr/bin/env python
"""
Decode sys.stdin using an HMM.

For each filename listed in sys.stdin, read the file and output a file called file.hmmfile.txt

TODO: Retrieve sigma from the model, not the hyperparameters!
"""

import sys
import string
from common.file import myopen
from common.stats import stats
import ghmm

import mapping
import popen2

import common.hyperparameters, common.options
HYPERPARAMETERS = common.hyperparameters.read("wordrepresentations-hmm")
HYPERPARAMETERS, options, args, newkeystr = common.options.reparse(HYPERPARAMETERS)
print >> sys.stderr, "Hyperparameters:", HYPERPARAMETERS

print >> sys.stderr, "Reading model from %s..." % HYPERPARAMETERS["hmmfile"]
print >> sys.stderr, stats()
#model = ghmm.HMMOpen(HYPERPARAMETERS["hmmfile"], model_index = 1) # Pick 1-st model out of the smo file
model = ghmm.HMMOpen(HYPERPARAMETERS["hmmfile"])
print >> sys.stderr, "...done reading model from %s" % HYPERPARAMETERS["hmmfile"]
print >> sys.stderr, stats()

# TODO: Retrieve sigma from the model, not the hyperparameters!
sigma = ghmm.IntegerRange(0, HYPERPARAMETERS["vocabulary"])

for f in sys.stdin:
    f = string.strip(f)
    fnew = "%s.%s.txt" % (f, HYPERPARAMETERS["hmmfile"])
    print >> sys.stderr, "Reading %s, writing %s..." % (f, fnew)
    print >> sys.stderr, stats()
    (child_stdout, child_stdin) = popen2.popen2("~/data/NER-GoldData/one-sentence-per-line.py < %s" % f)
    outfile = open(fnew, "wt")
    for l in child_stdout:
        if string.strip(l) == "": continue
        words = string.split(l)
        lst = [mapping.from_word(w) for w in words]
    #    lst = [int(n) for n in string.split(l) if int(n) < HYPERPARAMETERS["vocabulary"]]
        seq = ghmm.EmissionSequence(sigma, lst)
    
        posterior = model.posterior(seq)
        assert len(posterior) == len(lst)
        for p in posterior: assert len(p) == HYPERPARAMETERS["states"]
    #    print posterior
        for w, p in zip(words, posterior):
            outfile.write("%s %s\n" % (w, string.join([`pr` for pr in p])))
        outfile.write("\n")
