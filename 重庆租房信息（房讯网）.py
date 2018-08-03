# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree
import json
import time

def reqeust(url,header,cookie):
    try:
        r = requests.get(url,headers=header,cookies=cookie)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("不是200",url)

def parse_link(html):
    response = etree.HTML(html)
    urls = response.xpath('//ul[@class="fang-list"]//li//div[@class="title"]/a/@href')
    return urls

if __name__ =="__main__":

    f = open("d://重庆租房信息(房讯网).json","w",encoding = "utf-8")

    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }

    cookie = {
        "com.fashion.city":"5001",
        "JSESSIONID":"054E76D88C42C3A660C295F4856F968F"
    }
    start_urls = ["http://chongqing.fangtoo.com/rent/p%d/" % d for d in range(1,69)]
    for url in start_urls:
        try:
            start_html = reqeust(url,header,cookie)
        except:
            continue
        print(url)
        try:
            houseIdList = parse_link(start_html )
        except:
            continue
        for houseId in houseIdList:
            communityInfo = {}
            TransactionAttribute = {}
            url = "http://chongqing.fangtoo.com" + houseId
            try:
                html = reqeust(url,header,cookie)
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
                communityInfo['title'] = ''.join(response.xpath('//div[@class="title z"]/div/b/text()')[0].split())
                #所属小区
                #communityInfo['community'] = response.xpath('//div[@class="aroundInfo"]/div[3]/div/a[1]//text()')[0].strip()
                #所属位置
                communityInfo['position'] = ''.join(''.join(response.xpath('//div[@class="fang-info-jb z"]/ul[3]/li[3]/a/text()')).split())
                #建造年代
                communityInfo['year'] = ''.join(''.join(response.xpath('//div[@class="fang-info-jb z"]/ul[2]/li[4]//text()')).split())
                #建筑类型
                communityInfo['house_type'] = response.xpath('//div[@class="fang-info-jb z"]/ul[3]/li[1]//text()')[0].strip()
                #房屋户型
                communityInfo['house_style'] = ''.join(response.xpath('//div[@class="fang-info-jb z"]/ul[1]/li[2]/span[2]/text()')).strip()
                #面积
                communityInfo['area'] = response.xpath('//div[@class="fang-info-jb z"]/ul[1]/li[2]/span[1]/text()')[0]
                #室内面积
                #communityInfo['indoor_area'] = response.xpath('//div[@class="base"]/div[2]/ul/li[5]/text()')[0].strip()
                #房屋朝向
                communityInfo['aspect'] = response.xpath('//div[@class="fang-info-jb z"]/ul[2]/li[1]/text()')[0].strip()
                #楼层
                communityInfo['floor'] = response.xpath('//div[@class="fang-info-jb z"]/ul[2]/li[2]/text()')[0].strip()
                #总价
                #communityInfo['all_price'] = ''.join(response.xpath('//div[@class="sechand-info"]/div/h4//text()'))
                #发布时间
                communityInfo['publish_time'] = response.xpath('//div[@class="time C666"]/text()')[0]
                #单价
                #communityInfo['unit_price'] = response.xpath('//div[@class="sechand-info"]/div/div/span//text()')
                #月租
                communityInfo['monthly_rent'] = ''.join(response.xpath('//ul[@class="jba"]/li[1]/span[1]//text()'))
                #房屋标签
                #communityInfo['house_tag'] = response.xpath('//div[@class="sechand-detail-info"]/ul[3]/li[3]/span[2]/text()')
                #出租类型
                #communityInfo['rent_type'] = response.xpath('//div[@class="type fl"]/div[1]/text()')[0].strip()
                #首付
                #communityInfo['first_payment'] = ""
                #付款方式
                communityInfo['payment_style'] = ''.join(''.join(response.xpath('//ul[@class="jba"]/li[1]/span[2]//text()')).split())
                #装修程度
                communityInfo['decoration_level'] = response.xpath('//ul[@class="jbb"]/li[3]/text()')[0].strip()
                #描述
                communityInfo['descrip'] = ''.join(''.join(response.xpath('//div[@id="editor"]//p//text()')).split())
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
                print(communityInfo)
                json.dump(communityInfo, f, ensure_ascii=False, indent=4)
            except:
                print("出错啦！",url)
    f.close()
