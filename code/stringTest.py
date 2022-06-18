import spacy
import nltk
from HanTa import HanoverTagger as ht
tagger = ht.HanoverTagger('morphmodel_ger.pgz')


test = ["Wärmetauscher","Wärmetausch"]
test2=" konsequent technisch Weiterentwicklung Unternehmen Spitze Marktsegment PP Technologie bringen "

sent="Wärmetauscher Wärmepumpen Windräder"

#sentences = nltk.sent_tokenize(sent,language='german')

tokenized_sent = nltk.tokenize.word_tokenize(sent,language='german')
print("Wärmetausch" in test)
print(test.count("Wärmetausch"))

tags = tagger.tag_sent(tokenized_sent)
for tag in tags:
  lemma = tag[1]
  print(lemma)


#for word in test2.split(" "):
#  cur_word = word.lower()
#  print(cur_word)
#  cur_word_lemma = tagger.analyze(cur_word)[0]
#  print(cur_word_lemma)

