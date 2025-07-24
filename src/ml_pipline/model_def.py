from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import pandas as pd
import os


file_name = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'emails.csv')
)

def train_model():
  df = pd.read_csv(file_name, encoding='latin1')
  X = df["text"]
  y = df["label"]
  pipe = Pipeline([("tfidf", TfidfVectorizer(stop_words="english")), ("clf", LogisticRegression(max_iter= 1000))])
  param_grid = {
    'tfidf__max_features': [500, 1000, 1500],
    'tfidf__ngram_range': [(1,1), (1,2)],  # try unigrams and bigrams
    'clf__C': [0.01, 0.1, 1, 10],          # regularization strength
  }
  model = GridSearchCV(estimator=pipe, param_grid=param_grid, cv=5, scoring='f1', verbose=1)
  model.fit(X, y)
  #results_df = pd.DataFrame(model.cv_results_)
  best_model = model.best_estimator_
  return best_model