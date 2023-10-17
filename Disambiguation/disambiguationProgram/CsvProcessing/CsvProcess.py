from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import warnings
from sklearn.feature_extraction.text import CountVectorizer

class CsvProcessor(ABC):
    @abstractmethod
    def processCSV(self, input, output, level = None):
        pass
        
    # Creación de la matriz documentos-términos
    def createBinary(self, input, output):
        df = pd.read_csv(input)
        doc = df['processedMessage'].apply(lambda row: ' '.join([palabra.replace('.', '_') for palabra in eval(row)])).tolist()
        vectorizador = CountVectorizer(binary=True)
        matriz_termino_documento = vectorizador.fit_transform(doc)
        terms = vectorizador.get_feature_names_out()
        df_resultado = pd.DataFrame(matriz_termino_documento.toarray(), columns=terms)
        toret_df = pd.concat([df['mailType'], df_resultado], axis=1)
        toret_df.to_csv(output, index=False)

# Estructura de datos utilizada por las clases hijo      
class ChosenSynset:
    def __init__(self, synset=None, distance=10000, path=None, comparedWord = None):
        self.synset = synset
        self.distance = distance
        self.path = path
        self.comparedWord = comparedWord