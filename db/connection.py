# Функция для подулючения к БД
def connection():
    import sqlite3 as sq

    conn = sq.connect('../db/users.db')
    cur = conn.cursor()

    return conn, cur
