import psycopg2
import random
from psycopg2.extras import DictCursor
from psycopg2 import sql
from uuid import uuid4


competencies = ['4b2f78b2-d5ac-4be5-a234-c8e02a131b47', '5be5f3a4-5e91-4a16-9b5f-c048a72cc39d', '6486bb7a-7224-44db-bd2f-4480cc7ff7d0', '3aa74950-2e81-4a45-9d50-b51cfb298f30', '9fada050-0342-477c-b46d-a686054d5128', '5a6f6dcb-c3ec-4d6d-904b-c732c78483d9','cd79b74b-3158-4e8f-9d65-18d6f842c6b7','a8e5052a-26a9-47fd-bbf6-934d1a998246','e53a06d1-a85d-472d-8119-2bc6c369d0eb','8924c5e7-c6c6-4771-88d6-b5adae861ce7', '6fb09a36-10e9-4df0-a7b1-c599b31ef2eb', '45dbabc1-00b1-4748-a9ad-3340f215e70c', 'd321092a-8e7c-4488-91d0-ebe98a15ff5d', '877ccb25-7701-4600-8ac9-13da131be869','6fe83293-5821-446e-a230-da4a1c4a3a64','32673168-989d-4a52-8a9a-0e1ba00dda0c','a967e59a-8ba4-4bb5-a84e-ce762be9a8da','032cd9f2-0dcf-49ff-bc3a-86d747a315aa','1a8b9992-1131-4251-8840-2ea6df857f74','c216dbfe-856b-434c-92d1-7ee2d8b3d7af','327c231d-87f5-4fc2-917f-3e131e12b472','d2758dc2-15d7-41f8-871e-86c56bf439cd']
def insert():
    with psycopg2.connect(dbname='hackaton', user='postgres', password='postgres', host='127.0.0.1') as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            workers = ['ae91e78a-169b-4636-bfb7-3966240af424','9d39670d-56a9-4087-ae6f-a53cb9d8c8bf','18f20368-3822-42bb-997d-a58d091dd810']
            for worker in workers:
                for vacansy in competencies:
                    uuid = str(uuid4())
                    point =  random.randint(0,5)
                    my_sql = sql.SQL('INSERT INTO worker_vacancies values ({}, {}, {}, {})').format(
                        sql.Literal(uuid),
                        sql.Literal(worker),
                        sql.Literal(vacansy),
                        sql.Literal(point)
                    )
                    cursor.execute(my_sql)


insert()