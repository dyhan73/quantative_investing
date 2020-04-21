from datetime import datetime, timedelta
import calendar

import db_oper

"""
joined['PER'] = joined['시가총액'] / joined['당기순이익'] / 1000
joined['PSR'] = joined['시가총액'] / joined['매출액'] / 1000
joined['PCR'] = joined['시가총액'] / joined['영업현금흐름'] / 1000
joined['PBR'] = joined['시가총액'] / joined['자본총계'] / 1000
joined['ROA'] = joined['당기순이익'] / joined['자산총계']
joined['GPA'] = joined['매출총이익'] / joined['자산총계']
"""


# 분기별 데이터 생성
# q1_net_sales integer,
# q1_gross_profit integer,
# q1_operating_income integer
def calc_q1_values(date):
    where = ' and '.join((
        'net_sales is not null and net_sales != 0',
        'gross_profit is not null and gross_profit != 0',
        'operating_income is not null and operating_income != 0'))

    curr_df = db_oper.select_table('reports', where + ' and rdate=%s' % date)
    prev_df = db_oper.select_table('reports', where + ' and rdate=%s' % get_prev_report_day(date))

    curr_df = curr_df[['code', 'rdate', 'net_sales', 'gross_profit', 'operating_income']]
    prev_df = prev_df[['code', 'rdate', 'net_sales', 'gross_profit', 'operating_income']]

    curr_df = curr_df.astype({'code': 'object'})
    prev_df = prev_df.astype({'code': 'object'})

    # join
    join_df = curr_df.merge(prev_df, how='inner', suffixes=('', '_prev'), on='code')

    # 이후 순서가 중요
    join_df['q1_net_sales'] = join_df['net_sales'] - join_df['net_sales_prev']

    join_df['q1_gross_profit'] = join_df['gross_profit'] - join_df['gross_profit_prev']
    join_df['q1_gross_profit'] = join_df.apply(lambda x: x['gross_profit'] if x['q1_gross_profit'] < 0 else x['q1_gross_profit'], axis=1)

    join_df['q1_operating_income'] = join_df['operating_income'] - join_df['operating_income_prev']
    join_df['q1_operating_income'] = join_df.apply(lambda x: x['operating_income'] if x['q1_operating_income'] < 0 else x['q1_operating_income'], axis=1)

    join_df['q1_net_sales'] = join_df.apply(lambda x: x['net_sales'] if x['q1_net_sales'] < 0 else x['q1_net_sales'], axis=1)

    result = join_df[['code', 'rdate', 'q1_net_sales', 'q1_gross_profit', 'q1_operating_income']]

    print(curr_df.head())
    print(result.head())
    pass


def get_prev_report_day(report_date):
    dt = datetime.strptime(report_date, '%Y%m%d')
    prev_dt = dt - timedelta(days=95)
    last_day = calendar.monthrange(prev_dt.year, prev_dt.month)[1]
    prev_dt = prev_dt.replace(day=last_day)
    return prev_dt.strftime('%Y%m%d')


def get_report_days_of_year(report_date):
    result = [report_date]
    dt = report_date
    for i in range(3):
        dt = get_prev_report_day(dt)
        result.append(dt)
    return result


if __name__ == "__main__":
    rdate = '20191231'
    dt_rdate = datetime.strptime(rdate, '%Y%m%d')
    print(dt_rdate.strftime('%Y-%m-%d'))

    rdate = '20190331'
    dt_rdate = datetime.strptime(rdate, '%Y%m%d')
    print(dt_rdate.strftime('%Y%m%d'))

    dt_rdate2 = dt_rdate - timedelta(days=95)
    print(dt_rdate2)

    last_day = calendar.monthrange(dt_rdate2.year, dt_rdate2.month)[1]
    dt_rdate3 = dt_rdate2.replace(day=last_day)
    print(dt_rdate3)

    print(get_prev_report_day('20191231'))
    print(get_report_days_of_year('20191231'))

    calc_q1_values('20191231')
