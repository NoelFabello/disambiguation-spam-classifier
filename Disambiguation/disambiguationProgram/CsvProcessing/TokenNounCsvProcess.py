import re
import pandas as pd
from CsvProcessing.CsvProcess import ChosenSynset, CsvProcessor
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

class TokenNounCsvProcess(CsvProcessor):
    def processCSV(self, csv, output, level = None):
        df = pd.read_csv(csv)
        df['processedMessage'] = df['message'].apply(self._preprocessRow)
        df.drop(columns='message', axis=1, inplace=True)
        df.to_csv(output, index=False)
        
    # Obtención de sustantivos
    def _preprocessRow(self, sentence):
        sentence = re.sub(r'\b(?:(?:https?|ftp)://|www\.)\S+\b',' ', sentence) 
        sentence = re.sub('[^a-zA-Z\s]+', ' ', sentence)
        stop_words = set(stopwords.words('english'))
        tokenizedSentence = word_tokenize(sentence)
        nounSentence = self._ObtainNouns(tokenizedSentence)
        filtered_words = [word.lower() for word in nounSentence if word.lower() not in stop_words]
        resultSentence = [word for word in filtered_words if len(word) > 1]
        return resultSentence
    
    def _ObtainNouns(self, sentence):
        taggedSentence = pos_tag(sentence)
        nounsSentence = [word for word, tag in taggedSentence if tag == "NN" or tag == "NNS"]
        return [word for word in nounsSentence if len(wn.synsets(word)) > 0]
