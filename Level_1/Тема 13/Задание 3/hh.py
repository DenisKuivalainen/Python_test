"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import requests
import exceptions


class Hh:

    @staticmethod
    def _get_area_id(area):

        def get_area(areas, name):
            """Вернуть ID города 'name' из структуры 'areas'."""
            for item in areas:
                if "name" in item and item["name"] == name:
                    return int(item["id"])
                if "areas" in item and item["areas"]:
                    res = get_area(item["areas"], name)
                    if res:
                        return res

        api_url = "https://api.hh.ru/areas"
        params = dict(area_id=1)
        areas = requests.get(api_url, params).json()

        if "errors" in areas:
            raise exceptions.HhException(
                "Такого региона не существует!")

        area_id = get_area(areas, area)

        if not area_id:
            raise exceptions.HhException(
                "Такого региона не существует!")

        return area_id

    @staticmethod
    def _get_experience_id(experience):
        if isinstance(experience, float):
            raise ValueError(
                "\"experience\" не является целыми положительным числом.")
        if not(experience is None) and experience < 0:
            raise ValueError(
                "\"experience\" не является целыми положительным числом.")

        if experience is None or experience == 0:
            return "noExperience"
        elif experience >= 1 and experience < 3:
            return "between1And3"
        elif experience >= 3 and experience < 6:
            return "between3And6"
        elif experience >= 6:
            return "moreThan6"

    @staticmethod
    def search(title, area, salary=None, experience=None):
        params = dict(text=title, search_field="name", per_page=10)
        area = Hh._get_area_id(area)
        if area:
            params.update(area=area)
        if salary:
            params.update(salary=salary)
        params.update(experience=Hh._get_experience_id(experience))

        res = []

        api_url = "https://api.hh.ru/vacancies"
        vacancies = requests.get(api_url, params).json()

        for i, vacancy in enumerate(vacancies["items"]):
            vacancy.update({'id': i + 1})
            res.append(vacancy)

        return res
