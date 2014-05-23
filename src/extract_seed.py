#!/usr/bin/env python2.7

from __future__ import division
import os, sys
import collections
import operator
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--seed_dir", default="../data/seed")
parser.add_argument("--out_seed_file", default="../data/seed.txt")

args = parser.parse_args()

def ExtractSeed(seed_dir, seed_file):
  seed = open(seed_file, "w")
  stats = collections.defaultdict(int)
  types = collections.defaultdict(int)
  tokens = 0
  for path, dirs, files in os.walk(seed_dir):
    for f in files:
      label = f.split("_")[1].split(".")[0]
      for line in open(os.path.join(seed_dir, f)):
        line = line.strip().lower()
        if line and line.isalpha() and "-" not in line:
          stats[label]+=1
          types[line]+=1
          tokens += 1
          seed.write(line + "\t" + label.upper() + "\n")

  print "Num. tokens:", tokens
  print "Num. types:", len(types.keys())
  multilabel = sum([1 for k, v in types.iteritems() if v > 1])
  print "Num words with more than one label:", multilabel, "(", multilabel/len (types.keys())*100, "% of training data )"
  print "Stats per label:"
  for k, v in sorted(stats.iteritems(), key=operator.itemgetter(1), reverse=True):
    print k, v

def main():
  ExtractSeed(args.seed_dir, args.out_seed_file)

if __name__ == '__main__':
  main()

"""
Output:

Num. tokens: 1417
Num. types: 1325
Num words with more than one label: 86 ( 6.49056603774 % of training data )
Stats per label:
substance 189
feeling 165
perception 161
spatial 145
time 138
body 108
relation 100
social 99
quantity 92
behavior 88
mind 57
motion 42
weather 33

"""
