import pandas as pd
import numpy as np
from datetime import datetime


def convert_tick(path, nrows=None):
    '''converts mt5 tick data into a pandas dataframe

    Converts tick data csv from mt5 into a pandas dataframe 
    with bid and ask columns and a datetime index.
    Nan values are forward filled as mt5 does not record a 
    tick if it is the same as the last tick.

    Args:
        path:   path to csv file exported from mt5
        rows (int):   number of rows of CSV to read in and convert

    Returns: 
        Pandas dataframe (index = datetime, columns = (bid, ask))

    '''

    # reading in csv, converting it into a numpy array and flattening
    df = pd.read_csv(path, nrows=nrows).to_numpy().flatten()
    date_time, bid, ask = [[] for i in range(3)]
    loc = 0
    for _ in range(len(df)):
        # spliting relevent values into a list to index from
        data = df[loc].split('\t')
        # if bid/ask missing fill with nan
        if data[2] == '': data[2] = np.nan
        if data[3] == '': data[3] = np.nan
        date_time.append(datetime.strptime(f'{data[0]} {data[1]}', '%Y.%m.%d %H:%M:%S.%f'))
        bid.append(np.float(data[2]))
        ask.append(np.float(data[3]))
        loc += 1
    data = pd.DataFrame({'bid': bid, 'ask': ask}, index=date_time)
    # forward filling nan values
    data.fillna(method='ffill', inplace=True)
    return data
    

def convert_ohlc(path, nrows=None):
    '''converts mt5 ohlc data into a pandas dataframe
    
    Converts OHLC data from mt5 into a pandas dataframe
    with open, high, low, close, volume and spread columns 
    with a datetime index
    
    Args:
        path:   path to csv file exported from mt5
        rows (int):   number of rows of CSV to read in and convert

    Returns:
        Pandas dataframe(index = datetime, columns = (open, high, low, close, volume, spread))

    '''

    # reading in csv, converting it into a numpy array and flattening
    df = pd.read_csv(path, nrows=nrows).to_numpy().flatten()
    date_time, open_, high, low, close, tickvol, spread = [[] for i in range(7)]
    loc = 0
    for _ in range(len(df)):
        # spliting relevent values into a list to index from
        data = df[loc].split('\t')
        date_time.append(datetime.strptime(f'{data[0]} {data[1]}', '%Y.%m.%d %H:%M:%S'))
        # appending data in to relevent lists
        [x.append(np.float(y)) for x,y in zip([open_, high, low, close, tickvol, spread], data[2:])]
        loc += 1
    data = pd.DataFrame({'open': open_, 'high': high,
                         'low': low, 'close': close,
                         'volume': tickvol, 'spread': spread}, index=date_time)
    return data