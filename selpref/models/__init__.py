

class SelectionalPreferenceModel(object):

    def train(self, examples):
        """
        Train a selectional preference model given attested examples.

        Args:
            examples: A list of tuples of the form `(verb, arg)`, where each
                element is a string. Each tuple indicates that `verb` combines
                with `arg` in a training corpus.
        """
        raise NotImplementedError

    def rank(self, examples):
        """
        Rank a batch of candidate verb--argument combinations.

        Args:
            examples: List of tuples of the form `(verb, arg)`.
        """
        raise NotImplementedError

    def pseudo_disambiguate(self, disamb_examples):
        """
        Make pseudo-disambiguation predictions on a set of test inputs.

        Args:
            disamb_examples: A list of tuples of form `(v1, v2, arg)`, where
                each element is a string. `v1` and `v2` indicate two potential
                verbs which may appear with argument `arg`.

        Returns:
            disamb_predictions: A sequence of `0` and `1` values. If
                `disamb_predictions[i] == 0` then `v1` is preferred to `v2` in
                `disamb_examples[i]`; otherwise `v2` is preferred.
        """
        # TODO: can probably implement this abstractly in terms of the `rank`
        # method
        raise NotImplementedError
