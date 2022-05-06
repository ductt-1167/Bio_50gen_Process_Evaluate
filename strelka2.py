"""
Using strelka2 to predict somatic
"""

import os
import shutil


# /media/data/dungdv/ductt


def call_sort_bam(sam_file, gene_name, dest_path):
    """
    samtools view -b EA_T.sam > EA_T.bam
    samtools view -b -F 4 EA_T.bam > EA_T.mapped.bam
    samtools sort EA_T.mapped.bam -o EA_T.mapped.sorted.bam
    samtools index -b EA_T.mapped.sorted.bam > EA_T.mapped.sorted.bam.bai
    """
    bam_file = dest_path + gene_name + '_T.bam'
    mapped_bam_file = dest_path + gene_name + '_T.mapped.bam'
    mapped_sorted_bam_file = dest_path + gene_name + '_T.mapped.sorted.bam'
    mapped_sorted_bam_file_bai = dest_path + gene_name + '_T.mapped.sorted.bam.bai'

    os.system("samtools view -b {} > {}".format(sam_file, bam_file))
    os.system("samtools view -b -F 4 {} > {}".format(bam_file, mapped_bam_file))
    os.system("samtools sort {} -o {}".format(mapped_bam_file, mapped_sorted_bam_file))
    os.system("samtools index -b {} > {}".format(mapped_sorted_bam_file, mapped_sorted_bam_file_bai))


# convert sam to short bam
def sort_bam():
    source_folder_path = '/media/data/dungdv/ductt/sam_tumor/'
    dest_folder_path = '/media/data/dungdv/ductt/sorted_bam/'

    if not os.path.isdir(dest_folder_path):
        os.mkdir(dest_folder_path)

    list_labs = os.listdir(source_folder_path)

    for lab in list_labs:
        path_lab_folder = os.path.join(source_folder_path, lab)
        list_sam_file = [os.path.join(path_lab_folder, f) for f in os.listdir(path_lab_folder)]

        folder_save = dest_folder_path + lab + '/'
        os.mkdir(folder_save)

        for sam_file in list_sam_file:
            print(sam_file)
            name = os.path.basename(sam_file).split('.')[0]

            # copy file sam
            shutil.copyfile(sam_file, folder_save + name + '_T.sam')
            call_sort_bam(sam_file, name, folder_save)


def using_strelka2():
    """
    cd ~/strelka2

    python /bin/configureStrelkaGermlineWorkflow.py
    \ --bam ~/vc_tool_materials/NA24631_on_gen.mapped.sorted.bam
    \ --referenceFasta ~/GRCh38/GRCh38.fa
    \ --runDir NA24631_on_gen

    cd /bin/NA24631_on_gen
    python runWorkflow.py -m local -j 20
    """

    strelka_path = '/media/data/dungdv/strelka-2.9.2.centos6_x86_64/'
    dir_result = '/media/data/dungdv/ductt/strelka_result/'
    source_folder_path = '/media/data/dungdv/ductt/sorted_bam/'
    reference_path = '/media/data/dungdv/GRCh38.d1.vd1/GRCh38.d1.vd1.fa'

    list_labs = os.listdir(source_folder_path)

    for lab in list_labs:
        path_lab_folder = os.path.join(source_folder_path, lab)
        list_bam_file = os.listdir(path_lab_folder)

        list_sort_bam_file = []
        for i in list_bam_file:
            if 'mapped.sorted.bam' in i and 'mapped.sorted.bam.bai' not in i:
                list_sort_bam_file.append(i)

        folder_save = os.path.join(dir_result, lab)
        os.mkdir(folder_save)

        for bam_file in list_sort_bam_file:
            name = os.path.basename(bam_file).split('.')[0]
            sort_bam_file = os.path.join(path_lab_folder, bam_file)

            # command
            os.system(
                "python {}/bin/configureStrelkaGermlineWorkflow.py --bam {} --referenceFasta {} --runDir {}".format(
                    strelka_path, sort_bam_file, reference_path, os.path.join(folder_save, name)))

            os.system("python {}/runWorkflow.py -m local -j 20".format(os.path.join(folder_save, name)))



# main
# sort_bam()
using_strelka2()







