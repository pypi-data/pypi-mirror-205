import pandas as pd
from urllib import request

def load_boston():
  url_boston = 'https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/sklearn/datasets/data/boston_house_prices.csv'
  savename = "boston_house_prices.csv"
  request.urlretrieve(url_boston,savename)

  class __Boston:
    def __init__(self):
      df = pd.read_csv(savename, header=1)
      self.data = df.drop('MEDV', axis=1).values
      self.target = df['MEDV'].values
      self.feature_names = df.columns.values.tolist()
  return __Boston()