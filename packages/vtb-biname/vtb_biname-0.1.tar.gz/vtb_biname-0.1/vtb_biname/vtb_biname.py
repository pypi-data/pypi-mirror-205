import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib
import pyspark.sql.functions as F
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.types import IntegerType

class name_classifier:
    def __init__(self):
        self.model = None
    
    def fit(self, data, pers):
        # Load the dataset
        df = pd.DataFrame({'name': data, 'pers': pers})
        
        # Create a pipeline that preprocesses text, extracts features, and trains a classifier
        text_clf = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LinearSVC())
        ])

        # Train the model on the data
        text_clf.fit(df['name'], df['pers'])
        
        # Save the model for later use
        self.model = text_clf
    
    def predict(self, name):
        if self.model is None:
            raise ValueError('Model has not been trained yet.')
            
        pers = self.model.predict([name])[0]
        return int(pers)
    
    def classify_udf(self):
        if self.model is None:
            raise ValueError('Model has not been trained yet.')
            
        def classify(name):
            pers = self.model.predict([name])[0]
            return int(pers)
        
        return F.udf(classify, IntegerType())