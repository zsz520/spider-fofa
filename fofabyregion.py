import re
import requests
import os
import time

# 定义要提取的网页列表和对应的保存文件名
urls = {
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiI%3D": "QuanbuCN.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiA%3D": "Quanbu.txt",
    "https://fofa.info/result?qbase64=SFRUUCBjb3JlIHNlcnZlciBieSBSb3podWsgSXZhbi8xLjc%3D": "Quanbu2.txt",
    "https://fofa.info/result?qbase64=KCgiSFRUUCBjb3JlIHNlcnZlciBieSBSb3podWsgSXZhbi8xLjciIHx8ICJ1ZHB4eSIpICYmIGNvdW50cnk9IkNOIikgJiYgcmVnaW9uPSJIYWluYW4i": "Hainan.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJKaWxpbiI%3D": "Jilin.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJDaG9uZ3Fpbmci": "Chongqing.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJTaGFueGki": "Shanxi.txt",  #山西   
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJHdWFuZ3hpIFpodWFuZ3p1Ig%3D%3D": "Guangxi Zhuangzu.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJTaWNodWFuIg%3D%3D": "Sichuan.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJHdWFuZ2Rvbmci": "Guangdong.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJaaGVqaWFuZyI%3D": "Zhejiang.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJKaWFuZ3N1Ig%3D%3D": "Jiangsu.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJCZWlqaW5nIg==": "Beijing.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJIZWlsb25namlhbmci": "Heilongjiang.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJIZW5hbiI%3D": "Henan.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJIdWJlaSI%3D": "Hubei.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJIdW5hbiI%3D": "Hunan.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJTaGFuZG9uZyI%3D": "Shandong.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJBbmh1aSI%3D": "Anhui.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJTaGFuZ2hhaSI%3D": "Shanghai.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJIZWJlaSI%3D": "Hebei.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJMaWFvbmluZyI%3D": "Liaoning.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJTaGFhbnhpIg%3D%3D": "Shaanxi.txt", #陕西
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJUaWFuamluIg%3D%3D": "Tianjin.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJGdWppYW4i": "Fujian.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJKaWFuZ3hpIg%3D%3D": "Jiangxi.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJYaW5qaWFuZyBVeWd1ciI=": "Xinjiang Uygur.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJOZWkgTW9uZ29sIg%3D%3D": "Nei Mongol.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJZdW5uYW4i": "Yunnan.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJHdWl6aG91Ig==": "Guizhou.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJHYW5zdSI%3D": "Gansu.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJRaW5naGFpIg%3D%3D": "Qinghai.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJOaW5neGlhIEh1aXp1Ig%3D%3D": "Ningxia Huizu.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiByZWdpb249IlRXIg%3D%3D": "TW.txt",
    "https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjb3VudHJ5PSJDTiIgJiYgcmVnaW9uPSJISyI%3D": "HK.txt",
    "https://fofa.info/result?qbase64=KCgiSFRUUCBjb3JlIHNlcnZlciBieSBSb3podWsgSXZhbi8xLjciIHx8ICJ1ZHB4eSIpICYmIGNvdW50cnk9IkNOIikgJiYgcmVnaW9uPSJYaXphbmci": "Xizang.txt",#Xizang
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIg": "SXZ.txt",
    "https://fofa.info/result?qbase64=L1pIR1hUVi9pbmRleC5waHA%3D": "ZHGX.txt",
    "https://fofa.info/result?qbase64=c3RhdGljL3R2aC5qcy5neg%3D%3D": "TVH.txt",
    "https://fofa.info/result?qbase64=Imh0dHA6Ly9tdW11ZHZiLm5ldC8i": "MUMU.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04i": "udpandmsdcn.txt",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
# 遍历网页列表
for url, filename in urls.items():
    try:
        print(f'正在爬取{filename}.....')
        # 发送GET请求获取源代码
        response = requests.get(url, headers=headers)
        page_content = response.text
        # 查找所有符合指定格式的网址
        pattern = r'<a href="http://(.*?)" target="_blank">'
        urls_all = re.findall(pattern, page_content)
        urls = set(urls_all)  # 去重得到唯一的URL列表
        existing_urls = []
        # 检查文件是否存在，如果不存在则创建文件
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8'):
                pass
        # 读取已存在的URL
        with open(filename, 'r', encoding='utf-8') as file:
            existing_urls = file.readlines()
        existing_urls = [url.strip() for url in existing_urls]  # 去除每行末尾的换行符
        with open(filename, 'r+', encoding='utf-8') as file:
            content = file.read()
            file.seek(0, 0)  # 将文件指针移到文件开头
            for url in urls:
                if url not in existing_urls:
                    file.write(url + "\n")
                    print(url)
                    existing_urls.append(url)  # 将新写入的URL添加到已存在的URL列表中
            file.write(content)  # 将原有内容写回文件
    except Exception as e:
        print(f"爬取 {filename} URL {url} 失败：{str(e)}")
        continue
    # 暂停5秒
    time.sleep(5)
    print(f'{filename}爬取完毕,下一个')
