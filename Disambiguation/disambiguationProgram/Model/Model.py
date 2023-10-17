from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import cross_val_score, train_test_split
import os
import pickle
 
class ModelManager:
    def __init__(self, modelName):
        self._modelName = modelName
        model = None
        if modelName == "Gaussian":
            model = GaussianNB()
        elif modelName == "RandomForest":
            model = RandomForestClassifier(n_estimators=10, random_state=42)
        elif modelName == "DecisionTreeClasifier":
            model = DecisionTreeClassifier(criterion="entropy", random_state=42)
        elif modelName == "Bagging":
            model = BaggingClassifier(estimator=DecisionTreeClassifier(criterion='entropy'), n_estimators=10, random_state=42)
        
            
        self.model = model
        
    # Reinicio del modelo
    def resetModel(self):
        if self._modelName == "Gaussian":
            model = GaussianNB()
        elif self._modelName == "RandomForest":
            model = RandomForestClassifier(n_estimators=10, random_state=42)
        elif self._modelName == "DecisionTreeClasifier":
            model = DecisionTreeClassifier(criterion="entropy", random_state=42)
        elif self._modelName == "Bagging":
            model = BaggingClassifier(estimator=DecisionTreeClassifier(criterion='entropy'), n_estimators=10, random_state=42)
        self.model = model

    def save_model(self, output):
        try:
            with open('../models/' + output, 'wb') as archivo:
                pickle.dump(self.model, archivo)
        except Exception as e:
            print(f"Error al guardar el modelo: {str(e)}")
            raise e

    def load_model(self, modelFile):
        try:
            with open(modelFile, 'rb') as archivo:
                modelo = pickle.load(archivo)
                self.model =  modelo
        except Exception as e:
            print(f"Error al cargar el modelo: {str(e)}")
            raise e
    
    def train(self, csv, test_size = 0.25, cv=10):
        X_train, X_test, y_train, y_test = self._dataSplit(csv, test_size, save=True)

        self.model.fit(X_train, y_train)
        
        scores = cross_val_score(self.model, X_train, y_train, cv=cv)
        print(scores)
        return [X_train, X_test, y_train, y_test]
    
    def evaluate(self, X_test=None, y_test=None, show=True, outputName = ''):
        toretString = []
        if X_test is None or y_test is None:
            X_test = self.X_test
            y_test = self.y_test

        # Obtener las etiquetas predichas por el modelo
        print("TEST")
        y_pred = self.model.predict(X_test)
        cm = confusion_matrix(y_test,y_pred, labels=["ham", "spam"])
        report = classification_report(y_test, y_pred,labels=["ham", "spam"])
        print(report)
        cm_display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["ham", "spam"])
        cm_display.plot()
        if show:
            plt.show()
        else:
            plt.savefig('../disambiguationApp/src/assets/'+outputName+'_cm.png')
        tn, fp, fn, tp = cm.ravel()
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1_score = 2 * (precision * recall) / (precision + recall)
        accRep = "Accuracy: " + str(round(accuracy, 3))
        precRep = "Precision: " + str(round(precision, 3))
        recallRep = "Recall: " + str(round(recall, 3))
        f1Rep = "F1-score: " + str(round(f1_score, 3))
        print(accRep)
        print(precRep)
        print(recallRep)
        print(f1Rep)
        
        toretString = [float(round(accuracy,3)), float(round(precision,3)), float(round(recall,3)), float(round(f1_score,3))]
            
        fp_penalty = [1,9,999]
        for fp_pen in fp_penalty:
            TCR_score = (tn + fp) / (fp_pen * fp + fn)
            toretString.append(round(TCR_score, 3))
            print("TCR_Score lambda = ",fp_pen,": " , round(TCR_score, 3))
            
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        

        # Calcula el AUC y ROC
        auc = roc_auc_score(y_test, y_pred_proba)
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba, pos_label='spam')

        # Grafica la curva ROC
        plt.figure()
        plt.plot(fpr, tpr, label="ROC curve (area = %0.2f)" % auc)
        plt.plot([0, 1], [0, 1], "k--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Receiver operating characteristic example")
        plt.legend(loc="lower right")
        if show:
            plt.show()
        else:
            plt.savefig('../disambiguationApp/src/assets/'+outputName+'_roc.png')
        return toretString
        
    def selectMostImportantFeaturesIG(self, csv_file, output_file, num_features):
        df = pd.read_csv(csv_file)
        mostImportantFeatures = self._select_featuresIG(csv_file, num_features)
        resultdf = df.loc[:,mostImportantFeatures]
        resultdf = pd.concat([df["mailType"], resultdf], axis=1)
        resultdf.to_csv(output_file, index=False)
        return

    def _select_featuresIG(self, csv_file, num_features):
        data = pd.read_csv(csv_file)
        
        labels = np.array(data.iloc[:, 0]) 
        features = np.array(data.iloc[:, 1:])
        ig_scores = mutual_info_classif(features, labels, discrete_features=True, random_state=42)
        
        top_features = ig_scores.argsort()[-num_features:][::-1]
        
        feature_names = list(data.columns[1:])
        selected_features = [feature_names[i] for i in top_features]
        
        return selected_features
      
    def compareTwoCsv(self, baseCsv, comparedCsv):
        print(baseCsv, ' vs ', comparedCsv)
        print('----------------------', baseCsv, '--------------------------')
        
        X_train, X_test, y_train, y_test = self.train(baseCsv)
        self.evaluate(X_train, X_test, y_train, y_test)
        
        self.resetModel()
        
        print('----------------------', comparedCsv, '--------------------------')
        X_train, X_test, y_train, y_test = self.train(comparedCsv)
        self.evaluate(X_train, X_test, y_train, y_test)
        return
      
    # Comparación de dos csv, aplicando al más largo IG para que tengan las mismas características
    def compareTwoCsvwithIG(self, baseCsv, comparedCsv):
        baseCsvDFcolumns = len(pd.read_csv(baseCsv).columns)
        comparedCsvDFcolumns = len(pd.read_csv(comparedCsv).columns)
        
        print('baseCSV: ',baseCsvDFcolumns)
        print('comparedCSV:', comparedCsvDFcolumns)
        
        if baseCsvDFcolumns >= comparedCsvDFcolumns:
            largeDFName = baseCsv
            smallDFName = comparedCsv
            smallDF = comparedCsvDFcolumns
        else:
            largeDFName = comparedCsv
            smallDFName = baseCsv
            smallDF = baseCsvDFcolumns
            
        tempOutputName = 'tempOutputIG.csv'
        print(baseCsv, ' vs ', comparedCsv)
        print('----------------------', largeDFName, '--------------------------')
        
        self.selectMostImportantFeaturesIG(largeDFName, tempOutputName, smallDF)
        
        X_train, X_test, y_train, y_test = self.train(tempOutputName)
        self.evaluate(X_train, X_test, y_train, y_test)
        
        self.resetModel()
        
        print('----------------------', smallDFName, '--------------------------')
        X_train, X_test, y_train, y_test = self.train(smallDFName)
        self.evaluate(X_train, X_test, y_train, y_test)
        
        if os.path.exists(tempOutputName):
            os.remove(tempOutputName)
        return
            
        
    def _dataSplit(self, csv, test_size = 0.25, save = False):
        data = pd.read_csv(csv)
        X = data.iloc[:,1:]
        y = data["mailType"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        if save == True:
            self.X_train = X_train
            self.X_test = X_test
            self.y_train = y_train
            self.y_test = y_test
        return [X_train, X_test, y_train, y_test]