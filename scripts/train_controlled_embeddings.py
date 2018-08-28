"""
Train "controlled" GloVe word embeddings which are guaranteed to have not
observed particular word-word cooccurrences during training.
"""

from argparse import ArgumentParser
import logging
logging.basicConfig(level=logging.DEBUG)
from pathlib import Path
from subprocess import run

from tqdm import tqdm

L = logging.getLogger(__name__)


def main(args, glove_args):
    args.out_dir.mkdir(parents=True)

    with tqdm(total=5) as pbar:
        # Build vocabulary.
        vocab_path = args.out_dir / "vocab.txt"
        if not vocab_path.exists():
            L.debug("Building vocabulary")
            with args.corpus_path.open("r") as corpus, \
                    vocab_path.open("w") as vocab:
                L.debug("%s", [args.glove_bin / "voab_count"] + glove_args)
                ret = run([args.glove_bin / "vocab_count"] + glove_args,
                           stdin=corpus, stdout=vocab)
                if ret.returncode != 0:
                    raise RuntimeError("Vocab prep exited with error code %i" % ret.returncode)
        pbar.update(1)

        # Check exclusions.
        with args.exclude_path.open("r") as exclusions_f:
            exclusions = [line.strip().split() for line in exclusions_f if line.strip()]
        with vocab_path.open("r") as vocab_f:
            vocab = frozenset(line.strip().split()[0] for line in vocab_f if line.strip())
        for i, (w1, w2) in enumerate(exclusions):
            if w1 not in vocab:
                L.warning("Exclusion #%i: w1 '%s' not in vocab", i + 1, w1)
            if w2 not in vocab:
                L.warning("Exclusion #%i: w2 '%s' not in vocab", i + 1, w1)
        pbar.update(1)

        # Build cooccurrence matrix.
        cooccur_path = args.out_dir / "cooccurrence.bin"
        if not cooccur_path.exists():
            L.debug("Building cooccurrence matrix")
            with args.corpus_path.open("r") as corpus, \
                    cooccur_path.open("wb") as cooccur:
                ret = run([args.glove_bin / "cooccur",
                           "-vocab-file", vocab_path] + glove_args,
                          stdin=corpus, stdout=cooccur)
                if ret.returncode != 0:
                    raise RuntimeError("Cooccur exited with error code %i" % ret.returncode)
        pbar.update(1)

        # Shuffle cooccurrence matrix.
        cooccur_shuffle_path = args.out_dir / "cooccurrence.shuf.bin"
        L.debug("Shuffling cooccurrence matrix")
        with cooccur_path.open("rb") as cooccur, \
                cooccur_shuffle_path.open("wb") as cooccur_shuffled:
            ret = run([args.glove_bin / "shuffle"] + glove_args,
                      stdin=cooccur, stdout=cooccur_shuffled)
            if ret.returncode != 0:
                raise RuntimeError("Cooccur shuffle exited with error code %i" % ret.returncode)
        pbar.update(1)

        # Learn vectors.
        vector_path = args.out_dir / "vectors"
        L.debug("Learning vectors")
        ret = run([args.glove_bin / "glove",
                   "-save-file", vector_path,
                   "-binary", "2",
                   "-input-file", cooccur_shuffle_path,
                   "-vocab-file", vocab_path,
                   "-exclude-file", args.exclude_path] + glove_args)
        if ret.returncode != 0:
            raise RuntimeError("GloVe exited with error code %i" % ret.returncode)
        pbar.update(1)


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument("corpus_path", help="Path to plaintext corpus file", type=Path)
    p.add_argument("exclude_path", help="Path to file listing pairs of words to exclude", type=Path)
    p.add_argument("out_dir", type=Path)
    p.add_argument("--glove_bin", help="Path to GloVe binaries",
                   default=Path(__file__).absolute().parents[1] / "selpref" / "glove" / "build")

    args, glove_args = p.parse_known_args()
    main(args, glove_args)
