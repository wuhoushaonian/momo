# encoding:utf-8
import re
import time
import requests
import random
from requests import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver

path = 'ip.txt'  # 代理ip存储地址


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


# -----------------------------------------------代理抓取-----------------------------------------------------------------
def getproxies(urls):
    """1"""
    rep = requests.get(urls, headers={'User-Agent': random.choice(getheaders())}).text
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
    '''2'''
    # req = requests.get(urls, headers={'User-Agent': random.choice(getheaders())}).text
    # ips = re.findall(r'<td\sdata-title=\"IP\">(.*?)</td>', req)
    # ports = re.findall(r'<td\sdata-title=\"PORT\">(.*?)</td>', req)
    # types = re.findall(r'<td\sdata-title=\"类型\">(.*?)</td>', req)
    # for i in range(len(ips)):
    #     strings = '{}:{},{}\n'.format(ips[i], ports[i], types[i])
    #     record(strings)


# -----------------------------------------------清空文档-----------------------------------------------------------------
def clear_file():
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()


# -----------------------------------------------写入文档-----------------------------------------------------------------
def record(text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text)


# ---------------------------------------------ip网页抓取-------------------------------------------------------------
def ip_main():
    clear_file()
    for i in range(3):
        # 抓取3页:45个

        url = 'https://ip.jiangxianli.com/?page={}&country=%E4%B8%AD%E5%9B%BD'.format(i + 1)  # 1
        # url = 'https://www.kuaidaili.com/free/inha/{}/'.format(i + 1)  # 2
        try:
            getproxies(url)
        except RequestException:
            print("ip抓取不足")


# -----------------------------------------------------读取文档-----------------------------------------------------------
def readfile():
    ip_list = []
    with open('ip.txt', 'r', encoding='utf-8') as f:
        ips = f.readlines()
        for ip in ips:
            ip = ip.strip().split(',')
            if ip[1] == 'HTTP':
                ip_list.append(ip[0])
    return ip_list


# -----------------------------------------------------检查ip是否可用-----------------------------------------------------
def inspect():
    n = 0
    available_ip = []
    for ip in readfile():
        proxies = {"http": "http://{}".format(ip)}
        req = requests.get('https://www.baidu.com', headers={'User-Agent': random.choice(getheaders())},
                           proxies=proxies).status_code
        if req == 200:
            n += 1
            # available_ip.append(proxies) #requests用
            available_ip.append(ip)
    print("可用代理ip数量是:{}。".format(n))
    return available_ip


# -----------------------------------------------------访问分享链接-------------------------------------------------------
# requests 测试访问失败 改用selenium
# def interview(url, m):
#     n = 0
#     print("开始访问分享链接。。。")
#     for ip in inspect():
#         if n == m:
#             # 限制访问次数
#             break
#         try:
#             requests.get(url, headers=getheaders(), proxies=ip, timeout=15)
#             n += 1
#             print("分享链接访问成功!!!,访问第{}次。".format(n))
#             time.sleep(random.randint(1, 60))  # 随机生成访问间隔时间
#         except RequestException:
#             print("访问失败！！！")
#             print("代理ip失效，正在更换代理ip。。。")


# -----------------------------------------------测试selenium代理---------------------------------------------------------
def interview(url, m):
    n = 0
    option = webdriver.ChromeOptions()
    # option.add_argument('--user-agent=%s' % headers) #
    for ip in inspect():
        print('代理ip为:http://{}'.format(ip))
        if n == m:
            # 设置访问次数
            break
        option.add_argument('--proxy-server=http://{}'.format(ip))
        option.add_argument('--user-agent=%s' % random.choice(getheaders()))
        # 隐藏自动化测试横幅
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(options=option)
        # driver.delete_all_cookies()
        # driver.set_page_load_timeout(30)
        try:
            driver.get(url)
            time.sleep(20)
            driver.execute_script('window.stop()')  # 停止加载
            driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/p[1]')  # 获取网页元素以检测是否获取到网页
            for j in range(random.randint(5, 15)):
                driver.execute_script('var q=document.documentElement.scrollTop={}'.format(j * 800))
                time.sleep(0.5)
            n += 1
            print("分享链接访问成功!!!,访问第{}次。".format(n))
            time.sleep(random.randint(1, 30))  # 随机生成访问间隔时间
            driver.quit()

        except Exception:
            driver.quit()
            print("访问失败！！！")
            print("代理ip失效，正在更换代理ip。。。")
    print("访问结束!共访问{}次。".format(n))


# -------------------------------------------------------运行主函数-------------------------------------------------------


def main():
    ip_main()  # 获取代理ip
    url = input("请输入待访问链接:")
    times = int(input('请输入访问次数:'))
    interview(url, times)  # 访问分享链接


if __name__ == '__main__':
    main()
