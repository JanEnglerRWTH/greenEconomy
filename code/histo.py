import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
with open('data/metallbauer/ge_absolut.pkl', 'rb') as f:
  ge_absolut_metallbauer = pickle.load(f)
with open('data/anlagenfuehrer/ge_absolut_anlagenfuehrer.pkl', 'rb') as f:
  ge_absolut_anlagenfuehrer = pickle.load(f)
with open('data/mechatroniker/ge_absolut.pkl', 'rb') as f:
  ge_absolut_mechatroniker = pickle.load(f)

print(ge_absolut_metallbauer)

def print_histo():

  _ = plt.hist(ge_absolut_metallbauer, bins=np.arange(0.5, 15.5, 1),label="Metallbauer/in", density=True,alpha =1)  # arguments are passed to np.histogram
  _ = plt.hist(ge_absolut_anlagenfuehrer, bins=np.arange(0, 15, 1),label="Maschinen- und Anlagenführer/in", density=True,alpha =1)  # arguments are passed to np.histogram
  _ = plt.hist(ge_absolut_mechatroniker, bins=np.arange(-0.5, 14.5, 1),label="Mechatroniker/in", density=True,alpha =1)  # arguments are passed to np.histogram

  plt.xticks(np.arange(0, 15, 1))
  plt.legend()
  plt.title("Histogram with 'auto' bins")

  plt.show()#

def print_bar(x_metall, x_anlage, x_mechga):
  fig = plt.figure()
  ax = fig.add_subplot(111)
  x_axis = np.arange(0, 10, 1)
  ax.bar(x_axis + 0.00, x_mechga, color='b', width=0.25)
  ax.bar(x_axis + 0.25, x_anlage, color='g', width=0.25)
  ax.bar(x_axis + 0.50, x_metall, color='r', width=0.25)

  ax.set_ylabel('Prozent')
  ax.set_xlabel('Anzahl Green Words')
  #ax.set_title('Anteil der Stellen mit x Green Words')
  ax.set_xticks(np.arange(0, 10, 1))
  ax.set_yticks(np.arange(0, 66, 5))
  ax.legend(labels=['Mechatroniker/in', 'Maschinen- und Anlagenführer/in', "Metallbauer/in"])
  #ax = plt.gca()
  #plt.axis('on')
  #plt.show()
  plt.savefig('absolut_ge.png')
  plt.savefig('absolut_ge.pdf')


x_metall=[]
len_list= len(ge_absolut_metallbauer)
for num in range(0,10):
  count = ge_absolut_metallbauer.count(num)
  nurm_count=count/len_list *100
  x_metall.append(nurm_count)
  print(nurm_count)

x_anlage=[]
len_list= len(ge_absolut_anlagenfuehrer)
for num in range(0,10):
  count = ge_absolut_anlagenfuehrer.count(num)
  nurm_count=count/len_list *100
  x_anlage.append(nurm_count)
  print(nurm_count)
x_mechga = []
len_list = len(ge_absolut_mechatroniker)
for num in range(0, 10):
  count = ge_absolut_mechatroniker.count(num)
  nurm_count = count / len_list *100
  x_mechga.append(nurm_count)
  print(nurm_count)
print(x_mechga)
print_bar(x_metall,x_anlage,x_mechga)