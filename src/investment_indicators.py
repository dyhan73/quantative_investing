import db_oper
from utils import get_latest_meaningful_report_day, get_prev_report_day, get_report_days_of_year

"""
joined['PER'] = joined['시가총액'] / joined['당기순이익']
joined['PSR'] = joined['시가총액'] / joined['매출액']
joined['PCR'] = joined['시가총액'] / joined['영업현금흐름']
joined['PBR'] = joined['시가총액'] / joined['자본총계']
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


def proc_q1_values(rdate):
    q1_values = calc_q1_values(rdate)
    if q1_values is None or len(q1_values) <= 0:
        return None
    db_oper.update_table('reports', q1_values, ['code', 'rdate'])
    return len(q1_values)


def proc_all_q1_values():
    report_date = '20191231'

    while True:
        if proc_q1_values(report_date) is None:
            break
        report_date = get_prev_report_day(report_date)
    return


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


def proc_q4_values(rdate):
    q4_accums = calc_q4_values(rdate)
    if q4_accums is None or len(q4_accums) <= 0:
        return None
    db_oper.update_table('reports', q4_accums, ['code', 'rdate'])
    return len(q4_accums)


def proc_all_q4_values():
    report_date = '20191231'

    while True:
        if proc_q4_values(report_date) is None:
            break
        report_date = get_prev_report_day(report_date)
    return


# joined['ROA'] = joined['당기순이익'] / joined['자산총계']
# joined['GPA'] = joined['매출총이익'] / joined['자산총계']

def proc_roa_gpa(rdate=None):
    sql = "update reports set roa=100.0*q4_ongoing_operating_income/total_assets, gpa=100.0*q4_gross_profit/total_assets"
    if rdate is not None:
        sql = sql + 'and rdate=%s' % rdate
    db_oper.execute_by_query(sql)
    return


def do_all_sdate_proc_pxrs():
    date_df = db_oper.select_by_query("select distinct(sdate) as sdate from prices order by sdate desc")
    for idx, date in date_df.iterrows():
        # print(date)
        # print(date.sdate)
        proc_per_psr_pcr_pbr(str(date.sdate))
    return


def proc_per_psr_pcr_pbr(date):
    """
    per = 시가총액 / 당기순이익
    psr = 시가총액 / 매출액
    pcr = 시가총액 / 영업현금흐름
    pbr = 시가총액 / 자본총계
    per = reports.stock_shares * prices.close / reports.q4_ongoing_operating_income
    psr = reports.stock_shares * prices.close / reports.q4_net_sales
    pcr = reports.stock_shares * prices.close / reports.cash_flows_from_operatings
    pbr = reports.stock_shares * prices.close / reports.total_equity
    :param date: prices.sdate (yyyymmdd)
    :return:
    """
    rep_date = get_latest_meaningful_report_day(date)
    print("proc_PxRs : ", date, rep_date)
    sql = """
        select p.code, p.sdate,
               r.stock_shares * p.close as calc_market_cap,
               r.stock_shares * p.close / r.q4_ongoing_operating_income / 1000000.0 as per,
               r.stock_shares * p.close / r.q4_net_sales / 1000000.0 as psr,
               r.stock_shares * p.close / r.cash_flows_from_operatings / 1000000.0 as pcr,
               r.stock_shares * p.close / r.total_equity / 1000000.0 as pbr
        from prices p
        join reports r on p.code = r.code and r.rdate = '%s'
        where p.sdate = '%s'
        order by p.code
    """ % (rep_date, date)

    df = db_oper.select_by_query(sql)
    print(df.head())
    if len(df) > 0:
        db_oper.update_table('prices', df, ['code', 'sdate'])

    # 음수인 indicator 는 null 처리
    # db_oper.execute_by_query("update prices set per=null where per is not null and per <= 0 and sdate='%s'" % date)
    # db_oper.execute_by_query("update prices set psr=null where per is not null and psr <= 0 and sdate='%s'" % date)
    # db_oper.execute_by_query("update prices set pcr=null where per is not null and pcr <= 0 and sdate='%s'" % date)
    # db_oper.execute_by_query("update prices set pbr=null where per is not null and pbr <= 0 and sdate='%s'" % date)
    return


def update_stock_shares():
    """
    분기 마지막 거래일의 주식수 데이터 (prices 테이블) 를 보고서 (reports 테이블) 로 복사하기
    :return:
    """
    sql = """
        with
        final_day_of_quarter as (
            select substr(sdate, 1, 6) as yyyymm, max(sdate) as fddate
            from prices
            where total_shares is not null and substr(sdate, 5, 2) in ('03', '06', '09', '12')
            group by substr(sdate, 1, 6)
        )
        select r.code, r.rdate, p.total_shares as stock_shares
        from reports r
        join companies c on r.code = c.code
        join final_day_of_quarter fd on substr(r.rdate, 1, 6) = fd.yyyymm
        join prices p on r.code = p.code and sdate = fd.fddate
    """
    df = db_oper.select_by_query(sql)
    if len(df) > 0:
        db_oper.update_table('reports', df, ['code', 'rdate'])
    return


def do_main_proc_to_update_investment_indicators():
    proc_all_q1_values()
    proc_all_q4_values()
    proc_roa_gpa()
    update_stock_shares()
    do_all_sdate_proc_pxrs()


if __name__ == "__main__":
    # proc_q1_values()
    # proc_all_q4_values()
    # proc_roa_gpa()
    # update_stock_shares()
    proc_per_psr_pcr_pbr('20080303')
    # do_all_sdate_proc_pxrs()
