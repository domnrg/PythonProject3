import time

import psycopg2
from config import config
from src.hh_parser import HHParser


def create_database(db_name):
    """Создает базу данных"""
    params = config()
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()


def create_tables(db_name):
    """Создает таблицы работодателей и вакансий"""
    params = config()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS employers ("
                "id VARCHAR PRIMARY KEY,"
                "name VARCHAR(255) NOT NULL,"
                "open_vacancies INT)"
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    id VARCHAR PRIMARY KEY,
                    name TEXT NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    url TEXT,
                    area TEXT,
                    published_at TIMESTAMP,
                    experience TEXT,
                    employer_id VARCHAR REFERENCES employers(id)
                )
            """
            )
    conn.close()


def insert_employers(db_name):
    """Заполняет созданные таблицы данными о работодателях"""
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    params = config()
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute(
                    "INSERT INTO employers VALUES (%s, %s, %s)",
                    (employer["id"], employer["name"], employer["open_vacancies"]),
                )
    conn.close()


def insert_vacancies(db_name):
    """Заполняет созданные таблицы данными о вакансиях"""
    hh_parser = HHParser()
    employers = hh_parser.get_employers()
    params = config()

    try:
        with psycopg2.connect(dbname=db_name, **params) as conn:
            with conn.cursor() as cur:
                for employer in employers:
                    try:
                        vacancies = hh_parser.get_vacancies_by_employer_id(employer["id"])
                        for vacancy in vacancies:
                            try:
                                cur.execute(
                                    """
                                    INSERT INTO vacancies
                                    (id, name, salary_from, salary_to, url, area, published_at, experience, employer_id)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (id) DO NOTHING
                                    """,
                                    (
                                        vacancy["id"],
                                        vacancy["name"],
                                        vacancy["salary_from"],
                                        vacancy["salary_to"],
                                        vacancy["url"],
                                        vacancy["area"],
                                        vacancy["published_at"],
                                        vacancy["experience"],
                                        employer["id"],
                                    ),
                                )
                            except Exception as e:
                                print(f"Ошибка при вставке вакансии {vacancy['id']}: {e}")
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"Ошибка при получении вакансий работодателя {employer['id']}: {e}")
    except Exception as conn_err:
        print(f"Ошибка при подключении к БД: {conn_err}")
