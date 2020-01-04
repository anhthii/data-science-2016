from requests_html import HTMLSession
import csv
import numpy as np
import pandas as pd

session = HTMLSession()
r = session.get('https://tiki.vn/')
r.encoding = 'utf-8'

data = []
link_category_dict = dict()

def parse_link(href, currentPage = 1):
    page = href+"&page="+str(currentPage)
    _session = HTMLSession()
    _r = _session.get(page)
    items = _r.html.find('.content .title')

    if len(items) == 0:
        return
    for item in items:
        category = link_category_dict[href]
        data.append([item.text.strip().rstrip("."), category])
    nextPage = currentPage+1
    try:
        print("page ", page)
        parse_link(href, nextPage)
    except Exception as e:
        print("some errors occured", str(e))

def get_categories():
    categories = []
    item_list = r.html.find('li.MenuItem-tii3xq-0 ')
    for item in item_list:
        href = item.find('a', first=True).attrs["href"]
        category = item.text
        categories.append((href, category))
        link_category_dict[href] = category
    return categories

def crawl_data():
    category_tuples = get_categories()
    for category_tuple in category_tuples:
        (href, category_name) = category_tuple
        parse_link(href)

def save_data():
    np.random.shuffle(data)
    if len(data) != 0:
        with open('product.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["product_title", "category"])
            for item in data:
                writer.writerow(item)

category_tuples = get_categories()
def run():
    print("start crawling")
    crawl_data()
    save_data()

run()
