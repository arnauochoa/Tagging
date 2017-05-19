# -*- coding: utf-8 -*-

from skimage import io
from skimage.transform import rescale
from skimage import color
import ColorNaming as cn
import numpy as np
import matplotlib.pyplot as plt
import time

import KMeans as km

X = np.array([[250,191,260], [260,1,172], [224,72,242], [214,169,167], [156,218,147], [214,56,243]])
options = {'verbose':True, 'km_init': 'first'}
K = 2
k_m = km.KMeans(X, K, options)
k_m._init_centroids()
print 'CENTROIDS: '
print k_m.centroids

