from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("input_folder", type = str)
p.add_argument("output_folder", type = str)
p.add_argument("--dependency", action = "append")
p.add_argument("--language", action = "append")
args = p.parse_args()

inp_folder = args.input_folder
output_folder = args.output_folder
dependency = args.dependency
language = args.language
for lang in language:
	for dep in dependency:
		file1 = open((inp_folder + "/filtered/{}/v_a_filtered_lists_{}_{}".format(lang, dep, lang)), 'rb')
		file2 = open((inp_folder + "/filtered/{}/v_a_filtered_lists_{}_{}".format(lang, dep, lang)), 'rb')
		fileout1 = open((inp_folder + "/negative_filtered/{}/v_a_filtered_lists_{}_{}.negative".format(lang, dep, lang)), 'w', encoding = 'utf-8')
		fileout3 = open((inp_folder + "/negative_filtered/{}/v_a_filtered_pairs_{}_{}.negative".format(lang, dep, lang)), 'w', encoding = 'utf-8')
		positive = {}
		arguments = []
		for line in file1:
			line = line.decode('utf-8').split()
			positive[line[0]] = line[1:]
			for i in line[1:]:
				if i not in arguments:
					arguments.append(i)

		train = []
		for line in file2:
			line = line.decode('utf-8').split()
			train.append(line[0])

		for i in train:
			fileout1.write(i + '\t')
			for j in arguments:
				if j not in positive[i]:
					fileout1.write(j + '\t')
					fileout3.write(i + '\t' + j + '\n')
			fileout1.write('\n')

		file1.close()
		file2.close()
		fileout1.close()
		fileout3.close()

