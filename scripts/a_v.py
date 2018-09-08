from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("inp_folder", type = Path)
p.add_argument("output_folder" ,type = Path)
p.add_argument("--dependency", action = "append")
p.add_argument("--language", action = "append")
args = p.parse_args()

inp_folder = args.inp_folder
output_folder = args.output_folder
dependency = args.dependency
language = args.language

for lang in language:
	for dep in dependency:
		file1 = open((inp_folder / "{}/v_a_filtered_pairs_{}_{}".format(lang, dep, lang)), 'rb') # for positive files, remove ".negative"
		#file2 = open((inp_folder / "{}/v_a_pairs_{}_{}.negative.test".format(lang, dep, lang)), 'rb') # for positive files, remove ".negative"
		fileout1 = open((output_folder / "{}/a_v_filtered_lists_{}_{}".format(lang, dep, lang)), 'w', encoding = 'utf-8') # for positive files, remove ".negative"
		fileout3 = open((output_folder / "{}/a_v_filtered_pairs_{}_{}".format(lang, dep, lang)), 'w', encoding = 'utf-8') # for positive files, remove ".negative"

		arguments = {}
		for line in file1:
			line = line.decode('utf-8').split()
			if line[1] in arguments:
				arguments[line[1]].append(line[0])
			else:
				arguments[line[1]] = [line[0]]

		for i in arguments:
			fileout1.write(i + '\t')
			for j in arguments[i]:
				fileout1.write(j + '\t')
				fileout3.write(i + '\t' + j + '\n')
			fileout1.write('\n')

		

		file1.close()
		fileout1.close()
		fileout3.close()