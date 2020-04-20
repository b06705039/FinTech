import sys
import pandas as pd
filename = sys.argv[1]
df = pd.read_csv(filename, encoding='Big5',dtype={'到期月份(週別)' : str,'商品代號' : str})  

tx = df[df['商品代號']=='TX     '] 
tx.reset_index(drop=True, inplace=True)

time = tx.loc[(tx['成交時間'] >= 84500) & (tx['成交時間'] <= 144500)]
time.reset_index(drop=True, inplace=True)

month = time[time['到期月份(週別)'] == time.loc[0,'到期月份(週別)']]
month.reset_index(drop=True, inplace=True)

price = month[(month.成交價格 > 0)]
price.reset_index(drop=True, inplace=True)


openp = int(price.loc[0,'成交價格'])
closep = int(price.loc[len(price)-1,'成交價格'])
high = int(price.loc[price['成交價格'].idxmax(),'成交價格'])
low = int(price.loc[price['成交價格'].idxmin(),'成交價格'])


print(openp, high, low, closep)
