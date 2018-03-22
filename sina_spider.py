#coding:UTF-8
import os
import re
import requests
import lxml
from bs4 import BeautifulSoup

# 抓取新浪网
# 起始URL
url = "http://sports.sina.com.cn/lottery/col/5.html"
#url = "http://www.baidu.com"
html = requests.get(url)
# 解决中文乱码问题
#if html.encoding == "ISO-8859-1":
#    html.encoding = 'GBK'
#    html.encoding = 'utf-8'
#入口URL
#print(html.text)

soup = BeautifulSoup(html.content, "html.parser", from_encoding='utf-8')
#print(soup.prettify())

tags = soup.find_all("li")
#tags = soup.find_all("ul", class_="list1") # class_ 指定attr属性,可以查找带class属性的指定标签

url_pre = "http://sports.sina.com.cn"
for tag in tags:
    inner_url = tag.a['href']  # 取得内部链接
    auther_and_index = tag.a.get_text()  # 取得作者名和期数

    inner_url_abs = url_pre + inner_url
    
    auther = None
    index = None
    if re.search('18\d\d\d', auther_and_index):
        index = re.search('18\d\d\d', auther_and_index).group(0)  # 期数
    else:
        pass
    if re.search('^(.*)双色球', auther_and_index):
        auther = re.search('^(.*)双色球', auther_and_index).group(0)[:-3] #作者
    else:
        pass

    if index == '18031' and auther:
        html_inner = requests.get(inner_url_abs)
        soup_inner = BeautifulSoup(html_inner.content, "html.parser", from_encoding='utf-8')
        print("网址：" + inner_url_abs)
        print("专家：" + auther + ", 期数：" + index)
        tags_inner = soup_inner.find_all("p")
        for tag_inner in tags_inner:
            predict = tag_inner.get_text()
            pattern = re.compile(r'\d\d')
            if re.search("红球推荐", predict):
                red_list = pattern.findall(predict)
                print(red_list)
            elif re.search("蓝球推荐", predict):
                blue_list = pattern.findall(predict)
                print(blue_list)
            else:
                pass

