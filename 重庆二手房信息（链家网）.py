# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree
import json
import time

def reqeust(url,header,cookie):
    r = requests.get(url,headers=header,cookies=cookie)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

def parse_link(html):
    response = etree.HTML(html)
    urls = response.xpath('//ul[@log-mod="list"]//li/a/@href')
    return urls

if __name__ =="__main__":

    houseInfoDict = []

    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }

    cookie = {
        "all-lj":"762328e22710c88ff41f391dedabbc6f",
        "lianjia_ssid":"d592c167-ffc0-4a2f-930c-4389328856e8",
        "lianjia_uuid":"d49b4ae3-12ac-49a8-bd2f-a84901e66757",
        "select_city":"500000"
    }
    start_urls = ["https://cq.lianjia.com/ershoufang/pg%d/" % d for d in range(1,101)]
    for url in start_urls:
        try:
            start_html = reqeust(url,header,cookie)
            time.sleep(1)
        except:
            continue
        urls = parse_link(start_html )
        for url in urls:
            communityInfo = {}
            TransactionAttribute = {}
            html = reqeust(url,header,cookie)
            time.sleep(1)
            response = etree.HTML(html)
            try:
                #所属省份
                communityInfo['province'] = "重庆市"
                #标题
                communityInfo['title'] = ''.join(response.xpath('//h1[@class="main"]/@title')[0].split())
                #所属小区
                communityInfo['community'] = response.xpath('//div[@class="communityName"]/a[1]/text()')[0].strip()
                #所属位置
                communityInfo['position'] = ''.join(''.join(response.xpath('//div[@class="areaName"]/a[1]/text()')).split())
                #建造年代
                communityInfo['year'] = response.xpath('//div[@class="area"]/div[@class="subInfo"]/text()')[0].strip()
                #建筑类型
                communityInfo['house_type'] = response.xpath('//div[@class="base"]/div[2]/ul/li[6]/text()')[0].strip()
                #房屋户型
                communityInfo['house_style'] = ''.join(response.xpath('//div[@class="base"]/div[2]/ul/li[1]/text()')[0].split())
                #面积
                communityInfo['area'] = response.xpath('//div[@class="base"]/div[2]/ul/li[3]/text()')[0].strip()
                #室内面积
                communityInfo['indoor_area'] = response.xpath('//div[@class="base"]/div[2]/ul/li[5]/text()')[0].strip()
                #房屋朝向
                communityInfo['aspect'] = response.xpath('//div[@class="base"]/div[2]/ul/li[7]/text()')[0].strip()
                #楼层
                communityInfo['floor'] = response.xpath('//div[@class="base"]/div[2]/ul/li[2]/text()')[0].strip()
                #单价
                communityInfo['unit_price'] = response.xpath('//span[@class="unitPriceValue"]//text()')[0].strip()
                #首付
                communityInfo['first_payment'] = ""
                #装修程度
                communityInfo['decoration_level'] = response.xpath('//div[@class="base"]/div[2]/ul/li[9]/text()')[0].strip()
                #描述
                communityInfo['descrip'] = ''.join(''.join(response.xpath('//div[@class="txt"]//span//text()')).split())
                #电梯
                communityInfo['elevator'] = response.xpath('//div[@class="base"]/div[2]/ul/li[11]/text()')[0]
                #户型结构
                communityInfo['house_style_struct'] = response.xpath('//div[@class="base"]/div[2]/ul/li[4]/text()')[0]
                #建筑结构
                communityInfo['build_struct'] = response.xpath('//div[@class="base"]/div[2]/ul/li[8]/text()')[0]
                #梯户比例
                communityInfo['floor_house_ratio'] = response.xpath('//div[@class="base"]/div[2]/ul/li[10]/text()')[0]
                #产权年限
                communityInfo['property_right_year'] = response.xpath('//div[@class="base"]/div[2]/ul/li[12]/text()')[0]
                #挂牌时间
                TransactionAttribute['publish_time']=response.xpath('//div[@class="transaction"]/div[2]/ul/li[1]//span/text()')
                #上次交易时间
                TransactionAttribute['last_transaction_time'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[3]//span/text()')
                #房屋年限
                TransactionAttribute['house_year_limit'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[5]//span/text()')
                #抵押信息
                TransactionAttribute['pledge_info'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[7]/span[2]/@title')
                #交易权属
                TransactionAttribute['transaction_ownership'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[2]/span/text()')
                #房屋用途
                TransactionAttribute['house_use'] =response.xpath('//div[@class="transaction"]/div[2]/ul/li[4]/span/text()')
                #产权所属
                TransactionAttribute['ownership'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[6]/span/text()')
                #链接
                communityInfo['url'] = url
                houseInfoDict.append(communityInfo)
                houseInfoDict.append((TransactionAttribute))
                print(communityInfo,TransactionAttribute)
            except:
                print("出错啦！",url)

    with open("d://重庆二手房信息(链家网).json","w",encoding = "utf-8") as f:
        json.dump(houseInfoDict,f,ensure_ascii=False,indent=4)
        print("文件写入完成")
