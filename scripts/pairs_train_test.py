import os

lang = ['cs','de','en','zh']
for l in lang:
	lst = os.listdir('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/split/' + l + '/')
	for i in lst:
		if str(i)[:3] != 'v_a':
			continue
		print(str(i))
		file = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/split/' + l + '/' + str(i),'rb')
		print(str(i)[9:])
		fileout = open('/Users/ariaduan1.0/Desktop/summer_experiment/Roger/projects/Jon/Selectional_preference/core/split/' + l + '/' + 'v_a_pairs' + str(i)[9:], 'w', encoding = 'utf-8')
		for line in file:
			line = line.decode('utf-8').split()
			for j in line[1:]:
				fileout.write(line[0] + '\t' + j + '\n')
		file.close()
		fileout.close()