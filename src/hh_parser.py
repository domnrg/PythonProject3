import requests


class HHParser:

    def get_employers(self):
        params = {"sort_by": "by_vacancies_open", "per_page": 10}
        response = requests.get("https://api.hh.ru/employers", params=params)
        response.raise_for_status()
        data = response.json()["items"]
        employers = []
        for employer in data:
            employers.append(
                {"id": employer["id"], "name": employer["name"], "open_vacancies": employer["open_vacancies"]}
            )
        return employers

    def get_vacancies_by_employer_id(self, employer_id):
        vacancies = []

        while True:
            params = {"employer_id": employer_id, "per_page": 50}
            response = requests.get("https://api.hh.ru/vacancies", params=params)
            response.raise_for_status()
            data = response.json()

            for vacancy in data["items"]:
                salary_from = 0
                salary_to = 0
                if vacancy["salary"]:
                    salary_from = vacancy["salary"]["from"] or 0
                    salary_to = vacancy["salary"]["to"] or 0

                vacancies.append(
                    {
                        "id": vacancy["id"],
                        "name": vacancy["name"],
                        "salary_from": salary_from,
                        "salary_to": salary_to,
                        "url": vacancy["alternate_url"],
                        "area": vacancy["area"]["name"],
                        "published_at": vacancy["published_at"],
                        "experience": vacancy["experience"]["name"],
                    }
                )

            return vacancies
