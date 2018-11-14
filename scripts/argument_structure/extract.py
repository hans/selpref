"""
Extract a database of verb argument structures from a corpus.
"""


from argparse import ArgumentParser
from collections import namedtuple
import json
from pathlib import Path

from tqdm import tqdm


Token = namedtuple("Token", ["id", "word", "lemma", "pos_univ", "pos", "morph", "head", "deprel"])


def read_conllx(input_path):
  # stolen from spaCy and simplified

  text = input_path.open('r', encoding='utf-8').read()
  for sent in text.strip().split('\n\n'):
    lines = sent.strip().split('\n')
    if lines:
      while lines[0].startswith('#'):
        lines.pop(0)

      tokens = []
      for line in lines:
        parts = line.split('\t')
        id_, word, lemma, pos, tag, morph, head, deprel, _1, iob = parts
        if '-' in id_ or '.' in id_:
          continue
        try:
          id_ = int(id_) - 1
          head = (int(head) - 1) if head != '0' else None
          dep = 'ROOT' if deprel == 'root' else deprel
          pos = pos.lower()
          tag = pos if tag == '_' else tag
          tag = tag.lower()

          tokens.append(Token(id_, word, lemma, pos, tag, morph, head, deprel))
        except:
          print(line)
          raise

      yield tokens


def process_dependent(dep_idx, sentence):
  # Extract the full projection of the dependent.
  dependents = [dep_idx]
  queue = [dep_idx]
  while queue:
    node = sentence[queue.pop()]

    # TODO cache
    # Get dependents of node
    node_dependents = [idx for idx, tok in enumerate(sentence) if tok.head == node.id]
    dependents.extend(node_dependents)
    queue.extend(node_dependents)

  dependents = sorted(set(dependents))
  span_start, span_end = dependents[0], dependents[-1]
  return dep_idx, span_start, span_end


def process_sentence(sentence, deprels=None):
  """
  Yields:
    token: a verb token
    dependents: a list of dependent tuples `(dep, span)`, where `dep` is the
      direct dependent of `token` and `span` is the full projection of that
      dependent --- the contiguous span of tokens which are children under
      closure of the dependent
  """
  for idx, token in enumerate(sentence):
    if token.pos_univ == "verb":
      # Extract all dependents.
      dependents = [process_dependent(dep_idx, sentence)
                    for dep_idx, dep_token in enumerate(sentence)
                    if dep_token.head == idx
                    and (deprels is None or dep_token.deprel in deprels)]

      yield idx, dependents


def process_corpus(corpus_path, deprels):
  assert corpus_path.name.endswith(("conllu", "conll")), \
      "Only CoNLL-U corpus files supported."

  sentences = list(read_conllx(corpus_path))
  ret = []
  for i, sentence in tqdm(enumerate(sentences), desc="Sentence"):
    for token, dependents in process_sentence(sentence, deprels):
      ret.append((i, token, dependents))

  return sentences, ret


def main(args):
  deprels = args.include_deprel or None
  sentences, items = [], []
  for corpus in tqdm(args.corpus_path, desc="Corpus"):
    sentence_start_idx = len(sentences)

    c_sentences, c_items = process_corpus(corpus, deprels=deprels)
    c_sentences = [[token._asdict() for token in sentence]
                   for sentence in c_sentences]
    sentences.extend(c_sentences)

    for item in c_items:
      i = item[0]
      items.append((i + sentence_start_idx,) + item[1:])

  with args.out_path.open("w") as out:
    json.dump({"sentences": sentences, "items": items}, out)


if __name__ == '__main__':
  p = ArgumentParser()

  p.add_argument("corpus_path", nargs="+", type=Path)
  p.add_argument("-o", "--out_path", type=Path, default="verb_argument_structures.json")
  p.add_argument("-d", "--include_deprel", nargs="+", help="Track only the given dependency relation(s)")

  args = p.parse_args()
  main(args)
