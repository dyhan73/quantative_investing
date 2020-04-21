import sys
import sqlite3
import pandas as pd


def read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute( query )
        names = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame( rows, columns=names)
    finally:
        if cursor is not None:
            cursor.close()


def select_table(table, where='1=1'):
    conn = sqlite3.connect("./database/quantative_investing.db")
    cursor = conn.cursor()
    try:
        cursor.execute('select * from %s where %s'%(table, where))
        names = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=names)
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def insert_table(table, df):
    # company 정보 DB Insert
    conn = sqlite3.connect("./database/quantative_investing.db")
    for idx, row in df.iterrows():
        columns = ', '.join(row.keys())
        placeholders = ', '.join('?' * len(row.values))
        sql = 'INSERT OR IGNORE INTO {} ({}) VALUES ({})'.format(table, columns, placeholders)

        try:
            conn.execute(sql, row.values)
        except sqlite3.IntegrityError:
            pass  # 이미 인서트되어 발생하는 오류 무시
        except:
            print(sys.exc_info())
            pass
    conn.commit()
    conn.close()


def update_table(table, df, keys):
    # 업데이트 항목 추출 : df.keys() - keys
    # 조건 항목 : keys
    pass


def upsert_table(table, df):
    # company 정보 DB upsert
    # replace 라서 기존 필드값이 있었으나 df 에 없는 필드의 경우 사라짐 ㅠ.ㅠ
    conn = sqlite3.connect("./database/quantative_investing.db")
    for idx, row in df.iterrows():
        columns = ', '.join(row.keys())
        placeholders = ', '.join('?' * len(row.values))
        sql = 'INSERT OR REPLACE INTO {} ({}) VALUES ({})'.format(table, columns, placeholders)

        try:
            conn.execute(sql, row.values)
        except:
            print(sys.exc_info())
            pass
    conn.commit()
    conn.close()


if __name__ == "__main__":
    df = select_table('companies')
    print(df.head())