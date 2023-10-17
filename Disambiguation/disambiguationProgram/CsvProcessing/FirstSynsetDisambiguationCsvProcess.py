import re
import pandas as pd
from CsvProcessing.CsvProcess import ChosenSynset, CsvProcessor
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

class FirstSynsetDisambiguationCsvProcessor(CsvProcessor):
    def processCSV(self, input, output, level = None):
        df = pd.read_csv(input)
        df['processedMessage'] = df['message'].apply(self._synsetPreprocessRow)
        df['processedMessage'] = df['processedMessage'].apply(lambda row: self._synsetFirstSynsetDisambiguationProcess(row, level))
        df.drop(columns='message', axis=1, inplace=True)
        df.to_csv(output, index=False)

    # Obtención de los synsets sustantivos válidos de una cadena de texto, separados en frases 
    def _synsetPreprocessRow(self, sentence):
        sentence = re.sub(r'\b(?:(?:https?|ftp)://|www\.)\S+\b',' ', sentence) 
        sentence = re.sub('[^a-zA-Z\s.]+', ' ', sentence)
        sentence = sentence.split(".")
        result_words = []
        for i in sentence:
            tokenizedSentence = word_tokenize(i)
            nounsSentence = self._ObtainNouns(tokenizedSentence)
            stop_words = set(stopwords.words('english'))
            filtered_words = [word for word in nounsSentence if word.lower() not in stop_words]
            result_words.append(filtered_words)
        return result_words
    
    def _synsetFirstSynsetDisambiguationProcess(self, sentence, level = None):
        resultSentence = self._disambiguateRowByFirstSynset(sentence)
        toretSentence = []
        if level != None:
            for i in resultSentence:
                if len(i.path) >= level:
                    toretSentence.append(i.path[level - 1].name())
                else:
                    toretSentence.append(i.path[len(i.path) - 1].name())
            return toretSentence
        return [synset.synset.name() for synset in resultSentence]
    
    def _disambiguateRowByFirstSynset(self, row):
        resultRow = []
        for i in row:
            resultRow.append(self._disambiguateSentenceByFirstSynset(i))
        toret = [synset for sublist in resultRow for synset in sublist]
        return toret
    
    #Obtención del primer synset de cada palabra
    def _disambiguateSentenceByFirstSynset(self, sentence):
        nouns = self._getNounsFromSentence(sentence)
        resultSentence = []
        for i in nouns:
            resultSentence.append(ChosenSynset(i[0],path=max(i[0].hypernym_paths(), key=len)))
        return resultSentence

    def _ObtainNouns(self, sentence):
        taggedSentence = pos_tag(sentence)
        nounsSentence = [word for word, tag in taggedSentence if tag == "NN" or tag == "NNS"]
        resultSentence = [word for word in nounsSentence if len(wn.synsets(word)) > 0]
        return resultSentence
    
    def _getNounsFromSentence(self, array):
        validSynset = []
        for i in array:
            tempNouns = wn.synsets(i)
            tempNouns = self._getNounsFromSynset(tempNouns)
            if len(tempNouns) > 0:
                validSynset.append(tempNouns)
        return validSynset

    def _getNounsFromSynset(self, array):
            verbPattern = r"\.n\."
            validSynset = []
            for i in array:
                name = i.name()
                if(re.search(verbPattern,name)):
                        validSynset.append(i)
            return validSynset