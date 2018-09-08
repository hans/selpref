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
#		file2 = open((inp_folder + "/split/{}/v_a_lists_{}_{}.train".format(lang, dep, lang)), 'rb')
		file3 = open((inp_folder + "/split/{}/v_a_lists_{}_{}.test".format(lang, dep, lang)), 'rb')
		fileout1 = open((output_folder + "/v_a_lists_{}_{}.negative".format(lang, dep, lang)), 'w', encoding = 'utf-8')
#		fileout1 = open((output_folder + "/{}/v_a_lists_{}_{}.negative.train".format(lang, dep, lang)), 'w', encoding = 'utf-8')
"""
		fileout2 = open((output_folder + "/{}/v_a_lists_{}_{}.negative.test".format(lang, dep, lang)), 'w', encoding = 'utf-8')
		fileout3 = open((output_folder + "/{}/v_a_pairs_{}_{}.negative.train".format(lang, dep, lang)), 'w', encoding = 'utf-8')
		fileout4 = open((output_folder + "/{}/v_a_pairs_{}_{}.negative.test".format(lang, dep, lang)), 'w', encoding = 'utf-8')
"""
		positive = {}
		arguments = []
		for line in file1:
			line = line.decode('utf-8').split()
			positive[line[0]] = line[1:]
			for i in line[1:]:
				if i not in arguments:
					arguments.append(i)

		train = []
#		test = []
		for line in file2:
			line = line.decode('utf-8').split()
			train.append(line[0])

"""
		for line in file3:
			line = line.decode('utf-8').split()
			test.append(line[0])
"""
		for i in train:
			fileout1.write(i + '\t')
			for j in arguments:
				if j not in positive[i]:
					fileout1.write(j + '\t')
					fileout3.write(i + '\t' + j + '\n')
			fileout1.write('\n')
"""
		for i in test:
			fileout2.write(i + '\t')
			for j in arguments:
				if j not in positive[i]:
					fileout2.write(j + '\t')
					fileout4.write(i + '\t' + j + '\n')
			fileout2.write('\n')
"""
		file1.close()
		file2.close()
		file3.close()
		fileout1.close()
"""
		fileout2.close()
		fileout3.close()
		fileout4.close()
"""
