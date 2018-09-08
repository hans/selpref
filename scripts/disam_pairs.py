# encoding: utf-8
from argparse import ArgumentParser
from pathlib import Path
from random import randint

p = ArgumentParser()
p.add_argument("inp_dir", type = Path)
p.add_argument("out_dir", type = Path)
p.add_argument("words_freq_dir", type = Path)
p.add_argument("freq_words_dir", type = Path)
p.add_argument("--dependency", action = "append")
p.add_argument("--language", action = "append")
args = p.parse_args()

inp_dir = args.inp_dir
out_dir = args.out_dir
words_freq_dir = args.words_freq_dir
freq_words_dir = args.freq_words_dir
dependency = args.dependency
language = args.language

for lang in language:
	for dep in dependency:
		"""
		file1 = open((words_freq_dir / "args_freq_{}".format(lang)), 'rb') # a_v inp should replace args with verbs
		file2 = open((freq_words_dir / "freq_args_{}".format(lang)), 'rb') # a_v inp should replace args with verbs
		file3 = open((inp_dir / "{}/v_a_filtered_lists_{}_{}".format(lang, dep, lang)), 'rb') # a_v inp should replace v_a with a_v
		fileout = open((out_dir / "{}/v_a1_a2_filtered_pairs_{}_{}".format(lang, dep, lang)), 'w') # a_v inp should replace v_a with a_v
		fileout1 = open((out_dir / "{}/v_a1_a2_filtered_pairs_{}_{}.train".format(lang, dep, lang)), 'w') # a_v inp should replace v_a with a_v
		fileout2 = open((out_dir / "{}/v_a1_a2_filtered_pairs_{}_{}.test".format(lang, dep, lang)), 'w') # a_v inp should replace v_a with a_v
		"""
		file1 = open((words_freq_dir / "verbs_freq_{}".format(lang)), 'rb') # a_v inp should replace args with verbs
		file2 = open((freq_words_dir / "freq_verbs_{}".format(lang)), 'rb') # a_v inp should replace args with verbs
		file3 = open((inp_dir / "{}/a_v_filtered_lists_{}_{}".format(lang, dep, lang)), 'rb') # a_v inp should replace v_a with a_v
		fileout = open((out_dir / "{}/a_v1_v2_filtered_pairs_{}_{}".format(lang, dep, lang)), 'w') # a_v inp should replace v_a with a_v
		fileout1 = open((out_dir / "{}/a_v1_v2_filtered_pairs_{}_{}.train".format(lang, dep, lang)), 'w') # a_v inp should replace v_a with a_v
		fileout2 = open((out_dir / "{}/a_v1_v2_filtered_pairs_{}_{}.test".format(lang, dep, lang)), 'w') # a_v inp should replace v_a with a_v
		
		args_cnt = {}
		for line in file1:
			line = line.decode('utf-8').split()
			args_cnt[line[0]] = line[1]

		cnt_args = {}
		for line in file2:
			line = line.decode('utf-8').split()
			cnt_args[line[0]] = line[1:]

		for_split = {}
		for line in file3:
			line = line.decode('utf-8').split()
			for i in line[1:]:
				cnt = args_cnt[i]
				if cnt in cnt_args and len(cnt_args[cnt]) > 1:
					tmp = randint(0, len(cnt_args[cnt]) - 1)
					while cnt_args[cnt][tmp] == i:
						tmp = randint(0, len(cnt_args[cnt]) - 1)
					fileout.write(line[0] + '\t' + i + '\t' + cnt_args[cnt][tmp] + '\n')
					#print(cnt)
					if cnt not in for_split:
						for_split[cnt] = []
					for_split[cnt].append((line[0], i, cnt_args[cnt][tmp]))
		#print(for_split)
		cnt = 0
		to_split = sorted(for_split.items())
		#print(to_split)
		for num, lst in to_split:
			for i in range(len(lst)):
				v, a1, a2 = lst[i]
				if cnt == 4:
					fileout2.write(v + "\t" + a1 + "\t" + a2 + "\n")
					cnt = 0
					continue
				fileout1.write(v + "\t" + a1 + "\t" + a2 + "\n")
				cnt += 1


		file1.close()
		file2.close()
		file3.close()
		fileout.close()
		fileout1.close()
		fileout2.close()