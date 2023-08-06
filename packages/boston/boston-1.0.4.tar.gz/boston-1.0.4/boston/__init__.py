__version__='1.0.4'


def load_boston():
  filename = "boston_house_prices.csv"

  class __Boston:
    def __init__(self):
      df = pd.read_csv(filename, header=1)
      self.data = df.drop('MEDV', axis=1).values
      self.target = df['MEDV'].values
      self.feature_names = df.columns.values.tolist()
  return __Boston()