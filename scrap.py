import requests
from bs4 import BeautifulSoup
import re
import json

URL = 'https://quotes.toscrape.com'

def get_pageurl_list():
    url_list = []
    for i in range(1,11):
        url = f'{URL}/page/{i}/'
        url_list.append(url)
    return url_list

def authors():

    def get_authorsurl_list():
        for link in get_pageurl_list():
            html_doc = requests.get(link)
            soup = BeautifulSoup(html_doc.text, 'html.parser')
            content = soup.select('div[class=quote] span a[href]')
            authors_list = []
            for el in content:
                name = el['href']
                url = URL + name
                authors_list.append(url)
            return authors_list
        
    authorsurl_list = get_authorsurl_list()

    result_list = []

    for link in authorsurl_list:
        html_doc = requests.get(link)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        content = soup.select('div[class=author-details]')
        for el in content:
            result_dict = {}
            # name
            name = el.find('h3', attrs={'class': 'author-title'}).text
            result_dict['fullname'] = name

            # born date
            date = el.find('span', attrs={'class': 'author-born-date'}).text
            result_dict['born_date'] = date

            # born location
            loc = el.find('span', attrs={'class': 'author-born-location'}).text
            result_dict['born_location'] = loc

            # born description
            descr = el.find('div', attrs={'class': 'author-description'}).text
            result_dict['description'] = descr


            result_list.append(result_dict)

    return result_list

res = authors()

with open('authors.json', 'w', encoding='utf=8') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)