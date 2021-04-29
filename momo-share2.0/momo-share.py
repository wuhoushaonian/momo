# encoding:utf-8
import ip
import random
import requests
import time
from selenium import webdriver

ip.main()  # 抓取ip


# -----------------------------------------------------读取文档-----------------------------------------------------------
def readfile():
    ip_list = []
    with open('ip.txt', 'r', encoding='utf-8') as f:
        ips = f.readlines()
        for i in ips:
            ip_list.append(i.strip())
    return ip_list


# -----------------------------------------------------检查ip是否可用-----------------------------------------------------
def inspect():
    print('正在检查代理ip是否可用。。。')
    n = 0
    available_ip = []
    for i in readfile():
        proxies = {"http": "http://{}".format(i)}
        req = requests.get('https://www.baidu.com', headers={'User-Agent': random.choice(ip.getheaders())},
                           proxies=proxies).status_code
        if req == 200:
            n += 1
            available_ip.append(i)
    print("可用代理ip数量是:{}。".format(n))
    return available_ip


# -----------------------------------------------测试selenium代理---------------------------------------------------------
def interview(url, m):
    n = 0
    option = webdriver.ChromeOptions()
    # option.add_argument('--user-agent=%s' % headers) #
    for i in inspect():
        print('代理ip为:http://{}'.format(i))
        if n == m:
            # 设置访问次数
            break
        option.add_argument('--proxy-server=http://{}'.format(i))
        option.add_argument('--user-agent=%s' % random.choice(ip.getheaders()))
        # 隐藏自动化测试横幅
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(options=option)
        driver.set_page_load_timeout(10)
        # driver.delete_all_cookies()

        try:
            # 页面超时-停止加载
            try:
                driver.get(url)
            except Exception:
                driver.execute_script('window.stop()')  # 停止加载

            driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/p[1]')  # 获取网页元素以检测是否获取到网页
            # blogs
            # driver.find_element_by_xpath('//*[@id="div_digg"]/div[1]')  # 获取网页元素以检测是否获取到网页

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
    url = input("请输入待访问链接:")
    times = int(input('请输入访问次数:'))
    ip.main()  # 抓取代理
    interview(url, times)  # 访问分享链接


if __name__ == '__main__':
    main()
