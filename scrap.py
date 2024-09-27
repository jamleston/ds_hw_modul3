import requests
from bs4 import BeautifulSoup
import re
import json
import pymongo
from pymongo import MongoClient, InsertOne
from pymongo.server_api import ServerApi

URL = 'https://quotes.toscrape.com'

def get_pageurl_list():
    url_list = []
    for i in range(1,11):
        url = f'{URL}/page/{i}/'
        url_list.append(url)
    return url_list

pageurl_list = get_pageurl_list()

def authors():

    def get_authorsurl_list():
        for link in pageurl_list:
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

def quotes():

    quotes_list = []

    for link in pageurl_list:
        html_doc = requests.get(link)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        content = soup.select('div[class=quote]')
        
        for el in content:

            quote_dict = {}

            # tags
            tags = el.find_all('a', attrs={'class': 'tag'})
            def make_list(list):
                tags_list = []
                for el in list:
                    tag = el.text
                    tags_list.append(tag)
                return tags_list
            quote_dict['tags'] = make_list(tags)

            # author
            author = el.find('small', attrs={'class': 'author'}).text
            quote_dict['author'] = author

            # quote
            quote = el.find('span', attrs={'class': 'text'}).text
            quote_dict['quote'] = quote

            quotes_list.append(quote_dict)

        return quotes_list
    
    return quotes_list

authors_result = authors()
quotes_result = quotes()

with open('authors.json', 'w', encoding='utf=8') as f:
    json.dump(authors_result, f, ensure_ascii=False, indent=4)

with open('quotes.json', 'w', encoding='utf=8') as f:
    json.dump(quotes_result, f, ensure_ascii=False, indent=4)


# import to mongo

client = MongoClient(
    "mongodb+srv://user:12345@cluster0.mxpz2.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.scrap

collection1 = db.authors
requesting1 = []

with open(r"authors.json") as f:
    for jsonObj in f:
        myDict = json.loads(jsonObj)
        requesting1.append(InsertOne(myDict))

result = collection1.bulk_write(requesting1)
client.close()

collection2 = db.quotes
requesting2 = []

with open(r"quotes.json") as f:
    for jsonObj in f:
        myDict = json.loads(jsonObj)
        requesting2.append(InsertOne(myDict))

result = collection2.bulk_write(requesting2)
client.close()