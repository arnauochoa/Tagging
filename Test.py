# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 10:31:35 2017

@author: ramon
"""
import json
from skimage import io
from skimage.transform import rescale
import numpy as np

import os.path
if os.path.isfile('TeachersLabels.py'): 
    student = False
    import TeachersLabels as lb
    import TeachersKMeans as km
else:
    student = True
    import Labels as lb
    import KMeans as km


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
        if type(D) != type(DT):
            DT = np.array(DT)
            same = (D==DT).all()
        else:
            same = (D==DT)
            
        PrintTestResult(Message, D, DT, same)
    else:
        if type(D) is not list and type(D) is not float:
            D = D.tolist()
        with open(File, 'w') as outfile:
            json.dump(D, outfile, ensure_ascii=False)
    return same
            
######################################################################################################
def TestSolution(Test, Options, GTFile, NImage):
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
    
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    k_m = km.KMeans(im, Options['K'], Options)
    D=k_m.X[:10]
    Results.append(CheckTest(Message, D, File, student))
    Messages.append(Message)

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
    lab,_ = lb.getLabels(k_m, Options)
    Results.append(CheckTest(Message, lab, File, student))
    Messages.append(Message)
    
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-7 testing color labels extraction (compund labels)'
    File = TestFolder + '%02d'%Test + Message + '.txt'
    
    k_m = km.KMeans(im, Options['K'], Options)
    k_m.run()
    Options['single_thr']=1
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
    lab,_ = lb.getLabels(k_m, Options)
    Results.append(CheckTest(Message, lab, File, student))
    Messages.append(Message)
    
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    Message = '-9 testing similarity metric 100'
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
    Message = '-10 testing similarity metric 2'
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

######################################################################################################
GTFile = 'LABELSlarge.txt'
Options = {'colorspace':'RGB', 'K':6, 'km_init':'first', 'fitting':'Fisher', 'single_thr':0.6, 'metric':'basic', 'verbose':False}
TestSolution(1, Options, GTFile, 1)
TestSolution(2, Options, GTFile, 23)
Options = {'colorspace':'ColorNaming', 'K':3, 'km_init':'first', 'fitting':'Fisher', 'single_thr':0.6, 'metric':'basic', 'verbose':False}
TestSolution(3, Options, GTFile, 43)