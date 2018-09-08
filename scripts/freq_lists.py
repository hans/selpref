# encoding: utf-8
from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("inp_dir", type = Path)
p.add_argument("out_dir", type = Path)
p.add_argument("--type", action = "append")
p.add_argument("--language", action = "append")
args = p.parse_args()

inp_dir = args.inp_dir
out_dir = args.out_dir
typs = args.type
language = args.language

for lang in language:
	for typ in typs:
		file1 = open((inp_dir / "{}_freq_{}".format(typ, lang)), 'rb')
		fileout = open((inp_dir / "freq_{}_{}".format(typ, lang)), 'w')
		freq = {}
		for line in file1:
			line = line.decode('utf-8').split()
			if line[1] not in freq:
				freq[line[1]] = [line[0]]
			else:
				freq[line[1]].append(line[0])

		for i in freq:
			fileout.write(i + '\t')
			for j in freq[i]:
				fileout.write(j + '\t')
			fileout.write('\n')

		file1.close()
		fileout.close()