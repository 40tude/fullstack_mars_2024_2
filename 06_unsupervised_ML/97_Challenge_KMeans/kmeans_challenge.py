

import numpy as np
import pandas as pd

import random
from numpy.random import uniform
import math
from numpy import linalg as la



class My_KMeans():
  """kMeans simple implemantation"""

  def __init__(self, n_clusters=2, random_state='None', n_init="auto", n_iter="100"):
    self.n_clusters_    = n_clusters
    self.random_state_  = random_state
    self.n_init_        = n_init 
    self.n_iter_        = n_iter

    random.seed(self.random_state_)
    
  

  # X est un ensemble de 'nb lignes' points qui ont chacun 'nb colonnes' dimensions 

  # Algo : 
  # Utiliser random_state pour la répétabilité (voir constructeur)
  # Trouver les min et max sur chaque dimension
  # Placer k centroides dans le "cadre" à n dim MAIS pas trop rapprochés
  # Calculer la distance entre 1 centroide et tous les points
  # Associer chaque point au centroide le plus proche
  # Deplacer chaque centroide en le mettant au milieu des points qui lui sont tattachés
  # Boucle jusqu'à nb_iter atteint ou move<epsilon
  def fit(self, X):
    
    _, nb_dim = X.shape
    self.centroids_ = np.empty((self.n_clusters_, nb_dim))
    print(self.centroids_.shape)

    # Trouver les min et max sur chaque dimension (colonne)
    # min contient les min des colonnes (idem pour max)
    min = np.min(X, axis=0)
    max = np.max(X, axis=0)

    # Placer k centroides dans le "cadre" à n dim MAIS pas trop rapprochés
    # Pour l'instant, on va pas tester si ils sont trop rapprochés
    # La ligen ci-desous c'est la version vectorisée de bob = random(min, max)
    self.centroids_ = [uniform(min, max) for i in range(self.n_clusters_)]
    
    for k in range(self.n_clusters_):
      print(self.centroids_)

    
    # Calculer la distance entre 1 centroide et tous les points
    for x in X:
      for k in self.centroids_:
      d = la.norm(x, k)
    

    # https://towardsdatascience.com/create-your-own-k-means-clustering-algorithm-in-python-d7d4c9077670

    return self





X = np.array([  [-100,  -50,  -10],
                [  50,   70,  100],
                [ 200,  250,  300],
                [ 500,  750,  999],
              ])

print(X[2])

kmeans2 = My_KMeans(n_clusters=2, random_state=0, n_init="auto")
kmeans2.fit(X)













# from sklearn.datasets import load_iris
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans
# X, _ = load_iris(return_X_y=True, as_frame=True)
# X.head()


# sc = StandardScaler()
# X = sc.fit_transform(X)
# print (X.shape)
# X[:5]

# kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto")
# kmeans.fit(X)

# kmeans.cluster_centers_



