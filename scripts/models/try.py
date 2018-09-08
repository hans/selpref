from init import SelectionalPreferenceModel
import gensim
from gensim.test.utils import datapath
from gensim.models import KeyedVectors
import numpy as np
import torch
import gensim.downloader as api

word_vectors = api.load("glove-wiki-gigaword-100")
embeddings = KeyedVectors.load_word2vec_format(datapath('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/wiki_embeddings/embeddings_cs'), binary = False)
vec_a = word_vectors.wv.word_vec("a", use_norm = True)
print(vec_v)
