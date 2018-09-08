# encoding: utf-8
from argparse import ArgumentParser
from pathlib import Path
import os
import gzip as gz
import bz2

p = ArgumentParser()
p.add_argument("inp_dir", type = Path)
p.add_argument("out_dir", type = Path)
p.add_argument("--dependency", action = "append")
p.add_argument("--language", action = "append")
args = p.parse_args()

inp_dir = args.inp_dir
out_dir = args.out_dir
dependency = args.dependency
language = args.language
path = {"cs": "/om/data/public/corpora/web_1t_euro_5grams/web_1t_5gram_el_v1_d1/data/CZECH/4gms", "de": "/om/data/public/corpora/web_1t_euro_5grams/web_1t_5gram_el_v1_d3/data/GERMAN/4gms", "en": "/om/data/public/corpora/google_web_ngrams/data/4gms"}

for lang in language:
	lst = os.listdir(path[lang])
	gms = {}
	for f in lst:
		if f == '4gm.idx':
			continue
		print(f)
		file = bz2.open(path[lang] + '/' + f,'rb')
		#file = gz.open(path[lang] + '/' + f,'rb')
		for line in file:
			line = line.decode('utf-8').split()
			if len(line) < 5:
				continue
			if line[3] not in gms:
				gms[line[3]] = []
			for i in line[:3]:
				if i not in gms[line[3]]:
					gms[line[3]].append(i)
		file.close()
	for dep in dependency:
		file = open((inp_dir / "{}/v_a1_a2_filtered_pairs_{}_{}".format(lang, dep, lang)), "rb")
		fileout = open((out_dir / "{}/v_a1_a2_filtered_4gms_pairs_{}_{}".format(lang, dep, lang)), "w")
		for line1 in file:
			line1 = line1.decode("utf-8")
			line = line1.split()
			if line[0] in gms:
				if line[2] in gms[line[0]]:
					continue
			if line[2] in gms:
				if line[0] in gms[line[2]]:
					continue
			fileout.write(line1)

		file.close()
		fileout.close()