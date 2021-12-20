# encoding:utf-8
from os import environ
from ip import listIP, getheaders, ip_main
import asyncio
from aiohttp import ClientSession, TCPConnector

global n  # 记录访问成功次数
link = 'link'  # 设置link

# 如果检测到程序在 github actions 内运行，那么读取环境变量中的登录信息
if environ.get('GITHUB_RUN_ID', None):
    link = environ['link']


async def create_aiohttp(url, proxy_list):
    global n
    n = 0
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
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
                # 返回字符串形式的相应数据
                page_source = await response.text()
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
    asyncio.run(create_aiohttp(link, proxies))
    print(f"墨墨分享链接访问成功{n}次。")


if __name__ == '__main__':
    main()
