#-*- coding:utf-8 -*-

##运行代码python crawler.py

# Beautiful Soup是一个用来解析html或者xml文件的库，支持元素选择器
from bs4 import BeautifulSoup
from urlparse import urljoin
# requests是一个对使用者非常友好的http库
import requests
import csv

url = "http://sh.58.com/pinpaigongyu/pn/{page}/?minprice=3000_5000"

#已完成的页数序号，初时为0
page = 0

csv_file = open("rent.csv","wb")
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
    page += 1
    print "fetch: ", url.format(page=page)
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text,"html.parser")
    house_list = html.select(".list > li")

    # 循环在读不到新的房源时结束
    if not house_list:
        break

    for house in house_list:
        house_title = house.select("h2")[0].string.encode("utf8")
        house_url = urljoin(url, house.select("a")[0]["href"])
        house_info_list = house_title.split()

        # 如果第二列是公寓名则取第一列作为地址
        if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]

        house_money = house.select(".money")[0].select("b")[0].string.encode("utf8")
        csv_writer.writerow([house_title, house_location, house_money, house_url])

csv_file.close()
