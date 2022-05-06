import sys
import os

# using cmd: samtools view -h ../../WES_IL_T_2.bwa.dedup.bam 'chr9:130713043-130887675' > ABL1.sam
bam_in_file = sys.argv[1]

gene_name = str(sys.argv[2])  # 'SMARCB1'
chr_name = str(sys.argv[3])  # '22'
start = int(sys.argv[4])  # 24129153
end = int(sys.argv[5])  # 24180196
folder_name = str(sys.argv[6])

print('Gene: {} - Start: {} - End: {} - Length: {}'.format(gene_name, start, end, int(end) - int(start)))

path_save = '/media/data/dungdv/ductt/sam_normal/'+folder_name


sam_out_file = '{}/{}.sam'.format(path_save, gene_name)


infor = 'chr{}:{}-{}'.format(chr_name, start, end)

print('samtools view -h {} \'{}\' > {}'.format(bam_in_file, infor, sam_out_file))

os.system('samtools view -h {} \'{}\' > {}'.format(bam_in_file, infor, sam_out_file))
