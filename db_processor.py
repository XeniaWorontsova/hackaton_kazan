import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import sql
from uuid import uuid4
from db_config import db_name, user, password, host

def db_get_position():
    with psycopg2.connect(dbname=db_name, user=user, password=password, host=host) as conn:
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


def db_filter(position):
    with psycopg2.connect(dbname=db_name, user=user, password=password, host=host) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            result = {}
            all_worker = cursor.execute(
                sql.SQL('SELECT * FROM workers WHERE {}=(SELECT {} FROM {} WHERE name = {})').format(
                        sql.Identifier('position'), 
                        sql.Identifier('id'),
                        sql.Identifier('position'), 
                        sql.Literal(position)
                    )
            )
            all_worker = cursor.fetchall()
            id_tested_worker = cursor.execute(
                sql.SQL('SELECT DISTINCT {} FROM {}').format(sql.Identifier('worker'), sql.Identifier('worker_competencies'))
            )
            id_tested_worker = cursor.fetchall()
            id_tested_worker = [value[0] for value in id_tested_worker]
            all_worker = [dict(zip(value.keys(), value)) for value in all_worker]
            for worker in all_worker:
                index = worker['surname']+' ' + worker['name'] + ' ' + worker['patronymic']
                result[index]={}
                result[index]['phone'] = worker['phone'] if worker['phone'] else ''
                if worker['id'] in id_tested_worker:
                    result[index]['is_tested'] = True
                else:
                    result[index]['is_tested'] = False
            return result


def db_get_costing_data():
    with psycopg2.connect(dbname=db_name, user=user, password=password, host=host) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql.SQL('SELECT * FROM costing_data'))
            costing_data = cursor.fetchone()
            costing_data = dict(zip(costing_data.keys(), costing_data))
            return costing_data


def db_set_costing_data(vacancy_announcement_costs, payment_for_agency_services, reference_bonus, hr_salary_costs):
    with psycopg2.connect(dbname=db_name, user=user, password=password, host=host) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql.SQL('UPDATE costing_data SET {} = {}, {} = {}, {} = {}, {} = {}').format(
                sql.Identifier('vacancy_announcement_costs'),
                sql.Literal(vacancy_announcement_costs),
                sql.Identifier('payment_for_agency_services'),
                sql.Literal(payment_for_agency_services),
                sql.Identifier('reference_bonus'),
                sql.Literal(reference_bonus),
                sql.Identifier('hr_salary_costs'),
                sql.Literal(hr_salary_costs)
            )
        )


def db_get_scill_vacansies():
    with psycopg2.connect(dbname=db_name, user=user, password=password, host=host) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql.SQL('SELECT * FROM {}').format(
                    sql.Identifier('vacancies_competencies')
                )
            )
            vac_skill = cursor.fetchall()
            vac_skill = [dict(zip(value.keys(), value)) for value in vac_skill]
            for value in vac_skill:
                cursor.execute(sql.SQL('SELECT name FROM {} WHERE id={}').format(
                        sql.Identifier('vacancies'),
                        sql.Literal(value['vacancies'])
                    )
                )
                value['vacancies'] = cursor.fetchone()[0]
                cursor.execute(sql.SQL('SELECT name FROM {} WHERE id={}').format(
                        sql.Identifier('competencies'),
                        sql.Literal(value['competence'])
                    )
                )
                value['competence'] = cursor.fetchone()[0]
            result = {}
            for value in vac_skill:
                vacancie = value['vacancies']
                if vacancie not in result:
                    result[vacancie] = {'competence':{}, 'sum':0}
                
                result[vacancie]['competence'][value['competence']] = value['point']
                result[vacancie]['sum'] += value['point']
            return result


def db_get_scill_worker():
    with psycopg2.connect(dbname=db_name, user=user, password=password, host=host) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql.SQL('SELECT * FROM {}').format(
                    sql.Identifier('worker_competencies')
                )
            )
            vac_skill = cursor.fetchall()
            vac_skill = [dict(zip(value.keys(), value)) for value in vac_skill]
            for value in vac_skill:
                cursor.execute(sql.SQL('SELECT surname, name, patronymic  FROM {} WHERE id={}').format(
                        sql.Identifier('workers'),
                        sql.Literal(value['worker'])
                    )
                )
                worker = cursor.fetchone()
                value['worker'] = worker['surname']+' '+worker['name']+' '+worker['patronymic']
                cursor.execute(sql.SQL('SELECT name FROM {} WHERE id={}').format(
                        sql.Identifier('competencies'),
                        sql.Literal(value['competencies'])
                    )
                )
                value['competencies'] = cursor.fetchone()[0]
            result = {}
            for value in vac_skill:
                worker = value['worker']
                if worker not in result:
                    result[worker] = {'competence':{}, 'vacancies':{}}
                
                result[worker]['competence'][value['competencies']] = value['point']
                
            return result


