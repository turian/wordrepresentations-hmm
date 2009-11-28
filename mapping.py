"""
Mapping between int and word.
"""

import sys, string
from common.stats import stats
from common.file import myopen

def to_word(i):
    _read()
    return mapping_to_word[i]

def from_word(w):
    _read()
    if w not in mapping_from_word:
        assert mapping_to_word[0] == "*UNKNOWN*"
        return 0
    else:
        return mapping_from_word[w]

mapping_to_word = None
mapping_from_word = None
def _read():
    global mapping_to_word, mapping_from_word
    if mapping_to_word is not None: return
    import common.hyperparameters
    HYPERPARAMETERS = common.hyperparameters.read("wordrepresentations-hmm")
    print >> sys.stderr, "Reading map file %s" % HYPERPARAMETERS["train mapfile"]
    print >> sys.stderr, stats()
    mapping_to_word = {}
    mapping_from_word = {}
    cnt = 0
    for l in myopen(HYPERPARAMETERS["train mapfile"]):
        w = string.split(l)[0]
        mapping_to_word[cnt] = w
        mapping_from_word[w] = cnt
        cnt += 1
