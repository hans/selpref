# encoding: utf-8
from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("inp", type = Path)
p.add_argument("out_dir", type = Path)
p.add_argument("--dependency", help = "Specify the dependency relationship of input file" )
p.add_argument("--language", help = "Specify the language of input file")
args = p.parse_args()

inp_f = args.inp.open("rb")
out_dir = args.out_dir
dependency = args.dependency
language = args.language
out_files = {"pairs": (out_dir / "v_a_filtered_pairs_{}_{}".format(dependency, language)).open("w"), "lists": (out_dir / "v_a_filtered_lists_{}_{}".format(dependency, language)).open("w")}

dep = {}
for line in inp_f:
	line = line.decode('utf-8').split()
	if line[0] not in dep:
		dep[line[0]] = [line[1]]
	else:
		if line[1] not in dep[line[0]]:
			dep[line[0]].append(line[1])

for i in dep:
	out_files["lists"].write(i + '\t')
	for j in dep[i]:
		out_files["lists"].write(j + '\t')
		out_files["pairs"].write(i + '\t' + j + '\n')
	out_files["lists"].write('\n')

inp_f.close()
out_files["pairs"].close()
out_files["lists"].close()
