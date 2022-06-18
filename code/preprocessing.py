import gensim
import pandas as pd
import os
import pickle
import re  # For preprocessing
#import spacy
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


def preprocessPandas(filename):
  df = loadPandas(str(filename)+'.pkl')
  nlp = spacy.load("de_core_news_sm", disable=['ner', 'parser'])

  def cleaning(doc):
    # Lemmatizes and removes stopwords
    # doc needs to be a spacy Doc object
    txt = [token.lemma_ for token in doc if not token.is_stop] #.lower()
    # Word2Vec uses context words to learn the vector representation of a target word,
    # if a sentence is only one or two words long,
    # the benefit for the training is very small
    if len(txt) > 2:
      return ' '.join(txt)

  pattern = r'[' + """!"#$%&'()*+,-./:;<=>?@[\]•^_`{|}~1234567890""" + ']'
  brief_cleaning = (re.sub(pattern, ' ', row) for row in df[0]) #re.sub("[^A-Za-z']+", ' ', str(row))

  txt = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=500)]

  df_pre = pd.DataFrame(txt)
  df_pre = df_pre.dropna().drop_duplicates()
  print(df_pre.shape)
  file_name = str(filename)+'_pre.pkl'
  df_pre.to_pickle(file_name)
  return df_pre


def loadPandas(filepath):
  df = pd.read_pickle(filepath)
  #print(df[0][0])
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
  #print(pre_stellen)
  #filepath='data/anlagenfuehrer/anlagenfuehrer_1_100_pd.pkl'
  #filepath = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pd_pre.pkl'
  filename_mechatroniker = 'data/mechatroniker/mechatroniker_1_100_pre'
  filename_anlagenfuehrer = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pre_pd.pkl'
  filename_metallbauer = 'data/metallbauer/metallbauer_1_100_pre'
  #combinePickles("mechatroniker")
  pickleToPandas(filename_metallbauer)
  #df = loadPandas(str(filename_mechatroniker)+".pkl")
  #print(df[0][0])

  #df_pre = preprocessPandas(filename_mechatroniker)
  #filepath = 'data/anlagenfuehrer/anlagenfuehrer_1_100_pd_pre.pkl'
  #df_pre = loadPandas(str(filename_mechatroniker)+"_pre.pkl")
  #print(df_pre[0][0])
  #filename_mechatroniker = 'data/mechatroniker/mechatroniker_1_100_pd_pre.pkl'