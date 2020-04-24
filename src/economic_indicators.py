import copy
import utils

import pandas as pd
import numpy as np

import db_oper


def refine_column_footer(df):
    # Footer 첫햇의 첫 컬럼은 '출처:' 로 시작함
    footer_index = df[df['Unnamed: 0'] == '출처:'].index[0]
    df = df.iloc[:footer_index]
    # print(df)

    # 전체가 Nan 인 컬럼 제거
    df = df.dropna(how='all', axis=1)
    # 첫 열에 NaN 은 이전 값 가져와야함
    df[df.columns[0]] = df[df.columns[:1]].fillna(method='ffill')
    # print(df)

    # 2열이 보조지표명 (Unnamed: 로 시작) 이면 1열과 병합
    if df.columns[1].startswith('Unnamed:'):
        # df[df.columns[:2]] = df[df.columns[:2]].fillna('')
        df[df.columns[0]] = df[df.columns[0]] + '-' + df[df.columns[1]]
        df[df.columns[0]] = df[df.columns[0]].str.replace('\(%\)', '')
        del (df[df.columns[1]])

    # 컬럼명 정제 (년/월/일 구분)
    keys = [k for k in df.keys()]
    keys[0] = 'Indicator'
    df.columns = keys
    # print(df)
    return df


def insert_indicators_to_db(df, fv_dic):
    """
    db insert
    :param df:
    :param fv_dic:
    :return:
    """
    for idx, row in df.iterrows():
        # print(row.keys())
        dicts = copy.copy(fv_dic)
        # print(dicts)
        for col in row.keys():
            if col == 'Indicator':
                dicts['indicator'] = row[col].replace('\xa0', '')
                continue
            # 컬럼명에서 YYYY, QMM 가져오기
            dicts['year'] = int(col[:4])
            if dicts['term'] == 'M':
                dicts['qmm'] = int(col[4:6])
            elif dicts['term'] == 'Q':
                dicts['qmm'] = int(col[4:5])
            # 숫자값 채우기
            if type(row[col]) == str:
                row[col] = row[col].replace(',', '')
                if row[col] == '-':
                    row[col] = np.nan
            dicts['value'] = float(row[col])

            db_oper.insert_dict('indicators', dicts)
            # break
        # break


def do_main_proc_to_update_economic_indicators():
    files = utils.get_file_list('data/economic_indicators')
    for f in files:
        print('File name : ' + f)
        # 파일명에서 필요 정보 추출 (분류, 기간, 단위 등)
        vals = f.split('/')[-1:][0].split('.')[0].split('_')
        fv_dic = dict(zip(['category', 'term', 'lastdate', 'unit'], vals))
        del(fv_dic['lastdate'])

        df = pd.read_excel(f, header=[2])
        df = refine_column_footer(df)
        insert_indicators_to_db(df, fv_dic)
        # break


if __name__ == "__main__":
    do_main_proc_to_update_economic_indicators()
