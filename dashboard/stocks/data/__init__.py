import pandas as pd

from pathlib import Path
from django.utils.functional import cached_property


class Data:
    @cached_property
    def dataframe(self):
        return pd.read_csv(Path(__file__).parent / 'stock-ticker.csv')


stockData = Data()
