
import numpy as np
import preprocessing
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from random import shuffle

def scramble(sentence):
  #not mine!
  split = sentence.split()  # Split the string into a list of words
  shuffle(split)  # This shuffles the list in-place.
  return ' '.join(split)  # Turn the list back into a string


def absoluteGEIndikator(stellenString, df):
  geIndex = 0
  count_ge_index= 0
  bubble_string=""

  for index, row in df.iterrows():
    cur_word = row['Begriff']
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
  absoluteGE=[]
  #for stelle in stellen:
  for index, row_stellen in stellen.iterrows():
    cur_stellen_GE=0
    cur_stelle_absolut=0
    for index, row_woerter in df.iterrows():
      cur_word = row_woerter['Begriff']
      #cur_word_lemma = tagger.analyze(cur_word)[0]
      #count_cur=stelle.count(cur_word)
      if cur_word in row_stellen[0]:
        cur_val = row_woerter['Assoziations-Score']
        cur_stellen_GE += cur_val
        cur_stelle_absolut+=1
    stellenGE.append(cur_stellen_GE)
    absoluteGE.append(cur_stelle_absolut)
  return stellenGE, absoluteGE







if __name__ == "__main__":
  beruf = "metallbauer"
  # Load gruene Kompetenzen
  file_name_woerterbuch = 'extern/WAoeN/data/WAoeN_lemma.csv'
  green_words = pd.read_csv(file_name_woerterbuch, usecols=['Begriff', 'Assoziations-Score'])

  filename_mechatroniker = 'data/mechatroniker/mechatroniker_1_100_pd.pkl'  # _pre
  filename_anlagenfuehrer = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pre.pkl'


  if beruf ==  "anlagenfuehrer":
    filepath_pd = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pre_pd.pkl'
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
  individualBool=False

  if globalBool:
    geIndex, count_ge_index, bubble_string = absoluteGEIndikator(longString, green_words)

    print("Anzahl der Stellen: ", len(df_pre.index))
    print("Absolute GE Index: ", geIndex)
    print("Mean GE Index: ", geIndex / len(df_pre.index))
    print(count_ge_index, "der 1800 Wörter wurden benutzt")
    print(bubble_string)
    with open("data/"+str(beruf)+"/bubble_string_"+str(beruf)+".txt", "w") as text_file:
      text_file.write(bubble_string)
    round=False
    mask=None
    path = "data/" + str(beruf) + "/" + str(beruf) + "_wordcloud.png"
    if round:
      x, y = np.ogrid[:1000, :1000]

      mask = (x - 500) ** 2 + (y - 500) ** 2 > 400 ** 2
      mask = 255 * mask.astype(int)
      path = "data/" + str(beruf) + "/" + str(beruf) + "_wordcloud_round.png"
      #wordcloud = WordCloud(background_color="white", width=1920, height=1080, mask=mask).generate(text)
    bubble_string_random = scramble(bubble_string)
    wordcloud = WordCloud(background_color="white", width=1920, height=1080,mask=mask,max_words=100).generate(bubble_string_random)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    #path = "data/"+str(beruf) + "/" + str(beruf) + "_wordcloud_round.png"
    plt.savefig(path)




  if individualBool:

    print("Individual")
    stellenGE,absoluteGE = individualGEIndikator(df_pre, green_words)
    #print(stellenGE)
    print("MEAN: ",np.mean(stellenGE))
    print("Median: ",np.median(stellenGE))
    print("Max: ",np.max(stellenGE))
    print("75 percentile: ",np.percentile(stellenGE, 75))
    print("90 percentile: ",np.percentile(stellenGE, 90))
    print("65 percentile: ",np.percentile(stellenGE, 65))

    print("MEAN abs: ", np.mean(absoluteGE))
    print("Median abs: ", np.median(absoluteGE))
    print("Max abs: ", np.max(absoluteGE))
    print("75 percentile: ", np.percentile(absoluteGE, 75))
    print("90 percentile: ", np.percentile(absoluteGE, 90))
    print("65 percentile: ", np.percentile(absoluteGE, 65))

    ones=0
    twos=0
    threes=0
    for stelle_abs in absoluteGE:
      if stelle_abs > 2:
        threes +=1
      if stelle_abs > 1:
        twos += 1
      if stelle_abs > 0:
        ones += 1
    print("Ones: ", ones)
    print("Twos: ", twos)
    print("Threes: ", threes)
    print("Overall: ", len(absoluteGE))

  #with open('data/metallbauer/ge_absolut.pkl', 'wb') as f:
  #  pickle.dump(absoluteGE, f)
  #with open('data/metallbauer/ge_weighted.pkl', 'wb') as f:
  #  pickle.dump(stellenGE, f)


