import pandas as pd
import os
from Parser.Parser import Parser
class CsvDirector:
    def __init__(self, parser):
        self.parser = parser
    
    # Unifica los correos de un directorio en un csv
    def parseToCSV(self, folder, type, output):
        df = pd.DataFrame(columns=['mailType', 'message'])
        for file in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, file)):
                message = self.parser.parse(os.path.join(folder, file))
                if len(message) > 0:
                    df.loc[len(df.index)] = [type, message]
        df.to_csv(output, index=False, escapechar='\\')
    
    # Añade un correo a un csv
    def addToCSV(self, file, type, dfName):
        df = pd.read_csv(dfName, index_col=None)
        message = self.parser.parse(file)
        if len(message) > 0:
            df.loc[len(df.index)] = [type, message]
        df.to_csv(df, index=False)

    # Unifica csv en uno solo 
    def mergeCSV(self, csvList, ouptut):
        df = pd.concat([pd.read_csv(f) for f in csvList], ignore_index=True)
        df.to_csv(ouptut, index=False) 