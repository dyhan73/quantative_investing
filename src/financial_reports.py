"""
재무제표 Excel 파일 정제 및 Database Insert 수행
"""

import os
import re

import pandas as pd

from field_map import dic_companies, dic_reports
import db_oper


def get_yyyy_mm(path):
    # regex = re.compile(r'(....)년(..)월확정실적')
    regex = re.compile(r'/(\d\d\d\d).*(\d\d).*/')
    m = regex.search(path)
    return m[1], m[2]


def get_yyyymmdd(yyyy, mm):
    dd = '31'
    if mm in ('06', '09'):
        dd = '30'
    return '%s%s%s' % (yyyy, mm, dd)


def read_reports(file_path=None, ):
    if file_path is None:
        print("Excel file path is needed.")
        return None

    yyyy, mm = get_yyyy_mm(file_path)
    if '%s%s' % (yyyy, mm) >= '201812':
        report_list = pd.read_excel(file_path, sheet_name=None, header=[1, 2])
        for key in report_list:
            report = report_list[key]
            columns = [t[0] if str(t[1]).startswith('Unnamed') else "%s-%s" % (t[0].replace('\n', ''), t[1]) for t in
                       report.keys()]
            report.columns = columns
    else:
        report_list = pd.read_excel(file_path, sheet_name=None)
        for key in report_list:
            report = report_list[key]
            columns = report.keys()
            columns = [t if type(t) is str else "nonStringKey" for t in columns]
            columns = [t.replace('\n', '') for t in columns]
            columns = [t.replace(' ', '') for t in columns]
            report.columns = columns

    return report_list


def get_file_list(root):
    dirs = [root]
    files = []

    while len(dirs) > 0:
        path = dirs.pop(0)
        # print(path)

        for f in os.listdir(path):
            full_file_path = os.path.join(path, f)

            if os.path.isdir(full_file_path):  # and f.startswith('2009년12월'):
                dirs.append(full_file_path)
            elif os.path.isfile(full_file_path) \
                    and f.startswith('20') \
                    and 'Eng' not in f \
                    and 'Rank' not in f \
                    and 'ENG' not in f \
                    and '영문' not in f \
                    and 'hwp' not in f \
                    and 'txt' not in f \
                    and 'zip' not in f:
                files.append(full_file_path)
    files.sort(reverse=True)
    return files


def get_reports(reports, yyyy, mm):
    if '%s%s' % (yyyy, mm) >= '201812':
        return get_reports_after_201812(reports, yyyy, mm)
    else:
        return get_reports_before_201809(reports, yyyy, mm)


def get_reports_after_201812(reports, yyyy, mm):
    # 필요한 필드만 추출
    cols = ('종목코드', '자산총계', '유동자산', '자본총계', '부채총계',
            '매출액-', '매출원가', '매출총이익', '영업이익(보고서기재)',
            '당기순이익', '영업활동으로인한현금흐름', '부채비율')
    reports = reports[[k for k in reports.keys() if k.startswith(cols) and '비교' not in k and '3개월' not in k]]
    reports = reports[[k for k in reports.keys() if '-' not in k or '%s%s' % (yyyy, mm) in k]]
    reports['종목코드'] = reports['종목코드'].str[1:]

    reports.insert(1, 'rdate', get_yyyymmdd(yyyy, mm))

    # 필드명 정제
    cols = reports.keys()
    cols = [re.sub('-%s%s' % (yyyy, mm), '', k) for k in cols]
    cols = [re.sub('\(.*\)', '', k) for k in cols]  # (보고서기재) 제거
    cols = [re.sub('활동으로인한', '', k) for k in cols]  # 영업현금흐름 으로 정제
    cols = [re.sub('/누적', '', k) for k in cols]  # 201906/누적 => 201906 으로 정제
    reports.columns = cols

    for field in reports.keys():
        if field.endswith('율') or field in ('종목코드', 'rdate'):
            continue
        reports[field] = reports[field] / 1000  # 천원단위를 백만원단위로 변경

    return reports


def get_reports_before_201809(reports, yyyy, mm):
    cols = tuple(dic_reports.keys())
    reports = reports[[k for k in reports.keys() if k.startswith(cols) and '3개월' not in k]]
    cols = [k for k in reports.keys() if '(' not in k]
    cols = cols + [k for k in reports.keys() if '%s%s' % (yyyy, mm) in k]
    reports = reports[cols]
    reports['코드'] = reports['코드'].str[1:]

    reports.insert(1, 'rdate', get_yyyymmdd(yyyy, mm))

    # 필드명 정제
    cols = reports.keys()
    cols = [re.sub('누적', '', k) for k in cols]  # (보고서기재) 제거
    cols = [re.sub('\(%s%s\)' % (yyyy, mm), '', k) for k in cols]
    reports.columns = cols
    return reports


def remove_useless_companies(df):
    df = df[df['회사명'].str.len() > 0]
    df = df[~df['회사명'].str.contains('스팩')]
    df = df[~df['회사명'].str.endswith('우')]
    df = df[~df['회사명'].str.endswith('우B')]
    return df


def compare_fields(file_name):
    tabs = read_reports(file_name)
    print("%s, %s" % (file_name, tabs.keys()))


def get_companies(report, yyyy, mm):
    columns = [key for key in report.keys() if key in dic_companies]
    companies = report[columns]
    columns = [dic_companies[key] for key in columns]
    companies.columns = columns

    companies.loc[:, 'code'] = companies['code'].str[1:]

    return companies


def replace_field_name(df):
    dics = {}
    dics.update(dic_companies)
    dics.update(dic_reports)
    keys = df.keys()
    keys2 = [dics[k] if k in dics else k for k in keys]
    print(keys2)
    df.columns = keys2
    df = df[[k for k in df.keys() if k in dics.values()]]
    df.head()
    return df


if __name__ == "__main__":
    # reports_path = os.path.join(os.getcwd(), 'data', 'financial_reports')
    # reports_path = os.path.join('..', 'data', 'financial_reports')
    reports_path = os.path.join('data', 'financial_reports')
    files = get_file_list(reports_path)

    for f in files:
        print("processing file : ", f)
        yyyy, mm = get_yyyy_mm(f)

        report_list = read_reports(f)
        print("Tabs : ", report_list.keys())

        # 실적요약 탭은 제거
        if '실적요약' in report_list.keys():
            del(report_list['실적요약'])

        # 주재무제표 또는 전체가 있으면 그것만 쓰자
        if '주재무제표' in report_list.keys() or '전체' in report_list.keys():
            keys = list(report_list.keys())
            for key in keys:
                if key not in ('주재무제표', '전체'):
                    del(report_list[key])
        print("after del Tabs : ", report_list.keys())
        # continue

        for key in report_list:
            print("Working tab : ", key)

            df = report_list[key]
            print(df.keys())
            df = remove_useless_companies(df)

            company = get_companies(df, yyyy, mm)
            print(company.head())
            print(company.keys())
            db_oper.insert_table('companies', company)

            report = get_reports(df, yyyy, mm)
            report = replace_field_name(report)
            print(report.head())
            print(report.keys())
            db_oper.upsert_table('reports', report)
            # break

        # break
