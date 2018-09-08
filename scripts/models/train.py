import nn
import gensim
from gensim.test.utils import datapath
from gensim.models import KeyedVectors
import numpy as np
import torch
from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm

p = ArgumentParser()
p.add_argument("embeddings_folder", type = Path)
p.add_argument("output_folder", type = Path)
p.add_argument("vaa_pairs_folder", type = Path)
p.add_argument("avv_pairs_folder", type = Path)
p.add_argument("save_path", type = Path)
p.add_argument("--dependency", action = "append")
p.add_argument("--language", action = "append")
args = p.parse_args()
embeddings_folder = args.embeddings_folder
output_folder = args.output_folder
vaa_pairs_folder = args.vaa_pairs_folder
avv_pairs_folder = args.avv_pairs_folder
save_path = args.save_path
dependency = args.dependency
language = args.language

dim = 300
batch = 32
epoch = 5
for lang in language:
	embeddings = KeyedVectors.load_word2vec_format(datapath((embeddings_folder / "embeddings_{}".format(lang))), binary = False)
	file0 = open((embeddings_folder / "embeddings_{}".format(lang)), "rb")
	vocabulary = []
	file0.readline()
	for line in file0:
		line = line.decode('utf-8').split()
		vocabulary.append(line[0])
	file0.close()
	model = nn.DotProductModel(embeddings, vocabulary)
	for dep in dependency:
		vaa_train_f = open((vaa_pairs_folder / "{}/v_a1_a2_filtered_pairs_{}_{}.train".format(lang, dep, lang)),"rb")
		vaa_test_f = open((vaa_pairs_folder / "{}/v_a1_a2_filtered_pairs_{}_{}.test".format(lang, dep, lang)),"rb")
		avv_train_f = open((avv_pairs_folder / "{}/a_v1_v2_filtered_pairs_{}_{}.train".format(lang, dep, lang)),"rb")
		avv_test_f = open((avv_pairs_folder / "{}/a_v1_v2_filtered_pairs_{}_{}.test".format(lang, dep, lang)),"rb")
		log = open((save_path / "{}".format("log")), "a", encoding = "utf-8")
		fileout1 = open((output_folder / "M_ranking_v_a_{}_{}".format(dep, lang)), 'w', encoding = 'utf-8')
		fileout2 = open((output_folder / "M_disambiguate_v_a_{}_{}".format(dep, lang)), 'w', encoding = 'utf-8')

		examples = []
		evaluate_all = 0
		total_all = 0
		for line in vaa_train_f:
			line = line.decode("utf-8").split()
			examples.append((line))
		model.train(save_path, log, "vaa", dep, lang, examples, dim, batch, epoch) # self, save_path, log, dep, lang, examples, dim, batch, epoch
		examples = []
		for line in vaa_test_f:
			line = line.decode("utf-8").split()
			examples.append((line))
		results = model.evaluate(examples)
		print("{}_{}_ranking...".format(lang, dep))
		for i in tqdm(range(len(results))):
			v, a1, a2, rp, rn, d = results[i]
			fileout1.write(v + "\t" + a1 + "\t" + a2 + "\t" + str(rp) + "\t" + str(rn) + "\t" + str(d) + "\n")
			evaluate_all += (1-d)
			total_all += 1
		if total_all == 0:
			continue
		fileout1.write("evaluate_all:\t" + str(evaluate_all / total_all) + "\n")

		examples = []
		evaluate_all = 0
		total_all = 0
		for line in avv_train_f:
			line = line.decode("utf-8").split()
			examples.append((line))
		model.train(save_path, log, "avv", dep, lang, examples, dim, batch, epoch) # self, save_path, log, dep, lang, examples, dim, batch, epoch
		examples = []
		for line in avv_test_f:
			line = line.decode("utf-8").split()
			examples.append((line))
		results = model.evaluate(examples)
		print("{}_{}_disambiguating...".format(lang, dep))
		for i in tqdm(range(len(results))):
			v, a1, a2, rp, rn, d = results[i]
			fileout2.write(v + "\t" + a1 + "\t" + a2 + "\t" + str(rp) + "\t" + str(rn) + "\t" + str(d) + "\n")
			evaluate_all += (1-d)
			total_all += 1
		if total_all == 0:
			continue
		fileout2.write("evaluate_all:\t" + str(evaluate_all / total_all) + "\n")

		fileout1.close()
		fileout2.close()
		avv_test_f.close()
		avv_train_f.close()
		vaa_test_f.close()
		vaa_train_f.close()
		log.close()