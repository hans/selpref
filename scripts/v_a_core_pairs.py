from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

p = ArgumentParser()
p.add_argument("corpus_file", type=Path)
p.add_argument("out_dir", type=Path)
p.add_argument("--dependency", action="append", help="Specify a dependency relation to extract")

args = p.parse_args()

###

corpus_f = args.corpus_file.open("rb")
out_files = {dependency: (out_dir / "%s.tsv" % dependency).open("a")
			 for dependency in args.dependency}
# file1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/cs_UD','rb')
# fileout1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/cs/v_a_obj_cs','a',encoding = 'utf-8')
# fileout2 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/cs/v_a_iobj_cs','a',encoding = 'utf-8')
# fileout3 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/cs/v_a_subj_cs','a',encoding = 'utf-8')

verbs = {}
relations = defaultdict(dict)
for line in file1:
	line = line.decode('utf-8').split()
	if len(line) == 0:
		continue
	if line[0] == '#':
		# Sentence complete -- process and output located dependencies
		for dependency, dep_dict in relations:
			for index, (token, head_index) in dep_dict.items():
				if head_index in verbs:
					verb = verbs[head_index]
					out_files[dependency].write("%s\t%s\n" % verb, token)

		file1.readline()

		# Empty accumulators
		verbs = {}
		relations = defaultdict(dict)
		continue

	if line[3] == "VERB":
		verbs[line[0]] = line[2]#for Chinese line[2] is replaced by line[1]
	for dependency in args.dependency:
		if line[7] == dependency:
			relations[dependency][line[0]] = (line[2], line[6])#for Chinese line[2] is replaced by line[1]

corpus_f.close()
for out_file in out_files.values()
	out_file.close()
