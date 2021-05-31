# encoding:utf-8
import re
import time
import ip
import requests
from bs4 import BeautifulSoup


def gain_url():
    for i in range(3):
        url = 'http://http.taiyangruanjian.com/free/page{}/'.format(i + 1)  #
        getproxies7(url)
        time.sleep(2)


def getproxies7(urls):
    req = requests.get(urls, headers=ip.getheaders()).content.decode('utf-8')
    soup = BeautifulSoup(req, 'lxml')
    divs = soup.find('div', class_="list")
    for div in divs:
        ipl = re.findall('<div\sclass=\"td\std-\d\">(.*?)</div>', str(div))
        if not ipl:
            continue
        print('{}:{}'.format(ipl[0], ipl[1]))


if __name__ == '__main__':
    gain_url()
    # getproxies7('http://http.taiyangruanjian.com/free/page1/')
