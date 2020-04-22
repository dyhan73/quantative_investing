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
        'ongoing_operating_income is not null and ongoing_operating_income != 0'))

    curr_df = db_oper.select_table('reports', where + ' and rdate=%s' % date)
    prev_df = db_oper.select_table('reports', where + ' and rdate=%s' % get_prev_report_day(date))

    if curr_df is None or prev_df is None:
        return None

    curr_df = curr_df[['code', 'rdate', 'net_sales', 'gross_profit', 'ongoing_operating_income']]
    prev_df = prev_df[['code', 'rdate', 'net_sales', 'gross_profit', 'ongoing_operating_income']]

    curr_df = curr_df.astype({'code': 'object'})
    prev_df = prev_df.astype({'code': 'object'})

    # join
    join_df = curr_df.merge(prev_df, how='inner', suffixes=('', '_prev'), on='code')

    # 이후 순서가 중요
    # 일단 이번분기에서 전분기 값을 빼서 분기별 값 구함
    join_df['q1_net_sales'] = join_df['net_sales'] - join_df['net_sales_prev']
    join_df['q1_gross_profit'] = join_df['gross_profit'] - join_df['gross_profit_prev']
    join_df['q1_ongoing_operating_income'] = join_df['ongoing_operating_income'] - join_df['ongoing_operating_income_prev']

    # 전 분기가 결산월이면 1분기 - 1년치가 되어 매추이 음수가 됨 => 이 경우 당분기 값으로 대체
    join_df['q1_gross_profit'] = join_df.apply(lambda x: x['gross_profit'] if x['q1_net_sales'] <= 0 else x['q1_gross_profit'], axis=1)
    join_df['q1_ongoing_operating_income'] = join_df.apply(lambda x: x['ongoing_operating_income'] if x['q1_net_sales'] <= 0 else x['q1_ongoing_operating_income'], axis=1)
    # net_sales 는 마지막에... (위에서 양/음수 판단값으로 사용)
    join_df['q1_net_sales'] = join_df.apply(lambda x: x['net_sales'] if x['q1_net_sales'] < 0 else x['q1_net_sales'], axis=1)

    result = join_df[['code', 'rdate', 'q1_net_sales', 'q1_gross_profit', 'q1_ongoing_operating_income']]

    print("calc date : " + date)
    print(result.head())
    return result


def proc_q1_values():
    report_date = '20191231'

    while True:
        q1_values = calc_q1_values(report_date)
        if q1_values is None or len(q1_values) <= 0:
            break
        db_oper.update_table('reports', q1_values, ['code', 'rdate'])
        report_date = get_prev_report_day(report_date)


# 지난 4분기 합계 데이터 산출
# q4_net_sales integer,
# q4_gross_profit integer,
# q4_operating_income integer
def calc_q4_values(date):
    where = ' and '.join((
        'net_sales is not null and net_sales != 0',
        'gross_profit is not null and gross_profit != 0',
        'ongoing_operating_income is not null and ongoing_operating_income != 0'))

    report_date_list = get_report_days_of_year(date)

    df_list = []
    for report_date in report_date_list:
        df = db_oper.select_table('reports', where + ' and rdate=%s' % report_date)
        if df is None:
            return None
        df = df[['code', 'rdate', 'q1_net_sales', 'q1_gross_profit', 'q1_ongoing_operating_income']]
        df_list.append(df)

    # join
    join_df = df_list[0].merge(df_list[1], how='inner', suffixes=('', '_1'), on='code')
    join_df = join_df.merge(df_list[2], how='inner', suffixes=('', '_2'), on='code')
    join_df = join_df.merge(df_list[3], how='inner', suffixes=('', '_3'), on='code')

    # 누계 계산
    join_df['q4_net_sales'] = join_df['q1_net_sales'] + join_df['q1_net_sales_1'] + join_df['q1_net_sales_2'] + join_df['q1_net_sales_3']
    join_df['q4_gross_profit'] = join_df['q1_gross_profit'] + join_df['q1_gross_profit_1'] + join_df['q1_gross_profit_2'] + join_df['q1_gross_profit_3']
    join_df['q4_ongoing_operating_income'] = join_df['q1_ongoing_operating_income'] + join_df['q1_ongoing_operating_income_1'] + join_df['q1_ongoing_operating_income_2'] + join_df['q1_ongoing_operating_income_3']

    result = join_df[['code', 'rdate', 'q4_net_sales', 'q4_gross_profit', 'q4_ongoing_operating_income']]

    print("calc date : " + date)
    print(result.head())
    return result


def proc_q4_values():
    report_date = '20191231'

    while True:
        q4_accums = calc_q4_values(report_date)
        if q4_accums is None or len(q4_accums) <= 0:
            break
        db_oper.update_table('reports', q4_accums, ['code', 'rdate'])
        report_date = get_prev_report_day(report_date)


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


def test_get_day_functions():
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


if __name__ == "__main__":
    # proc_q1_values()
    proc_q4_values()
