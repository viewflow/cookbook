import pickle
import datetime as dt
import pandas as pd

from pathlib import Path
from django.utils.functional import cached_property


class Data:
    @cached_property
    def dataframe(self):
        df = pd.read_csv(Path(__file__).parent / 'wellspublic.csv')
        df['Date_Well_Completed'] = pd.to_datetime(df['Date_Well_Completed'])
        df = df[df['Date_Well_Completed'] > dt.datetime(1960, 1, 1)]
        return df

    @cached_property
    def points(self):
        return pickle.load(open(Path(__file__).parent / 'points.pkl', "rb"))

    @cached_property
    def dataset(self):
        trim = self.dataframe[['API_WellNo', 'Well_Type', 'Well_Name']]
        trim.index = trim['API_WellNo']
        return trim.to_dict(orient='index')


oildata = Data()
