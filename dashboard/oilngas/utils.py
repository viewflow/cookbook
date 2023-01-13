import math
import datetime as dt


def human_format(num):
    if num <= 0:
        return num
    magnitude = int(math.log(num, 1000))
    mantissa = str(int(num / (1000**magnitude)))
    return mantissa + ['', 'K', 'M', 'G', 'T', 'P'][magnitude]


def filter_dataframe(df, well_statuses, well_types, year_slider):
    dff = df[df['Well_Status'].isin(well_statuses)
             & df['Well_Type'].isin(well_types)
             & (df['Date_Well_Completed'] > dt.datetime(year_slider[0], 1, 1))
             & (df['Date_Well_Completed'] < dt.datetime(year_slider[1], 1, 1))]
    return dff


def fetch_individual(points, api):
    try:
        points[api]
    except Exception:
        return None, None, None, None

    index = list(range(min(points[api].keys()), max(points[api].keys()) + 1))
    gas = []
    oil = []
    water = []

    for year in index:
        try:
            gas.append(points[api][year]['Gas Produced, MCF'])
        except Exception:
            gas.append(0)
        try:
            oil.append(points[api][year]['Oil Produced, bbl'])
        except Exception:
            oil.append(0)
        try:
            water.append(points[api][year]['Water Produced, bbl'])
        except Exception:
            water.append(0)

    return index, gas, oil, water


def fetch_aggregate(points, selected, year_slider):
    index = list(range(max(year_slider[0], 1985), 2016))
    gas = []
    oil = []
    water = []

    for year in index:
        count_gas = 0
        count_oil = 0
        count_water = 0
        for api in selected:
            try:
                count_gas += points[api][year]['Gas Produced, MCF']
            except Exception:
                pass
            try:
                count_oil += points[api][year]['Oil Produced, bbl']
            except Exception:
                pass
            try:
                count_water += points[api][year]['Water Produced, bbl']
            except Exception:
                pass
        gas.append(count_gas)
        oil.append(count_oil)
        water.append(count_water)

    return index, gas, oil, water
