import ghmm

# example code for a discrete HMM for generating random DNA sequences

file = "/u/turian/dev/common-scripts/integers-english-wikitext.lowercase.validation.50K.txt.gz"
mapfile = "/u/turian/dev/python/language-model/embeddings-wikipedia-20090819-english.lowercase.with-unknown-word.LEARNING_RATE=0_0000000032_EMBEDDING_LEARNING_RATE=0_0000032.model-1080000000.txt"
hmmfile = "hmm-integers-english-wikitext.lowercase.validation.50K.xml"
vocab = 50000
states = 80

# Cap number of training sequences
trainingseqs = 10

#vocab = 10
#states = 2

sigma = ghmm.IntegerRange(0, vocab)

import numpy
A = numpy.random.rand(states, states).tolist()
B = numpy.random.rand(states, vocab).tolist()
pi = [0.5] * states

# generate model from parameter matrices
model = ghmm.HMMFromMatrices(sigma,ghmm.DiscreteDistribution(sigma), A, B, pi)

# re-normalize model parameters
model.normalize()

import sys
import string
from common.file import myopen

mapping = {}
cnt = 0
for l in myopen(mapfile):
    mapping[cnt] = string.split(l)[0]
    cnt += 1

seqs = []
for l in myopen(file):
    lst = [int(n) for n in string.split(l)]
#    lst = [int(n) for n in string.split(l) if int(n) < vocab]
    if len(lst) > 0:
        seqs.append(lst)
#        print [mapping[n] for n in lst]
print >> sys.stderr, "Making sequence set"
# FIXME
seqs = seqs[:trainingseqs]
seqs = ghmm.SequenceSet(sigma, seqs)
print seqs

# train model parameters
print >> sys.stderr, "Estimation"
#model.baumWelch(seqs)
model.baumWelch(seqs,loglikelihoodCutoff=0.001)
#model.baumWelch(seq_set)
#model.baumWelch(seq_set,5,0.01)

# sample 10 sequences of length 20
seq_set = model.sample(10,20)
#print seq_set
for s in seq_set:
    print [mapping[n] for n in s]

print >> sys.stderr, "Writing hmm to %s" % hmmfile
model.write(hmmfile)

print >> sys.stderr, "Reading hmm from %s" % hmmfile
model2 = ghmm.HMMOpen(hmmfile)

# sample 10 sequences of length 20
seq_set = model2.sample(10,20)
#print seq_set
for s in seq_set:
    print [mapping[n] for n in s]
