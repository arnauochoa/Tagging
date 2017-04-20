
"""

@author: ramon, bojana
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
from sklearn.decomposition import PCA
from copy import deepcopy

    
def distance(X, C):
    """@brief   Calculates the distance between each pixel and each centroid

    @param  X  numpy array PxD 1st set of data points (usually data points)
    @param  C  numpy array KxD 2nd set of data points (usually cluster centroids points)

    @return dist: PxK numpy array position ij is the distance between the
    i-th point of the first set an the j-th point of the second set
    """

    dist = []
    for i in range(0, len(X)):
        for j in range(0, len(C)):
            dist[i][j] = np.linalg.norm(X[i] - C[j])
    return dist

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
        if self.K>0:
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

        self.centroids = []
        if self.options['km_init'].lower() == 'first':
            for index in range(0, self.K):
                self.centroids.append(self.X[index])

            # ==== per a que no siguin iguals ====
            # num_centroids = 0
            # index = 0
            # while num_centroids < self.K:
            #     pixel = self.X[index]
            #     if pixel not in self.centroids:
            #         self.centroids.append(pixel)
            #         num_centroids += 1
            #     index += 1

        elif self.options['km_init'].lower() == 'random':
            for n in range(0, self.K):
                index = np.random.randint(0, len(self.X))
                self.centroids.append(self.X[index])

            # ==== per a que no siguin iguals ====
            # num_centroids = 0
            # index = 0
            # while num_centroids < self.K:
            #     pixel = self.X[index]
            #     if pixel not in self.centroids:
            #         self.centroids.append(pixel)
            #         num_centroids += 1
            #     index = np.random.randint(0, self.X.__len__())

        
    def _cluster_points(self):  #TODO: no tinc clar que sigui aixi
        """@brief   Calculates the closest centroid of all points in X
        """

        distances = distance(self.X, self.centroids)
        for pixel_index in range(0, len(self.X)):
            self.clusters[pixel_index] = np.argmin(distances[pixel_index])

        
    def _get_centroids(self): #TODO: falta testejar
        """@brief   Calculates coordinates of centroids based on the coordinates 
                    of all the points assigned to the centroid
        """

        self.old_centroids = deepcopy(self.centroids)

        for cluster in range(0, self.K):
            cluster_pixels = []
            for pixel in range(0, len(self.X)):
                if self.clusters[pixel] == cluster:
                    cluster_pixels.append(self.X[pixel])
            if cluster_pixels:
                self.centroids[cluster] = np.mean(cluster_pixels, axis=0)
                

    def _converges(self):  #TODO: falta testejar
        """@brief   Checks if there is a difference between current and old centroids
        """

        converges = True
        for centroids in zip(self.centroids, self.old_centroids):
            if np.linalg.norm(centroids[0], centroids[1]) > self.options['tolerance']:
                converges = False
        return converges

        
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
           @return B is the best K found.
        """
#######################################################
##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
##  AND CHANGE FOR YOUR OWN CODE
#######################################################
        self._init_rest(4)
        self.run()        
        fit = self.fitting()
        return 4

        
    def fitting(self):
        """@brief  return a value describing how well the current kmeans fits the data
        """
#######################################################
##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
##  AND CHANGE FOR YOUR OWN CODE
#######################################################
        if self.options['fitting'].lower() == 'fisher':
            return np.random.rand(1)
        else:
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