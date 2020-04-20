import sys
import sqlite3


def get_rows_of_talbe(table):
    # 인서트 전 row 수
    conn = sqlite3.connect("./database/quantative_investing.db")
    cur = conn.cursor()
    cur.execute("select count(*) from %s" % table)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    companies_db_before = rows[0][0]
    print(rows)


def insert_table(table, df):
    # company 정보 DB Insert
    conn = sqlite3.connect("./database/quantative_investing.db")
    for idx, row in df.iterrows():
        columns = ', '.join(row.keys())
        placeholders = ', '.join('?' * len(row.values))
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, columns, placeholders)

        try:
            conn.execute(sql, row.values)
        except sqlite3.IntegrityError:
            pass  # 이미 인서트되어 발생하는 오류 무시
        except:
            print(sys.exc_info())
            pass
    conn.commit()
    conn.close()


def upsert_table(table, df):
    # company 정보 DB upsert
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

