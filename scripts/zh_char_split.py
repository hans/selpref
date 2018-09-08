# encoding: utf-8
from hanziconv import HanziConv
from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("input_file", type = Path)
p.add_argument("out_file_sim", type = Path)
p.add_argument("out_file_tra", type = Path)
args = p.parse_args()

file1 = open(args.input_file,"rb")
fileout1 = open(args.out_file_sim,"w")
fileout2 = open(args.out_file_tra,"w")

for line in file1:
	line = line.decode('utf-8')
	sim = HanziConv.toSimplified(line)
	tra = HanziConv.toTraditional(line)
	if line == sim:
		fileout1.write(line)
	if line == tra:
		fileout2.write(line)
file1.close()
fileout1.close()
fileout2.close()
"""
# encoding: utf-8
from hanziconv import HanziConv
from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("input_dir", type = Path)
p.add_argument("out_dir_sim", type = Path)
p.add_argument("out_dir_tra", type = Path)
p.add_argument("--dependency", action = "append")
args = p.parse_args()

input_dir = args.input_dir
out_dir_sim = args.out_dir_sim
out_dir_tra = args.out_dir_tra
dependency = args.dependency

for dep in dependency:
	file1 = open((input_dir / "v_a_filtered_pairs_{}_zh".format(dep)), 'rb')
	fileout1 = open((out_dir_sim / "v_a_filtered_pairs_{}_zh_sim".format(dep)), 'w')
	fileout2 = open((out_dir_tra / "v_a_filtered_pairs_{}_zh_tra".format(dep)), 'w')
	for line in file1:
		line = line.decode('utf-8')
		sim = HanziConv.toSimplified(line)
		tra = HanziConv.toTraditional(line)
		if line == sim:
			fileout1.write(line)
		if line == tra:
			fileout2.write(line)

	file1.close()
	fileout1.close()
	fileout2.close()
"""