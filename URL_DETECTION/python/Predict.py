from FeatureExtraction import FeatureExtraction
import pandas as pd
import pickle
from os import path

file_path = path.abspath(__file__) 
dir_path = path.dirname(file_path) 
file_model_path = path.join(dir_path,'URL_Classifier_XGB.pkl') 

class PredictURL:
    def __init__(self):
        with open(file_model_path, 'rb') as file:  
            self.model = pickle.load(file)
        file.close()

    def predict(self, url):
        feature = FeatureExtraction()
        status_df = pd.DataFrame({'url': [url]})

        for func_name in dir(FeatureExtraction):
            if not func_name.startswith('__') and callable(getattr(FeatureExtraction, func_name)):
                status_df[func_name] = status_df['url'].apply(getattr(feature, func_name))

        status_df.drop(columns=['url'], inplace=True)
        test = pd.DataFrame(status_df, columns=status_df.columns)
        return self.classify(test)
    
    def classify(self, features):
        res = self.model.predict_proba(features)
        if res[0][1] > res[0][0]:
            return (1, float(res[0][1]))
        return (0, float(res[0][0]))

