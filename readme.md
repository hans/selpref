In /Selectional_preference/UD_data folder, there are all the corpora from Universal Dependency for Chinese, English, German, and Czech. zh_UD, en_UD, de_UD, and cs_UD files are joint corpora of zh, en, de, and cs folders. Code for this process is append_corpora.py in /Selectional_preference/scripts folder.

In /Selectional_preference/core folder, there are three folders: raw, filtered, split. In raw folder, there are extracted verb-argument pairs for each language. We extracted three types of verb-argument pairs: verb-direct object(obj) pairs, verb-indirect object(iobj) pairs, verb-subjective(subj) pairs. Raw folder contains all the pairs that are directly obtained from UD_data, so there might be some repetitive pairs in it. Code for this process is v_a_core_paires.py in /Selectional_preference/scripts folder.

In filtered folder in core folder, the v-a pairs are filtered to remove those repetitive pairs in raw folder. There are two format for the files: 
			pair:  verb 	argument
			list:  verb 	argument1 	argument2 	argument3
Code for this is filter.py in /Selectional_preference/scripts folder.

In split folder in core folder, the v-a pairs for each language are split into training files and test files. The format for the files is list. The ratio of training set and test set is 4:1. Code for this is split.py in /Selectional_preference/scripts folder.


#####################


How to use codes:
append_corpora.py:
usage: append_corpora.py [-h] inp_dir out_dir
e.g.
python append_corpora.py /Selectional_preference/UD_data /Selectional_preference/UD_data

v_a_core_pairs.py:
usage: v_a_core_pairs.py [-h] [--dependency DEPENDENCY] [--language LANGUAGE]
                         inp out_folder
e.g.
python v_a_core_pairs.py /Selectional_preference/UD_data/zh_UD /Selectional_preference/core/raw/zh --dependency obj --dependency iobj --dependency nsubj --language zh                   

filter.py: 
usage: filter.py [-h] [--dependency DEPENDENCY] [--language LANGUAGE]
                 inp out_dir
e.g. 
python filter.py /Selectional_preference/core/raw/zh/v_a_iobj_zh /Selectional_preference/core/filtered/zh --dependency iobj --language zh

split.py:
usage: split.py [-h] [--dependency DEPENDENCY] [--language LANGUAGE]
                input corpus out_dir
e.g.
python split.py /Selectional_preference/core/filtered/zh/v_a_filtered_lists_iobj_zh /Selectional_preference/UD_data/zh_UD /Selectional_preference/core/split/zh --dependency iobj --language zh
