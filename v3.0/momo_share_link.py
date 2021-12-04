# encoding:utf-8
import os.path

# 判断文件是否存在，不存在则创建
file = 'E:\\Desktop\\momo_link.txt'
if os.path.isfile(file):
    momo_share_link = open("E:\\Desktop\\momo_link.txt", 'r', encoding='utf-8')
    print(momo_share_link.readline())
else:
    os.mknod(file)  # 创建文件
