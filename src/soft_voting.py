#!/usr/bin/env python2.7

from __future__ import division
import sys
import json
import argparse
import collections
from nltk.corpus import wordnet as wn

parser = argparse.ArgumentParser()

parser.add_argument("--predicted_results", required=True)
parser.add_argument("--out_synset_file", default=None)
parser.add_argument("--out_lemma_file", default=None)

args = parser.parse_args()

def PosteriorList():
  return ([], [])

def CollectResults(predicted_results):
  synsets = collections.defaultdict(PosteriorList)
  for line in open(predicted_results):
    instance, label, posteriors_str = line.strip().split("\t")
    posteriors = json.loads(posteriors_str)
    # covert_substance_antonym
    word = instance.split("_")[0].lower()
    for synset in wn.synsets(word, wn.ADJ):
      p_list, w_list = synsets[synset]
      p_list.append(posteriors)
      w_list.append(word)
  return synsets

def ProcessResults(synsets, out_synset_file):
  for synset, (p_list, w_list) in synsets.iteritems():
    merged_posteriors = collections.defaultdict(float)
    for posteriors in p_list:
      for k, v in posteriors.iteritems():
        merged_posteriors[k] += v
    normalize_by = len(p_list)
    max_val, max_k = 0.0, None
    for k in merged_posteriors:
      merged_posteriors[k] /= normalize_by
      if merged_posteriors[k] > max_val:
        max_val = merged_posteriors[k]
        max_k = k
    out_synset_file.write("{}\t{}\t{}\t{}\n".format(synset, max_k, json.dumps(merged_posteriors), w_list))
  
def RemoveMetadata(predicted_results, out_lemma_file):
  out_file = open(out_lemma_file, "w")
  for line in open(predicted_results):
    word, label, vec = line.split("\t")
    out_file.write("{}\t{}\t{}".format(word.split("_")[0], label, vec))

def main():
  """
  if args.out_file is not None:
    out_file = open(args.out_file, "a")
  else:
    out_file = sys.stdout
  """
  RemoveMetadata(args.predicted_results, args.out_lemma_file)
  synsets = CollectResults(args.predicted_results)
  ProcessResults(synsets, open(args.out_synset_file, "w"))

if __name__ == '__main__':
  main()


