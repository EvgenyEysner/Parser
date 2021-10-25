import requests
import csv
import json
from bs4 import BeautifulSoup

# добавляю заголовок чтобы обойти защиту
# узнать о защите можно -> https://www.site/robots.txt
domain = 'https://www.'
header = {'user-agent': ''}

# TO DO добавить асинхронность/ многопоточность + исключения


# сохраняю страницу в файл на случай бана
def get_page(page):
    req = requests.get(page, headers=header)
    src = req.text

    with open('parsed_data/index.html', 'w') as file:
        index = file.write(src)
    return index


# далее работаю с сохраненным файлом
# ищу категории
def get_category(index):
    categories = {}  # 1615 категории
    with open(index) as f:
        src = f.read()

        soup = BeautifulSoup(src, 'lxml')
        categories_html = soup.find('div', id='lsidebar').find_all('li')
        for item in categories_html:
            name = item.find('a').text
            link = domain + item.find('a').get('href')
            categories[name] = link

    # запись категорий
    with open('category.json', 'w') as file:
        # indent - отступы, ensure_ascii - убирает символы и позволяет устранить проблемы с кодировкой
        json.dump(categories, file, indent=4, ensure_ascii=False)


# получаю ссылки на продукты
def get_product_links(categories):
    with open(f'parsed_data/{categories}') as file:
        all_categories = json.load(file)

    products = []
    count = 0
    # в цикле прохожу поо каждой категории и сохраняю ссылки на продукты
    for name, url in all_categories.items():

        html = requests.get(url=url, headers=header)
        src = html.text
        soup = BeautifulSoup(src, 'lxml')
        products_html = soup.find_all('div', class_='block')

        for item in products_html:
            count += 1
            category_name = name
            product_name = item.find('a', class_='header').text
            link = domain + item.find('a').get('href')
            products.append(
                {
                    category_name:
                        {
                            'position': count,
                            'name': product_name,
                            'url': link
                        }
                }
            )
            print('Downloaded: ', count)
            # запись продуктов/ ссылок
    with open('products.json', 'w') as file:
        json.dump(products, file, indent=4, ensure_ascii=False)


#  информация о продукте
def get_product_data(product_links):

    articles = []

    with open(f'parsed_data/{product_links}') as file:
        products = file.read()
        dict_list = json.loads(products)
        count = len(dict_list)
        for item in dict_list:
            for val in item.values():
                count -= 1
                url = val['url']
                html = requests.get(url, headers=header)
                src = html.text
                soup = BeautifulSoup(src, 'lxml')

                # категория и изготовитель
                breadcrumbs = soup.find('div', id='breadcrumbs').text.split(' → ')  # беру из крошек категорию для записи
                category = breadcrumbs[2]  # категории

                # название
                name = soup.find('div', id='hits-long').find('h1').text
                # цена
                price = soup.find('span', class_='price').text.strip()

                # описание
                desc_html = soup.find('div', id='tabs-1').find('table').find_all('td')

                # получаю фото
                image_url = domain + soup.find('div', class_='big_preview').find('a').get('href')
                req = requests.get(url=image_url, stream=True)
                image_name = image_url.split('/')[5]
                response = req.content
                with open(f'media/{image_name}', 'wb') as file:
                    file.write(response)
                    with open(f'media/{image_name}', 'rb') as f:
                        img = f.read()

                articles.append(
                    {
                        'category': category,
                        'name': name,
                        'price': price,
                        'description': [child.text.strip() for child in desc_html],
                        'image': img,

                    }
                )
            print('Обработано: ', count)
    # итоговый json
    with open('articles.json', 'w') as file:
        json.dump(products, file, indent=4, ensure_ascii=False)

    return articles


def main():
    get_page('some-site')
    get_category('index.html')
    get_product_links('category.json')
    get_product_data('products.json')


if __name__ == '__main__':
    main()
