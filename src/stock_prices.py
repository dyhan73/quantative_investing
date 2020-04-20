import os

import pandas as pd

import db_oper


if __name__ == "__main__":
    price_root = '../Korea_Stocks/Korea_Stocks_Full'
    files = os.listdir(price_root)
    print(len(files))

    for f in files:
        if not f.endswith('.csv'): continue
        code = f.replace('.csv', '')
        print(code, f)
        prices = pd.read_csv('%s/%s'%(price_root, f))
        prices.insert(0, 'code', code)
        # prices.columns = [key.lower() for key in prices.keys()]
        prices.columns = ['code', 'sdate', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
        prices['date'] = prices['date'].str.replace('-', '')
        
        print(len(prices))
        print(prices.head(3))
        
        db_oper.insert_table('prices', prices)
        # break
