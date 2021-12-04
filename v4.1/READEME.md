对4.0进行略微改进:

1. aiohttp.ClientSession() 只实例化一次即可。
2. 导入import encodings.idna 
   - 解决抓取代理网页抛出的异常:unknown encoding: idna。
   - 此问题是Pyinstaller打包程序之后出现。