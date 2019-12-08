from requests_html import HTMLSession
import threading
import time
import random
import csv
import numpy as np


session = HTMLSession()
r = session.get('https://tiki.vn/')

data = []

def parse_link(href, currentPage = 1):
    _session = HTMLSession()
    _r = _session.get(href)
    category_tag = _r.html.find(".breadcrumb span", first=True)
    items = _r.html.find('.content .title')
    print("page = ", currentPage)

    if len(items) == 0:
        return
    for item in items:
        data.append([item.text.rstrip("."), category_tag.text])
    nextPage = currentPage+1
    time.sleep(1.0)
    parse_link(href+"&page="+str(nextPage), nextPage)
    

items = r.html.find('li.MenuItem-tii3xq-0 a')
for item in items:
    href = item.attrs["href"]
    time.sleep(0.2)
    parse_link(href)

np.random.shuffle(data)

with open('product.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["product_title", "category"])
    for item in data:
        writer.writerow(item)