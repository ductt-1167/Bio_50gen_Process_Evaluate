import os
import shutil


vcf_output_folder = '/media/data/dungdv/ductt/strelka_result_vcf'
vcf_truth_file = ''

# =========================================== copy file predict variants.vcf.gz and gunzip  =========================================================
def gunzip():
    strelka_output_folder = '/media/data/dungdv/ductt/strelka_result'
    

    list_lab = os.listdir(strelka_output_folder)
    for lab in list_lab:
        list_gen = os.listdir(os.path.join(strelka_output_folder, lab))
        for gen in list_gen:
            path_file = "{}/{}/{}/results/variants/variants.vcf.gz".format(strelka_output_folder, lab, gen)
            
            # copy gz file to vcf_output_folder
            os.makedirs("{}/{}/{}".format(vcf_output_folder, lab, gen))
            shutil.copy(path_file, "{}/{}/{}".format(vcf_output_folder, lab, gen))  # Not exist /media/data/dungdv/ductt/strelka_result_vcf/WES_EA_T_1/PDGFRA_T/variants.vcf.gz
            
            # gunzip 
            os.system("gunzip {}/{}/{}/variants.vcf.gz".format(vcf_output_folder, lab, gen))
            
            # remove gz file
            os.remove("{}/{}/{}/variants.vcf.gz".format(vcf_output_folder, lab, gen))
        print("Done lab {}".format(lab))

# # copy file predict variants.vcf.gz and gunzip 
# gunzip()


# =========================================== get all ground truth in vcf file for each gen =========================================================
gene_info = {
    'ABL1': [9, 130713043, 130887675],
    'AKT1': [14, 104769349, 104795748],
    'ALK': [2, 29190992, 29921589],
    'APC': [5, 112707498, 112846239],
    'ATM': [11, 108222484, 108369102],
    'BRAF': [7, 140713328, 140924929],
    # 'BRCA2': [13, 32315508, 32400268],
    'CDH1': [16, 68737292, 68835537],
    'CDKN2A': [9, 21967752, 21995324],
    'CSF1R': [5, 150053295, 150113365],
    'CTNNB1': [3, 41199422, 41240445],
    'EGFR': [7, 55019017, 55211628],
    'ERBB2': [17, 39688094, 39728660],
    'ERBB4': [2, 211375717, 212538802],
    'EZH2': [7, 148807374, 148884344],
    'FBXW7': [4, 152320544, 152536873],
    'FGFR1': [8, 38411143, 38468635],
    'FGFR2': [10, 121478330, 121598458],
    'FGFR3': [4, 1793293, 1808872],
    'FLT3': [13, 28003274, 28100587],
    'GNA11': [19, 3094362, 3123999],
    'GNAQ': [9, 77716097, 78031811],
    'GNAS': [20, 58839681, 58911192],
    'HNF1A': [12, 120977683, 121002512],
    'HRAS': [11, 532242, 535576],
    'IDH1': [2, 208236227, 208255071],
    'IDH2': [15, 90083045, 90102468],
    'JAK2': [9, 4984390, 5129948],
    'JAK3': [19, 17824782, 17848071],
    'KDR': [4, 55078481, 55125595],
    'KIT': [4, 54657957, 54740715],
    'KRAS': [12, 25205246, 25250929],
    'MET': [7, 116672196, 116798386],
    'MLH1': [3, 36993487, 37050846],
    'MPL': [1, 43336875, 43354466],
    'NOTCH1': [9, 136494433, 136546048],
    'NPM1': [5, 171387116, 171410900],
    'NRAS': [1, 114704469, 114716771],
    'PDGFRA': [4, 54229127, 54298245],
    'PIK3CA': [3, 179148114, 179240093],
    'PTEN': [10, 87863625, 87971930],
    'PTPN11': [12, 112418915, 112509918],
    'RB1': [13, 48303751, 48481890],
    'RET': [10, 43077069, 43130351],
    'SMAD4': [18, 51030213, 51085042],
    'SMARCB1': [22, 23786966, 23838009],
    'SMO': [7, 129188633, 129213548],
    'SRC': [20, 37344690, 37406050],
    'STK11': [19, 1205778, 1228431],
    'TP53': [17, 7668421, 7687490],
    'VHL': [3, 10141778, 10153667]
}

def create_vcf_truth(file_path):
    fo = open(file_path, 'a')
    return fo


def get_necessary_data_vcf(vcf_file):
    fi = open(vcf_file, 'r')
    data = fi.read().split('\n')[:-1]
    
    data_necessary = []
    for line in data:
        if line[0] != '#':
            data_necessary.append(line)
            
    return data_necessary


all_data_truth_vcf = []
all_data_truth_vcf.extend(get_necessary_data_vcf('datatest/high-confidence_sINDEL_in_HC_regions_v1.2.vcf'))
all_data_truth_vcf.extend(get_necessary_data_vcf('datatest/high-confidence_sSNV_in_HC_regions_v1.2.vcf'))
print(len(all_data_truth_vcf))


def get_vcf_truth_each_gen(folder_save):
    os.makedirs(folder_save, exist_ok=True)
    
    for gen, values in gene_info.items():
        num_chr = values[0]
        start = values[1]
        end = values[2]
        
        fo = create_vcf_truth(os.path.join(folder_save, gen+'.txt'))
        
        for line in all_data_truth_vcf:
            line_split = line.split('\t')
            
            _chr = line_split[0]
            _pos = line_split[1]
            
            if _chr == 'chr'+str(num_chr) and start <= int(_pos) <= end:
                fo.write(line+'\n')         
    
# get_vcf_truth_each_gen('truth_label_each_gen/')   
        
# ========================================================================== Evaluate: Precision, Recall ===============================================================
"""
TP là số biến thể phát hiện đúng
FP là số biến thể phát hiện nhưng không chính xác
FN là số biến thể không phát hiện được

Recall = TP / (TP + FN)
Precision = TP / (TP + FP)

Predict label has 2 types:
- ...NoPassed... (Eg. LowGQX;LowDepth;NoPassedVariantGTs)
- PASS

Truth label has 1 type:
- PASS: PASS;MedConf - PASS;HighConf

"""   
strelka2_predict_folder = 'data/strelka_result_vcf/'
truth_folder = 'truth_label_each_gen/'
log_file = 'precision_recall_log.txt'

fo = open(log_file, 'a')

def get_vcf_data(vcf_file):
    fi = open(vcf_file, 'r')
    data = fi.read().split('\n')[:-1]
    
    _pos = []
    _ref = []
    _alt = []
    _filter = []
    
    for line in data:
        if line[0] != '#':
            line_split = line.split('\t')
            _pos.append(line_split[1])
            _ref.append(line_split[3])
            _alt.append(line_split[4])
            _filter.append(line_split[6])
            
    return _pos, _ref, _alt, _filter 


def compare(truth, predict):
    """
    Return True if pair is same
    """
    _pos_truth, _ref_truth, _alt_truth, _filter_truth = truth
    _pos_predict, _ref_predict, _alt_predict, _filter_predict = predict
    
    if _pos_truth == _pos_predict and _ref_truth == _ref_predict and _alt_truth == _alt_predict and _filter_predict == 'PASS':
        return True
    else:
        return False 
    

def get_confusion_matrix(lab, gen):
    predict_file = 'data/strelka_result_vcf/{}/{}/variants.vcf'.format(lab, gen+'_T')
    truth_file = 'truth_label_each_gen/{}.txt'.format(gen)
    
    _pos_truth, _ref_truth, _alt_truth, _filter_truth = get_vcf_data(truth_file)
    _pos_predict, _ref_predict, _alt_predict, _filter_predict = get_vcf_data(predict_file)
    
    TP=FP=FN=0
    
    for i in range(len(_pos_truth)):
        for j in range(len(_pos_predict)):
            if compare((_pos_truth[i], _ref_truth[i], _alt_truth[i], _filter_truth[i]), (_pos_predict[j], _ref_predict[j], _alt_predict[j], _filter_predict[j])):
                TP +=1
                
    FN = len(_pos_truth) - TP 
    FP = -TP 
    for i in _filter_predict:
        if i == 'PASS':
            FP += 1 
    
    return TP, FP, FN
    
    
list_lab = os.listdir('data/strelka_result_vcf')
list_gen = ['ABL1', 'AKT1', 'ALK', 'APC', 'ATM', 'BRAF', 'CDH1', 'CDKN2A', 'CSF1R', 'CTNNB1', 'EGFR', 'ERBB2',
            'ERBB4', 'EZH2', 'FBXW7', 'FGFR1', 'FGFR2', 'FGFR3', 'FLT3', 'GNA11', 'GNAQ', 'GNAS', 'HNF1A', 'HRAS',
            'IDH1', 'IDH2', 'JAK2', 'JAK3', 'KDR', 'KIT', 'KRAS', 'MET', 'MLH1', 'MPL', 'NOTCH1', 'NPM1', 'NRAS',
            'PDGFRA', 'PIK3CA', 'PTEN', 'PTPN11', 'RB1', 'RET', 'SMAD4', 'SMARCB1', 'SMO', 'SRC', 'STK11', 'TP53',
            'VHL']

precision_mean = []
recall_mean = []

for i in list_lab:
    middle_p = 0
    middle_r = 0
    for j in list_gen:
        tp, fp, fn = get_confusion_matrix(i, j)
        
        if tp == 0 and fp == 0 and fn ==0:
            print('{} - {}: Precision: {} - Recall: {}'.format(i, j, 1, 1))
            middle_r += 1 
            middle_p += 1
        else:
            try:
                precision = tp/(tp+fp)
            except:
                precision = 1
                
            try:
                recall = tp/(tp+fn)
            except:
                recall = 1
            
            middle_r += recall
            middle_p += precision
            
            fo.write('{} - {}: Precision: {} - Recall: {}\n'.format(i, j, precision, recall))
    
    precision_mean.append(middle_p/50)
    recall_mean.append(middle_r/50)

fo.write('==========================================\n')
for i in range(len(list_lab)):
    fo.write('Lab {}: Precision: {} - Recall: {}\n'.format(list_lab[i], precision_mean[i], recall_mean[i]))
        


