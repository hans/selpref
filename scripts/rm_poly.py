from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("word_list_folder", type = Path)
p.add_argument("output_folder", type = Path)
p.add_argument("--languages", action = "append", help = "Specify the language of input file")

args = p.parse_args()

word_list_folder = args.word_list_folder
output_folder = args.output_folder
languages = args.languages

for language in languages:
	lst = ['obj', 'iobj', 'subj']
	v = []
	a = []
	for i in lst:
		file = open((word_list_folder / "{}/v_a_filtered_lists_{}_{}".format(language, i, language)), 'rb')
		for line in file:
			line = line.decode('utf-8').split()
			if line[0] not in v:
				v.append(line[0])
			for i in line[1:]:
				if i not in a:
					a.append(i)
		file.close()
	
	fileout = open((output_folder / "polysemy_{}".format(language)), 'w', encoding = 'utf-8')
	for i in v:
		if i in a:
			fileout.write(i + "\t")
	
	fileout.close()