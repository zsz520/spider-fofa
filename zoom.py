import re
import requests
import os
import time
import json


# 定义要提取的网页列表和对应的保存文件名
urls = {
    "https://www.zoomeye.org/api/search?q=app%253A%2522udpxy%2522%252Bcountry%253A%2522CN%2522&page=1&pageSize=20&t=v4%2Bv6%2Bweb": "zoomquanbu.txt",

}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
# 遍历网页列表
for url, filename in urls.items():
    try:
        response = requests.get(url, headers=headers)
        #print(response.text)
        data = json.loads(response.text)
        matches = data["matches"]
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
            for match in matches:
                ip = match["ip"]
                port = match["portinfo"]["port"]
                url = f"{ip}:{port}"
                if url not in existing_urls:
                    file.write(url + "\n")
                    print(url)
                    existing_urls.append(url)  # 将新写入的URL添加到已存在的URL列表中
            file.write(content)  # 将原有内容写回文件
    except Exception as e:
        print(f"爬取 {filename} URL {url} 失败：{str(e)}")
        continue
    # 暂停2秒
    time.sleep(2)
    print(f'{filename}爬取完毕,下一个')




