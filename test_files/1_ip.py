# encoding:utf-8
import re
import time
import ip
import random
import requests
from bs4 import BeautifulSoup


def gain_url():
    for i in range(3):
        url = 'http://www.nimadaili.com/gaoni/{}/'.format(i + 1)  # 泥马代理
        getproxies6(url)
        time.sleep(2)


def getproxies6(urls):
    req = requests.get(urls, headers=ip.getheaders()).text
    soup = BeautifulSoup(req, 'lxml')
    tr = soup.find_all('tr')[1:]

    for i in tr:
        ip_post = re.findall(r'<td>(.*?)</td>', str(i))[0]
        print(ip_post)
    #     post = re.findall(r'<td\sdata-title="PORT">(.*?)</td>', str(i))[0]
    #     print('{}:{}'.format(ip_address, post))


if __name__ == '__main__':
    gain_url()
    # getproxies6('http://www.nimadaili.com/gaoni/1/')
