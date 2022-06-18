import json
import pickle
import csv
import numpy as np
import preprocessing
import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from random import shuffle
def scramble(sentence):
  split = sentence.split()  # Split the string into a list of words
  shuffle(split)  # This shuffles the list in-place.
  return ' '.join(split)  # Turn the list back into a string


def absoluteGEIndikator(stellenString, df):
  geIndex = 0
  count_ge_index= 0
  bubble_string=""
  #stellenString_list = stellenString.split(" ")
  for index, row in df.iterrows():
    cur_word = row['Begriff']
    #cur_word_lemma = tagger.analyze(cur_word)[0]
    times_cur_word = stellenString.count(cur_word)
    bubble_string += times_cur_word * (cur_word + " ")

    #if cur_word in stellenString and cur_word not in stellenString_list:
    #  print(cur_word)
    #  #find= re.findall( rf"{cur_word}.*?", stellenString)
    #  find = re.search(cur_word + '(.+)', stellenString)
    #  print(find)
    if cur_word in stellenString: #or cur_word_lemma in stellenString_list:
      count_ge_index += 1
    #print(cur_word, " appears ", times_cur_word, " times")
    cur_val = row['Assoziations-Score']
    geIndex +=  times_cur_word*cur_val

  #print(geIndex)
  return geIndex, count_ge_index, bubble_string

def individualGEIndikator(stellen, df):
  stellenGE=[]
  #for stelle in stellen:
  for index, row_stellen in stellen.iterrows():
    cur_stellen_GE=0
    for index, row_woerter in df.iterrows():
      cur_word = row_woerter['Begriff']
      #cur_word_lemma = tagger.analyze(cur_word)[0]
      #count_cur=stelle.count(cur_word)
      if cur_word in row_stellen[0]:
        cur_val = row_woerter['Assoziations-Score']
        cur_stellen_GE += cur_val
    stellenGE.append(cur_stellen_GE)
  return stellenGE







if __name__ == "__main__":
  beruf = "anlagenfuehrer"
  #file_name = 'extern/WAoeN/data/WAoeN.csv'
  # Load gruene Kompetenzen
  file_name_woerterbuch = 'extern/WAoeN/data/WAoeN_lemma.csv'
  green_words = pd.read_csv(file_name_woerterbuch, usecols=['Begriff', 'Assoziations-Score'])
  #
  #from HanTa import HanoverTagger as ht
  #tagger = ht.HanoverTagger('morphmodel_ger.pgz')
  filename_mechatroniker = 'data/mechatroniker/mechatroniker_1_100_pd.pkl'  # _pre
  filename_anlagenfuehrer = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pre.pkl'


  if beruf ==  "anlagenfuehrer":
    filepath_pd = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pre_pd.pkl'
    #filepath = filename_anlagenfuehrer
  elif beruf == "mechatroniker":
    filepath_pd = 'data/mechatroniker/mechatroniker_1_100_pre_pd.pkl'
  elif beruf == "metallbauer":
    filepath_pd = 'data/metallbauer/metallbauer_1_100_pre_pd.pkl'
  else:
    print("Invalid Job")


  df_pre = preprocessing.loadPandas(filepath_pd)
  #with open(filepath, 'rb') as f:
  #  stellen = pickle.load(f)

  longString = ""
  for index, row in df_pre.iterrows():
    longString += row[0]

  globalBool=True
  individualBool=True

  if globalBool:
    geIndex, count_ge_index, bubble_string = absoluteGEIndikator(longString, green_words)

    print("Anzahl der Stellen: ", len(df_pre.index))
    print("Absolute GE Index: ", geIndex)
    print("Mean GE Index: ", geIndex / len(df_pre.index))
    print(count_ge_index, "der 1800 Wörter wurden benutzt")
    print(bubble_string)
    with open("data/"+str(beruf)+"/bubble_string_"+str(beruf)+".txt", "w") as text_file:
      text_file.write(bubble_string)

    bubble_string_random = scramble(bubble_string)
    wordcloud = WordCloud(background_color="white", width=1920, height=1080).generate(bubble_string_random)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    path = "data/"+str(beruf) + "/" + str(beruf) + "_wordcloud.pdf"
    plt.savefig(path)




  if individualBool:

    print("Individual")
    stellenGE = individualGEIndikator(df_pre, green_words)
    #print(stellenGE)
    print("MEAN: ",np.mean(stellenGE))
    print("Median: ",np.median(stellenGE))
    print("Max: ",np.max(stellenGE))
    print("75 percentile: ",np.percentile(stellenGE, 75))
    print("90 percentile: ",np.percentile(stellenGE, 90))
    print("65 percentile: ",np.percentile(stellenGE, 65))



