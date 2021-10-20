对4.1进行略微改进:

### 解决
ssl问题 [参考](https://www.pythonheidong.com/blog/article/506776/f797119eef523700648a/)

### 新的坑
DeprecationWarning: The explicit passing of coroutine objects to asyncio.wait() is deprecated since Python 3.8, and scheduled for removal in Python 3.11.
await asyncio.wait(task)
【弃用警告：自 Python 3.8 起不推荐将协程对象显式传递给 asyncio.wait()，并计划在 Python 3.11.await asyncio.wait(task) 中删除】