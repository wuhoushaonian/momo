# encoding:utf-8
import re
from os import environ
from random import choice
import asyncio
from aiohttp import ClientSession, ClientTimeout, TCPConnector
import uvloop
from bs4 import BeautifulSoup

global n  # 记录访问成功次数
listIP = []  # 保存IP地址
link = 'link'  # 设置link

# 如果检测到程序在 github actions 内运行，那么读取环境变量中的登录信息
if environ.get('GITHUB_RUN_ID', None):
    link = environ['link']


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


# 实例化请求对象
async def create_aiohttp_ip():
    async with ClientSession(connector=TCPConnector(ssl=False, limit=2)) as session:
        task = [
            asyncio.create_task(get_page('http://www.kxdaili.com/dailiip/2/1.html', session=session)),
            asyncio.create_task(get_page('https://www.kuaidaili.com/free/inha/1/', mod=2, session=session)),
            asyncio.create_task(get_page('https://www.kuaidaili.com/free/intr/2/', mod=2, session=session)),
            asyncio.create_task(
                get_page('https://www.proxy-list.download/api/v1/get?type=http', mod=5, session=session)),
            # asyncio.create_task(get_page('http://www.66ip.cn/areaindex_1/1.html', session=session)),
            # asyncio.create_task(get_page('http://www.66ip.cn/areaindex_5/1.html', session=session)),
            # asyncio.create_task(get_page('http://www.66ip.cn/areaindex_14/1.html', session=session)),
        ]
        for i in range(2):
            task.append(
                asyncio.create_task(get_page(f'http://www.nimadaili.com/http/{i + 1}/', mod=4, session=session)))

            task.append(
                asyncio.create_task(get_page(f'https://www.89ip.cn/index_{i + 1}.html', mod=3, session=session)))

            task.append(asyncio.create_task(
                get_page(f'http://http.taiyangruanjian.com/free/page{i + 1}/', mod=1, session=session)))

            task.append(
                asyncio.create_task(get_page(f'http://www.kxdaili.com/dailiip/1/{i + 1}.html', session=session)))

            task.append(
                asyncio.create_task(get_page(f'http://www.ip3366.net/free/?stype=1&page={i + 1}', session=session)))

            # task.append(asyncio.create_task(get_page(f'http://www.66ip.cn/areaindex_1{i + 1}/1.html', session=session)))

            task.append(asyncio.create_task(
                get_page(f'https://www.dieniao.com/FreeProxy/{i + 1}.html', mod=6, session=session)))

        # try:
        #     # 获取站大爷分享ip地址
        #     async with await session.get(url='https://www.zdaye.com/dayProxy.html',
        #                                  headers=await getheaders()) as response:
        #         page_zdy = await response.text()
        #         content = re.search(r'\"(/dayProxy/ip/\d+.html)\"', page_zdy).group(1)
        #         get_url = f'https://www.zdaye.com{content}'
        #     task.append(get_page(get_url, mod=7, session=session))
        # except Exception:
        #     pass
        await asyncio.wait(task)


# 访问网页
async def get_page(url, session, mod=0):
    tout = ClientTimeout(total=30)
    hd = await getheaders()
    try:
        async with await session.get(url=url, headers=hd, timeout=tout) as response:
            page_source = await response.text()
            await soup_page(page_source, mod=mod)
    except Exception as e:
        print(f"['{url}']抓取失败:", e)


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
            listIP.append(f'http://{ips.group()}:{posts.group(1)}')

    elif mod == 1:
        # 太阳
        soup = BeautifulSoup(source, 'lxml')
        lists = soup.find_all('div', class_='tr ip_tr')
        for li in lists:
            ips = re.findall(r'<div\sclass="td\std-4">(.*?)</div>', str(li))
            posts = re.findall(r'<div\sclass="td\std-2">(.*?)</div>', str(li))
            listIP.append(f'http://{ips[0]}:{posts[0]}')

    elif mod == 2:
        # 快代理
        soup = BeautifulSoup(source, 'lxml')
        tr = soup.find_all('tr')
        for t in tr:
            ips = re.findall(r'<td\s.*?="IP">(.*?)</td>', str(t))
            posts = re.findall(r'<td\s.*?="PORT">(.*?)</td>', str(t))
            if not ips or not posts:
                continue
            listIP.append(f'http://{ips[0]}:{posts[0]}')
    elif mod == 3:
        # 89代理
        soup = BeautifulSoup(source, 'lxml')
        tr = soup.select('tr')[1:]
        for td in tr:
            t = td.select('td')
            ips = re.search(r'(\d+\.){3}\d+', str(t[0]))
            posts = re.search(r'\d{2,4}', str(t[1]))
            listIP.append(f'http://{ips.group()}:{posts.group()}')
    elif mod == 4:
        # 泥马代理
        soup = BeautifulSoup(source, 'lxml')
        tr = soup.find_all('tr')[1:]
        for i in tr:
            ip_post = re.findall(r'<td>(.*?)</td>', str(i))[0]
            listIP.append(f'http://{ip_post}')
    elif mod == 5:
        # https://www.proxy-list.download/api/v1/get?type=http
        ip_list = source.split('\r\n')[:-1]
        for ip in ip_list:
            listIP.append(f'http://{ip}')
    elif mod == 6:
        # 蝶鸟
        ip_list = re.findall(r"<span\sclass='f-address'>(.*?)</span>", source)[1:]
        port_list = re.findall(r"<span class='f-port'>(\d+)</span>", source)
        for i in range(len(ip_list)):
            listIP.append(f'http://{ip_list[i]}:{port_list[i]}')
    elif mod == 7:
        # 站大爷
        soup = BeautifulSoup(source, 'lxml')
        tr = soup.find_all('tr')
        for t in tr:
            get_ip = re.search(r'(\d+\.){3}\d+', str(t))
            get_post = re.search(r'<td>(\d{1,4}).*?</td>', str(t))
            listIP.append(f'{get_ip.group(1)}:{get_post.group(1).strip()}')


def ip_main():
    asyncio.run(create_aiohttp_ip())
    print(f"代理ip抓取完成,共{len(listIP)}个可用代理ip地址。")


async def create_aiohttp(url, proxy_list):
    global n
    n = 0
    async with ClientSession() as session:
        # 生成任务列表
        task = [asyncio.create_task(web_request(url=url, proxy=proxy, session=session)) for
                proxy in proxy_list]
        await asyncio.wait(task)


# 网页访问
async def web_request(url, proxy, session):
    # 并发限制
    async with asyncio.Semaphore(20):
        try:
            async with await session.get(url=url, headers=await getheaders(), proxy=proxy,
                                         timeout=10) as response:
                page_source = await response.text()  # 返回字符串形式的相应数据
                await page(page_source)
        except Exception:
            pass


# 判断访问是否成功
async def page(page_source):
    global n
    if "学习天数" in page_source:
        n += 1


def main():
    ip_main()  # 抓取代理
    proxies = [i.strip() for i in listIP]  # 生成代理列表
    uvloop.install()
    asyncio.run(create_aiohttp(link, proxies))
    print(f"墨墨分享链接访问成功{n}次。")


if __name__ == '__main__':
    main()
