# -*- coding: utf-8 -*-
"""

@author: ramon, bojana
"""
import re
import numpy as np
import ColorNaming as cn
from skimage import color
import KMeans as km


def NIUs():
    return 1392654, 1392663

def loadGT(fileName):
    """@brief   Loads the file with groundtruth content
    
    @param  fileName  STRING    name of the file with groundtruth
    
    @return groundTruth LIST    list of tuples of ground truth data
                                (Name, [list-of-labels])
    """

    groundTruth = []
    fd = open(fileName, 'r')
    for line in fd:
        splitLine = line.split(' ')[:-1]
        labels = [''.join(sorted(filter(None,re.split('([A-Z][^A-Z]*)',l)))) for l in splitLine[1:]]
        groundTruth.append( (splitLine[0], labels) )

    return groundTruth


def evaluate(description, GT, options):
    """@brief   EVALUATION FUNCTION
    @param description LIST of color name lists: contain one lsit of color labels for every images tested
    @param GT LIST images to test and the real color names (see  loadGT)
    @options DICT  contains options to control metric, ...
    @return mean_score,scores mean_score FLOAT is the mean of the scores of each image
                              scores     LIST contain the similiraty between the ground truth list of color names and the obtained
    """
#########################################################
##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
##  AND CHANGE FOR YOUR OWN CODE
#########################################################


    scores = []
    i = 0
    for gt in GT:
        scores.append(similarityMetric(description[i], gt[1], options))
        i += 1
    suma_scores = sum(scores)
    return suma_scores/len(description), scores



def similarityMetric(Est, GT, options):
    """@brief   SIMILARITY METRIC
    @param Est LIST  list of color names estimated from the image ['red','green',..]
    @param GT LIST list of color names from the ground truth
    @param options DICT  contains options to control metric, ...
    @return S float similarity between label LISTs
    """

    if options == None:
        options = {}
    if not 'metric' in options:
        options['metric'] = 'basic'

    if options['metric'].lower() == 'basic'.lower():
        intersection = 0.0
        for label in Est:
            if label in GT:
                intersection += 1.0
        total = intersection/len(Est)
        return total
    else:
        return 0

def getLabels(kmeans, options):
    """@brief   Labels all centroids of kmeans object to their color names
    
    @param  kmeans  KMeans      object of the class KMeans
    @param  options DICTIONARY  options necessary for labeling
    
    @return colors  LIST    colors labels of centroids of kmeans object
    @return ind     LIST    indexes of centroids with the same color label
    """

    numPoints = np.array([(kmeans.clusters == k).sum() for k in range(kmeans.centroids.shape[0])])
    # acaca = -np.sort(-numPoints)
    sortedCentroids = np.empty((0, kmeans.centroids.shape[1]))

    for k in range(len(numPoints)):
        index = np.argmax(numPoints)
        sortedCentroids = np.append(sortedCentroids, np.array([kmeans.centroids[index]]), axis=0)
        numPoints[index] = 0

    meaningful_colors = []
    unique = []

    sum_centroids = sortedCentroids.sum(axis=1)

    for i in range(kmeans.centroids.shape[0]):
        main_value = 0
        position = 0

        for j in range(kmeans.centroids.shape[1]):
            if sortedCentroids[i][j] > main_value:
                main_value = sortedCentroids[i][j]
                position = j

        if main_value >= options['single_thr']:
            if not cn.colors[position] in meaningful_colors:
                meaningful_colors.append(cn.colors[position])
                unique.append([i])
            else:
                index = meaningful_colors.index(cn.colors[position])
                unique[index].append(i)

        else:
            second_value = 0
            second_position = 0

            for k in range(kmeans.centroids.shape[1]):
                if sortedCentroids[i][k] > second_value and sortedCentroids[i][k] != main_value:
                    second_value = sortedCentroids[i][k]
                    second_position = k
            if cn.colors[position] < cn.colors[second_position]:
                doublecolor = cn.colors[position] + cn.colors[second_position]
            else:
                doublecolor = cn.colors[second_position] + cn.colors[position]

            if doublecolor not in meaningful_colors:
                meaningful_colors.append(doublecolor)
                unique.append([i])

            else:
                index = meaningful_colors.index(doublecolor)
                unique[index].append(i)

    return meaningful_colors, unique


def processImage(im, options):
    """@brief   Finds the colors present on the input image
    
    @param  im      LIST    input image
    @param  options DICTIONARY  dictionary with options
    
    @return colors  LIST    colors of centroids of kmeans object
    @return indexes LIST    indexes of centroids with the same label
    @return kmeans  KMeans  object of the class KMeans
    """

#########################################################
##  YOU MUST ADAPT THE CODE IN THIS FUNCTIONS TO:
##  1- CHANGE THE IMAGE TO THE CORRESPONDING COLOR SPACE FOR KMEANS
##  2- APPLY KMEANS ACCORDING TO 'OPTIONS' PARAMETER
##  3- GET THE NAME LABELS DETECTED ON THE 11 DIMENSIONAL SPACE
#########################################################

##  1- CHANGE THE IMAGE TO THE CORRESPONDING COLOR SPACE FOR KMEANS
    if options['colorspace'].lower() == 'ColorNaming'.lower():
        imcn = cn.ImColorNamingTSELabDescriptor(im)
        im = np.reshape(imcn, (-1, imcn.shape[2]))
    elif options['colorspace'].lower() == 'RGB'.lower():
        im = np.reshape(im, (-1, im.shape[2]))
    elif options['colorspace'].lower() == 'Lab'.lower():
        imlab = color.rgb2lab(im)
        im = np.reshape(imlab, (-1, imlab.shape[2]))
##  2- APPLY KMEANS ACCORDING TO 'OPTIONS' PARAMETER
    if options['K'] < 2:
        kmeans = km.KMeans(im, 0, options)
        kmeans.bestK()
    else:
        kmeans = km.KMeans(im, options['K'], options)
        kmeans.run()

##  3- GET THE NAME LABELS DETECTED ON THE 11 DIMENSIONAL SPACE
    if options['colorspace'].lower() == 'RGB'.lower():
        kmeans.centroids = cn.ImColorNamingTSELabDescriptor(kmeans.centroids)
    elif options['colorspace'].lower() == 'Lab'.lower():
        print kmeans.centroids
        print color.lab2rgb(kmeans.centroids)
        kmeans.centroids = cn.ImColorNamingTSELabDescriptor(color.lab2rgb(kmeans.centroids))

#########################################################
##  THE FOLLOWING 2 END LINES SHOULD BE KEPT UNMODIFIED
#########################################################
    colors, which = getLabels(kmeans, options)
    return colors, which, kmeans
