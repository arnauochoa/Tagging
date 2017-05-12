
"""

@author: ramon, bojana
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
from sklearn.decomposition import PCA
from copy import deepcopy
from math import sqrt

    
def distance(X, C):
    """@brief   Calculates the distance between each pixel and each centroid

    @param  X  numpy array PxD 1st set of data points (usually data points)
    @param  C  numpy array KxD 2nd set of data points (usually cluster centroids points)

    @return dist: PxK numpy array position ij is the distance between the
    i-th point of the first set an the j-th point of the second set
    """

    dist = np.ndarray((len(X), len(C)))

    for i in range(len(X)):
        for j in range(len(C)):
            dist[i, j] = np.linalg.norm(X[i] - C[j])
    return dist

def fisher_discriminant(u, v):
    return np.divide(abs(np.mean(u) - np.mean(v)), np.var(u) + np.var(v))

class KMeans():
    
    def __init__(self, X, K, options=None):
        """@brief   Constructor of KMeans class
        
        @param  X   LIST    input data
        @param  K   INT     number of centroids
        @param  options DICT dctionary with options
        """

        self._init_X(X)                                    # LIST data coordinates
        self._init_options(options)                        # DICT options
        self._init_rest(K)                                 # Initializes de rest of the object
        
#############################################################
##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
#############################################################

        
    def _init_X(self, X):
        """@brief Initialization of all pixels
        
        @param  X   LIST    list of all pixel values. Usually it will be a numpy 
                            array containing an image NxMx3

        sets X an as an array of data in vector form (PxD  where P=N*M and D=3 in the above example)
        """

        self.X = np.reshape(X, (-1, X.shape[2]))
        self.num_pix = len(self.X)

            
    def _init_options(self, options):
        """@brief Initialization of options in case some fields are left undefined
        
        @param  options DICT dctionary with options
        sets de options parameters
        """

        if options == None:
            options = {}
        if not 'km_init' in options:
            options['km_init'] = 'first'
        if not 'verbose' in options:
            options['verbose'] = False
        if not 'tolerance' in options:
            options['tolerance'] = 0
        if not 'max_iter' in options:
            options['max_iter'] = np.inf
        if not 'fitting' in options:
            options['fitting'] = 'Fisher'

        self.options = options
        
#############################################################
##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
#############################################################

        
    def _init_rest(self, K):
        """@brief   Initialization of the remainig data in the class.
        
        @param  options DICT dctionary with options
        """
        self.K = K                                             # INT number of clusters
        if self.K > 0:
            self._init_centroids()                             # LIST centroids coordinates
            self.old_centroids = np.empty_like(self.centroids) # LIST coordinates of centroids from previous iteration
            self.clusters = np.zeros(len(self.X))              # LIST list that assignes each element of X into a cluster
            self._cluster_points()                             # sets the first cluster assignation
        self.num_iter = 0                                      # INT current iteration
            
#############################################################
##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
#############################################################

    def _init_centroids(self):
        """@brief Initialization of centroids
        depends on self.options['km_init']
        """

        #TODO: com comprovar que no son iguals?

        self.centroids = np.empty(self.K)
        if self.options['km_init'].lower() == 'first':
            self.centroids = self.X[0:self.K]
        else:
            self.centroids = [self.X[np.random.randint(self.num_pix)] for _ in range(self.K)]

    def _cluster_points(self):  #TODO: no tinc clar que sigui aixi
        """@brief   Calculates the closest centroid of all points in X
        """

        self.clusters = np.argmin(distance(self.X, self.centroids), axis=1)

    def _get_centroids(self): #TODO: falta testejar
        """@brief   Calculates coordinates of centroids based on the coordinates 
                    of all the points assigned to the centroid
        """

        """self.old_centroids = deepcopy(self.centroids)"""

        self.old_centroids = np.array(self.centroids, copy=True)

        """for cluster in range(self.K):
            cluster_pixels = np.array([])
            for pixel in range(len(self.X)):
                if self.clusters[pixel] == cluster:
                    np.append(cluster_pixels, self.X[pixel])
            if cluster_pixels:
                a = np.mean(cluster_pixels)
                print cluster_pixels
                print a
                self.centroids[cluster] = a"""

        for cluster in range(self.K):
            cluster_pixel = 0.0
            num_cluster_pixels = 0.0
            for pixel in range(self.num_pix):
                if self.clusters[pixel] == cluster:
                    cluster_pixel += self.X[pixel]
                    num_cluster_pixels += 1
            if num_cluster_pixels > 0:
                """mean = np.mean(cluster_pixel)
                print mean"""
                """mean = cluster_pixel / num_cluster_pixels"""
                mean = np.divide(cluster_pixel, num_cluster_pixels)
                self.centroids[cluster] = mean

    def _converges(self):  #TODO: falta testejar
        """@brief   Checks if there is a difference between current and old centroids
        """

        converges = 0

        dist = distance(self.old_centroids, self.centroids)
        #
        # converges_arr = dist > self.options['tolerance']
        # print(converges_arr.all())
        # if converges_arr.all():
        #     converges = True
        # return converges

        for i in dist:
            for j in i:
                if j <= self.options['tolerance']:
                    converges += 1
        if converges < len(dist):
            return False
        return True

    def _iterate(self, show_first_time=True):
        """@brief   One iteration of K-Means algorithm. This method should 
                    reassigne all the points from X to their closest centroids
                    and based on that, calculate the new position of centroids.
        """
        self.num_iter += 1
        self._cluster_points()
        self._get_centroids()
        if self.options['verbose']:
            self.plot(show_first_time)

    def run(self):
        """@brief   Runs K-Means algorithm until it converges or until the number
                    of iterations is smaller than the maximum number of iterations.=
        """
        if self.K==0:
            self.bestK()
            return        
        
        self._iterate(True)
        self.options['max_iter'] = np.inf
        if self.options['max_iter'] > self.num_iter:
            while not self._converges() :
                self._iterate(False)

    def bestK(self):
        """@brief   Runs K-Means multiple times to find the best K for the current 
                    data given the 'fitting' method. In cas of Fisher elbow method 
                    is recommended.
                    
                    at the end, self.centroids and self.clusters contains the 
                    information for the best K. NO need to rerun KMeans.
           @return bestK is the best K found.
        """

        fit = np.array([])
        reps = 10
        second_der = np.array([])

        for K in range(reps):
            self._init_rest(4)
            self.run()
            fit[K] = self.fitting()
        for K in range(reps-2):
            second_der[K] = fit[K+1] + fit[K-1] - 2 * fit[K]
        bestK = 1 + np.argmax(second_der)
        return bestK


    def get_pix_clust(self, clust):
        """@brief   Gets all pixels form one cluster

           @param  clust 89INT cluster number

           @return NUMPY ARRAY array with all pixels
        """
        clust_pix = []
        for pixel in self.X:
            if self.clusters[pixel] is clust:
                clust_pix.append(pixel)
        return np.array(clust_pix)

    def fitting(self):
        """@brief  return a value describing how well the current kmeans fits the data
        """

        if self.options['fitting'].lower() == 'fisher':
            #calcul mu's
            mu = np.mean(self.X, axis=0) #fa referencia al centroide mitja?
            mu_k = []
            for centroid in range(self.K):
                mu_k[centroid] = np.mean(self.get_pix_clust(centroid))

            #calcul between variance i within variance
            bet_var = 0
            with_var = 0
            for centroid in range(self.K):
                bet_var += np.linalg.norm(mu_k[centroid] - mu)
                clust_pix = self.get_pix_clust(centroid)
                for pixel in range(len(clust_pix)):
                    with_var += sqrt((clust_pix[pixel] - mu_k[centroid])**2)
            bet_var = bet_var/self.K
            with_var = with_var/self.K

            #calcul discriminant
            discriminant = with_var/bet_var

            return discriminant

            #return fisher_discriminant(self.centroids, self.old_centroids)

        else: # TODO provar a fer silhouette
            return np.random.rand(1)


    def plot(self, first_time=True):
        """@brief   Plots the results
        """

        #markersshape = 'ov^<>1234sp*hH+xDd'	
        markerscolor = 'bgrcmybgrcmybgrcmyk'
        if first_time:
            plt.gcf().add_subplot(111, projection='3d')
            plt.ion()
            plt.show()

        if self.X.shape[1]>3:
            if not hasattr(self, 'pca'):
                self.pca = PCA(n_components=3)
                self.pca.fit(self.X)
            Xt = self.pca.transform(self.X)
            Ct = self.pca.transform(self.centroids)
        else:
            Xt=self.X
            Ct=self.centroids

        for k in range(self.K):
            plt.gca().plot(Xt[self.clusters==k,0], Xt[self.clusters==k,1], Xt[self.clusters==k,2], '.'+markerscolor[k])
            plt.gca().plot(Ct[k,0:1], Ct[k,1:2], Ct[k,2:3], 'o'+'k',markersize=12)

        if first_time:
            plt.xlabel('dim 1')
            plt.ylabel('dim 2')
            plt.gca().set_zlabel('dim 3')
        plt.draw()
        plt.pause(0.01)