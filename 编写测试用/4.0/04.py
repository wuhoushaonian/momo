# encoding:utf-8
import re
import requests
from bs4 import BeautifulSoup

url = 'https://www.89ip.cn/index_1.html'


def general(urls):
    req = requests.get(urls).text
    soup = BeautifulSoup(req, 'lxml')
    tr = soup.select('tr')[1:]
    for td in tr:
        t = td.select('td')
        ips = re.search(r'(\d+\.){3}\d+', str(t[0]))
        ports = re.search(r'\d{2,4}', str(t[1]))
        print("{}:{}\n".format(ips.group(), ports.group()))


general(url)
