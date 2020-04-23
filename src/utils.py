import calendar
from datetime import datetime, timedelta


def get_yyyymmdd(yyyy, mm):
    dd = '31'
    if mm in ('06', '09'):
        dd = '30'
    return '%s%s%s' % (yyyy, mm, dd)


def get_latest_meaningful_report_day(date):
    """
    거래일을 입력받아 참고할 보고서 작성일 구하기
    예) 1~3월 중 거래일 -> 전년 9월 보고서, 4~6월 -> 전년 12월 보고서, 7~9월 -> 당년 3월 보고서, 10~12월 -> 당년 6월 보고서
    :param date:
    :return:
    """
    curr_yyyy = date[:4]
    curr_mm = date[4:6]
    rep_yyyy = None
    rep_mm = None
    # print(curr_yyyy, curr_mm, date)
    if curr_mm in ('01', '02', '03'):
        return '%s0930' % (int(curr_yyyy) - 1)
    elif curr_mm in ('04', '05', '06'):
        return '%s1231' % (int(curr_yyyy) - 1)
    elif curr_mm in ('07', '08', '09'):
        return '%s0331' % curr_yyyy
    elif curr_mm in ('10', '11', '12'):
        return '%s0630' % curr_yyyy


def get_prev_report_day(report_date):
    """
    분기 보고서 작성일 (분기 마지막날짜) 을 입력받아 이전 분기 보고서 작성일 구하기
    :param report_date: 분기 보고서 작성일
    :return:
    """
    dt = datetime.strptime(report_date, '%Y%m%d')
    prev_dt = dt - timedelta(days=95)
    last_day = calendar.monthrange(prev_dt.year, prev_dt.month)[1]
    prev_dt = prev_dt.replace(day=last_day)
    return prev_dt.strftime('%Y%m%d')


def get_report_days_of_year(report_date):
    """
    분기 보고서 작성일 (분기 마지막날짜) 을 입력받아 이전 4개 분기 보고서 작성일 리스트 구하기
    :param report_date: 분기 보고서 작성일
    :return: 이전 4개 분기 보고서 작성일 리스트
    """
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

    print(get_latest_meaningful_report_day('20190122'))
    print(get_latest_meaningful_report_day('20190222'))
    print(get_latest_meaningful_report_day('20190322'))
    print(get_latest_meaningful_report_day('20190422'))
    print(get_latest_meaningful_report_day('20190522'))
    print(get_latest_meaningful_report_day('20190622'))
    print(get_latest_meaningful_report_day('20190722'))
    print(get_latest_meaningful_report_day('20190822'))
    print(get_latest_meaningful_report_day('20190922'))
    print(get_latest_meaningful_report_day('20191022'))
    print(get_latest_meaningful_report_day('20191122'))
    print(get_latest_meaningful_report_day('20191222'))
    return