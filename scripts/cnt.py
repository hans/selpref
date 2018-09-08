# encoding: utf-8
from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("input_folder", type = Path)
p.add_argument("corpus_folder", type = Path)
p.add_argument("out_dir", type = Path)
p.add_argument("--language", action = "append", help = "Specify the language of input file")
p.add_argument("--dependency", action = "append")
args = p.parse_args()

inp_folder = args.input_folder
corpus_folder = args.corpus_folder
out_dir = args.out_dir
language = args.language
dependency = args.dependency

for lang in language:
	verbs = {}
	args = {}
	for dep in dependency:
		inp_f = (inp_folder / "{}/v_a_filtered_lists_{}_{}".format(lang, dep, lang)).open("rb")
		for line in inp_f:
			line = line.decode('utf-8').split()
			if line[0] not in verbs:
				verbs[line[0]] = 0
			for i in line[1:]:
				if i not in args:
					args[i] = 0
	
	corpus_f = (corpus_folder / "{}_UD".format(lang)).open("rb")
	for line in corpus_f:
		line = line.decode('utf-8').split()
		if len(line) < 3 or line[0] == '#':
			continue
		if line[1] in verbs:
			verbs[line[1]] += 1
		if line[1] in args:
			args[line[1]] += 1
	
	out_file1 = (out_dir / "verbs_freq_{}".format(lang)).open("w")
	out_file2 = (out_dir / "args_freq_{}".format(lang)).open("w")
	for i in verbs:
		out_file1.write(i + '\t' + str(verbs[i]) + '\n')
	for i in args:
		out_file2.write(i + '\t' + str(args[i]) + '\n')

	inp_f.close()
	corpus_f.close()
	out_file1.close()
	out_file2.close()