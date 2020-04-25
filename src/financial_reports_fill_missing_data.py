"""
재무제표 누락데이터 채우기
누락데이터 기준 : total_assets 가 누락된 행
누락데이터 보유 파일 :
"""

import os
import re

# import pandas as pd

import db_oper
import financial_reports as fr


def get_rdate_list():
    df = db_oper.select_by_query('select distinct rdate from reports order by rdate')
    rdate_df = df[['rdate']]
    # print(rdate_df.head())
    result = list(rdate_df.rdate)
    result.sort()
    # print(result)
    return result


def do_main_proc_for_financial_reports_fill_missing_data():
    # pd.set_option('display.width', None)
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_colwidth', -1)

    # 파일 목록 읽어둠
    reports_path = os.path.join('data', 'financial_reports')
    files = fr.get_file_list(reports_path)

    rdate_list = get_rdate_list()

    # 1. total_assets 가 누락된 row 찾기
    missing_df = db_oper.select_table('reports', 'total_assets is null or total_assets = 0')
    print('missing data count : ', len(missing_df))
    # print(missing_df.head())

    # 누락값을 하나씩 돌면서
    for idx, row in missing_df.iterrows():
        miss_rdate = str(row['rdate'])
        miss_yyyy = miss_rdate[:4]
        miss_mm = miss_rdate[4:6]
        miss_code = row['code']
        print('\n\n## missing data : ', miss_rdate, miss_code)

        # 누락분기 이후 4개 분기 날짜를 가져와서
        idx = rdate_list.index(row['rdate'])
        rdate_4q = rdate_list[idx:min(idx+4, len(rdate_list))]

        # 가장 최신 분기데이터부터 검색
        for rd in rdate_4q:
            rd = str(rd)
            yyyy = rd[:4]
            mm = rd[4:6]
            # print(rd, yyyy, mm)
            # fq4 = [f for f in files if re.search('reports/%s.*%s.*/' % (yyyy, mm), f)]
            fq4 = [f for f in files if re.search('%s.*%s.*' % (yyyy, mm), os.path.split(os.path.dirname(f))[1])]

            # 보고서 엑셀파일을 돌면서
            for f_report in fq4:
                dfs = fr.read_reports(f_report)

                # 각 탭을 돌면서 찾음
                for tab in dfs.keys():
                    df = dfs[tab]

                    df = fr.remove_useless_companies(df)

                    report = fr.get_reports(df, miss_yyyy, miss_mm)
                    report = fr.replace_field_name(report)
                    # print(report.head())
                    # print(report.keys())
                    report = report[report['code'] == miss_code]
                    if len(report) == 0:
                        continue
                    # print('total_assets : ', report.total_assets)
                    if report.total_assets.any() <= 0:
                        continue
                    # NaN 컬럼 삭제
                    report = report.dropna(axis=1)
                    print(f_report)
                    print('tab : ', tab)
                    print(report)
                    db_oper.update_table('reports', report, ['code', 'rdate'])
                    # break

        # break
    return


if __name__ == "__main__":
    do_main_proc_for_financial_reports_fill_missing_data()



