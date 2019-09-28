import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import sql
from uuid import uuid4

def db_get_position():
    with psycopg2.connect(dbname='hackaton', user='postgres', password='postgres', host='127.0.0.1') as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            select_position = sql.SQL('SELECT DISTINCT {}, {} FROM {}, (SELECT count({}) FROM {} group by {}) as count').format(
                sql.Identifier('name'),
                sql.Identifier('count'),
                sql.Identifier('position'),
                sql.Identifier('position'),
                sql.Identifier('workers'),
                sql.Identifier('position')
            )
            cursor.execute(select_position)
            return cursor.fetchall()
