import os 
import glob

path = 'data/vcf'
list_file = glob.glob('{}/*'.format(path))
print(len(list_file))

def get_data(file):
    f = open(file, 'r')
    data = f.read().split('\n')[:-1]
    result = []
    for line in data:
        if line[0] != '#':
            result.append(line.split('\t')[6])
    return result

file_check = 'all_type_label_truth.txt'
fo = open(file_check, 'a')

for i in list_file:
    data = get_data(i)
    for j in data:
        fo.write(j+'\n')


# check data 
fi = open(file_check, 'r')
count =0
print('Pass' in 'PASS')
data= fi.read().split('\n')[:-1]
for i in data:
    if i != 'PASS' and 'NoPassed' not in i:
        print(i)
        count +=1  
        
print(count)
        
