import telebot
from configbot import token
from functions import get_dict, get_weather, keyboard_start

"""
metacastbot v.1.0 - телеграмм бот основанный на telebot, информации получаемой при парсинге сайта gismeteo
Для бота специально не использовалась предоставляемая gismeteo API для целей изучения возможности получения
информации путем парсинга.
В качестве основной информации для парсинга используется словарь населенных пунктов России, позволяющий покрыть
большое количество населенных пунктов в России. Словарь получен путем парсинга сайта gismeteo, при этом
в словаре не было учтено наличие населенных пунктов имеющих одинаковое название.
В связи с тем, что список населенных пунктов в различных субъектах России достаточно большой и неудобно
пользоваться в телеграмме длинными списками, было принято решение о том, что наименование интересующего
населенного пункта вводит пользователь.
"""

weatherbot = telebot.TeleBot(token)
dict_of_regions = {}
name = ''

@weatherbot.message_handler(commands=['start'])
def start_com(message):
    greetings = 'Добро пожаловать!!!\nКак Вас зовут?'
    weatherbot.send_message(message.chat.id, greetings)
    weatherbot.register_next_step_handler(message, reg_name)
def reg_name(message):
    global name
    name = message.text
    weatherbot.send_message(
        message.chat.id, f"""{name} приятно с Вами познакомиться!
        Для получения данных о погоде, введите "/run"
        Если Вам нужна помощь введите "/help" 
        Или нажмите на соответсвующие кнопки ниже""", reply_markup=keyboard_start())

@weatherbot.message_handler(commands=['run'])
def run_com(message):
    global dict_of_regions
    if get_dict():
        dict_of_regions = get_dict()
    else:
        weatherbot.send_message(message.chat.id, 'Извините, сервис в текущее время недоступен')
    weatherbot.send_message(message.chat.id, 'Пожалуйства введите интересующий Вас населенный пункт (например: Тюмень, Санкт-Петербург)')

@weatherbot.message_handler(commands=['help'])
def help_com(message):
    help_text = """
    Для перезагрузки бота введите: "/start"
    Для получения помощи введите: "/help"
    Для начала работы бота введите: "/run"
    """
    weatherbot.send_message(message.chat.id, help_text)

@weatherbot.message_handler(content_types=['text'])
def check_weather(message):
    name = message.text.lower()
    if name in dict_of_regions:
        urls = dict_of_regions[name]
        get_weather(urls)
        temperature, wind = get_weather(urls)
        weatherbot.send_message(message.chat.id, f"В населенном пункте {message.text}")
        weatherbot.send_message(message.chat.id, f"температура воздуха: {temperature}С")
        weatherbot.send_message(message.chat.id, f"ветер: {wind}")
    else:
        weatherbot.send_message(message.chat.id, f'Извините, населенный пункт с названием {message.text} в базе не найден\nПроверьте правильность написания названия')


weatherbot.polling()
