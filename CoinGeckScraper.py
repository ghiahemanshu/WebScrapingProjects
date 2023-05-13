#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib.request
import json
import csv
from bs4 import BeautifulSoup

url_template = "https://www.coingecko.com/?page={}"
req = urllib.request.Request(url_template.format(1))
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
req.add_header('Accept-Language', 'en-US,en;q=0.5')

response = urllib.request.urlopen(req)
soup = BeautifulSoup(response, 'html.parser')

last_page = int(soup.find('ul', {'class': 'pagination'}).find_all('a')[-2].text)

coin_list = []
for page in range(1, last_page + 1):
    url = url_template.format(page)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')

    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    
    coin_table = soup.find('table', {'class': 'table-scrollable'})
    
    for row in coin_table.tbody.find_all('tr'):
        coin = {}
        coin['name'] = row.find_all('td')[2].a.text.split('\n')[2].strip()
        #coin['name'] = row.find_all('td')[2].a.text
        coin['url'] = "https://www.coingecko.com" + row.find_all('td')[2].a['href']
        coin_list.append(coin)
        print(f"Coin Name: {coin['name']}, URL: {coin['url']}")

# Writing the coin list to a CSV file
with open('coin_list.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'URL'])
    for coin in coin_list:
        writer.writerow([coin['name'], coin['url']])

