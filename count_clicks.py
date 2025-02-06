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
    if 'invalid url' in response.text:
        raise requests.exceptions.HTTPError('Несуществующая ссылка')
    return response


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
	if 'invalid key' in response.text:
		raise requests.exceptions.HTTPError('Несуществующая ссылка')
	return response


def is_shorten_link(url):
	return urlparse(url).netloc == 'vk.cc'


def main():
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    
    user_input = input('Укажите ссылку для сокращения: ')

    if is_shorten_link(user_input):
    	try:
    		clicks_count = count_clicks(access_token, user_input)
    	except requests.exceptions.HTTPError as e:
    		print(f'Ошибка: {e}')
    		return
    	print('Количество кликов по ссылке:', clicks_count.json()['response']['stats'][0]['views'])
    else:
	    try:
	        short_link = shorten_link(access_token, user_input)
	    except requests.exceptions.HTTPError as e:
	        print(f'Ошибка: {e}')
	        return
	    short_link = short_link.json()['response']['short_url']
	    print('Сокращенная ссылка:', short_link)


if __name__ == '__main__':
    main()