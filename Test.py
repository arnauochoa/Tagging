# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 10:31:35 2017

@author: ramon
"""
import json

import xlsxwriter as xlsxwriter
from skimage import io
from skimage.transform import rescale
import numpy as np
import ColorNaming as cn
import time

import os.path
if os.path.isfile('TeachersLabels.py') and True: 
    student = False
    import TeachersLabels as lb
    import TeachersKMeans as km
else:
    student = True
    import Labels as lb
    import KMeans as km

student=True
TestFolder = 'Test/'
ImageFolder = 'Images/'
if not os.path.isdir(TestFolder):
    os.makedirs(TestFolder)


def TestInfo(Test,Options,GTFile, NImage):
    global student
    File = TestFolder + '%02d'%Test + 'Test' + '.txt'
    if student:
        with open(File) as infile:
            data= json.load(infile)
        Options = data['o']
        GTFile = data['f']
        NImage = data['i']
    else:
        with open(File, 'w') as outfile:
            json.dump({'o':Options,'f':GTFile,'i':NImage}, outfile, ensure_ascii=False)
    return Options,GTFile, NImage

def PrintTestResult(Mess,s,t,ok):
    print     '========================== '+ Mess + ' =========================='
    if ok:
        print '                              SUCCESFUL'
        print '==============================================================================\n'
    else:
        print '                                FAIL!!!'
        print '==============================================================================\n'
        print 'your result >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print s
        print 'desired result <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        print t
        print '\n\n'
        
def CheckTest(Message, D, File, student):
    same = 0
    if student:
        with open(File) as infile:
            DT = json.load(infile)
        try:
            if type(D) is list:
                same = (D==DT)
            else:
                if type(D) is float:
                    D = np.array(D)
                DT = np.array(DT)
#                same = (D==DT).all()
                same = np.allclose(D,DT,rtol=0.0001,atol=0)
        except:
            pass
            
        PrintTestResult(Message, D, DT, same)
    else:
        if type(D) is not list and type(D) is not float:
            D = D.tolist()
        with open(File, 'w') as outfile:
            json.dump(D, outfile, ensure_ascii=False)
    return same
            
######################################################################################################
def TestSolution(Test, Options, GTFile, NImage, worksheet, row):
    global student
    Options, GTFile, NImage = TestInfo(Test, Options, GTFile, NImage)
    ######################################################################################################
    GT = lb.loadGT(ImageFolder + GTFile)
    
    im = io.imread(ImageFolder + GT[NImage][0])
    im = rescale(im, 0.7, preserve_range=True)
    
    Messages = []
    Results = []
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
    print '!!!!!!!!!!!!!!!!!!!   TEST '+str(Test)+'   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-1 testing data init'

    #inicialización variables de estadisticas
    start_time = time.time()
    col = 0
    
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    k_m = km.KMeans(im, Options['K'], Options)
    D=k_m.X[:10]
    Results.append(CheckTest(Message, D, File, student))
    Messages.append(Message)

    #escritura en excel de estadisticas
    worksheet.write(row, col, "1")
    print "I'm wirtting on excel (ADE stuff)"

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-2 testing distance function'
    
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    X=np.arange(50,0,-0.5).reshape(-1,4)
    C=np.arange(6,0,-0.5).reshape(-1,4)
    D = km.distance(X,C)
    Results.append(CheckTest(Message, D, File, student))
    Messages.append(Message)


    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-3 testing cluster grouping'
    
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    k_m = km.KMeans(im, Options['K'], Options)
    k_m._cluster_points()
    D=k_m.clusters[:100]
    Results.append(CheckTest(Message, D, File, student))
    Messages.append(Message)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-4 testing centroid update'
    
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    k_m = km.KMeans(im, Options['K'], Options)
    k_m._iterate()
    D=k_m.centroids
    Results.append(CheckTest(Message, D, File, student))
    Messages.append(Message)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-5 testing centroid convergence'
    
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    k_m = km.KMeans(im, Options['K'], Options)
    k_m.run()
    D=k_m.centroids
    Results.append(CheckTest(Message, D, File, student))
    Messages.append(Message)
    
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-6 testing color labels extraction (simple labels)'
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    k_m = km.KMeans(im, Options['K'], Options)
    k_m.run()
    Options['single_thr']=0

    if k_m.centroids.shape[1]==3:
        k_m.centroids = cn.ImColorNamingTSELabDescriptor(k_m.centroids) 
    lab,_ = lb.getLabels(k_m, Options)
    Results.append(CheckTest(Message, lab, File, student))
    Messages.append(Message)
    
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-7 testing color labels extraction (compound labels)'
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    k_m = km.KMeans(im, Options['K'], Options)
    k_m.run()
    Options['single_thr']=1

    if k_m.centroids.shape[1]==3:
        k_m.centroids = cn.ImColorNamingTSELabDescriptor(k_m.centroids) 
    lab,_ = lb.getLabels(k_m, Options)
    Results.append(CheckTest(Message, lab, File, student))
    Messages.append(Message)
    
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-8 testing color labels extraction (0.6)'
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    k_m = km.KMeans(im, Options['K'], Options)
    k_m.run()
    Options['single_thr']=0.6
    
    if k_m.centroids.shape[1]==3:
        k_m.centroids = cn.ImColorNamingTSELabDescriptor(k_m.centroids) 
    lab,_ = lb.getLabels(k_m, Options)
    Results.append(CheckTest(Message, lab, File, student))
    Messages.append(Message)
    
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-9 testing process image function'
    File = TestFolder + '%02d'%Test + Message + '.txt'
    Options['single_thr'] /= 10
    
    lab,ind,k_m = lb.processImage(im, Options)
    Results.append(CheckTest(Message, lab, File, student))
    Messages.append(Message)

    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-10 testing similarity metric 100'
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    import random
    A = GT[NImage][1]
    B = GT[NImage][1][:]
    random.shuffle(B)
    D = lb.similarityMetric(A,B, Options)
    Results.append(CheckTest(Message, D, File, student))
    Messages.append(Message)
    
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-11 testing similarity metric 2'
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    import random
    A = GT[NImage][1]
    B = GT[NImage+2][1][:]
    random.shuffle(B)
    D = lb.similarityMetric(A,B, Options)
    Results.append(CheckTest(Message, D, File, student))
    Messages.append(Message)
    
    if student:
        print "\n\n\n                SUMMARY  TEST " + str(Test)
        for i in range(len(Messages)):
            print Messages[i] + "    " + ("OK" if Results[i] else "FAIL")
        print "\n\n"
        return sum(Results),len(Results)
    return 0,0

######################################################################################################
GTFile = 'LABELSlarge.txt'


score=[]
row = 0

#==============TEST 1 ===================
workbook = xlsxwriter.Workbook('IAP2' + 'Test' + str(1) + '.xlsx')
worksheet = workbook.add_worksheet()

Options = {'colorspace':'RGB', 'K':6, 'km_init':'first', 'fitting':'Fisher', 'single_thr':0.6, 'metric':'basic', 'verbose':False}
print "1" + str(row)
score.append(TestSolution(1, Options, GTFile, 1, worksheet, row))
Options = {'colorspace':'RGB', 'K':6, 'km_init':'first', 'fitting':'Fisher', 'single_thr':0.6, 'metric':'basic', 'verbose':False}
row += 10
print "2" + str(row)
score.append(TestSolution(1, Options, GTFile, 1, worksheet, row))

workbook.close()



#==============TEST 2====================
Options = {'colorspace':'RGB', 'K':6, 'km_init':'first', 'fitting':'Fisher', 'single_thr':0.6, 'metric':'basic', 'verbose':False}

workbook = xlsxwriter.Workbook('IAP2' + 'Test' + str(2) + '.xlsx')
worksheet = workbook.add_worksheet()
row += 10

print "3" + str(row)

score.append(TestSolution(2, Options, GTFile, 23, worksheet, row))

workbook.close()

#==============TEST 3====================
Options = {'colorspace':'ColorNaming', 'K':3, 'km_init':'first', 'fitting':'Fisher', 'single_thr':0.6, 'metric':'basic', 'verbose':False}

workbook = xlsxwriter.Workbook('IAP2' + 'Test' + str(3) + '.xlsx')
worksheet = workbook.add_worksheet()
row += 10

print "4" + str(row)

score.append(TestSolution(3, Options, GTFile, 43, worksheet, row))

workbook.close()

#==============TEST 4====================
Options = {'colorspace':'Lab', 'K':3, 'km_init':'first', 'fitting':'Fisher', 'single_thr':0.6, 'metric':'basic', 'verbose':False}

workbook = xlsxwriter.Workbook('IAP2' + 'Test' + str(4) + '.xlsx')
worksheet = workbook.add_worksheet()
row += 10

score.append(TestSolution(4, Options, GTFile, 43, worksheet, row))

workbook.close()
#==============TEST 5====================
Options = {'colorspace':'HSV', 'K':3, 'km_init':'first', 'fitting':'Fisher', 'single_thr':0.6, 'metric':'basic', 'verbose':False}

workbook = xlsxwriter.Workbook('IAP2' + 'Test' + str(5) + '.xlsx')
worksheet = workbook.add_worksheet()
row += 10

score.append(TestSolution(5, Options, GTFile, 43, worksheet, row))

workbook.close()
###########################################

GT = lb.loadGT(ImageFolder + GTFile)
im = io.imread(ImageFolder + GT[0][0])
im = rescale(im, 0.5, preserve_range=True)

Final = sum([x[0] for x in score])
Over =  sum([x[1] for x in score])

print "NIUs: ",lb.NIUs()
print "Final Score: %d / %d"%(Final,Over)

Options = {'colorspace':'HSV', 'K':0, 'km_init':'first', 'fitting':'Fisher', 'single_thr':0.6, 'metric':'basic', 'verbose':False}
lab,ind,k_m = lb.processImage(im, Options)
print lab
