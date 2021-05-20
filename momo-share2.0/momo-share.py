# encoding:utf-8
import ip
import random
import time
from selenium import webdriver
global ip_counter


# -----------------------------------------------------读取文档-----------------------------------------------------------
def readfile():
    ip_list = []
    with open('ip.txt', 'r', encoding='utf-8') as f:
        ips = f.readlines()
        for i in ips:
            ip_list.append(i.strip())
    global ip_counter
    ip_counter = len(ip_list)
    print("可用代理ip数量是:{}个。".format(ip_counter))
    return ip_list


# -----------------------------------------------测试selenium代理---------------------------------------------------------
def interview(url, m):
    n = 0
    s = 0
    option = webdriver.ChromeOptions()
    # option.add_argument('--user-agent=%s' % headers) #
    for i in readfile():
        s += 1
        print('正在使用第{}个代理IP,IP剩余数量为:{}'.format(s, ip_counter - s))
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
            for j in range(random.randint(5, 15)):
                driver.execute_script('var q=document.documentElement.scrollTop={}'.format(j * 850))
                time.sleep(0.5)
            n += 1
            print("分享链接访问成功!!!,访问第{}次。".format(n))
            time.sleep(random.randint(1, 30))  # 随机生成访问间隔时间
            driver.quit()

        except Exception:
            driver.quit()
            print("访问失败！！！代理ip失效，正在更换代理ip。。。")
    path1 = 'E:\\Desktop\\访问成功{}次.txt'.format(n)
    f1 = open(path1, 'w', encoding='utf-8')
    f1.close()


# -------------------------------------------------------运行主函数-------------------------------------------------------


def main():
    url = input("请输入待访问链接:")
    # times = int(input('请输入访问次数:'))
    ip.main()  # 抓取代理
    interview(url, 20)  # 访问分享链接


if __name__ == '__main__':
    main()
