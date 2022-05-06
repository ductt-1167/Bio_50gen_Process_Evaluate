import os
import json


all_gene = ['ABL1', 'AKT1', 'ALK', 'APC', 'ATM', 'BRAF',
            # 'BRCA2',
            'CDH1', 'CDKN2A', 'CSF1R', 'CTNNB1', 'EGFR', 'ERBB2',
            'ERBB4', 'EZH2', 'FBXW7', 'FGFR1', 'FGFR2', 'FGFR3', 'FLT3', 'GNA11', 'GNAQ', 'GNAS', 'HNF1A', 'HRAS',
            'IDH1', 'IDH2', 'JAK2', 'JAK3', 'KDR', 'KIT', 'KRAS', 'MET', 'MLH1', 'MPL', 'NOTCH1', 'NPM1', 'NRAS',
            'PDGFRA', 'PIK3CA', 'PTEN', 'PTPN11', 'RB1', 'RET', 'SMAD4', 'SMARCB1', 'SMO', 'SRC', 'STK11', 'TP53',
            'VHL']

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

log_file = '/log_depth_50_gen.txt'
fout = open(log_file, 'a')


def compute_depth_coverage(sam_file):
    f = open(sam_file, 'r')
    data = f.read().split('\n')[:-1]

    gen_name = os.path.basename(sam_file).split('.')[0]
    start_gen = gene_info[gen_name][1]
    end_gen = gene_info[gen_name][2]

    start_read = end_gen + 1
    end_read = -1
    total_length_read = 0

    have_data = False   # file CDKN2A.sam in WES_LL_T1 not have data

    for line in data:
        line_split = line.split('\t')
        if len(line_split) > 10:
            have_data = True
            for j in range(len(line_split)):
                total_length_read += len(line_split[9])

                if int(line_split[3]) < start_gen or int(line_split[3])+len(line_split[9]) > end_gen:
                    if int(line_split[3]) < start_gen:
                        start_read = start_gen
                        total_length_read -= start_gen - int(line_split[3]) + 1
                    if int(line_split[3])+len(line_split[9]) > end_gen:
                        end_read = end_gen
                        total_length_read -= int(line_split[3]) + len(line_split[9]) - end_gen + 1
                else:
                    start_read = min(start_read, int(line_split[3]))
                    end_read = max(end_read, int(line_split[3]) + len(line_split[9]))

    if not have_data:
        depth = 0
        coverage = 0
    else:
        depth = total_length_read/(end_gen-start_gen+1)
        coverage = (end_read-start_read+1)/(end_gen-start_gen+1)

    return depth, coverage
#
# sam_file = 'CDKN2A.sam'
# print(compute_depth_coverage(sam_file))


def start():
    sam_folder = 'datatest/'
    list_lab = os.listdir(sam_folder)
    for lab in list_lab:
        depth_total = 0
        coverage_total = 0

        fout.write(lab+'\n')
        lab_path = os.path.join(sam_folder, lab)

        result_depth_dict = {}
        result_coverage_dict = {}

        list_sam_file = [os.path.join(lab_path, f) for f in os.listdir(lab_path)]
        for sam_file in list_sam_file:
            name_gen = os.path.basename(sam_file).split('.')[0]

            if name_gen != 'BRCA2':
                depth, coverage = compute_depth_coverage(sam_file)

                depth_total += depth
                coverage_total += coverage

                result_depth_dict[name_gen] = depth
                result_coverage_dict[name_gen] = coverage
            fout.write('Depth:\n')
            fout.write(json.dumps(result_depth_dict))

            fout.write('Coverage:\n')
            fout.write(json.dumps(result_coverage_dict))

            fout.write('\n')
        print("Lab {} has depth: {} and coverage: {}".format(lab, depth_total/len(list_sam_file), coverage_total/len(list_sam_file)))

start()
fout.close()