import re
import requests
import os
import time

# 定义要提取的网页列表和对应的保存文件名
urls = {
  #sichuan
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9ImNoZW5nZHUi": "Chengdu.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Im5hbmNob25nIg%3D%3D": "Nanchong.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9InN1aW5pbmci": "Suining.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Im5laWppYW5nIg%3D%3D": "Neijiang.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Imxlc2hhbiI%3D": "Leshan.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Ikx1emhvdSI%3D": "Luzhou.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlppZ29uZyI%3D": "Zigong.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IllpYmluIg%3D%3D": "Yibin.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Ik1pYW55YW5nIg%3D%3D": "Mianyang.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IkRleWFuZyI%3D": "Deyang.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IkRhemhvdSI%3D": "Dazhou.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IkJhemhvbmci": "Bazhong.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Ikd1YW5nJ2FuIg%3D%3D": "Guang'an.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Ikd1YW5neXVhbiI%3D": "Guangyuan.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlppeWFuZyI%3D": "Ziyang.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IllhJ2FuIg%3D%3D": "Ya'an.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Im1laXNoYW4i": "Meishan.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9InBhbnpoaWh1YSI%3D": "Panzhihua.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IkJhcmthbSI%3D": "Barkam.txt",#aba
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9ImxpYW5nc2hhbiI%3D": "Liangshan.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlhpY2hhbmci": "Xichang.txt",#Liangshan
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IkthbmdkaW5nIg%3D%3D": "Kangding.txt",#ganzi
    
    
    
  #hubei
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Ind1aGFuIg%3D%3D": "Wuhan.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlhpYW5neWFuZyI%3D": "Xiangyang.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Ikppbmd6aG91Ig%3D%3D": "Jingzhou.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Ikh1YW5nc2hpIg%3D%3D": "Huangshi.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlNoaXlhbiI%3D": "Shiyan.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9Ikh1YW5nZ2FuZyI%3D": "Huanggang.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlhpYW9nYW4i": "Xiaogan.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IllpY2hhbmci": "Yichang.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlhpYW5uaW5nIg%3D%3D": "Xianning.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IkppbmdtZW4i": "Jingmen.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IkVuc2hpIg%3D%3D": "Enshi.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IkV6aG91Ig%3D%3D": "Ezhou.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlN1aXpob3Ui": "Suizhou.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlRpYW5tZW4i": "Tianmen.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9IlhpYW50YW8i": "Xiantao.txt",
    "https://fofa.info/result?qbase64=KCJIVFRQIGNvcmUgc2VydmVyIGJ5IFJvemh1ayBJdmFuLzEuNyIgfHwgInVkcHh5IikgJiYgY291bnRyeT0iQ04iICYmIGNpdHk9InFpYW5qaWFuZyI%3D": "Qianjiang.txt",
    

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
