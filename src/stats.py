import collections
from operator import itemgetter
from nltk.corpus import wordnet as wn
from nltk.corpus import semcor

wn_lemmas = set()
for lemma in wn.all_lemma_names(pos=wn.ADJ):
  wn_lemmas.add(lemma)

wn_adj_synsets = collections.defaultdict(set)

for word in wn_lemmas:
  for synset in wn.synsets(word, wn.ADJ):
    wn_adj_synsets[synset.name.lower()] = [lemma.lower() for lemma in synset.lemma_names ]

semcor_adjectives = set()
i = 0
for sent in semcor.tagged_sents(tag='both'):
  for c,chk in enumerate(sent):
    if chk.node and len(chk.node)>3 and chk.node[-3]=='.' and chk.node[-2:].isdigit() and chk[0].node.startswith('JJ'):
      if len(chk.leaves()) == 1:
        semcor_adjectives.add(chk.leaves()[0].lower())


semcor_synsets = set()
for s, words in wn_adj_synsets.items():
  for w in words:
    if w in semcor_adjectives:
      semcor_synsets.add(s.lower())

vectors = set()
vector_adj_file = open("data/VSM/eacl14-faruqui-en-svd-de-64.adj", "w")
for line in open("data/VSM/eacl14-faruqui-en-svd-de-64.adj.txt"):
  w = line.split()[0]
  vectors.add(w)
  if w in wn_lemmas:
    vector_adj_file.write(line)




len(wn_lemmas)
len(wn_adj_synsets)
len(semcor_adjectives)
len(semcor_synsets)
len(semcor_adjectives & vectors & wn_lemmas)

"""
After lowercase

>>> len(wn_lemmas)
21479
>>> len(wn_adj_synsets)
18156
>>> len(semcor_adjectives)
5370
>>> len(semcor_synsets)
7809
>>> len(semcor_adjectives & vectors & wn_lemmas)
4400
>>> 
>>> len(wn_lemmas &  vectors)
12148
>>> 

>>> 

"""


