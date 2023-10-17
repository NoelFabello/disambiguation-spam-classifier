from CsvProcessing.FatherCsvProcess import FatherCsvProcessor
from CsvProcessing.PathCsvProcess import PathCsvProcessor
from CsvProcessing.TokenNounCsvProcess import TokenNounCsvProcess
from CsvProcessing.FirstSynsetDisambiguationCsvProcess import FirstSynsetDisambiguationCsvProcessor
from Model.Model import ModelManager
import webview
import os
from nltk.corpus import wordnet as wn


# Clase con la que se comunica la aplicación de angular
class Api:
    def __init__(self):
        self.windows = None
        self.model = None
        self.preprocessing = False
        self.lastPreprocessed = None

    def obtainFile(self):
        response = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG, directory='../')
        
        return response[0] if response else None
    
    def preProcess(self, method, file, level, outputFile, outputBinaryTableFile):
        if not outputFile.endswith(".csv"):
            outputFile += ".csv"
        if not outputBinaryTableFile.endswith(".csv"):
            outputBinaryTableFile += ".csv"
        if self.preprocessing:
            return {'error': True, 'message' : 'Ya existe un preprocesamiento en curso.', 'code' : 1}
        
        self.preprocessing = True
        try:
            if not os.path.exists(file):
                raise FileNotFoundError(f"El archivo '{file}' no existe.")
            
            outputFile = '../outputs/preprocessedFiles/' + outputFile
            outputBinaryTableFile = '../outputs/trainMatrix/' + outputBinaryTableFile
            
            if method == 'father':
                processor = FatherCsvProcessor()
            elif method == 'first-synset':
                processor = FirstSynsetDisambiguationCsvProcessor()
            elif method == 'tokenize':
                processor = TokenNounCsvProcess()
            elif method == 'path':
                processor = PathCsvProcessor()
                
            try:
                level = int(level)
            except Exception:
                level = 0
                
            if level < 1:
                level = None
                
            processor.processCSV(file, outputFile, level=level)
            
            processor.createBinary(outputFile, outputBinaryTableFile)
            
            if isinstance(processor, TokenNounCsvProcess) and level is not None and level > 0:
                ig = ModelManager('')
                ig.selectMostImportantFeaturesIG(outputBinaryTableFile, outputBinaryTableFile, num_features=level)

            self.lastPreprocessed = outputBinaryTableFile
            
            result =  {'error' : False, 'message': ''}
        except Exception as e:
            print('Error: ', str(e))
            result =  {'error': True, 'message' : str(e), 'code' : 0}
        finally:
            self.preprocessing = False
        
        return result
    
    def cargarModelo(self, file):
        try:
            if not os.path.exists(file):
                raise FileNotFoundError(f"El archivo '{file}' no existe.")
            self.model = ModelManager('')
            self.model.load_model(file)
            return {'error' : False, 'message' : ''}
        except Exception as e:
            print('Error: ', str(e))
            return {'error' : True, 'message' : str(e)}

    def guardarModelo(self, outputName):
        if not outputName.endswith(".pkl"):
            outputName += ".pkl"
        try:
            self.model.save_model(outputName)
            return {'error' : False, 'message' : ''}
        except Exception as e:
            print('Error: ', str(e))
            return {'error' : True, 'message' : str(e)}
        
    def train(self, file, modelName, trainRate, cv):
        try:
            if not os.path.exists(file):
                raise FileNotFoundError(f"El archivo '{file}' no existe.")
            try:
                trainRate = int(trainRate)
            except ValueError:
                trainRate = 75
            try:
                cv = int(cv)
            except ValueError:
                cv = 10
            
            model = ModelManager(modelName)
            model.train(file, test_size=1-(float(trainRate)/100), cv=int(cv))
            self.model = model
            return {'error' : False, 'message' : ''}
        except Exception as e:
            print('Error: ', str(e))
            return {'error' : True, 'message' : str(e)}
        
    def evaluate(self, outputName):
        try:
            toret = self.model.evaluate(show=False, outputName=outputName)
            toretDict = {
                'exactitud' : toret[0],
                'precision' : toret[1],
                'recall' : toret[2],
                'f1' : toret[3],
                'tcr1' : toret[4],
                'tcr9' : toret[5],
                'tcr999' : toret[6]
            }
            return {'error': False, 'message': toretDict}
        except Exception as e:
            print('Error: ', str(e))
            return {'error' : True, 'message' : str(e)}
        
    def evaluateFile(self, csv, test_size, outputName):
        try:
            if not os.path.exists(csv):
                raise FileNotFoundError(f"El archivo '{csv}' no existe.")
            try:
                test_size = int(test_size)
            except ValueError:
                test_size = 25
                
            _, X_test, _, y_test = self.model._dataSplit(csv, (float(test_size)/100),save=False)
            toret = self.model.evaluate(X_test=X_test, y_test=y_test, show=False, outputName=outputName)
            toretDict = {
                'exactitud' : toret[0],
                'precision' : toret[1],
                'recall' : toret[2],
                'f1' : toret[3],
                'tcr1' : toret[4],
                'tcr9' : toret[5],
                'tcr999' : toret[6]
            }
            return {'error' : False, 'message' : toretDict}
        except Exception as e:
            print('Error: ', str(e))
            return {'error' : True, 'message' : str(e)}
    
    def getModelCheck(self):
        try:
            if self.model is not None and self.model.model is not None:
                return {'error' : False, 'message' : True}
            else:
                return {'error' : False, 'message' : False}
        except Exception as e:
            print('Error: ', str(e))
            return {'error' : True, 'message' : str(e)}
        
    def desambiguar(self, text, method):
        try:
            processor = None
            if method == 'father':
                processor = FatherCsvProcessor()
                words = processor._synsetPreprocessRow(text)
                toretWords = processor._FatherProcessDisambiguation(words)
            elif method == 'first-synset':
                processor = FirstSynsetDisambiguationCsvProcessor()
                words = processor._synsetPreprocessRow(text)
                toretWords = processor._synsetFirstSynsetDisambiguationProcess(words)
            elif method == 'path':
                processor = PathCsvProcessor()
                words = processor._synsetPreprocessRow(text)
                toretWords = processor._PathProcessDisambiguation(words)
            toretDict = {'words' : [word for sentence in words for word in sentence if len(processor._getNounsFromSynset(wn.synsets(word)))] 
                         if method != 'path' else [word for word in words if len(processor._getNounsFromSynset(wn.synsets(word)))],
                         'synsets' : toretWords,
                         'definitions' : [wn.synset(i).definition() for i in toretWords]}
            return {'error': False, 'message': toretDict}
        except Exception as e:
            print('Error: ', str(e))
            return {'error' : True, 'message' : str(e)}
    
    def closeWindow(self):
        self.windows.destroy()

# Inicio de la aplicación y conexión
if __name__ == '__main__':
    api = Api()
    windowTrain = webview.create_window('Disambiguation', 'http://localhost:4200', js_api=api, height=1040, width=1920)
    api.windows = windowTrain
    webview.start()
