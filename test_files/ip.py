# encoding:utf-8
# from selenium import webdriver
import random
import requests
import re
from bs4 import BeautifulSoup

path = 'ip.txt'  # 代理ip存储文件

from requests import RequestException


# url = 'http://icanhazip.com'  # 测试代理
# url = 'https://www.baidu.com/'
# url ='https://www.bilibili.com/video/BV1Ni4y1c7jK?p=1'
# url = 'https://ip.jiangxianli.com/?page=1&country=%E4%B8%AD%E5%9B%BD'


def getheaders():
    """设置请求头"""
    headers_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36", ]
    headers = {'User-Agent': random.choice(headers_list)}
    return headers


# -----------------------------------------------测试selenium代理---------------------------------------------------------
# option = webdriver.ChromeOptions()
# # option.add_argument('--user-agent=%s' % headers) #
# option.add_argument('--proxy-server=http://113.108.190.50:8080')
# option.add_argument('--user-agent=%s' % random.choice(headers))
# driver = webdriver.Chrome(options=option)
# # driver.delete_all_cookies()
# driver.get(url)

# -----------------------------------------------代理抓取-----------------------------------------------------------------
def getproxies(urls):
    rep = requests.get(urls, headers=getheaders()).text
    soup = BeautifulSoup(rep, 'lxml')
    tbodies = soup.find_all('tr')
    for tbody in tbodies:
        res = re.findall(r'<td>(.*?)</td>', str(tbody))[:4]
        # - 判断列表是否为空
        if not res:
            continue
        # - 写入文件
        string = '{}:{},{}\n'.format(res[0], res[1], res[-1])
        record(string)


# ------------------------------------------------代理抓取1---------------------------------------------------------------
# 89代理抓取
def getproxies2(urls):
    req = requests.get(urls, headers=getheaders()).text
    soup = BeautifulSoup(req, 'lxml')
    tr = soup.find_all('tr')[1:]
    for t in tr:
        # - 判断列表是否为空
        if not t:
            continue
        td = re.findall(r'<td>\s+(..*?)\s+</td>', str(t))
        ips = '{}:{}\n'.format(td[0], td[1])
        record(ips)


# -----------------------------------------------清空文档-----------------------------------------------------------------
def clear_file():
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()


# -----------------------------------------------写入文档-----------------------------------------------------------------
def record(text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text)


def main():
    clear_file()
    for i in range(5):
        # url = 'https://ip.jiangxianli.com/?page={}&country=%E4%B8%AD%E5%9B%BD'.format(i + 1)
        url = 'https://www.89ip.cn/index_{}.html'.format(i + 1)  # 89代理
        try:
            getproxies2(url)
        except RequestException:
            print("ip抓取不足")


if __name__ == '__main__':
    main()
