#!/usr/bin/env python2.7

import sys, os
import collections
import argparse
from nltk.corpus import wordnet as wn

#TODO filter out proposals to expand the set that contradict with other training sets. 

parser = argparse.ArgumentParser()

parser.add_argument("--labeled_data", required=True)
parser.add_argument("--out_file", required=True)
parser.add_argument("--expand", action='store_true', default=False)

args = parser.parse_args()

relation_priorities = {
  'seed': 10,
  'ADJ-er': 11,
  'ADJ-est': 11,
  'un-ADJ': 11,
  'im-ADJ': 11,
  'in-ADJ': 11,
  'ADJ-less': 11,
  'synonym': 20,
  'antonym': 20,
  'hypernym': 30,
  'synonym-noun': 40,
  'antonym-noun': 40,
  'hypernym-noun': 50,
  'noun-supersense': 100,
}

def FindRelated(word):
  related = set()
  word = word.lower().strip()
  synsets = wn.synsets(word, wn.ADJ)
  for w in synsets:
    for synonym in w.lemmas:  
      related.add( (synonym.name, "synonym") )
      for hypernym in w.hypernyms():  
        related.add( (hypernym.name, "hypernym") )
      for antonym in synonym.antonyms():
        related.add( (antonym.name, "antonym") )

  related_through_lemma = set()
  for w, relation in related:
    related_through_lemma.update(ExpandThroughLemma(w))
  related.update(related_through_lemma)

  related_through_nouns = set()
  for w, relation in related:
    related_through_nouns.update(ExpandThroughNouns(w))
  related.update(related_through_nouns)

  return related

def ExpandThroughLemma(word):
  lemma_related = set()
  synsets = wn.synsets(word+"er", wn.ADJ)
  for w in synsets:
    for synonym in w.lemmas:  
      lemma_related.add( (synonym.name, "ADJ-er") )

  synsets = wn.synsets(word+"less", wn.ADJ)
  for w in synsets:
    for synonym in w.lemmas:  
      lemma_related.add( (synonym.name, "ADJ-less") )

  synsets = wn.synsets(word+"est", wn.ADJ)
  for w in synsets:
    for synonym in w.lemmas:  
      lemma_related.add( (synonym.name, "ADJ-est") )

  synsets = wn.synsets("un"+word, wn.ADJ)
  for w in synsets:
    for synonym in w.lemmas:  
      lemma_related.add( (synonym.name, "un-ADJ") )

  synsets = wn.synsets("in"+word, wn.ADJ)
  for w in synsets:
    for synonym in w.lemmas:  
      lemma_related.add( (synonym.name, "in-ADJ") )

  synsets = wn.synsets("im"+word, wn.ADJ)
  for w in synsets:
    for synonym in w.lemmas:  
      lemma_related.add( (synonym.name, "im-ADJ") )

  return lemma_related

def ExpandThroughNouns(word):
  nouns = set()
  for w in wn.synsets(word, wn.NOUN):
    for synonym in w.lemmas:  
      nouns.add( (synonym.name, "synonym-noun") )
      for hypernym in w.hypernyms():  
        nouns.add( (hypernym.name, "hypernym-noun") )
      for antonym in synonym.antonyms():
        nouns.add( (antonym.name, "antonym-noun") )
  noun_related = set()
  for (w, relation) in nouns:
    synsets = wn.synsets(w, wn.ADJ)
    for s in synsets:
      noun_related.add( (w, relation) )
  return noun_related

def LoadAndExpandSeed(filename, expand):
  word_dict = collections.defaultdict(list)
  for line in open(filename):
    if line.strip() == "" : 
      continue
    tokens = line.strip().lower().split()
    if len(tokens) == 3:
      word, label, relation = tokens
    else:
      word, label = tokens
    word_dict[word].append((label, "seed"))
    if expand:
      for related, relation in FindRelated(word):
        word_dict[related].append( (label, relation) )
  return word_dict

def LabelsFromVariants(variants):
  labels = {}
  for label, relation in variants:
    if label not in labels or relation == "seed":
      labels[label] = relation
  return labels
  
def main(argv):
  word_dict = LoadAndExpandSeed(args.labeled_data, args.expand)
  out_file = open(args.out_file, "w")
  for word, variants in word_dict.iteritems():
    labels = LabelsFromVariants(variants)
    while len(labels) > 1:
      lowest_priority = 0
      for label, relation in variants:
        lowest_priority = max(lowest_priority, relation_priorities[relation])

      new_variants = []
      for label, relation in variants:
        if relation_priorities[relation] < lowest_priority:
          new_variants.append( (label, relation) )
      variants = new_variants
      labels = LabelsFromVariants(variants)
    for label, relation in labels.iteritems():
      out_file.write("{}\t{}\t{}\n".format(word, label, relation))

if __name__ == '__main__':
  main(sys.argv)

