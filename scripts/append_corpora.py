lst_cs =['CAC-master/cs_cac-ud-train','CAC-master/cs_cac-ud-test','CAC-master/cs_cac-ud-dev','CLTT-master/cs_cltt-ud-train','CLTT-master/cs_cltt-ud-test','CLTT-master/cs_cltt-ud-dev','FicTree-master/cs_fictree-ud-train','FicTree-master/cs_fictree-ud-test','FicTree-master/cs_fictree-ud-dev','PDT-master/cs_pdt-ud-train-c','PDT-master/cs_pdt-ud-train-l','PDT-master/cs_pdt-ud-train-m','PDT-master/cs_pdt-ud-train-v','PDT-master/cs_pdt-ud-test','PDT-master/cs_pdt-ud-dev','PUD-master/cs_pud-ud-test']
lst_de = ['GSD-master/de_gsd-ud-train','GSD-master/de_gsd-ud-test','GSD-master/de_gsd-ud-dev']
lst_en = ['EWT-master/en_ewt-ud-train','EWT-master/en_ewt-ud-test','EWT-master/en_ewt-ud-dev','GUM-master/en_gum-ud-train','GUM-master/en_gum-ud-test','GUM-master/en_gum-ud-dev','LinES-master/en_lines-ud-train','LinES-master/en_lines-ud-test','LinES-master/en_lines-ud-dev','ParTUT-master/en_partut-ud-train','ParTUT-master/en_partut-ud-test','ParTUT-master/en_partut-ud-dev','PUD-master/en_pud-ud-test']
lst_zh = ['CFL-master/zh_cfl-ud-test','GSD-master/zh_gsd-ud-train','GSD-master/zh_gsd-ud-test','GSD-master/zh_gsd-ud-dev','HK-master/zh_hk-ud-test','PUD-master/zh_pud-ud-test']
fileout1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/cs_UD','w',encoding = 'utf-8')
fileout2 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/de_UD','w',encoding = 'utf-8')
fileout3 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/en_UD','w',encoding = 'utf-8')
fileout4 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/zh_UD','w',encoding = 'utf-8')

for i in lst_cs:
	name = '/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/cs/UD_Czech-' + i + '.conllu'
	file = open(name, 'rb')
	for line in file:
		line = line.decode('utf-8')
		fileout1.write(line)
	file.close()

for i in lst_de:
	name = '/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/de/UD_German-' + i + '.conllu'
	file = open(name, 'rb')
	for line in file:
		line = line.decode('utf-8')
		fileout2.write(line)
	file.close()

for i in lst_en:
	name = '/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/en/UD_English-' + i + '.conllu'
	file = open(name, 'rb')
	for line in file:
		line = line.decode('utf-8')
		fileout3.write(line)
	file.close()

for i in lst_zh:
	name = '/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/zh/UD_Chinese-' + i + '.conllu'
	file = open(name, 'rb')
	for line in file:
		line = line.decode('utf-8')
		fileout4.write(line)
	file.close()

fileout1.close()
fileout2.close()
fileout3.close()
fileout4.close()
