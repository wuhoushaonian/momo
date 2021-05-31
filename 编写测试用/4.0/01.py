# encoding:utf-8
import ip


# ip.ip_main()

def readfile():
    ip_list = []
    with open('ip.txt', 'r', encoding='utf-8') as f:
        ips = f.readlines()
    return ips


print(['http://' + i.strip() for i in readfile()])
