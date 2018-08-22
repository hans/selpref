file1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/cs_UD','rb')
fileout1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/cs/v_a_obj_cs','a',encoding = 'utf-8')
fileout2 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/cs/v_a_iobj_cs','a',encoding = 'utf-8')
fileout3 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/cs/v_a_subj_cs','a',encoding = 'utf-8')

verbs = {}
objs = {}
iobjs = {}
subjs = {}
for line in file1:
	line = line.decode('utf-8').split()
	if len(line) == 0:
		continue
	if line[0] == '#':
		for i in objs:
			if objs[i][1] in verbs:
				fileout1.write(verbs[objs[i][1]] + '\t' + objs[i][0] + '\n')
		for i in iobjs:
			if iobjs[i][1] in verbs:
				fileout2.write(verbs[iobjs[i][1]] + '\t' + iobjs[i][0] + '\n')
		for i in subjs:
			if subjs[i][1] in verbs:
				fileout3.write(verbs[subjs[i][1]] + '\t' + subjs[i][0] + '\n')
		file1.readline()
		verbs = {}
		objs = {}
		iobjs = {}
		subjs = {}
		continue
	if line[3] == "VERB":
		verbs[line[0]] = line[2] #for Chinese line[2] is replaced by line[1]
	if line[7] == 'obj':
		objs[line[0]] = [line[2],line[6]] #for Chinese line[2] is replaced by line[1]
	if line[7] == 'iobj':
		iobjs[line[0]] = [line[2],line[6]] #for Chinese line[2] is replaced by line[1]
	if line[7] == 'nsubj':
		subjs[line[0]] = [line[2],line[6]] #for Chinese line[2] is replaced by line[1]

file1.close()
fileout1.close()
fileout2.close()
fileout3.close()