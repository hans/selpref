from selpref.models import SelectionalPreferenceModel


class DotProductModel(SelectionalPreferenceModel):
    """
    Simple non-probabilistic ranking model which scores verb--argument
    combinations based on the dot product of their embeddings.
    """

    def __init__(self, embeddings):
        self.embeddings = embeddings

    def train(self, examples):
        pass

    def rank(self, examples):
        # TODO
        raise NotImplementedError
