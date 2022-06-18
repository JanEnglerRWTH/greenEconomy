import gensim
import pandas as pd
from sklearn.cluster import KMeans
from nltk.cluster import KMeansClusterer
from sklearn import cluster
import nltk
import numpy as np
from sklearn import cluster

from gensim.models import Word2Vec
from nltk.cluster import KMeansClusterer
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling

modelDir = 'models/'
#os.chdir(modelDir)
from gensim.models import word2vec
#model = gensim.models.KeyedVectors.load_word2vec_format("models/german.model", binary=True)

file_name='data/mechatroniker/bubble_string_mechatroniker.txt'
with open(file_name, 'r') as file:
  data = file.read()
#print(data)
boolProcess = False


def word_count(str):
  counts = dict()
  counts2=[]
  words = str.split()

  for word in words:
    if word in counts:
      counts[word] += 1
    else:
      counts[word] = 1
  for key, value in counts.items():
    if value > 10:
      #print(key)
      counts2.append(key)
  return counts, counts2

counts, frequent_words = word_count(data)

words = data.split()
words = frequent_words
#print (" ".join(sorted(set(words), key=words.index)))
green_words = sorted(set(words), key=words.index)
#print(green_words)
model = gensim.models.KeyedVectors.load_word2vec_format("models/german.model", binary=True)
in_vocab=[]
not_in_vocab=[]
data_embeddings=[]
for green_word in green_words:
  if green_word in list(model.index_to_key):
    data_embeddings.append(model[green_word])
    in_vocab.append(green_word)
  else:
    not_in_vocab.append(green_word)


def kMeans(data, k):


  clusters_number = k
  kclusterer = KMeansClusterer(clusters_number, distance=nltk.cluster.util.cosine_distance, repeats=50)

  assigned_clusters = kclusterer.cluster(data, assign_clusters=True)

  #words = list(model.index_to_key)
  cluster_words = {}
  cluster_values = {}
  for i, word in enumerate(in_vocab):
    if assigned_clusters[i] in cluster_words.keys():
      cluster_words[assigned_clusters[i]].append(word)
      cluster_values[assigned_clusters[i]].append(data[i])
    else:
      cluster_words[assigned_clusters[i]] = [word]
      cluster_values[assigned_clusters[i]] = [data[i]]

  for key, value in cluster_words.items():
    print("Cluster: ", key)
    print(value)
    #print(cluster_values[key])
    mean_vec = np.mean(cluster_values[key], axis = 0)
    #print(mean_vec)
    close_words = model.most_similar([mean_vec])
    print(close_words)
    print()



  sklearnBool=False
  if sklearnBool:

    kmeans = cluster.KMeans(n_clusters=clusters_number)
    kmeans.fit(data)

    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    for i, word in enumerate(in_vocab):
      print(word + ":" + str(labels[i]))
      if labels[i] in clusters2.keys():
        clusters2[labels[i]].append(word)
      else:
        clusters2[labels[i]] = [word]
    for key, value in clusters2.items():
      print("Cluster: ", key)
      print(value)




kMeans(data_embeddings, 6)

#print(green_words)

#print(word_count(data))

