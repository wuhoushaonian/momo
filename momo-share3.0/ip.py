# encoding:utf-8
import re
import random
from requests import get
from bs4 import BeautifulSoup
from requests import RequestException

path = 'ip.txt'  # 文件保存地址


# ------------------------------------------------设置请求头--------------------------------------------------------------
# 返回一个随机的请求头 headers
def getheaders():
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
    # headers = {'User-Agent': random.choice(headers_list)}
    return headers_list


# --------------------------------------------------代理提取--------------------------------------------------------------
# 西拉代理
def getproxies3(urls):
    req = get(urls, headers={'User-Agent': random.choice(getheaders())}).text
    soup = BeautifulSoup(req, 'lxml')
    tr = soup.find_all('tr')
    for td in tr:
        res = re.findall(r'<td>(.*?)</td>', str(td))
        if not res:
            continue
        record('{}\n'.format(res[0]))


# 泥马代理
def getproxies6(urls):
    req = get(urls, headers={'User-Agent': random.choice(getheaders())}).text
    soup = BeautifulSoup(req, 'lxml')
    tr = soup.find_all('tr')[1:]

    for i in tr:
        ip_post = re.findall(r'<td>(.*?)</td>', str(i))[0]
        record('{}\n'.format(ip_post))


# 太阳代理
def sun_ip(urls):
    req = get(urls, headers={'User-Agent': random.choice(getheaders())}).text
    soup = BeautifulSoup(req, 'lxml')
    lists = soup.find_all('div', class_='tr ip_tr')
    for li in lists:
        ips = re.findall(r'<div\sclass="td\std-4">(.*?)</div>', str(li))
        posts = re.findall(r'<div\sclass="td\std-2">(.*?)</div>', str(li))
        record('{}:{}\n'.format(ips[0], posts[0]))


# 快代理
def quick(urls):
    req = get(urls, headers={'User-Agent': random.choice(getheaders())}).text
    soup = BeautifulSoup(req, 'lxml')
    tr = soup.find_all('tr')
    for t in tr:
        ips = re.findall(r'<td\s.*?="IP">(.*?)</td>', str(t))
        posts = re.findall(r'<td\s.*?="PORT">(.*?)</td>', str(t))
        if not ips or not posts:
            continue
        record("{}:{}\n".format(ips[0], posts[0]))


# 开心代理||高可用全球免费代理库||小幻||云代理
def general(urls):
    req = get(urls, headers={'User-Agent': random.choice(getheaders())}).text
    soup = BeautifulSoup(req, 'lxml')
    tr = soup.find_all('tr')
    for t in tr:
        ips = re.search(r'(\d+\.){3}\d+', str(t))
        posts = re.search(r'<td>(\d{1,4})</td>', str(t))
        if not ips or not posts:
            continue
        record("{}:{}\n".format(ips.group(), posts.group(1)))


# -----------------------------------------------清空文档-----------------------------------------------------------------
def clear_file():
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()


# -----------------------------------------------写入文档-----------------------------------------------------------------
def record(text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text)


# -----------------------------------------------网址生成-----------------------------------------------------------------
def geturl():
    print("正在抓取代理IP。。。")
    for i in range(2):
        if i < 1:
            # finally:
            #     pass
            # getproxies6('http://www.nimadaili.com/gaoni/{}/'.format(i + 1))
            # getproxies3('http://www.xiladaili.com/http/{}/'.format(i + 1))
            try:
                general('http://www.kxdaili.com/dailiip.html')
            except RequestException:
                pass
            try:
                quick('https://www.kuaidaili.com/free/inha/{}/'.format(i + 1))
                quick('https://www.kuaidaili.com/free/intr/{}/'.format(i + 1))
            except RequestException:
                pass
            try:
                general('https://ip.ihuan.me/address/5Lit5Zu9.html?page=b97827cc')
            except RequestException:
                pass

        try:
            general('https://ip.jiangxianli.com/?page={}&country=%E4%B8%AD%E5%9B%BD'.format(i + 1))
        except RequestException:
            pass
        try:
            sun_ip('http://http.taiyangruanjian.com/free/page{}/'.format(i + 1))
        except RequestException:
            pass

        try:
            general('http://www.ip3366.net/free/?stype=1&page={}'.format(i + 1))
        except RequestException:
            pass

    print('代理ip抓取完成！！！')


# -----------------------------------------------运行主函数---------------------------------------------------------------
def ip_main():
    clear_file()
    geturl()


# ip_main()
