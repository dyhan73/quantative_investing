import os
import sys

from datetime import datetime, timedelta
import calendar

import pandas as pd
import numpy as np

import db_oper


def get_target_date(start_date, days=365):
    dt_date = datetime.strptime(start_date, '%Y%m%d')
    dt_target = dt_date + timedelta(days=days)
    return dt_target.strftime('%Y%m%d')


def get_plus_per_by_date(date, lowest_market_cap_ratio=0.2):
    # 유의미한 투자지표를 가진 종목 조회
    sql = """
    with
    price_date as (
        select min(sdate) as sdate
        from prices
        where sdate >= %s
        group by sdate
        having count(*) > 1000
    ),
    cnt as (
        select count(*) as cnt from prices where sdate = (select sdate from price_date)
    ),
    col_prices as (
        select * from prices
        where sdate = (select sdate from price_date)
        order by calc_market_cap
        limit cast((select cnt from cnt) * %f as int)
    ),
    rep_date_latest as (
        select max(rdate) as rdate from reports where rdate < (select sdate from price_date)
    ),
    rep_date as (
        select max(rdate) as rdate from reports where rdate < (select rdate from rep_date_latest)
    ),
    reps as (
        select *
        from reports where rdate = (select rdate from rep_date)
    ),
    candidates as (
        select p.code, c.company, p.sdate, max(p.open, p.high, p.low, p.close, ifnull(p.adj_close, 0)) as price,
               p.calc_market_cap, p.per, p.psr, p.pcr, p.pbr, r.roa, r.gpa, r.debt_to_equity_ratio
        from col_prices p
        join reps r on p.code = r.code
        join companies c on p.code = c.code
        where per is not null and per > 0
    )
    select * from candidates
    """ % (date, lowest_market_cap_ratio)

    # print(type(sql))
    df_candidates = db_oper.select_by_query(sql)
    # low20.head()
    return df_candidates


def set_indicator_ranking(df):
    # 각 지표 Ranking 구하기
    df['PER_Rank'] = df['per'].rank(method='max')
    df['PSR_Rank'] = df['psr'].rank(method='max')
    df['PCR_Rank'] = df['pcr'].rank(method='max')
    df['PBR_Rank'] = df['pbr'].rank(method='max')
    df['ROA_Rank'] = df['roa'].rank(method='max', ascending=False)
    df['GPA_Rank'] = df['gpa'].rank(method='max', ascending=False)
    df['s_value'] = df['PER_Rank'] + df['PSR_Rank'] + df['PCR_Rank'] + df['PBR_Rank']  # 슈퍼가치전략
    df['PBRGPA'] = df['PBR_Rank'] + df['GPA_Rank']  # 신마법공식
    df['s_v_m'] = df['PER_Rank'] + df['PSR_Rank'] + df['PBR_Rank'] + df['GPA_Rank']  # 슈퍼밸류모멘텀
    return df


def get_dict_candidates_of_strategies(df):
    # # 그레이엄 마지막 선물 업그레이드 (야는 하위 20%가 아니얌)
    # graham = df[df['debt_to_equity_ratio'].astype(float) < 50.0]
    # graham = graham[graham['roa'] < 5]
    # graham = graham[graham['pbr'] >= 0.2]
    # graham = graham.sort_values(['PBR_Rank']).head(30)

    # 슈퍼가치전략
    super_values = df.sort_values(['s_value']).head(50)
    # 신마법공식 2.0
    magic = df.sort_values(['PBRGPA']).head(30)
    # 슈퍼밸류모멘텀
    svm = df.sort_values(['s_v_m']).head(50)
    # return {'graham': graham, 'super_values': super_values, 'magic': magic, 'svm': svm}
    return {'super_values': super_values, 'magic': magic, 'svm': svm}


def get_earnings_of_date(df, date, seed_money):
    sql = """
        with
        price_date as (
            select min(sdate) as sdate
            from prices
            where sdate >= '%s'
            group by sdate
            having count(*) > 1000
        )
        
        -- select code, sdate, max(open, high, low, close, ifnull(adj_close, 0)) as price
        select code, sdate, open, high, low, close, adj_close, trading_volume
        from prices
        where sdate = (select sdate from price_date)
            and code in ('%s')
    """ % (date, "','".join(df.code))
    sval_next = db_oper.select_by_query(sql)
    sval_next['price'] = sval_next.apply(get_price, axis=1)
    # sval_next.head()

    sval_rslt = df.merge(sval_next, how='left', on='code', suffixes=['', '_1'])

    sval_rslt = sval_rslt[['code', 'company', 'price', 'price_1']]
    sval_rslt['stock_cnt'] = seed_money / len(sval_rslt) / sval_rslt['price']
    sval_rslt['buy'] = sval_rslt['stock_cnt'] * sval_rslt['price']
    sval_rslt['sell'] = sval_rslt['stock_cnt'] * sval_rslt['price_1']
    sval_rslt['gain'] = sval_rslt['sell'] - sval_rslt['buy']
    return sval_rslt


def get_price(row):
    if row.open == 0 and row.high == 0 and row.low == 0:
        return 0
    if row.trading_volume == 0:
        return 0
    return row.close


if __name__ == "__main__":
    start_date = '20200428'

    df = get_plus_per_by_date(start_date)
    df = set_indicator_ranking(df)
    strategies = get_dict_candidates_of_strategies(df)
    # print(strategies['svm'])

    strategies['graham'].to_excel(os.path.join('output', 'graham_%s.xlsx' % start_date))
    strategies['svm'].to_excel(os.path.join('output', 'super_value_momentum_%s.xlsx' % start_date))
    strategies['magic'].to_excel(os.path.join('output', 'magic_%s.xlsx' % start_date))
    strategies['super_values'].to_excel(os.path.join('output', 'super_values_%s.xlsx' % start_date))
