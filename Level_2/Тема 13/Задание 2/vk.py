"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import requests
import time
import matplotlib.pyplot as plt


class VK:
    """Класс VK получает информацию о друзьях в ВК,
    создает столбчатую диаграмму по количеству друзей в городах
    """

    FIELDS = ("user_id", "first_name", "last_name", "city")

    def __init__(self, user_id, token):
        """Инициализация класса
        Свойства:
            - self._user_id - ид пользователя
            - self._token - токен
            - self._data - информация о друзьях в ВК
        """
        assert isinstance(user_id, int),\
            "Ид пользователя должен быть типа 'int'"
        assert isinstance(token, str),\
            "Токен должен быть типа 'str'"

        self._user_id = user_id
        self._token = token
        self._data = []

        self._get_data()

    def __str__(self):
        """Возвращает строковое представление информации о друзьях"""
        string = "Список друзей({}):".format(len(self._data))
        string += "\n{0:11}{1:15}{2:15}{3:15}{4}".format(VK.FIELDS[0],
                                                         VK.FIELDS[1],
                                                         VK.FIELDS[2],
                                                         VK.FIELDS[3],
                                                         VK.FIELDS[4])
        for i in self._data:
            string += "\n{0:11}{1:15}{2:15}{3:15}{4}".\
                      format(str(i[VK.FIELDS[0]]), i[VK.FIELDS[1]],
                             i[VK.FIELDS[2]], i[VK.FIELDS[3]],
                             i[VK.FIELDS[4]])
        fio, value = self.most_common_friends()
        string += "\nДруг, с которым больше всего общих знакомых:"
        string += "\n Ф.И.О. - {}\n Кол-во общих друзей - {}".format(fio,
                                                                     value)
        fio, value = self.most_popular_friend()
        string += "\nСамый популярный друг:"
        string += "\n Ф.И.О. - {}\n Кол-во друзей - {}".format(fio, value)
        return(string)

    def _get_data(self):
        """Получает данные о друзьях"""
        data = []
        method_url = 'https://api.vk.com/method/friends.get?'
        dct = dict(access_token=self._token, user_id=self._user_id,
                   fields=('city'), name_case="nom")
        r = requests.post(method_url, dct)
        result = r.json()
        assert not result.get("error", None), "Произошла ошибка при"\
            " выполнении friends.get! Код ошибки"\
            " - {}".format(result["error"]["error_code"])
        data = result['response']
        for i in data:
            dct = {}
            for field in i:
                if field in VK.FIELDS:
                    dct[field] = i[field]



            dct["city"] = self._get_city(dct["city"])
            time.sleep(0.2)
            self._data.append(dct)

    def _get_city(self, city):
        """Возвращает название города по id"""
        if not city:
            return "None"
        try:
            method_url = 'https://api.vk.com/method/database.getCitiesById?'
            dct = dict(access_token=self._token, city_ids=city)
            r = requests.post(method_url, dct)
            result = r.json()
            assert not result.get("error", None), "Произошла ошибка при"\
                " выполнении database.getCitiesById! Код ошибки"\
                " - {}".format(result["error"]["error_code"])
        except AssertionError as err:
            print(err)
            return "None"
        return result['response'][0]['name']

    def most_common_friends(self):
        """Возвращает друга с наибольшим количеством общих друзей"""
        method_url = "https://api.vk.com/method/friends.getMutual?"
        data = []
        for i in self._data:
            try:
                dct = dict(access_token=self._token, target_uid=i["user_id"])
                r = requests.post(method_url, dct)
                result = r.json()
                assert not result.get("error", None), "Произошла ошибка при"\
                    " выполнении friends.getMutual! Код ошибки"\
                    " - {}".format(result["error"]["error_code"])
                time.sleep(0.3)
                fio = ' '.join([i['first_name'], i['last_name']])
                data.append((fio, len(result["response"])))
            except AssertionError as err:
                print(err)
        data.sort(key=lambda x: x[1])
        return data[-1]

    def most_popular_friend(self):
        """Возвращает самого популярного друга"""
        data = []
        for i in self._data:
            try:
                method_url = 'https://api.vk.com/method/friends.get?'
                dct = dict(access_token=self._token, user_id=i['user_id'],
                           name_case="nom")
                r = requests.post(method_url, dct)
                result = r.json()
                assert not result.get("error", None), "Произошла ошибка при"\
                    " выполнении friends.get! Код ошибки"\
                    " - {}".format(result["error"]["error_code"])
                time.sleep(0.3)
                fio = ' '.join([i['first_name'], i['last_name']])
                data.append((fio, len(result['response'])))
            except AssertionError as err:
                print(err)
        data.sort(key=lambda x: x[1])
        return data[-1]

    def _make_plot(self):
        """Генерирует изображение, не отображая его"""
        assert len(self._data) > 0, "Нет данных для вывода!"

        fig, ax = plt.subplots()
        fig.canvas.set_window_title("Количество друзей из ВК в городах")

        ax.set_title("Количество друзей из ВК в городах")

        ax.set_xlabel("Количество(чел.)")
        lst = [i["city"] for i in self._data]
        city = {i: lst.count(i) for i in lst}

        tick_label = list(city.keys())
        size = list(city.values())
        nums = [x + 1 for x in range(len(size))]
        ax.barh(nums, size, tick_label=tick_label)
        return fig

    def show_plot(self):
        """Создать изображение и показать его на экране."""
        self._make_plot()
        plt.show()
