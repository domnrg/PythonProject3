import psycopg2

from config import config


class DBManager:
    def __init__(self, db_name):
        self.__db_name = db_name

    def __execute_query(self, query, params=None):
        """Выполняет SQL-запрос к базе данных и возвращает результат"""
        config_params = config()
        with psycopg2.connect(dbname=self.__db_name, **config_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall()
        return result

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        query = """
        SELECT employers.name AS company_name,
               COUNT(vacancies.id) AS total_vacancies
        FROM employers
        JOIN vacancies ON vacancies.employer_id = employers.id
        GROUP BY employers.name
        ORDER BY total_vacancies DESC;
    """
        return self.__execute_query(query)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, вакансии и зарплаты и ссылки на вакансию"""
        query = """
            SELECT employers.name AS company_name,
                   vacancies.name AS vacancy_name,
                   vacancies.salary_from,
                   vacancies.salary_to,
                   vacancies.url
            FROM vacancies
            JOIN employers ON vacancies.employer_id = employers.id
        """
        return self.__execute_query(query)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        query = "SELECT AVG(salary_from) FROM vacancies"
        result = self.__execute_query(query)
        return result[0][0] if result and result[0][0] is not None else 0

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query = """
            SELECT name, salary_from
            FROM vacancies
            WHERE salary_from IS NOT NULL
            AND salary_from > (SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL)
            ORDER BY salary_from DESC
        """
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = f"""
                SELECT name, salary_from, salary_to, url
                FROM vacancies
                WHERE name ILIKE '%{keyword}%'
            """
        return self.__execute_query(query)
