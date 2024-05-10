from FeatureExtraction import FeatureExtraction
import pandas as pd
import pickle
from os import path

file_path = path.abspath(__file__) 
dir_path = path.dirname(file_path) 
file_model_path = path.join(dir_path,'URL_Classifier.pkl') 

class PredictURL:
    def __init__(self):
        pass

    def predict(self, url):
        fe = FeatureExtraction()
        features = pd.DataFrame({'url': [url]})

        features["haveIP"] = features["url"].apply( lambda x: fe.haveIP(x))
        features["lenURL"] = features["url"].apply( lambda x: fe.lenURL(x))
        features["lenHostname"] = features["url"].apply( lambda x: fe.lenHostname(x))
        features["tinyURL"] = features["url"].apply( lambda x: fe.tinyURL(x))
        features["abnormal_url"] = features["url"].apply( lambda x: fe.abnormal_url(x))
        features["suspicious_tlds"] = features["url"].apply( lambda x: fe.suspicious_tlds(x))
        features["digit_count"] = features["url"].apply( lambda x: fe.digit_count(x))
        features["letter_count"] = features["url"].apply( lambda x: fe.letter_count(x))
        features["special_chars_count"] = features["url"].apply( lambda x: fe.special_chars_count(x))
        features["have@"] = features["url"].apply( lambda x: fe.haveAtSign(x))
        features["redirection"] = features["url"].apply( lambda x: fe.redirection(x))
        features["have-"] = features["url"].apply( lambda x: fe.haveDash(x))
        features["subDomains"] = features["url"].apply( lambda x: fe.subDomains(x))

        features.drop(columns=['url'], inplace=True)
        return self.classify(features)
    
    def classify(self, features):
        with open(file_model_path, 'rb') as file:  
            model = pickle.load(file)
        file.close()
        res = model.predict(features)
        return "Đây có thể là đường dẫn đến trang web độc hại" if res == 1 else "Đây có thể là đường dẫn đến trang web an toàn"

