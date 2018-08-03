# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree
import json
import time

def reqeust(url,header):
    try:
        r = requests.get(url,headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("不是200",url)

def parse_link(html):
    response = etree.HTML(html)
    urls = response.xpath('//h4[@class="house-title"]/a/@href')
    return urls

if __name__ =="__main__":


    f = open("d://重庆租房信息(中原地产网).json","w",encoding = "utf-8")

    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }

    # cookie = {
    #     "bwlasttime":"1527406145.467",
    #     "guid":	"904815432",
    #     "lastpage":"5http%3A//cq.rent.house365.com/district/dl_p2.html",
    #     "lasttime":"1527406145.467",
    #     "PHPSESSID":"11266cd34c9dcab051f5282da603826d",
    #     "sessionid":"379724382domain=",
    #     "tf_city":"cq",
    #     "todayfirst":"false"
    # }
    start_urls = ["https://cq.centanet.com/zufang/g%d/" % d for d in range(1,54)]
    for url in start_urls:
        try:
            start_html = reqeust(url,header)
        except:
            continue
        try:
            houseIdList = parse_link(start_html )
        except:
            continue
        for id in houseIdList:
            communityInfo = {}
            TransactionAttribute = {}
            url = "https://cq.centanet.com" + id
            try:
                html = reqeust(url,header)
            except:
                continue
            try:
                response = etree.HTML(html)
            except:
                continue
            try:
                #所属省份
                communityInfo['province'] = "重庆市"
                #标题
                communityInfo['title'] = ''.join(response.xpath('//div[@class="house-detail-top"]/dl/dd/h2/text()')[0].split())
                # #所属小区
                communityInfo['community'] = response.xpath('//div[@class="xiaop"]/p/span[1]/a[1]/text()')[0].strip()
                # #所属位置
                communityInfo['position'] = ''.join(''.join(response.xpath('//div[@class="xiaop"]/p[2]/span[1]/text()')).split())
                # #建造年代
                communityInfo['year'] = response.xpath('//div[@class="infomid"]/p[2]/span[3]/text()')[0].strip()
                # #建筑类型
                communityInfo['house_type'] = response.xpath('//table[@class="baseinf"]//tr[1]/td[1]/text()')[0].strip()
                # #房屋户型
                communityInfo['house_style'] = ''.join(response.xpath('//div[@class="infomid"]/p[1]/span[1]/text()'))
                # #面积
                communityInfo['area'] = response.xpath('//table[@class="baseinf"]//tr[2]/td[2]/text()')[0]
                # #室内面积
                communityInfo['indoor_area'] = response.xpath('//table[@class="baseinf"]//tr[1]/td[2]/text()')[0].strip()
                # #房屋朝向
                # #communityInfo['aspect'] = response.xpath('//div[@class="sechand-detail-info"]//ul[2]/li[2]/span[2]/text()')[0]
                # #楼层
                communityInfo['floor'] = response.xpath('//table[@class="baseinf"]//tr[4]/td[2]/text()')[0]
                # #总价
                # #communityInfo['all_price'] = ''.join(response.xpath('//div[@class="sechand-info"]/div/h4//text()'))
                # #发布时间
                communityInfo['publish_time'] = response.xpath('//p[@class="labeltag"]/cite[3]/text()')[0]
                # #单价
                # #communityInfo['unit_price'] = ''.join(response.xpath('//div[@class="sechand-info"]/div/div/span//text()'))
                # #月租
                communityInfo['monthly_rent'] = ''.join(''.join(response.xpath('//div[@class="infotop"]/p[2]//text()')).split())
                # #首付
                # #communityInfo['first_payment'] = ""
                # #付款方式
                communityInfo['payment_style'] = ''.join(''.join(response.xpath('//table[@class="baseinf"]//tr[2]/td[1]/text()')).split())
                # #装修程度
                communityInfo['decoration_level'] = response.xpath('//div[@class="infomid"]/p[2]/span[2]/text()')[0].strip()
                # #描述
                communityInfo['descrip'] = ''.join(''.join(response.xpath('//div[@class="detailComment"]//p//text()')).split())
                #地铁
                #communityInfo['subway'] = ''.join(response.xpath('//div[@class="tab-cont-right"]/div[4]/div/div[2]/span/text()')).strip()
                #电梯
                #communityInfo['elevator'] = ''.join(response.xpath('//div[@class="sechand-detail-info"]//ul[2]/li[3]/span[2]/text()')).strip()
                #产权信息
                #communityInfo['property_right_info'] = ''.join(response.xpath('//div[@class="sechand-detail-info"]//ul[3]/li[3]/span[2]/text()')).strip()
                #户型结构
                #communityInfo['house_style_struct'] = response.xpath('//div[@class="base"]/div[2]/ul/li[4]/text()')[0]
                #建筑结构
                #communityInfo['build_struct'] = response.xpath('//div[@class="base"]/div[2]/ul/li[8]/text()')[0]
                #梯户比例
                #communityInfo['floor_house_ratio'] = response.xpath('//div[@class="base"]/div[2]/ul/li[10]/text()')[0]
                #产权年限
                #communityInfo['property_right_year'] = response.xpath('//div[@class="_2LqAj"]/div[2]/li[5]/span[2]/text()')
                #挂牌时间
                # TransactionAttribute['publish_time']=response.xpath('//div[@class="transaction"]/div[2]/ul/li[1]//span/text()')
                # #上次交易时间
                # TransactionAttribute['last_transaction_time'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[3]//span/text()')
                # #房屋年限
                # TransactionAttribute['house_year_limit'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[5]//span/text()')
                # #抵押信息
                # TransactionAttribute['pledge_info'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[7]/span[2]/@title')
                # #交易权属
                # TransactionAttribute['transaction_ownership'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[2]/span/text()')
                # #房屋用途
                # TransactionAttribute['house_use'] =response.xpath('//div[@class="transaction"]/div[2]/ul/li[4]/span/text()')
                # #产权所属
                # TransactionAttribute['ownership'] = response.xpath('//div[@class="transaction"]/div[2]/ul/li[6]/span/text()')
                #链接
                communityInfo['url'] = url
               # houseInfoDict.append((TransactionAttribute))
                print(communityInfo)
                json.dump(communityInfo, f, ensure_ascii=False, indent=4)
            except:
                print("出错啦！",url)

    f.close()
