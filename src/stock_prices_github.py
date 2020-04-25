import os

import pandas as pd

import db_oper


def do_main_proc_to_update_stock_prices_github():
    price_root = os.path.join('..', 'Korea_Stocks', 'Korea_Stocks_Full')
    files = os.listdir(price_root)
    files.sort()
    print(len(files))

    for f in files:
        if not f.endswith('.csv'):
            continue
        code = f.replace('.csv', '')
        print(code, f)
        # prices = pd.read_csv('%s/%s' % (price_root, f))
        prices = pd.read_csv(os.path.join(price_root, f))
        prices.insert(0, 'code', code)
        # prices.columns = [key.lower() for key in prices.keys()]
        prices.columns = ['code', 'sdate', 'open', 'high', 'low', 'close', 'trading_volume', 'adj_close']
        prices['sdate'] = prices['sdate'].str.replace('-', '')

        print(len(prices))
        print(prices.head(3))

        db_oper.insert_table('prices', prices)
        # break
    return


if __name__ == "__main__":
    do_main_proc_to_update_stock_prices_github()
