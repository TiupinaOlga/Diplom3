from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import acces_token, comunity_token
from core import VkTools
from db import create_tables, drop_tables


class BotInterface:

    def __init__(self,token):
        self.bot = vk_api.VkApi(token=token)

    """Функция для отправки сообщения пользователю"""
    def message_send(self, user_id, message, attachment=None):
        self.bot.method('messages.send',
                  {'user_id': user_id,
                   'message': message,
                   'attachment': attachment,#медиавложения
                   'random_id': randrange(10 ** 7)},)

    """Функция для отправки профилей найденных пользователей"""
    def print_profiles(self, user_id, profiles):
        for profile in profiles:
            profile_id = f"@id{profile['id']}({profile['name']})" #ссылка на профиль
            photos = self.tools.photos_get(profile['id']) #получение списка фото у пользователя
            if photos:
                for photo in photos:
                    media = photo['media']
                    self.message_send(user_id, f'{profile_id}', media)
            else:
                self.message_send(user_id, f'{profile_id} у данного пользователя нет фото')

    """Функция для обработки действий пользователя"""
    def handler(self):

        longpoll = VkLongPoll(self.bot)
        context='one'

        for event in longpoll.listen(): #эхо
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text #полученый текст от пользователя в чате

                self.tools = VkTools(acces_token)

                if context == 'one':
                    if request.lower() == "привет":
                        info = self.tools.get_profile_info(event.user_id)  # информация о пользователе
                        age = self.tools.get_age(event.user_id)  # вычислить возраст
                        sex = self.tools.get_sex_for_search(event.user_id)  # вычислить противоположный пол
                        city_id = self.tools.get_city_id(event.user_id)  # id города для поиска
                        self.message_send(event.user_id,
                                          f"Привет, {info[0]['first_name']}!  Я чат-бот VKinder\n"
                                          f"Я могу осуществить поиск подходящей пары для тебя\n"
                                          f"Критерии: город, возраст в промежутке +/- 3 года от твоего возраста\n"
                                          f"Для начала поиска введите: поиск\n"
                                          )

                    elif request.lower() == "поиск":
                        if city_id == 0 or age == 0 or sex == 0:
                            if city_id == 0:
                                context = 'city_add'
                                self.message_send(event.user_id, 'Введите дополнительную информацию для поиска - город:')
                            else:
                                if age == 0:
                                    context = 'age_add'
                                    self.message_send(event.user_id, 'Введите дополнительную информацию для поиска - возраст:')
                                else:
                                    if sex == 0:
                                        context = 'add_sex'
                                        self.message_send(event.user_id,'Введите дополнительную информацию для поиска - пол(м/ж):')
                        else:
                            age_from = age - 3
                            age_to = age + 3
                            profiles = self.tools.user_search(city_id,age_from,age_to,sex,6,offset=0) #получили список пользователей подходящих по поиску
                            self.print_profiles(event.user_id, profiles)

                    elif request.lower() == "далее":
                        pass

                    elif request.lower() == "пока":
                        self.message_send(event.user_id, "Спасибо за использование чат-бота. Пока!")

                    else:
                        self.message_send(event.user_id, "Не поняла вашего ответа...")

                elif context == 'city_add':
                    city_name = request.lower()
                    city_id = self.tools.search_city_id(city_name)
                    # print(city_id)
                    context = 'one'
                    self.message_send(event.user_id, 'Введите для продолжения: поиск')

                elif context == 'age_add':
                    age = request.lower()
                    context = 'one'
                    self.message_send(event.user_id, 'Введите для продолжения: поиск')

                elif context == 'add_sex':
                    sex = request.lower()
                    if sex == 'ж':
                        sex = 2
                        context = 'one'
                        self.message_send(event.user_id, 'Введите для продолжения: поиск')
                    elif sex == 'м':
                        sex =1
                        context = 'one'
                        self.message_send(event.user_id, 'Введите для продолжения: поиск')
                    else:
                        self.message_send(event.user_id, "Не поняла вашего ответа...")
                    context = 'one'

if __name__ == '__main__':
    bot = BotInterface(comunity_token)
    bot.handler()