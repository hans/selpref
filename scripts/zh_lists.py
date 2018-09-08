from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("inp_dir_sim", type = Path)
p.add_argument("inp_dir_tra", type = Path)
p.add_argument("--dependency", action = "append")
args = p.parse_args()

inp_dir_sim = args.inp_dir_sim
inp_dir_tra = args.inp_dir_tra
dependency = args.dependency

for dep in dependency:
	file1 = open((inp_dir_sim / "v_a_filtered_pairs_{}_zh_sim".format(dep)), 'rb')
	fileout1 = open((inp_dir_sim / "v_a_filtered_lists_{}_zh_sim".format(dep)), 'w')
	verbs = {}
	for line in file1:
		line = line.decode('utf-8').split()
		if line[0] in verbs:
			verbs[line[0]].append(line[1])
		else:
			verbs[line[0]] = [line[1]]

	for i in verbs:
		fileout1.write(i + '\t')
		for j in verbs[i]:
			fileout1.write(j + '\t')
		fileout1.write('\n')

	file1.close()
	fileout1.close()

	file1 = open((inp_dir_tra / "v_a_filtered_pairs_{}_zh_tra".format(dep)), 'rb')
	fileout1 = open((inp_dir_tra / "v_a_filtered_lists_{}_zh_tra".format(dep)), 'w')
	verbs = {}
	for line in file1:
		line = line.decode('utf-8').split()
		if line[0] in verbs:
			verbs[line[0]].append(line[1])
		else:
			verbs[line[0]] = [line[1]]

	for i in verbs:
		fileout1.write(i + '\t')
		for j in verbs[i]:
			fileout1.write(j + '\t')
		fileout1.write('\n')

	file1.close()
	fileout1.close()