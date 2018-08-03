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
    urls = response.xpath('//ul[@class="listUl"]//li/div[@class="des"]/h2/a[1]/@href')
    return urls

if __name__ =="__main__":

    f = open("d://重庆二手房信息(58同城网).json", "w", encoding="utf-8")
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }

    cookie = {
        "58home":"cn",
        "58tj_uuid":"8e2578a2-8657-4e96-a8e3-198356bd46f4",
        "als":"0",
        "city":"cn",
        "commontopbar_ipcity":"cq|é��åº�|0",
        "commontopbar_myfeet_tooltip":"end",
        "commontopbar_new_city_info":"2258|å�¶ä»�|cn",
        "f":"n",
        "id58":	"c5/njVsNaZCGNd9AA8ZUAg==",
        "new_session":"0",
        "new_uv":"1",
        "wmda_new_uuid":"1",
        "wmda_session_id_2385390625025":"1527605694963-09c4bf19-7ba0-c0f7",
        "wmda_uuid":"9b1c678d85480cbcc54ddcba6e43df09",
        "wmda_visited_projects":";2385390625025",
        "xxzl_deviceid":"Ok07dJCp81nZPsqfDrvvP8IreYX+zQ+ZyInfRALFPb6JELYerYRLj3nMbGFR43H0"
    }

    chuzu1 = ["http://cn.58.com/chuzu/pn%d/?PGTID=0d3090a7-008d-22ff-be01-919044cfec22&ClickID=1" % d for d in range(1,5)]
    chuzu2 = ["http://cn.58.com/chuzu/0/pn%d/?PGTID=0d3090a7-008d-2b53-40a1-e1e912d95914&ClickID=1" % d for d in range(1,4)]

    start_urls = chuzu1 + chuzu2
    start_urls.append("http://cn.58.com/chuzu/1/?PGTID=0d3090a7-008d-2d63-8bf2-2618548c6d6e&ClickID=1")

    for url in start_urls:
        try:
            start_html = reqeust(url,header)
        except:
            continue
        houseIdList = parse_link(start_html )
        for url in houseIdList:
            communityInfo = {}
            TransactionAttribute = {}
            try:
                html = reqeust(url, header)
            except:
                continue
            try:
                response = etree.HTML(html)
            except:
                continue
            try:
                # 所属省份
                communityInfo['province'] = "重庆市"
                # 标题
                communityInfo['title'] = response.xpath('//div[@class="house-title"]/h1/text()')[0]
                # # 所属小区
                communityInfo['community'] = response.xpath('//ul[@class="f14"]/li[4]/span[2]/a/text()')
                # # 所属位置
                communityInfo['position'] = ''.join(''.join(response.xpath('//ul[@class="f14"]/li[5]/span[2]/text()')).split())
                # # 建造年代
                # #communityInfo['year'] = response.xpath('//div[@class="_2LqAj"]/div[2]/li[2]/span[2]/text()')[0]
                # # 建筑类型
                # communityInfo['house_type'] = response.xpath('//div[@class="exp-box no-mbb"]/div[1]/p[2]/span/text()')[0]
                # # 房屋户型
                communityInfo['house_style'] = response.xpath('//ul[@class="f14"]/li[2]/span[2]/text()')
                # # 面积
                communityInfo['area'] = response.xpath('//ul[@class="f14"]/li[2]/span[2]/text()')
                # # 室内面积
                # #communityInfo['indoor_area'] = response.xpath('//div[@class="base"]/div[2]/ul/li[5]/text()')[0].strip()
                # # 房屋朝向
                communityInfo['aspect'] = response.xpath('//ul[@class="f14"]/li[3]/span[2]/text()')
                # # 楼层
                communityInfo['floor'] = response.xpath('//ul[@class="f14"]/li[3]/span[2]/text()')
                #租房方式
                communityInfo['rent_style'] = response.xpath('//ul[@class="f14"]/li[1]/span[2]/text()')
                # # 总价
                # communityInfo['all_price'] = ''.join(response.xpath('//div[@class="lp-con-box"]/dl/dd[1]/p[2]//text()'))
                # # 发布时间
                # publishTime = ''.join(''.join(response.xpath('//div[@class="exp-box"]/div[2]/p[3]/span/text()')).split())
                communityInfo['publish_time'] = response.xpath('//div[@class="house-title"]/p/text()')
                # # 单价
                # communityInfo['unit_price'] = response.xpath('//div[@class="exp-box"]/div[1]/p[1]/span/text()')[0]
                # # 月租
                communityInfo['monthly_rent'] = response.xpath('//div[@class="house-basic-desc"]/div/div/span/b/text()')
                # # 首付
                # communityInfo['first_payment'] = ''.join(response.xpath('//div[@class="lp-con-box"]/dl/dd[2]/p[2]//text()'))
                # # 付款方式
                communityInfo['payment_style'] = ''.join(''.join(response.xpath('//div[@class="house-basic-desc"]/div/div/span[2]/text()')).split())
                # # 装修程度
                communityInfo['decoration_level'] = response.xpath('//ul[@class="f14"]/li[2]/span[2]/text()')
                # # 描述
                communityInfo['descrip'] = ''.join(''.join(response.xpath('//ul[@class="introduce-item"]//p/text()')).split())
                # #绿化率
                # communityInfo['green_rate'] = response.xpath('//div[@class="esf-left-side"]/div[2]/div[2]/div[2]/p[2]/span/text()')[0]
                # #周边购物
                # communityInfo['around_shop'] = response.xpath('//div[@class="esf-left-side"]/div[2]/div[2]/div[3]/p[1]/span/text()')[0]
                # #周边医院
                # communityInfo['around_hospital'] = response.xpath('//div[@class="esf-left-side"]/div[2]/div[2]/div[3]/p[2]/span/text()')[0]
                # #周边学院
                # communityInfo['around_school'] = \
                #     response.xpath('//div[@class="esf-left-side"]/div[2]/div[2]/div[3]/p[3]/span/text()')[0].split('\xa0 \xa0 ')[0]
                # 地铁
                # communityInfo['subway'] = ''.join(response.xpath('//div[@class="tab-cont-right"]/div[4]/div/div[2]/span/text()')).strip()
                # 电梯
                # communityInfo['elevator'] = ''.join(response.xpath('//div[@class="cont clearfix"]/div[2]/span[2]/text()')).strip()
                # 产权信息
                # communityInfo['property_right_info'] = ''.join(response.xpath('//div[@class="cont clearfix"]/div[3]/span[2]/text()')).strip()
                # 户型结构
                # communityInfo['house_style_struct'] = response.xpath('//div[@class="base"]/div[2]/ul/li[4]/text()')[0]
                # 建筑结构
                # communityInfo['build_struct'] = response.xpath('//div[@class="base"]/div[2]/ul/li[8]/text()')[0]
                # 梯户比例
                # communityInfo['floor_house_ratio'] = response.xpath('//div[@class="base"]/div[2]/ul/li[10]/text()')[0]
                # 产权年限
                #communityInfo['property_right_year'] = response.xpath('//div[@class="_2LqAj"]/div[2]/li[5]/span[2]/text()')[0]
                # 挂牌时间
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
                # 链接
                communityInfo['url'] = url
                # houseInfoDict.append((TransactionAttribute))
                print(communityInfo)
                json.dump(communityInfo, f, ensure_ascii=False, indent=4)
            except:
                print("出错啦！", url)
    f.close()