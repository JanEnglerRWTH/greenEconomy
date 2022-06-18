import pandas as pd
from HanTa import HanoverTagger as ht
import pickle
tagger = ht.HanoverTagger('morphmodel_ger.pgz')

file_name='extern/WAoeN/data/WAoeN.csv'
df=pd.read_csv(file_name, usecols= ['Begriff','Assoziations-Score'])
print(df['Begriff'].head(20))

df['Begriff'] = df['Begriff'].apply(tagger.analyze2)
df = df.drop_duplicates(subset=['Begriff'])
file_name_new='extern/WAoeN/data/WAoeN_lemma.csv'
#df.to_pickle(file_name_new)
df.to_csv(file_name_new,index=False)
#print(df)