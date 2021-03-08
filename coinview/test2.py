import numpy as np #pip install numpy
from tqdm import tqdm #pip install tqdm
from binance.client import Client #pip install python-binance
import pandas as pd #pip install pandas
from datetime import datetime
import random

SMA_LOW = 40
SMA_HIGH = 150

def compute_sma(data, window):
    sma = data.rolling(window=window).mean()
    return sma


#select cryptocurrencies you'd like to gather and time interval
ratios = ['BTC','ETH','LTC','XLM','XRP','XMR','TRX','LINK','IOTA','EOS','DASH','ZRX']
START_TIME = '28 Mar, 2019'
END_TIME = '1 Jun, 2020'
api_key=''
api_secret=''

client = Client(api_key=api_key,api_secret=api_secret)

merge = False
for ratio in ratios:
    print(f'Gathering {ratio} data...')
    data = client.get_historical_klines(symbol=f'{ratio}USDT',interval=Client.KLINE_INTERVAL_1MINUTE,start_str=START_TIME,end_str=END_TIME)
    cols = ['time','Open','High','Low',f'{ratio}-USD_close',f'{ratio}-USD_volume','CloseTime','QuoteAssetVolume','NumberOfTrades','TBBAV','TBQAV','null']
    
    temp_df = pd.DataFrame(data,columns=cols)
    temp_df = temp_df[['time',f'{ratio}-USD_close']]
    
    if merge == False:
        df = temp_df
    else:
        df = pd.merge(df,temp_df,how='inner',on='time')
    merge = True
    print('complete')
    time.sleep(60) #sleep for a bit so the binance api doesn't kick you out for too many data asks


for col in df.columns:
    if col != 'time':
        df[col] = df[col].astype(np.float64)

for ratio in ratios:
    df[f'{ratio}_{SMA_LOW}'] = compute_sma(df[f'{ratio}-USD_close'], SMA_LOW)
    df[f'{ratio}_{SMA_HIGH}'] = compute_sma(df[f'{ratio}-USD_close'], SMA_HIGH)
    
#clip NaNs
df = df[SMA_HIGH:]
df = df.reset_index(drop=True)

#convert binance timestamp to datetime
for i in tqdm(range(len(df))):
    df['time'][i] = datetime.fromtimestamp(int(df['time'][i]/1000))

df.to_csv('12-coins-Mar18_Jun20')