import os
import pandas as pd
import numpy as np

from field_map import dic_prices
import db_oper


if __name__ == "__main__":
    price_root = 'data/stock_prices'
    files = os.listdir(price_root)
    files.sort()
    print(len(files))
    print(files[:10])

    for f in files:
        prices = pd.read_csv('%s/%s' % (price_root, f), dtype={'종목코드': str})
        # print(prices.head())
        # print(prices[['종목코드', '시가총액']].head())

        # 정수형 데이터 처리 (',' 포함 문자열)
        num_cols = ['현재가', '대비', '거래량', '거래대금', '시가', '고가', '저가', '시가총액', '상장주식수', '외국인 보유주식수']
        for col in num_cols:
            # prices[col] = prices[col].str.replace(",", "").astype(np.int64)
            prices[col] = prices[col].apply(lambda x: x.replace(',', '') if type(x) is str else x)
            if col == '시가총액':
                prices[col] = prices[col].str[:-6]
        # print(prices.head())
        # print(prices[['종목코드', '시가총액']].head())

        # 컬럼명 변경
        cols = tuple(dic_prices.keys())
        prices = prices[[k for k in prices.keys() if k.startswith(cols)]]
        keys = prices.keys()
        keys2 = [dic_prices[k] if k in dic_prices else k for k in keys]
        # print(keys2)
        prices.columns = keys2
        prices.insert(1, 'sdate', f[:-4])
        print(f, prices.head(3))

        db_oper.upsert_table('prices', prices)

        # break


