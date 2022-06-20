import pandas as pd
import os
import pickle
import re  # For preprocessing
import nltk
#nltk.download('stopwords')
from HanTa import HanoverTagger as ht

def combinePickles(beruf):
    alle_stellen=[]
    files=['data/'+str(beruf)+'/'+str(beruf)+'_1_20_pre.pkl',
           'data/' + str(beruf)+'/'+str(beruf) + '_21_40_pre.pkl',
           'data/' + str(beruf)+'/'+str(beruf) + '_41_60_pre.pkl',
           'data/' + str(beruf)+'/'+str(beruf) + '_61_80_pre.pkl',
           'data/' + str(beruf)+'/'+str(beruf) + '_81_100_pre.pkl',
           ]
    print(files)
    for file in files:
        if os.path.exists(file):
            with open(file, 'rb') as f:
                 stellen = pickle.load(f)
            alle_stellen.extend(stellen)

    with open('data/' + str(beruf)+'/'+str(beruf) + '_1_100_pre.pkl', 'wb') as f:
        pickle.dump(alle_stellen, f)


def preprocessText(text, tagger, german_stop_words):
  pattern = r'[' + """!"#$%&'()*+,-./:;<=>?@[\]^_•`{|}~1234567890""" + ']'
  brief_cleaning = (re.sub(pattern, ' ', text))
  tokenized_sent = nltk.tokenize.word_tokenize(brief_cleaning, language='german')
  tags = tagger.tag_sent(tokenized_sent)

  pre_text = []
  for tag in tags:
    lemma = tag[1]
    if lemma not in german_stop_words:
      pre_text.append(lemma)

  return ' '.join(pre_text)


def preprocessDict(file_path):
  with open(file_path+'.pkl', 'rb') as f:
    stellen = pickle.load(f)
  tagger = ht.HanoverTagger('morphmodel_ger.pgz')
  german_stop_words = nltk.corpus.stopwords.words('german')
  new_dict=[]
  for stelle in stellen:
    pre_stelle = preprocessText(stelle, tagger, german_stop_words)
    new_dict.append(pre_stelle)
  with open(file_path+'_pre.pkl', 'wb') as f:
    pickle.dump(new_dict, f)
  return new_dict


def pickleToPandas(filepath):
  with open(filepath+".pkl", 'rb') as f:
    stellen = pickle.load(f)
  df = pd.DataFrame.from_dict(stellen)
  df.to_pickle(filepath+"_pd.pkl")



def loadPandas(filepath):
  df = pd.read_pickle(filepath)
  return df




if __name__ == "__main__":

  #text ="Hallo das sind viele Beispiele"
  filepath = 'data/metallbauer/metallbauer_1_20'
  filepath2 = 'data/metallbauer/metallbauer_21_40'
  filepath3 = 'data/metallbauer/metallbauer_41_60'
  filepath4 = 'data/metallbauer/metallbauer_61_80'
  filepath5 = 'data/metallbauer/metallbauer_81_100'
  #
  #pre_stellen = preprocessDict(filepath)
  #pre_stellen = preprocessDict(filepath2)
  #pre_stellen = preprocessDict(filepath3)
  #pre_stellen = preprocessDict(filepath4)
  #pre_stellen = preprocessDict(filepath5)
  #combinePickles("metallbauer")


  filename_mechatroniker = 'data/mechatroniker/mechatroniker_1_100_pre'
  filename_anlagenfuehrer = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pre'
  filename_metallbauer = 'data/metallbauer/metallbauer_1_100_pre'
  #combinePickles("mechatroniker")
  pickleToPandas(filename_metallbauer)
