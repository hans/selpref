file1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/filtered/zh/v_a_filtered_lists_iobj_zh','rb')
file2 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/UD_data/zh_UD','rb')
fileout1 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/split/zh/v_a_lists_iobj_zh.train','w',encoding = 'utf-8')
fileout2 = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/split/zh/v_a_lists_iobj_zh.test','w',encoding = 'utf-8')

verbs = {}
args = {}
for line in file1:
	line = line.decode('utf-8').split()
	verbs[line[0]] = 0
	args[line[0]] = line[1:]

for line in file2:
	line = line.decode('utf-8').split()
	if len(line) < 3 or line[0] == '#':
		continue
	if line[1] in verbs:
		verbs[line[1]] += 1

sort = {}
for i in verbs:
	if verbs[i] in sort:
		sort[verbs[i]].append(i)
	else:
		sort[verbs[i]] = [i]

lstkey = sorted(sort.keys())

lst = []
for i in lstkey:
	for j in sort[i]:
		lst.append(j)

cnt = 0
i = 0
while i < len(lst):
	fileout1.write(lst[i] + '\t')
	for j in args[lst[i]]:
		fileout1.write(j + '\t')
	fileout1.write('\n')
	cnt += 1
	i += 1
	if cnt == 4:
		fileout2.write(lst[i] + '\t')
		for j in args[lst[i]]:
			fileout2.write(j + '\t')
		fileout2.write('\n')
		i += 1
		cnt = 0

file1.close()
file2.close()
fileout1.close()
fileout2.close()