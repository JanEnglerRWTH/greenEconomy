import json
import pickle
import csv
import numpy as np
import preprocessing
import pandas as pd

# import these modules

file_name='extern/WAoeN/data/WAoeN.csv'
file_name_new='extern/WAoeN/data/WAoeN_lemma.csv'
df=pd.read_csv(file_name_new, usecols= ['Begriff','Assoziations-Score'])
from HanTa import HanoverTagger as ht
tagger = ht.HanoverTagger('morphmodel_ger.pgz')
print(df)





from random import shuffle

def scramble(sentence):
   split = sentence.split()  # Split the string into a list of words
   shuffle(split)  # This shuffles the list in-place.
   return ' '.join(split)  # Turn the list back into a string

def individualGEIndikator(stellen, df):
  stellenGE=[]
  for stelle in stellen:
    cur_stellen_GE=0
    for index, row in df.iterrows():
      cur_word = row['Begriff']
      #cur_word_lemma = tagger.analyze(cur_word)[0]
      if cur_word in stelle:
        cur_val = row['Assoziations-Score']
        cur_stellen_GE += cur_val
    stellenGE.append(cur_stellen_GE)
  return stellenGE

def absoluteGEIndikator(stellenString, df):
  geIndex = 0
  count_ge_index= 0
  bubble_string=""
  stellenString_list = stellenString.split(" ")
  for index, row in df.iterrows():
    cur_word = row['Begriff']
    cur_word_lemma = tagger.analyze(cur_word)[0]
    times_cur_word = stellenString_list.count(cur_word_lemma)
    bubble_string += times_cur_word * (cur_word + " ")

    if cur_word != cur_word_lemma and cur_word in stellenString_list and cur_word not in df["Begriff"]:
      times_cur_word = stellenString_list.count(cur_word)
      bubble_string += times_cur_word * (cur_word + " ")

    if cur_word in stellenString_list or cur_word_lemma in stellenString_list:
      count_ge_index += 1
    #print(cur_word, " appears ", times_cur_word, " times")
    cur_val = row['Assoziations-Score']
    geIndex +=  times_cur_word*cur_val

  print(geIndex)
  return geIndex, count_ge_index, bubble_string


filepath = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pre.pkl'
filename_anlagenfuehrer = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pre_pd.pkl'
filename_mechatroniker = 'data/mechatroniker/mechatroniker_1_100_pd.pkl' #_pre
df_pre = preprocessing.loadPandas(filename_anlagenfuehrer)
with open(filepath, 'rb') as f:
  stellen = pickle.load(f)
print(df_pre[0][0])
longString = ""
print("Hier")
for index, row in df_pre.iterrows():
  longString += row[0]

#print(longString)


invAnalyse=True
if invAnalyse:
  stellenGE=individualGEIndikator(stellen, df)
  print(stellenGE)
  print(np.mean(stellenGE))
  print(np.median(stellenGE))
  print(np.max(stellenGE))
  print(np.percentile(stellenGE, 75))
  print(np.percentile(stellenGE, 90))
  print(np.percentile(stellenGE, 65))

geAlanyse= False
if geAlanyse:

  geIndex, count_ge_index, bubble_string = absoluteGEIndikator(longString, df)

  print("Anzahl der Stellen: ", len(df_pre.index))
  print("Absolute GE Index: ", geIndex)
  print("Mean GE Index: ", geIndex / len(df_pre.index))
  print(count_ge_index, "der 1800 Wörter wurden benutzt")
  #print(bubble_string)
  with open("longString_mechatroniker.txt", "w") as text_file:
    text_file.write(longString)

  boolWordcloud=False
  if boolWordcloud:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    bubble_string_random= scramble(bubble_string)
    wordcloud = WordCloud(background_color="white",width=1920, height=1080).generate(bubble_string_random)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('anlagenfuehrer.pdf')
    #plt.show()


testBool=False




if testBool:





  print(u'f\u00fcr'.encode("utf-8"))

  # Text definieren
  s_iso88591 = u'f\u00fcr'

  # Text nach Unicode umwandeln
  s_unicode = s_iso88591.encode("iso-8859-1")

  # Text nach UTF-8 umwandeln
  s_utf8 = s_iso88591.encode("utf-8")

  print(s_iso88591)
  print(s_unicode)
  print(s_utf8)