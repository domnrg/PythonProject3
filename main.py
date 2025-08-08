from src.utils import create_tables, create_database, insert_employers, insert_vacancies
from src.db_manager import DBManager

db_name = "course5"
create_database(db_name)
create_tables(db_name)
insert_employers(db_name)
insert_vacancies(db_name)


def user_interaction():
    """Основная функция взаимодействия с пользователем."""
    db_manager = DBManager(db_name)
    while True:
        print("\n1: Вывести список всех компаний и количество вакансий у каждой компании")
        print("2: Вывести список всех вакансий с названием компании, вакансией, зарплатой и ссылкой")
        print("3: Вывести среднюю зарплату по вакансиям")
        print("4: Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("5: Вывести список всех вакансий, в названии которых содержатся ключевое слово")
        print("0: Выйти")
        choice = input("Введите номер действия: ")

        if choice == "1":
            vacancies = db_manager.get_companies_and_vacancies_count()
            for name, total in vacancies:
                print(f"\n{name} - {total}")

        elif choice == "2":
            vacancies = db_manager.get_all_vacancies()
            for vac in vacancies:
                company, name, salary_from, salary_to, url = vac
                print(f"\nКомпания: {company}")
                print(f"Вакансия: {name}")
                print(f"Зарплата: от {salary_from or 'не указано'} до {salary_to or 'не указано'}")
                print(f"Ссылка: {url}")

        elif choice == "3":
            avg = db_manager.get_avg_salary()
            if avg:
                print(f"\nСредняя зарплата: {round(avg, 2)}")
            else:
                print("\nНет данных для расчёта средней зарплаты.")

        elif choice == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for name, salary in vacancies:
                print(f"\nВакансия: {name}")
                print(f"Зарплата: {salary}")

        elif choice == "5":
            keyword = input("Введите слово: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vac in vacancies:
                name, salary_from, salary_to, url = vac
                print(f"Вакансия: {name}")
                print(f"Зарплата: от {salary_from or 'не указано'} до {salary_to or 'не указано'}")
                print(f"Ссылка: {url}")

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
