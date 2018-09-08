# encoding: utf-8
from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("input", type = Path)
p.add_argument("corpus", type = Path)
p.add_argument("out_dir", type = Path)
p.add_argument("--dependency", help = "Specify the dependency relationship of input file" )
p.add_argument("--language", help = "Specify the language of input file")
args = p.parse_args()

inp_f = args.input.open("rb")
corpus_f = args.corpus.open("rb")
out_dir = args.out_dir
dependency = args.dependency
language = args.language
out_list_files = {"train": (out_dir / "v_a_lists_{}_{}.train".format(dependency, language)).open("w"), "test": (out_dir / "v_a_lists_{}_{}.test".format(dependency, language)).open("w")}
out_pair_files = {"train": (out_dir / "v_a_pairs_{}_{}.train".format(dependency, language)).open("w"), "test": (out_dir / "v_a_pairs_{}_{}.test".format(dependency, language)).open("w")}

verbs = {}
args = {}
for line in inp_f:
	line = line.decode('utf-8').split()
	verbs[line[0]] = 0
	args[line[0]] = line[1:]

for line in corpus_f:
	line = line.decode('utf-8').split()
	if len(line) < 3 or line[0] == '#':
		continue
	if line[1] in verbs:
		verbs[line[1]] += 1

sort = {}
for i in verbs:
	if verbs[i] in sort:
		sort[verbs[i]].append(i)
	else:
		sort[verbs[i]] = [i]

lstkey = sorted(sort.keys())

lst = []
for i in lstkey:
	for j in sort[i]:
		lst.append(j)

cnt = 0
i = 0
while i < len(lst):
	out_list_files["train"].write(lst[i] + '\t')
	for j in args[lst[i]]:
		out_list_files["train"].write(j + '\t')
		out_pair_files["train"].write(lst[i] + '\t' + j + '\n')
	out_list_files["train"].write('\n')
	cnt += 1
	i += 1
	if cnt == 4:
		out_list_files["test"].write(lst[i] + '\t')
		for j in args[lst[i]]:
			out_list_files["test"].write(j + '\t')
			out_pair_files["test"].write(lst[i] + '\t' + j + '\n')
		out_list_files["test"].write('\n')
		i += 1
		cnt = 0

inp_f.close()
corpus_f.close()
out_list_files["train"].close()
out_list_files["test"].close()
out_pair_files["train"].close()
out_pair_files["test"].close()


'''
file1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/filtered/zh/v_a_filtered_lists_iobj_zh','rb')
file2 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/zh_UD','rb')
fileout1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/split/zh/v_a_lists_iobj_zh.train','w',encoding = 'utf-8')
fileout2 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/split/zh/v_a_lists_iobj_zh.test','w',encoding = 'utf-8')

verbs = {}
args = {}
for line in file1:
	line = line.decode('utf-8').split()
	verbs[line[0]] = 0
	args[line[0]] = line[1:]

for line in file2:
	line = line.decode('utf-8').split()
	if len(line) < 3 or line[0] == '#':
		continue
	if line[1] in verbs:
		verbs[line[1]] += 1

sort = {}
for i in verbs:
	if verbs[i] in sort:
		sort[verbs[i]].append(i)
	else:
		sort[verbs[i]] = [i]

lstkey = sorted(sort.keys())

lst = []
for i in lstkey:
	for j in sort[i]:
		lst.append(j)

cnt = 0
i = 0
while i < len(lst):
	fileout1.write(lst[i] + '\t')
	for j in args[lst[i]]:
		fileout1.write(j + '\t')
	fileout1.write('\n')
	cnt += 1
	i += 1
	if cnt == 4:
		fileout2.write(lst[i] + '\t')
		for j in args[lst[i]]:
			fileout2.write(j + '\t')
		fileout2.write('\n')
		i += 1
		cnt = 0

file1.close()
file2.close()
fileout1.close()
fileout2.close()
'''