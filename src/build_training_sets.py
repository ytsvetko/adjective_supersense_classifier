#!/usr/bin/env python2.7

import sys, os
import collections
import codecs
import argparse
from itertools import izip
import json 

parser = argparse.ArgumentParser()

parser.add_argument("--in_file", required=True)
parser.add_argument("--out_feat", required=True)
parser.add_argument("--out_labels", required=True)

parser.add_argument("--test_set")
parser.add_argument("--out_test_feat")
parser.add_argument("--out_test_labels")
parser.add_argument("--features")
parser.add_argument("--include_training", action='store_true', default=False)

args = parser.parse_args()

def LoadVectors(embeddings_filename):
  feature_vectors = {}
  for line in open(embeddings_filename):
    tokens = line.strip().split()
    word = tokens[0].lower()
    features = tokens[1:]
    if not word.isalpha():
      continue
    features_dict = { "V_"+str(ind) : float(str_feat) for ind, str_feat in enumerate(features) }
    feature_vectors[word] = features_dict
  return feature_vectors

def main(argv):
  vectors = LoadVectors(args.features)

  out_features = open(args.out_feat, "w")
  out_labels = open(args.out_labels, "w")
  seen_in_training = set()
  for line in open(args.in_file):
    tokens = line.strip().split("\t")
    if len(tokens) == 1:
      continue
    if len(tokens) == 2:
      tokens.append("seed")
    word, label, relation = tokens
    if word not in vectors:
      continue
    seen_in_training.add(word)
    features_str = json.dumps(vectors[word], sort_keys=True)
    out_features.write("{}_{}_{}\t{}\n".format(word, label, relation, features_str))
    out_labels.write("{}_{}_{}\t{}\n".format(word, label, relation, label.upper()))

  if args.out_test_feat:
    test_features_file = open(args.out_test_feat, "w")
    if args.test_set is None:
      for word, features in sorted(vectors.iteritems()):
        if not args.include_training and word in seen_in_training:
          continue
        features_str = json.dumps(features, sort_keys=True)
        test_features_file.write("{}_vocab\t{}\n".format(word, features_str))
    else:
      test_labels_file = open(args.out_test_labels, "w")
      for line in open(args.test_set):
        word, label, relation = line.strip().split("\t")
        if word not in vectors:
          continue
        if word in seen_in_training:
          continue
        features_str = json.dumps(vectors[word], sort_keys=True)
        test_features_file.write("{}_{}_{}\t{}\n".format(word, label, relation, features_str))
        test_labels_file.write("{}_{}_{}\t{}\n".format(word, label, relation, label.upper()))

if __name__ == '__main__':
  main(sys.argv)

