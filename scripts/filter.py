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

'''
file1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/zh/v_a_obj_zh','rb')
file2 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/zh/v_a_iobj_zh','rb')
file3 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/zh/v_a_subj_zh','rb')
fileout1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/filtered/zh/v_a_filtered_pairs_obj_zh','w',encoding = 'utf-8')
fileout2 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/filtered/zh/v_a_filtered_pairs_iobj_zh','w',encoding = 'utf-8')
fileout3 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/filtered/zh/v_a_filtered_pairs_subj_zh','w',encoding = 'utf-8')
fileout4 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/filtered/zh/v_a_filtered_lists_obj_zh','w',encoding = 'utf-8')
fileout5 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/filtered/zh/v_a_filtered_lists_iobj_zh','w',encoding = 'utf-8')
fileout6 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/filtered/zh/v_a_filtered_lists_subj_zh','w',encoding = 'utf-8')

obj = {}
iobj = {}
subj = {}
for line in file1:
	line = line.decode('utf-8').split()
	if line[0] not in obj:
		obj[line[0]] = [line[1]]
	else:
		if line[1] not in obj[line[0]]:
			obj[line[0]].append(line[1])
for line in file2:
	line = line.decode('utf-8').split()
	if line[0] not in iobj:
		iobj[line[0]] = [line[1]]
	else:
		if line[1] not in iobj[line[0]]:
			iobj[line[0]].append(line[1])
for line in file3:
	line = line.decode('utf-8').split()
	if line[0] not in subj:
		subj[line[0]] = [line[1]]
	else:
		if line[1] not in subj[line[0]]:
			subj[line[0]].append(line[1])

for i in obj:
	fileout4.write(i + '\t')
	for j in obj[i]:
		fileout4.write(j + '\t')
		fileout1.write(i + '\t' + j + '\n')
	fileout4.write('\n')
for i in iobj:
	fileout5.write(i + '\t')
	for j in iobj[i]:
		fileout5.write(j + '\t')
		fileout2.write(i + '\t' + j + '\n')
	fileout5.write('\n')
for i in subj:
	fileout6.write(i + '\t')
	for j in subj[i]:
		fileout6.write(j + '\t')
		fileout3.write(i + '\t' + j + '\n')
	fileout6.write('\n')

file1.close()
file2.close()
file3.close()
fileout1.close()
fileout2.close()
fileout3.close()
fileout4.close()
fileout5.close()
fileout6.close()
'''