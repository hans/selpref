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
p.add_argument("--dependency", action = "append")
p.add_argument("--language", action = "append")
args = p.parse_args()
embeddings_folder = args.embeddings_folder
output_folder = args.output_folder
vaa_pairs_folder = args.vaa_pairs_folder
avv_pairs_folder = args.avv_pairs_folder
dependency = args.dependency
language = args.language


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
		file1 = open((vaa_pairs_folder / "{}/v_a1_a2_filtered_pairs_{}_{}".format(lang, dep, lang)), "rb")
		file2 = open((avv_pairs_folder / "{}/a_v1_v2_filtered_pairs_{}_{}".format(lang, dep, lang)), "rb")
		fileout1 = open((output_folder / "ranking_v_a_{}_{}".format(dep, lang)), 'w', encoding = 'utf-8')
		fileout2 = open((output_folder / "disambiguate_v_a_{}_{}".format(dep, lang)), 'w', encoding = 'utf-8')

		evaluate_all = 0
		total_all = 0
		evaluate = 0
		total = 0
		examples = []
		for line in file1:
			line = line.decode("utf-8").split()
			examples.append(line)
		results = model.pseudo_disambiguate(examples)
		print("{}_{}_ranking...".format(lang, dep))
		for i in tqdm(range(len(results))):
			v, a1, a2, rp, rn, d = results[i]
			if (i != 0 and v != results[i-1][0]) or i == len(results) - 1:
				fileout1.write("evaluate:\t" + str(evaluate / total) + "\n")
				evaluate_all += evaluate
				total_all += total
				evaluate = 0
				total = 0
		#for v, a1, a2, rp, rn, d in results:
			fileout1.write(v + "\t" + a1 + "\t" + a2 + "\t" + str(rp) + "\t" + str(rn) + "\t" + str(d) + "\n")
			evaluate += (1-d)
			total += 1
		if total_all == 0:
			continue
		fileout1.write("evaluate_all:\t" + str(evaluate_all / total_all) + "\n")

		evaluate_all = 0
		total_all = 0
		evaluate = 0
		total = 0
		examples = []
		for line in file2:
			line = line.decode("utf-8").split()
			examples.append(line)
		results = model.pseudo_disambiguate(examples)
		print("{}_{}_disambiguating...".format(lang, dep))
		for i in tqdm(range(len(results))):
			v, a1, a2, rp, rn, d = results[i]
			if (i != 0 and v != results[i-1][0]) or i == len(results) - 1:
				fileout2.write("evaluate:\t" + str(evaluate / total) + "\n")
				evaluate_all += evaluate
				total_all += total
				evaluate = 0
				total = 0
		#for v, a1, a2, rp, rn, d in results:
			fileout2.write(v + "\t" + a1 + "\t" + a2 + "\t" + str(rp) + "\t" + str(rn) + "\t" + str(d) + "\n")
			evaluate += (1-d)
			total += 1
		if total_all == 0:
			continue
		fileout2.write("evaluate_all:\t" + str(evaluate_all / total_all) + "\n")

		file1.close()
		file2.close()
		fileout1.close()
		fileout2.close()
"""
		posi_v_a = {}
		posi_a_v = {}
		nega_v_a = {}
		nega_a_v = {}
		for line in file1:
			line = line.decode('utf-8').split()
			if line[0] not in posi_v_a:
				posi_v_a[line[0]] = []
				nega_v_a[line[0]] = []
			posi_v_a[line[0]].append(line[1])
			nega_v_a[line[0]].append(line[2])
		for line in file2:
			line = line.decode('utf-8').split()
			if line[0] not in posi_a_v:
				posi_a_v[line[0]] = []
				nega_a_v[line[0]] = []
			posi_a_v[line[0]].append(line[1])
			nega_a_v[line[0]].append(line[2])

		print("ranking...")
		fileout1.write("v\targ_posi\targ_nega\trank_posi\trank_nega\tdisambiguate\n")
		evaluate_all = 0
		total_all = 0
		for cnt in tqdm(range(len(posi_v_a))):
			i = list(posi_v_a.keys())[cnt]
			examples = []
			for j in posi_v_a[i]:
				examples.append((i, j))
			posi_ranks = model.rank(examples)
			examples = []
			for j in nega_v_a[i]:
				examples.append((i, j))
			nega_ranks = model.rank(examples)

			evaluate = 0
			total = 0
			print(len(posi_ranks))
			print(len(nega_ranks))
			for n in range(len(posi_ranks)):
				disam = 1
				total += 1
				if len(posi_ranks[n]) < 3 or len(nega_ranks[n]) < 3:
					continue
				if posi_ranks[n][2] > nega_ranks[n][2]:
					disam = 0
					evaluate += 1
				fileout1.write(posi_ranks[n][0] + "\t" + posi_ranks[n][1] + "\t" + nega_ranks[n][1] + "\t" + str(posi_ranks[n][2]) + "\t" + str(nega_ranks[n][2]) + "\t" + str(disam) + "\n")
			fileout1.write("evaluate:\t" + str(evaluate / total) + "\n")
			evaluate_all += evaluate
			total_all += total
		fileout1.write("evaluate_all:\t" + str(evaluate_all / total_all) + "\n")

		print("disambiguating...")
		fileout2.write("arg\tv_posi\tv_nega\trank_posi\trank_nega\tdisambiguate\n")
		evaluate_all = 0
		total_all = 0
		for cnt in tqdm(range(len(posi_a_v))):
			i = list(posi_a_v.keys())[cnt]
			examples = []
			for j in posi_a_v[i]:
				examples.append((i, j))
			posi_ranks = model.rank(examples)
			examples = []
			for j in nega_a_v[i]:
				examples.append((i, j))
			nega_ranks = model.rank(examples)

			evaluate = 0
			total = 0
			for n in range(len(posi_ranks)):
				disam = 1
				total += 1
				if len(posi_ranks[n]) < 3 or len(nega_ranks[n]) < 3:
					continue
				if posi_ranks[n][2] > nega_ranks[n][2]:
					disam = 0
					evaluate += 1
				fileout2.write(posi_ranks[n][0] + "\t" + posi_ranks[n][1] + "\t" + nega_ranks[n][1] + "\t" + str(posi_ranks[n][2]) + "\t" + str(nega_ranks[n][2]) + "\t" + str(disam) + "\n")
			fileout2.write("evaluate:\t" + str(evaluate / total) + "\n")
			evaluate_all += evaluate
			total_all += total
		fileout2.write("evaluate_all:\t" + str(evaluate_all / total_all) + "\n")
"""
