#!/usr/bin/env python2.7

import sys, os
import collections
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--predictions", required=True)
parser.add_argument("--orig_seed", required=True)
parser.add_argument("--out_file", required=True)

args = parser.parse_args()

def FilterUnmatching(in_file, out_file):
  for line in in_file:
    instance, predicted_label, weights = line.strip().split("\t")
    word, expanded_label, expand_method = instance.split("_")
    expanded_label = expanded_label.upper()
    if expanded_label == predicted_label:
      out_file.write("{}\t{}\n".format(word, expanded_label))

def main(argv):
  out_file = open(args.out_file, "w")
  for line in open(args.orig_seed):
    if len(line.strip()) != 0:
      out_file.write(line)
  predictions_file = open(args.predictions)
  FilterUnmatching(predictions_file, out_file)


if __name__ == '__main__':
  main(sys.argv)

