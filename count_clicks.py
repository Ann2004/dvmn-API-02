import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlparse


def shorten_link(token, url_to_shorten):
    url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'access_token': token,
        'url': url_to_shorten,
        'v': '5.199'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    if 'error' in response.json():
        raise requests.exceptions.HTTPError('Несуществующая ссылка')
    short_link = response.json()['response']['short_url']
    return short_link


def count_clicks(token, short_link):
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    path = urlparse(short_link).path
    params = {
        'access_token': token,
        'key': path[1:],
        'interval': 'forever',
        'v': '5.199'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    if 'error' in response.json():
        raise requests.exceptions.HTTPError('Несуществующая ссылка')
    clicks_count = response.json()['response']['stats'][0]['views']
    return clicks_count


def is_shorten_link(token, short_url):
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    path = urlparse(short_url).path
    params = {
        'access_token': token,
        'key': path[1:],
        'interval': 'forever',
        'v': '5.199'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return 'error' in response.json()


def main():
    load_dotenv()
    access_token = os.environ['VK_TOKEN']
    
    user_input = input('Укажите ссылку: ')

    if is_shorten_link(access_token, user_input):
        try:
            short_link = shorten_link(access_token, user_input)
        except requests.exceptions.HTTPError as e:
            print(f'Ошибка: {e}')
            return       
        print('Сокращенная ссылка:', short_link)       
    else:
        try:
            clicks_count = count_clicks(access_token, user_input)
        except requests.exceptions.HTTPError as e:
            print(f'Ошибка: {e}')
            return
        print('Количество кликов по ссылке:', clicks_count)


if __name__ == '__main__':
    main()