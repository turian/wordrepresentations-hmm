#!/usr/bin/env python
"""
Train an HMM on the given data.

TODO: Want to be able to infer vocabulary size based upon the map file.
TODO: Or, better yet, just learn HMM directly over word vocabulary, not integer vocabulary.
"""

import sys
import string
from common.file import myopen
from common.stats import stats
import ghmm

import common.hyperparameters, common.options
HYPERPARAMETERS = common.hyperparameters.read("wordrepresentations-hmm")
HYPERPARAMETERS, options, args, newkeystr = common.options.reparse(HYPERPARAMETERS)
print >> sys.stderr, "Hyperparameters:", HYPERPARAMETERS

sigma = ghmm.IntegerRange(0, HYPERPARAMETERS["vocabulary"])

# WARNING: I do not know if the HMM initialization is correct.
import numpy
numpy.random.seed(0)
A = numpy.random.rand(HYPERPARAMETERS["states"], HYPERPARAMETERS["states"]).tolist()
B = numpy.random.rand(HYPERPARAMETERS["states"], HYPERPARAMETERS["vocabulary"]).tolist()
pi = [0.5] * HYPERPARAMETERS["states"]

# generate model from parameter matrices
model = ghmm.HMMFromMatrices(sigma,ghmm.DiscreteDistribution(sigma), A, B, pi)

# re-normalize model parameters
model.normalize()

print >> sys.stderr, "Reading map file %s" % HYPERPARAMETERS["train mapfile"]
print >> sys.stderr, stats()
mapping = {}
cnt = 0
for l in myopen(HYPERPARAMETERS["train mapfile"]):
    mapping[cnt] = string.split(l)[0]
    cnt += 1

print >> sys.stderr, "Reading train file %s" % HYPERPARAMETERS["train file"]
print >> sys.stderr, stats()
seqs = []
for l in myopen(HYPERPARAMETERS["train file"]):
    lst = [int(n) for n in string.split(l)]
#    lst = [int(n) for n in string.split(l) if int(n) < HYPERPARAMETERS["vocabulary"]]
    if len(lst) > 0:
        seqs.append(lst)
#        print [mapping[n] for n in lst]
    if len(seqs) >= HYPERPARAMETERS["maximum training sequences"] and HYPERPARAMETERS["maximum training sequences"] is not None:
        print >> sys.stderr, "Whoops! Stopping reading after %d sequences" % len(seqs)
        break
print >> sys.stderr, "Making sequence set"
print >> sys.stderr, stats()
seqs = ghmm.SequenceSet(sigma, seqs)
print >> sys.stderr, seqs

initial_nll = -model.loglikelihood(seqs)
print >> sys.stderr, "Initial negative log-likelihood =", initial_nll

# train model parameters
print >> sys.stderr, "Estimation"
print >> sys.stderr, stats()
# WARNING: I am not sure if my Baum-Welch stopping criterion is appropriate.
#model.baumWelch(seqs,loglikelihoodCutoff=0.001)
model.baumWelch(seqs)

trained_nll = -model.loglikelihood(seqs)
print >> sys.stderr, "Final negative log-likelihood =", trained_nll 
print >> sys.stderr, "Baum-Welch training improved the log-likelihood by ", initial_nll - trained_nll

#print seq_set
print >> sys.stderr, "Sampling"
print >> sys.stderr, stats()
# sample 10 sequences of length 20
seq_set = model.sample(10,20)
for s in seq_set:
#    print >> sys.stderr, [n for n in s]
    print >> sys.stderr, [mapping[n] for n in s]

print >> sys.stderr, "Writing hmm to %s" % HYPERPARAMETERS["hmmfile"]
print >> sys.stderr, stats()
model.write(HYPERPARAMETERS["hmmfile"])

#print >> sys.stderr, "Reading hmm from %s" % HYPERPARAMETERS["hmmfile"]
#model2 = ghmm.HMMOpen(HYPERPARAMETERS["hmmfile"])
#
## sample 10 sequences of length 20
#seq_set = model2.sample(10,20)
##print seq_set
#for s in seq_set:
#3    print [mapping[n] for n in s]
