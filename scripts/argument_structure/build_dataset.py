"""
From an extracted database of verb argument structures, build a dataset amenable to modeling.
"""

from argparse import ArgumentParser
import json
from pathlib import Path


def main(args):
  with args.input_path.open("r") as corpus_f:
    corpus = json.load(corpus_f)

  deprels = set(args.include_deprel)
  assert len(deprels) >= 1

  # build examples
  for token, dependents in corpus:
    # print("%s\t%s" % (token["word"], " ".join(dep["deprel"] for dep, _ in dependents)))

    # For now: a verb with N dependents generates N independent positive
    # examples.
    #
    # Later, the dataset+model should take into account dependencies between
    # the dependents (hehe).
    for dep, span in dependents:
      if dep["deprel"] not in deprels:
        continue

      span_str = " ".join(child["word"] for child in span)
      if dep["deprel"] == "obl":
        # HACK for English: PP head is the PP for now.
        mod_head = span[0]["word"]
      else:
        mod_head = dep["word"]
      print("%s\t%s\t%s\t%s" % (token["word"], mod_head, dep["deprel"], span_str))


if __name__ == '__main__':
  p = ArgumentParser()
  p.add_argument("input_path", type=Path)
  p.add_argument("-d", "--include_deprel", nargs="+", default=["obl", "nmod"])

  main(p.parse_args())
