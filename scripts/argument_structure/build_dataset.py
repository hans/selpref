"""
From an extracted database of verb argument structures, build a dataset amenable to modeling.
"""

from argparse import ArgumentParser
import json
from pathlib import Path


def main(args):
  with args.input_path.open("r") as corpus_f:
    corpus = json.load(corpus_f)

  sentences, items = corpus["sentences"], corpus["items"]

  deprels = set(args.include_deprel) if args.include_deprel is not None else None
  exclude_deprels = set(args.exclude_deprel)

  # build examples
  for sentence_id, token_id, dependents in items:
    sentence = sentences[sentence_id]
    sentence_str = " ".join(tok["word"] for tok in sentence)
    token = sentence[token_id]

    # For now: a verb with N dependents generates N independent positive
    # examples.
    #
    # Later, the dataset+model should take into account dependencies between
    # the dependents (hehe).
    for dep, span_start, span_end in dependents:
      dep = sentence[dep]
      if deprels is not None and dep["deprel"] not in deprels:
        continue
      if dep["deprel"] in exclude_deprels:
        continue

      span_str = " ".join(sentence[child]["word"] for child in range(span_start, span_end + 1))
      if dep["deprel"] == "obl":
        # HACK for Euro languages: PP head is the PP for now.
        mod_head = sentence[span_start]["word"]
      else:
        mod_head = dep["word"]
      print("%s\t%s\t%s\t%s\t%s" % (sentence_str, token["word"], mod_head, dep["deprel"], span_str))


if __name__ == '__main__':
  p = ArgumentParser()
  p.add_argument("input_path", type=Path)
  p.add_argument("-d", "--include_deprel", nargs="+")
  p.add_argument("-e", "--exclude_deprel", nargs="+", default=set(["punct"]))

  main(p.parse_args())
