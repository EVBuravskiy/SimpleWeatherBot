import requests
import telebot.types
from bs4 import BeautifulSoup as bs
import json

st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
# формируем хеш заголовков
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

dict_of_regions = {}

def keyboard_start():
    keyboard_markup = telebot.types.ReplyKeyboardMarkup()
    btn_run = telebot.types.KeyboardButton('/run')
    btn_help = telebot.types.KeyboardButton('/help')
    keyboard_markup.row(btn_run)
    keyboard_markup.row(btn_help)
    return keyboard_markup

def create_dict(urls='https://www.gismeteo.ru/catalog/russia/'):
    """Функция формирования словаря пар имя:url-адрес путем парсинга сайта www.gismeteo.ru"""
    global dict_of_regions
    response_get = requests.get(urls, headers=headers)
    print(response_get)
    if response_get.status_code == 200:
        soup = bs(response_get.text, 'html.parser')
        regions = soup.find_all('a', class_='link-item')
        print(regions)
        for elem in regions:
            name = elem.text.lower()
            url_elem = elem['href']
            if '/weather-' in url_elem:
                urls = f'https://www.gismeteo.ru{elem["href"]}'
                dict_of_regions[name] = urls
                print(f"Внесено в словарь: {name}: {urls}")
            else:
                urls = f'https://www.gismeteo.ru{elem["href"]}'
                print("Продолжаем", name, urls)
                create_dict(urls)
    else:
        print("Ошибка на сервере, пробуем еще раз")
        create_dict(urls)

def jsondict():
    """Функция записи словаря в json-файл"""
    with open('regions.txt', 'w') as file:
        json.dump(dict_of_regions, file)


def get_dict():
    """Функция получения данных из json-файла"""
    with open('regions.txt', 'r') as file:
        new_dict = json.load(file)
        return(new_dict)


def get_weather(url):
    """Функция получения данных о температуре воздуха и ветре, основанная на парсинге сайта www.gismeteo.ru"""
    url_now = url+'now/'
    response_get = requests.get(url_now, headers=headers)
    print(response_get)
    if response_get.status_code == 200:
        soup = bs(response_get.text, 'html.parser')
        temperature = soup.find('span', class_='unit unit_temperature_c')
        wind = soup.find('div', class_='unit unit_wind_m_s')
        print(temperature.text)
        print(wind.text)
        return(temperature.text, wind.text)
    else:
        return None

if __name__ == '__main__':
    """создание словаря для возможности использования бота"""
    create_dict()
    print(dict_of_regions)
    print(len(dict_of_regions))
    for key, value in dict_of_regions.items():
        print(key, value)
    jsondict()
    get_dict()
    print("Словарь сформирован")
