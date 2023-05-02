import datetime

import vk_api
from config import acces_token
from vk_api.exceptions import ApiError
from datetime import date

from operator import itemgetter #для сортировки словаря

# from db import create_tables, DB_tools, get_worksheet, insert_db
# from config import DNS

class VkTools():
    def __init__(self, token):
        self.ext_api = vk_api.VkApi(token=token)

    """Функция для получения информации о пользователе"""
    def get_profile_info(self,user_id):
        try:
            info = self.ext_api.method('users.get',
                                       {'user_id':user_id,
                                        'fields': 'bdate, city,sex,relation'
                                        }
                                       )
        except ApiError:
            return
        return info

    """Функция для поиска пары для пльзователя"""
    def user_search(self,city_id,age_from,age_to,sex,status = None,offset = None):
        try:
            profiles = self.ext_api.method('users.search',
                                       {'city_id':city_id,
                                        'age_from':age_from,
                                        'age_to':age_to,
                                        'sex':sex,
                                        'count':50,
                                        'offset':offset,
                                        'status':status
                                        }
                                       )
        except ApiError:
            return

        profiles = profiles['items']

        result = []
        for profile in profiles:
            if profile['is_closed'] == False:
                result.append({'name': profile['first_name']+ ' ' + profile['last_name'],
                              'id': profile['id']
                               })
        return result

    """Функция для получения массива данных о фото пользователя"""
    def photos_get(self,user_id):
        photos = self.ext_api.method('photos.get',
                                    {'album_id': 'profile',
                                    'owner_id': user_id,
                                     'extended': 1
                                    })

        try:
            photos = photos['items']
        except KeyError:
            return

        # if photos:
        #     self.photo_sort(photos)
        # print(photos)

        photos_sort = []
        for num, photo in enumerate(photos):
            photos_sort.append({'owner_id': photo['owner_id'],
                           'id': photo['id'],
                           'media': (f'photo{photo["owner_id"]}_{photo["id"]}'),
                           'likes': photo['likes']['count'] + photo['comments']['count']})
            # if num == 2:
            #     break

        photos_sort.sort(key=itemgetter('likes')) #отсортированный список словарей с данными по фото - надо взять последние 3
        photos_sort = photos_sort[::-1] # переворачиваем список вобратном порядке

        result = [] # возвращаем топ-3
        for num, photos_sort in enumerate(photos_sort):
            # print(photos_sort)
            result.append({'owner_id': photos_sort['owner_id'],
                           'id': photos_sort['id'],
                           'media': photos_sort['media']})
                           # 'likes': photos_sort['likes']})
            # print(result)
            if num == 2:
                break
        return result
        # return result_end

    """Функция для вычисления возраста пользователя"""
    def get_age(self, user_id): #вычисление возраста пользователя, который ведет поиск
        info = self.get_profile_info(user_id)
        bdate = info[0]['bdate']
        if len(bdate) == 10: #если указан год рождения
            # print(bdate)
            bdate = datetime.datetime.strptime(bdate, '%d.%m.%Y')
            today = date.today()
            return today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
        else:
            return 0

    """Функция для определения пола пользователей"""
    def get_sex_for_search(self,user_id): #пол человека для поиска
        info = self.get_profile_info(user_id)
        sex = info[0]['sex'] #пол пользователя, который ищет
        if sex == 1:
            return 2
        elif sex == 2:
            return 1
        else:
            return 0

    """Функция для определения id города из профиля"""
    def get_city_id(self,user_id): #получение id города пользователя из профиля
        info = self.get_profile_info(user_id)
        if 'city' in info[0]:
            return info[0]['city']['id']
        else:
            return 0

    """Функция для определения id города из сообщения"""
    def search_city_id(self,q): #поиск id города, который ввел пльзователь для поиска
        try:
            city = self.ext_api.method('database.getCities',
                                           {'q': q,
                                            }
                                           )
        except ApiError:
            return
        if city['count'] != 0:
            return city['items'][0]['id']
        else:
            return 0

    def check_profile(self, profiles):
        for profile in profiles:
            worksheet_id = profile['id']
            if get_worksheet(db_tools.engine, worksheet_id=worksheet_id): #если есть в бд
                del profiles[0]
            else: #если нет в бд
                return profiles


if __name__ == '__main__':
    tools = VkTools(acces_token) #объект класса VkTools
    info = tools.get_profile_info('4584140') #сюда передать id человека из чата, он ищет пару
    profiles = tools.user_search(338, 33, 39, 0, 6)
    photos = tools.photos_get(97399357)

    db_tools = DB_tools(DNS)

    if info:
        # print(info)
        # print(info[0]['bdate'])
        # print(info[0]['city']['id'])
        # print(info[0]['first_name'])
        pass
    else:
        pass #сообщить об ошибке

    if photos:
        for photo in photos:
            print(photo)
    else:
        pass #сообщить об ошибке

    # if profiles: #список словарей
    #     for profile in profiles:
    #         print(profile)


    # print(profiles)
    #
    # profiles = tools.check_profile(profiles)
    # print(profiles)



    # if profiles:
    #     print(profiles)
    #     for profile in profiles:
    #         print(profile['id'])
    #         photos = tools.photos_get(profile['id'])
    #         # if photos:
    #         #     for photo in photos:
    #         #         print(photo)
    #                 # media = f'photo{profile["id"]}_{photo["id"]}'
    #                 # print(media)
    # else:
    #     pass #сообщить об ошибке

    # if photos:
    #     for photo in photos:
    #         print(photo)
    #         # media = f'photo_97399357_311790567'
    # else:
    #     pass #сообщить об ошибке

    # age = tools.get_age(458997111)
    # print(f'возраст {age}')
    #
    # sex = tools.get_sex_for_search(458997111)
    # print(f'пол {sex}')
    #
    # city_id = tools.get_city_id(4584140)
    # print(f'город {city_id}')
    #
    # city_id = tools.search_city_id('жопа')
    # print(f'идентификатор города {city_id}')

    # medias = tools.get_media(profile)
    #
    # if medias:
    #     for media in medias:
    #         print(media)

    # photos = tools.photos_get(382074370)
    #
    # tools.photo_sort(photos)

    # print(profiles)
    # print(profiles.pop(0))
    # print(profiles)