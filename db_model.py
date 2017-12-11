import mysql.connector
import json
import numpy as np
import globalVar


def connect2Mysql():
    conn = mysql.connector.connect(
        user='root', password='as56210', database='flow3', use_unicode=True)
    cursor = conn.cursor()
    return conn, cursor


def fetch_entry_untreated(version=0):
    conn, cursor = connect2Mysql()
    cursor.execute(
        'select * from t_item where version = %s limit 0,1', (version,))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(values) == 0:
        print('||||||||||||||没有读取到|||||||||||||')
        return False
    else:
        print('||||||||||||||读取到一条未运算的文章|||||||||||||')
        return values[0]


def mark_entry_as_treated(entryId, version=0):
    newVersion = version + 1
    conn, cursor = connect2Mysql()
    cursor.execute('update t_item set version = %s where id = %s', [
                   newVersion, entryId])
    insert_id = cursor.lastrowid
    conn.commit()
    cursor.close()
