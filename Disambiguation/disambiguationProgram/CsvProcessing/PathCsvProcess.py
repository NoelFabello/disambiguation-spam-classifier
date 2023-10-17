import re
import pandas as pd
from CsvProcessing.CsvProcess import ChosenSynset, CsvProcessor
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

class PathCsvProcessor(CsvProcessor):
    def processCSV(self, input, output, level = None):
        df = pd.read_csv(input)
        df['processedMessage'] = df['message'].apply(self._synsetPreprocessRow)
        df['processedMessage'] = df['processedMessage'].apply(lambda row: self._PathProcessDisambiguation(row, level))
        df.drop(columns='message', axis=1, inplace=True)
        df.to_csv(output, index=False)
    
    #Obtención de los synsets sustantivos válidos de una cadena de texto
    def _synsetPreprocessRow(self, sentence):
        sentence = re.sub(r'\b(?:(?:https?|ftp)://|www\.)\S+\b',' ', sentence) 
        sentence = re.sub('[^a-zA-Z\s.]+', ' ', sentence)
        tokenizedSentence = word_tokenize(sentence)
        nounsSentence = self._ObtainNouns(tokenizedSentence)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in nounsSentence if word.lower() not in stop_words]
        return filtered_words
    
    def _PathProcessDisambiguation(self, sentence, level=None):
        resultSentence = self._disambiguateRowBySimilarPath(sentence)
        toretSentence = []
        if level != None:
            for i in resultSentence:
                if len(i.path) >= level:
                    toretSentence.append(i.path[level - 1].name())
                else:
                    toretSentence.append(i.path[len(i.path) - 1].name())
            return toretSentence
        return [synset.synset.name() for synset in resultSentence]
    
    def _disambiguateRowBySimilarPath(self, row):
        nouns = self._getNounsFromSentence(row)
        resultSentence = []
        for i in range(len(nouns)):
            previousSynset = ChosenSynset(distance=0)
            nextSynset = ChosenSynset(distance=0)
            chosenSynset = ChosenSynset(distance=0)
            if len(nouns) > 1:
                if i >= 1:
                    previousSynset = self._getSimilarPath(nouns[i], nouns[i-1])
                if i < (len(nouns) - 1):
                    nextSynset = self._getSimilarPath(nouns[i], nouns[i+1])
            else:
                try:
                    nextSynset = ChosenSynset(nouns[i][0], path=max(nouns[i][0].hypernym_paths(), key=len), distance=1)
                except Exception:
                    nextSynset = ChosenSynset(nouns[i][0], path=[])
            for synset in [previousSynset,nextSynset]:
                if synset.distance > chosenSynset.distance:
                    chosenSynset = synset
            if chosenSynset.synset is not None:
                resultSentence.append(chosenSynset)
        return resultSentence
    
    # Obtiene el synset de synArray com más similitud a una acepción de comparedSynArray
    def _getSimilarPath(self, synArray, comparedSynArray):
        result = ChosenSynset(distance=0)
        for i in synArray:
            for j in comparedSynArray:
                distance = i.path_similarity(j)
                if distance > result.distance:
                    result.synset = i
                    result.distance = distance
                    result.comparedWord = j
                    result.path = max(i.hypernym_paths(), key=len)
        return result
    
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
    