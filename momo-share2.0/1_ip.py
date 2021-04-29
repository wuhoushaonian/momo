# encoding:utf-8
import re

import ip
import random
import requests
from bs4 import BeautifulSoup

url = 'http://www.xiladaili.com/http/'

req = requests.get(url, headers={'User-Agent': random.choice(ip.getheaders())}).text
soup = BeautifulSoup(req, 'lxml')
tr = soup.find_all('tr')
for td in tr:
    res = re.findall(r'<td>(.*?)</td>', str(td))
    if not res:
        continue
    print(res[0])
