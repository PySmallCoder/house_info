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
    urls = response.xpath('//dl[@id="JS_listPag"]//h3/a/@href')
    return urls

if __name__ =="__main__":

    f = open("d://重庆租房信息（365淘房网).json","w",encoding = "utf-8")
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }

    cookie = {
        "guid":	"904815432",
        "PHPSESSID":"07144ca71b6c1ec17611510b4fce70b3",
        "sessionid":"1853463454domain=",
        "tf_city":"cq",
        "todayfirst":"false"
    }
    start_urls = ["http://cq.rent.house365.com/district/dl_p%d.html" % d for d in range(1,7)]
    for url in start_urls:
        try:
            start_html = reqeust(url,header,cookie)
        except:
            continue
        houseIdList = parse_link(start_html )
        for url in houseIdList:
            communityInfo = {}
            TransactionAttribute = {}
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
                communityInfo['title'] = ''.join(response.xpath('//div[@class="titleT"]/h1/text()')[0].split())
                #所属小区
                communityInfo['community'] = response.xpath('//div[@class="houseInfoMain"]/dl[8]/dd/text()')[0].strip()
                #所属位置
                communityInfo['position'] = ''.join(''.join(response.xpath('//div[@class="houseInfoMain"]/dl[7]/dd//text()')).split())
                #建造年代
                #communityInfo['year'] = response.xpath('//div[@class="sechand-detail-info"]//ul[1]/li[3]/span[2]/text()')[0]
                #建筑类型
                communityInfo['house_type'] = response.xpath('//div[@class="houseInfoMain"]/dl[4]/dd//text()')[0].strip()
                #房屋户型
                communityInfo['house_style'] = ''.join(''.join(response.xpath('//div[@class="houseInfoMain"]/dl[5]/dd//text()')).split())
                #面积
                communityInfo['area'] = response.xpath('//div[@class="houseInfoMain"]/dl[2]/dd//text()')[0][:-2]
                #室内面积
                #communityInfo['indoor_area'] = response.xpath('//div[@class="base"]/div[2]/ul/li[5]/text()')[0].strip()
                #房屋朝向
                #communityInfo['aspect'] = response.xpath('//div[@class="sechand-detail-info"]//ul[2]/li[2]/span[2]/text()')[0]
                #楼层
                communityInfo['floor'] = ''.join(''.join(response.xpath('//div[@class="houseInfoMain"]/dl[6]//text()')).split())
                #总价
                #communityInfo['all_price'] = ''.join(response.xpath('//div[@class="sechand-info"]/div/h4//text()'))
                #发布时间
                publishTime = ''.join(''.join(response.xpath('//div[@class="time"]/text()')).split())
                communityInfo['publish_time'] = re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',publishTime)[0]
                #单价
                #communityInfo['unit_price'] = ''.join(response.xpath('//div[@class="sechand-info"]/div/div/span//text()'))
                #月租
                communityInfo['monthly_rent'] = ''.join(response.xpath('//div[@class="houseInfoMain"]/dl[1]/dd//text()'))
                #首付
                #communityInfo['first_payment'] = ""
                #付款方式
                #communityInfo['payment_style'] = ''.join(''.join(response.xpath('//div[@class="trl-item_top"]/div[2]//text()')).split())
                #装修程度
                communityInfo['decoration_level'] = response.xpath('//div[@class="houseInfoMain"]/dl[3]/dd//text()')[0].strip()
                #描述
                communityInfo['descrip'] = ''.join(''.join(response.xpath('//div[@class="text"]//text()')).split())
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