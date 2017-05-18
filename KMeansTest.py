# -*- coding: utf-8 -*-
"""

@author: Ramon
"""

from skimage import io
from skimage.transform import rescale
from skimage import color
import ColorNaming as cn
import numpy as np
import matplotlib.pyplot as plt
import time

import KMeans as km


plt.close("all")
if __name__ == "__main__":
    im = io.imread('Images/0065.jpg')
    # im = rescale(im, 0.4, preserve_range=True)

    # === ex8 ===
    # im = color.rgb2lab(im)
    # print '--> Valor pixel: '
    # print im[41][31]
    # print '===================='

    # === ex9 ===
    # im = cn.ImColorNamingTSELabDescriptor(im)
    print '--> Valor pixel: '
    print im[17][65]
    print '===================='



    plt.figure(1)
    plt.imshow(im/255)
    plt.axis('off')

    X = np.reshape(im, (-1, im.shape[2]))
    print X
    results = []
    #for k in range(1,13):
    k = 3
    plt.figure(3)
    options = {'verbose':True, 'km_init': 'first'}
    #=== ex7 ===
    #options = {'verbose':True, 'km_init': 'custom'}

    k_m = km.KMeans(X, k, options)
    t = time.time()
    k_m.run()
    print time.time()-t
    results.append(k_m.fitting())
    plt.figure(2)
    plt.cla()
    plt.plot(range(1,k+1),results)
    plt.xlabel('K')
    plt.ylabel('fitting score')
    plt.draw()
    plt.pause(0.01)

    print k_m.centroids
    
    plt.figure(3)
    k_m.plot()
#plt.savefig('foo.png', bbox_inches='tight')