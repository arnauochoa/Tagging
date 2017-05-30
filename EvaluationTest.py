# -*- coding: utf-8 -*-
"""

@author: ramon
"""
from time import time
import xlsxwriter
from skimage import io
import matplotlib.pyplot as plt


import Labels as lb


plt.close("all")


def execute(options, worksheet, row):

    # print dels headers
    headers_list = ["km_init", "fitting", "colorspace", "single_thr", "k", "encert promig", "temps"]
    header_position = 0
    for column in range(len(headers_list)):
        worksheet.write(row, column, headers_list[header_position])
        header_position += 1

    DBcolors = []
    start_time = time()
    for t in range(1, 3):
        options["single_thr"] = float(t)/float(5)
        for k in range(3, 5):
            options["K"] = k
            for gt in GT:
                print gt[0]
                im = io.imread(ImageFolder + "/" + gt[0])
                colors, _, _ = lb.processImage(im, options)
                DBcolors.append(colors)
            encert, _ = lb.evaluate(DBcolors, GT, options)
            print "Encert promig: " + '%.2f' % (encert * 100) + '%'
            elapsed_time = time() - start_time

            #omplir columnes segons K
            row += 1
            worksheet.write(row, 0, options["km_init"])
            worksheet.write(row, 1, options["fitting"])
            worksheet.write(row, 2, options["colorspace"])
            worksheet.write(row, 3, options["single_thr"])
            worksheet.write(row, 4, options["K"])
            worksheet.write(row, 5, '%.2f' % (encert * 100) + '%')
            worksheet.write(row, 6, str(elapsed_time))

if __name__ == "__main__":

    #'colorspace': 'RGB', 'Lab' o 'ColorNaming'
    ImageFolder = 'Images'
    GTFile = 'test.txt'

    GTFile = ImageFolder + '/' + GTFile
    GT = lb.loadGT(GTFile)

    optionsList = []
    row = 0

    workbook = xlsxwriter.Workbook('EvaluationTest' + 'Test' + str(1) + '.xlsx')
    worksheet = workbook.add_worksheet()

    #==================================PARA Km_init=first==========================

    #===PARA colorspace=RGB
        #PARA fitting=fisher
    options = {'colorspace':'RGB', 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'fisher', 'synonyms':False}
    optionsList.append(options)
        #PARA fitting=silhouette
    options = {'colorspace':'RGB', 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'silhouette', 'synonyms':False}
    optionsList.append(options)

    for i in range(len(optionsList)):
        execute(optionsList[i], worksheet, row)
        row += 97
        worksheet.write(row, 0, str(i))
        row += 3

    workbook.close()

    #===PARA colorspace=LAB
            # PARA fitting=fisher
    options = {'colorspace':'Lab', 'K':4, 'single_thr':0.6, 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'fisher', 'synonyms':False}
    optionsList.append(options)
            # PARA fitting=sil
    options = {'colorspace':'Lab', 'K':6, 'single_thr':0.6, 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'silhouette', 'synonyms':False}
    optionsList.append(options)


    #===PARA colorspace=HSV
            # PARA fitting=fisher
    options = {'colorspace':'HSV', 'K':6, 'single_thr':0.6, 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'fisher', 'synonyms':False}
    optionsList.append(options)
            # PARA fitting=sil
    options = {'colorspace':'HSV', 'K':6, 'single_thr':0.6, 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'silhouette', 'synonyms':False}
    optionsList.append(options)





    # ==================================PARA Km_init=RANDOM==========================

    # ===PARA colorspace=RGB
        # PARA fitting=fisher
    options = {'colorspace':'RGB', 'K':6, 'single_thr':0.6, 'verbose':False, 'km_init':'random', 'metric':'basic', 'fitting':'fisher', 'synonyms':False}
    optionsList.append(options)
        # PARA fitting=sil
    options = {'colorspace':'RGB', 'K':6, 'single_thr':0.6, 'verbose':False, 'km_init':'random', 'metric':'basic', 'fitting':'silhouette', 'synonyms':False}
    optionsList.append(options)

    # ===PARA colorspace=LAB
        # PARA fitting=fisher
    options = {'colorspace':'RGB', 'K':6, 'single_thr':0.6, 'verbose':False, 'km_init':'random', 'metric':'basic', 'fitting':'fisher', 'synonyms':False}
    optionsList.append(options)
        # PARA fitting=sil
    options = {'colorspace':'RGB', 'K':6, 'single_thr':0.6, 'verbose':False, 'km_init':'random', 'metric':'basic', 'fitting':'silhouette', 'synonyms':False}
    optionsList.append(options)

    # ===PARA colorspace=HSV
        # PARA fitting=fisher
    options = {'colorspace':'RGB', 'K':6, 'single_thr':0.6, 'verbose':False, 'km_init':'random', 'metric':'basic', 'fitting':'fisher', 'synonyms':False}
    optionsList.append(options)
        # PARA fitting=sil
    options = {'colorspace':'RGB', 'K':6, 'single_thr':0.6, 'verbose':False, 'km_init':'random', 'metric':'basic', 'fitting':'silhouette', 'synonyms':False}
    optionsList.append(options)
