#!/usr/bin/env python2.7

import argparse
import collections
import math
import random

parser = argparse.ArgumentParser()

parser.add_argument("--seed_file", required=True)
parser.add_argument("--out_test", required=True)
parser.add_argument("--out_train", required=True)
parser.add_argument("--features", required=True)
parser.add_argument("--fraction", type=float, default=0.10)

args = parser.parse_args()

def LoadSeed(filename, vocab):
  result = collections.defaultdict(list)
  for line in open(filename):
    tokens = line.strip().lower().split("\t")
    if len(tokens) == 1:
      continue
    if len(tokens) == 2:
      tokens.append("seed")
    word, label, relation = tokens
    if word not in vocab:
      print "Not in vocab" , word
      continue
    result[label].append( (word, relation) )
  return result

def LoadVocab(filename):
  result = set()
  for line in open(filename):
    result.add(line.strip().split()[0].lower())
  return result

def main():
  vocab = LoadVocab(args.features)
  seed = LoadSeed(args.seed_file, vocab)
  random.seed(4567)
  out_test = open(args.out_test, "w")
  out_train = open(args.out_train, "w")
  for label, elems in seed.iteritems():
    num_for_test = int(math.ceil(len(elems) * args.fraction))
    test_elems = set(random.sample(elems, num_for_test))
    print "label:", label, "\tnum_train:", len(elems) - num_for_test, "\tnum_test:", num_for_test
    for elem in elems:
      word, relation = elem
      if elem in test_elems:
        out_test.write("{}\t{}\t{}\n".format(word, label, relation))
      else:
        out_train.write("{}\t{}\t{}\n".format(word, label, relation))

if __name__ == '__main__':
  main()


