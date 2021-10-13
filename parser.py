import requests
import csv
import json
from bs4 import BeautifulSoup
from PIL import Image

# добавляю заголовок чтобы обойти защиту
# узнать о защите можно -> https://www.regard.ru/robots.txt
domain = 'https://www.regard.ru'
header = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'}
page_url = 'https://www.regard.ru'


# bs = BeautifulSoup(html.text, 'lxml')

# сохраняю страницу в файл на случай бана
# src = html.text
#
# with open('index.html', 'w') as file:
#     file.write(src)

# далее работаю с сохраненным файлом

with open('index.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

# ищу категории
# categories_html = soup.find('div', id='lsidebar').find_all('li')
# categories = {}  # 1615 категории
#
# for item in categories_html:
#     name = item.find('a').text
#     link = domain + item.find('a').get('href')
#     categories[name] = link
#
#
# with open('category.json', 'w') as file:
#     json.dump(categories, file, indent=4, ensure_ascii=False)  # indent - отступы, ensure_ascii - убирает символы и позволяет устранить проблемы с кодировкой

# with open('category.json') as file:
#     all_categories = json.load(file)
#
# products = []
# count = 0
# for name, url in all_categories.items():
#
#     html = requests.get(url=url, headers=header)
#     src = html.text
#     soup = BeautifulSoup(src, 'lxml')
#     products_html = soup.find_all('div', class_='block')
#
#     for item in products_html:
#         count += 1
#         category_name = name
#         product_name = item.find('a', class_='header').text
#         link = domain + item.find('a').get('href')
#         products.append(
#             {
#                 category_name:
#                     {
#                         'position': count,
#                         'name': product_name,
#                         'url': link
#                     }
#             }
#         )
#     # print(products)
# with open('products.json', 'w') as file:
#     json.dump(products, file, indent=4, ensure_ascii=False)

with open('parsed_data/products.json') as file:
    products = file.read()
    dict_list = json.loads(products)
    # print(dict_list)
    for item in dict_list:
        for val in item.values():
            url = val['url']
            html = requests.get(url=url, headers=header)
            src = html.text
            soup = BeautifulSoup(src, 'lxml')
            name = soup.find('div', id='hits-long').find('h1').text
            price = soup.find('span', class_='price').text
            description = soup.find('div', id='tabs-1').find('table').text
            image_url = domain + soup.find('div', class_='big_preview').find('a').get('href')
            req = requests.get(url=image_url, stream=True)
            image_name = image_url.split('/')[5]
            print(image_name)
            response = req.content
            with open(f'media/{image_name}', 'wb') as file:
                file.write(response)




# def main():
#     # https://www.regard.ru/catalog
#     all_links = []
#     pass


# if __name__ == 'main':
#     main()
