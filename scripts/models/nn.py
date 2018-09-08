from init import SelectionalPreferenceModel
import gensim
from gensim.test.utils import datapath
from gensim.models import KeyedVectors
import numpy as np
import torch
from torch import tensor
from tqdm import tqdm
import M

class DotProductModel(SelectionalPreferenceModel):
    """
    Simple non-probabilistic ranking model which scores verb--argument
    combinations based on the dot product of their embeddings.
    """

    def __init__(self, embeddings, vocabulary): 
    	# embeddings = KeyedVectors.load_word2vec_format(datapath('.vec'), binary = False)
        self.embeddings = embeddings
        self.vocabulary = vocabulary

    def train(self, save_path, log, form, dep, lang, examples, dim, batch, epoch):
    	# TODO train for a parameter M
    	exam = []
    	for a, v1, v2 in examples:
    		if a not in self.vocabulary or v1 not in self.vocabulary or v2 not in self.vocabulary:
    			continue
    		vec_a = self.embeddings[a]
    		vec_v1 = self.embeddings[v1]
    		vec_v2 = self.embeddings[v2]
    		exam.append((tensor(vec_a), tensor(vec_v1), tensor(vec_v2)))
    	self.para = M.train(save_path, log, form, dep, lang, exam, dim, batch, epoch)
    	return self.para

    def rank(self, examples):
    	ranks = []
    	#print("examples:\n")
    	for v, a in examples:
    	#for cnt in tqdm(range(len(examples))):
    	#	v, a = examples[cnt]
    		if v not in self.vocabulary or a not in self.vocabulary:
    			continue
    		#print(self.embeddings.wv.vocab[v])
    		#print(self.embeddings.wv.vectors_norm)
    		vec_v = self.embeddings[v]
    		vec_a = self.embeddings[a]
    		#vec_a = self.embeddings.wv.word_vec(a, use_norm = True)
    		rank_tmp = np.dot(vec_v, vec_a)
    		ranks.append((v, a, rank_tmp))
    	return ranks
    	raise NotImplementedError


    def pseudo_disambiguate(self, disamb_examples):
    	#inputs: Args: A list of tuples of form `(v1, v2, arg)`, where Returns: disamb_predictions: A sequence of `0` and `1` values.
    	results = []
    	for a, v1, v2 in disamb_examples:
    		if a not in self.vocabulary or v1 not in self.vocabulary or v2 not in self.vocabulary:
    			continue
    		rank1 = self.rank([(a, v1)])
    		rank2 = self.rank([(a, v2)])
    		if rank1[0][2] > rank2[0][2]:
    			results.append((a, v1, v2, rank1[0][2], rank2[0][2], 0))
    		else:
    			results.append((a, v1, v2, rank1[0][2], rank2[0][2], 1))
    	return results
    	raise NotImplementedError

    def evaluate(self, examples):
    	# after training
    	results = []
    	for a, v1, v2 in examples:
    		if a not in self.vocabulary or v1 not in self.vocabulary or v2 not in self.vocabulary:
    			continue
    		vec_a = tensor(self.embeddings[a])
    		vec_v1 = tensor(self.embeddings[v1])
    		vec_v2 = tensor(self.embeddings[v2])
    		tmp = self.para(vec_a)
    		rank1 = torch.dot(tmp, vec_v1)
    		rank2 = torch.dot(tmp, vec_v2)
    		if rank1 > rank2:
    			results.append((a, v1, v2, float(rank1), float(rank2), 0))
    		else:
    			results.append((a, v1, v2, float(rank1), float(rank2), 1))
    	return results
    	raise NotImplementedError
