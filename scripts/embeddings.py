from argparse import ArgumentParser
from pathlib import Path

p = ArgumentParser()
p.add_argument("word_list_folder", type = Path)
p.add_argument("embedding_folder", type = Path)
p.add_argument("output_folder", type = Path)
p.add_argument("--languages", action = "append", help = "Specify the language of input file")

args = p.parse_args()

word_list_folder = args.word_list_folder
embedding_folder = args.embedding_folder
output_folder = args.output_folder
languages = args.languages

for language in languages:
	voca = []
	lst = ['obj', 'iobj', 'subj']
	for i in lst:
		file = open((word_list_folder / "{}/v_a_filtered_lists_{}_{}".format(language, i, language)), 'rb')
		for line in file:
			line = line.decode('utf-8').split()
			for i in line:
				if i not in voca:
					voca.append(i)
		file.close()
	
	file1 = open((embedding_folder / "wiki.{}.vec".format(language)), 'rb')
	fileout = open((output_folder / "embeddings_{}".format(language)), 'w', encoding = 'utf-8')
	for line in file1:
		line = line.decode('utf-8')
		tmp = line.split()
		if tmp[0] in voca:
			fileout.write(line)
	
	file1.close()
	fileout.close()