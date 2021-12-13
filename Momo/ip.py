# encoding:utf-8
import re
from random import choice
import asyncio
# import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import encodings.idna

path = 'ip.txt'  # 文件保存地址


# 随机返回请求头
async def getheaders():
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
    headers = {'User-Agent': choice(headers_list)}
    return headers


# 清空文档
def clear_file():
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()


# 写入文档
async def record(text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text)


# 实例化请求对象
async def create_aiohttp():
    async with ClientSession() as session:  # 实例化一个请求对象
        task = [
            get_page('http://www.kxdaili.com/dailiip/2/1.html', session=session),
            get_page('https://www.kuaidaili.com/free/inha/1/', mod=2, session=session),
            get_page('https://www.kuaidaili.com/free/intr/2/', mod=2, session=session),
            get_page('http://www.66ip.cn/areaindex_1/1.html', session=session),
            get_page('https://www.proxy-list.download/api/v1/get?type=http', mod=5, session=session)
        ]
        for i in range(2):
            task.append(get_page(f'http://www.nimadaili.com/http/{i + 1}/', mod=4, session=session))
            task.append(get_page(f'https://www.89ip.cn/index_{i + 1}.html', mod=3, session=session))
            task.append(get_page(f'http://http.taiyangruanjian.com/free/page{i + 1}/', mod=1, session=session))
            task.append(get_page(f'http://www.kxdaili.com/dailiip/1/{i + 1}.html', session=session))
            task.append(get_page(f'http://www.ip3366.net/free/?stype=1&page={i + 1}', session=session))

        await asyncio.wait(task)


# 访问网页
async def get_page(url, session, mod=0):
    header = await getheaders()
    try:
        async with await session.get(url=url, headers=header) as response:  # 异步请求
            page_source = await response.text()  # 返回字符串形式的相应数据
            await soup_page(page_source, mod=mod)
            # 请求 和 响应时要加上阻塞 await
    except Exception as e:
        print(f"['{url}']抓取失败:", e)


# 清洗页面 提取IP
# 生成代理链接格式: http://ip:port
async def soup_page(source, mod):
    if mod == 0:
        # 通用
        soup = BeautifulSoup(source, 'lxml')
        tr = soup.find_all('tr')
        for t in tr:
            ips = re.search(r'(\d+\.){3}\d+', str(t))
            posts = re.search(r'<td>(\d{1,4})</td>', str(t))
            if not ips or not posts:
                continue
            await record(f"http://{ips.group()}:{posts.group(1)}\n")
    elif mod == 1:
        # 太阳
        soup = BeautifulSoup(source, 'lxml')
        lists = soup.find_all('div', class_='tr ip_tr')
        for li in lists:
            ips = re.findall(r'<div\sclass="td\std-4">(.*?)</div>', str(li))
            posts = re.findall(r'<div\sclass="td\std-2">(.*?)</div>', str(li))
            await record(f'http://{ips[0]}:{posts[0]}\n')
    elif mod == 2:
        # 快代理
        soup = BeautifulSoup(source, 'lxml')
        tr = soup.find_all('tr')
        for t in tr:
            ips = re.findall(r'<td\s.*?="IP">(.*?)</td>', str(t))
            posts = re.findall(r'<td\s.*?="PORT">(.*?)</td>', str(t))
            if not ips or not posts:
                continue
            await record(f"http://{ips[0]}:{posts[0]}\n")
    elif mod == 3:
        # 89代理
        soup = BeautifulSoup(source, 'lxml')
        tr = soup.select('tr')[1:]
        for td in tr:
            t = td.select('td')
            ips = re.search(r'(\d+\.){3}\d+', str(t[0]))
            ports = re.search(r'\d{2,4}', str(t[1]))
            await record(f"http://{ips.group()}:{ports.group()}\n")
    elif mod == 4:
        # 泥马代理
        soup = BeautifulSoup(source, 'lxml')
        tr = soup.find_all('tr')[1:]
        for i in tr:
            ip_post = re.findall(r'<td>(.*?)</td>', str(i))[0]
            await record(f'http://{ip_post}\n')
    elif mod == 5:
        ip_list = source.split('\r\n')[:-1]
        one = f'http://{ip_list[0]}\n'
        res = '\nhttp://'.join(ip_list)
        await record(f'{one}{res}\n')


def ip_main():
    clear_file()  # 清空存放代理文件
    print('正在抓取代理ip。。。')
    asyncio.run(create_aiohttp())
    print("代理抓取成功！")

# ip_main()
