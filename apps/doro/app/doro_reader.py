import pandas as pd

class DoroReader:
    def __init__(self):
        pass

    def get_data(self):
        df = pd.read_csv("한국도로공사_교통사고통계_20241231.csv", encoding="cp949")
        print(df.head(10))

