#!/usr/bin/env python
"""
Decode sys.stdin using an HMM.

TODO: Retrieve sigma from the model, not the hyperparameters!
"""

import sys
import string
from common.file import myopen
from common.stats import stats
import ghmm

import common.hyperparameters, common.options
HYPERPARAMETERS = common.hyperparameters.read("wordrepresentations-hmm")
HYPERPARAMETERS, options, args = common.options.reparse(HYPERPARAMETERS)
print >> sys.stderr, "Hyperparameters:", HYPERPARAMETERS

print >> sys.stderr, "Reading model from %s..." % HYPERPARAMETERS["hmmfile"]
print >> sys.stderr, stats()
#model = ghmm.HMMOpen(HYPERPARAMETERS["hmmfile"], model_index = 1) # Pick 1-st model out of the smo file
model = ghmm.HMMOpen(HYPERPARAMETERS["hmmfile"])
print >> sys.stderr, "...done reading model from %s" % HYPERPARAMETERS["hmmfile"]
print >> sys.stderr, stats()

# TODO: Retrieve sigma from the model, not the hyperparameters!
sigma = ghmm.IntegerRange(0, HYPERPARAMETERS["vocabulary"])

print >> sys.stderr, "Reading sys.stdin..."
print >> sys.stderr, stats()
for l in sys.stdin:
    lst = [int(n) for n in string.split(l)]
#    lst = [int(n) for n in string.split(l) if int(n) < HYPERPARAMETERS["vocabulary"]]
    seq = ghmm.EmissionSequence(sigma, lst)

    posterior = model.posterior(seq)
    assert len(posterior) == len(lst)
    for p in posterior: assert len(p) == HYPERPARAMETERS["states"]
    print posterior
