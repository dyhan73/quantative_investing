"""
재무제표 누락데이터 채우기
누락데이터 기준 : total_assets 가 누락된 행
누락데이터 보유 파일 :
"""

import os
import re

import pandas as pd

from field_map import dic_companies, dic_reports
import db_oper
import financial_reports as fr


def get_rdate_list():
    df = db_oper.select_by_query('select distinct rdate from reports order by rdate')
    rdate_df = df[['rdate']]
    # print(rdate_df.head())
    result = list(rdate_df.rdate)
    result.sort()
    print(result)
    return result


if __name__ == "__main__":
    reports_path = os.path.join('data', 'financial_reports')
    files = fr.get_file_list(reports_path)

    rdate_list = get_rdate_list()

    # 1. total_assets 가 누락된 row 찾기
    missing_df = db_oper.select_table('reports', 'total_assets is null or total_assets = 0')
    print(len(missing_df))
    print(missing_df.head())

    for idx, row in missing_df.iterrows():
        idx = rdate_list.index(row['rdate'])
        print(rdate_list[idx:idx+4])
        print(idx)
        break




