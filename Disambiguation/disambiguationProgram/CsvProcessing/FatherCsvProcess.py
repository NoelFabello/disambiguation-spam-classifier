import re
import pandas as pd
from CsvProcessing.CsvProcess import ChosenSynset, CsvProcessor
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


class FatherCsvProcessor(CsvProcessor):
    def processCSV(self, input, output, level = None):
        df = pd.read_csv(input)
        df['processedMessage'] = df['message'].apply(self._synsetPreprocessRow)
        df['processedMessage'] = df['processedMessage'].apply(lambda row: self._FatherProcessDisambiguation(row, level))
        df.drop(columns='message', axis=1, inplace=True)
        df.to_csv(output, index=False)
    
    #Obtención de los synsets sustantivos válidos de una cadena de texto, separados en frases
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
    
    #Se aplica la desambiguación por hiperónimos y la selección de granularidad
    def _FatherProcessDisambiguation(self, sentence, level = None):
        resultSentence = self._disambiguateRowByClosestFather(sentence)
        toretSentence = []
        if level != None:
            for i in resultSentence:
                if len(i.path) >= level:
                    toretSentence.append(i.path[level - 1].name())
                else:
                    toretSentence.append(i.path[len(i.path) - 1].name())
            return toretSentence
        return [synset.synset.name() for synset in resultSentence]
    
    def _disambiguateRowByClosestFather(self, row):
        resultRow = []
        for i in row:
            resultRow.append(self._disambiguateSentenceByClosestFather(i))
        toret = [synset for sublist in resultRow for synset in sublist]
        return toret
    
    def _disambiguateSentenceByClosestFather(self, sentence):
        result = []
        nouns = self._getNounsFromSentence(sentence)
        for i in range(len(nouns)):
            nextSynset = ChosenSynset()
            previousSynset = ChosenSynset()
            chosenSynset = ChosenSynset()
            if len(nouns) > 1:
                if i < (len(nouns) - 1):
                    nextSynset = self._getClosestSynsetByClosestFather(nouns[i], nouns[i+1])
                if i >= 1:
                    previousSynset = self._getClosestSynsetByClosestFather(nouns[i], nouns[i-1])
            else:
                try:
                    nextSynset = ChosenSynset(nouns[i][0], path=max(nouns[i][0].hypernym_paths(), key=len), distance=1)
                except Exception:
                    nextSynset = ChosenSynset(nouns[i][0], path=[])
            chosenSynset = sorted([previousSynset, nextSynset], key= lambda x: x.distance)[0]
            if chosenSynset.synset is not None:
                result.append(chosenSynset)
        return result
    
    # Encuentra los hiperónimos más cercanos y devuelve la acepción de synsetList, que más cerca esté a una de comparedSynsetList
    def _getClosestSynsetByClosestFather(self, synsetList, comparedSynsetList):
        closestSynset = ChosenSynset()
        
        for i in synsetList:
            for j in comparedSynsetList:
                common_hypernyms = i.lowest_common_hypernyms(j)
                if len(common_hypernyms) >=1:
                    closestFather = common_hypernyms[0]
                else:
                    closestFather = i.lowest_common_hypernyms(i)[0]
                distance = i.shortest_path_distance(closestFather)
                if distance < closestSynset.distance:
                    closestSynset = ChosenSynset(synset=i, distance=distance, path=max(i.hypernym_paths(), key=len), comparedWord=j)
        return closestSynset
    
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
    