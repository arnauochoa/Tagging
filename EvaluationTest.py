# -*- coding: utf-8 -*-
"""

@author: ramon
"""
import xlsxwriter
from skimage import io
import matplotlib.pyplot as plt


import Labels as lb


plt.close("all")


def execute(options, worksheet, row):
    DBcolors = []
    worksheet.write(row, 0, "JODER")
    #for gt in GT:
    print GT[0][0]
    im = io.imread(ImageFolder + "/" + GT[0][0])
    colors, _, _ = lb.processImage(im, options)
    DBcolors.append(colors)
    #encert, _ = lb.evaluate(DBcolors, GT, options)
    #print "Encert promig: " + '%.2f' % (encert * 100) + '%'


if __name__ == "__main__":

    #'colorspace': 'RGB', 'Lab' o 'ColorNaming'
    ImageFolder = 'Images'
    GTFile = 'LABELSsmall.txt'

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
        #PARA fitting=sil
    options = {'colorspace':'RGB', 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'silhouette', 'synonyms':False}
    optionsList.append(options)


    #===PARA colorspace=LAB
            # PARA fitting=fisher
    options = {'colorspace':'LAB', 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'fisher', 'synonyms':False}
    optionsList.append(options)
            # PARA fitting=sil
    options = {'colorspace':'LAB', 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'silhouette', 'synonyms':False}
    optionsList.append(options)


    #===PARA colorspace=HSV
            # PARA fitting=fisher
    options = {'colorspace':'HSV', 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'fisher', 'synonyms':False}
    optionsList.append(options)
            # PARA fitting=sil
    options = {'colorspace':'HSV', 'verbose':False, 'km_init':'first', 'metric':'basic', 'fitting':'silhouette', 'synonyms':False}
    optionsList.append(options)





    # ==================================PARA Km_init=RANDOM==========================

    # ===PARA colorspace=RGB
        # PARA fitting=fisher
    options = {'colorspace': 'RGB', 'verbose': False, 'km_init': 'random', 'metric': 'basic', 'fitting': 'fisher', 'synonyms': False}
    optionsList.append(options)
        # PARA fitting=sil
    options = {'colorspace': 'RGB', 'verbose': False, 'km_init': 'random', 'metric': 'basic', 'fitting': 'silhouette', 'synonyms': False}
    optionsList.append(options)

    # ===PARA colorspace=LAB
        # PARA fitting=fisher
    options = {'colorspace': 'LAB', 'verbose': False, 'km_init': 'random', 'metric': 'basic', 'fitting': 'fisher', 'synonyms': False}
    optionsList.append(options)
        # PARA fitting=sil
    options = {'colorspace': 'LAB', 'verbose': False, 'km_init': 'random', 'metric': 'basic', 'fitting': 'silhouette', 'synonyms': False}
    optionsList.append(options)

    # ===PARA colorspace=HSV
        # PARA fitting=fisher
    options = {'colorspace': 'HSV', 'verbose': False, 'km_init': 'random', 'metric': 'basic',
               'fitting': 'fisher', 'synonyms': False}
    optionsList.append(options)
        # PARA fitting=sil
    options = {'colorspace': 'HSV', 'verbose': False, 'km_init': 'random', 'metric': 'basic',
               'fitting': 'silhouette', 'synonyms': False}
    optionsList.append(options)



    for i in range(len(optionsList)):
        execute(optionsList[i], worksheet, row)
        row += 5

    workbook.close()
