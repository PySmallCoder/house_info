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
    urls = response.xpath('//ul[@class="lplist-ul"]/li/a[1]/@href')
    return urls

if __name__ =="__main__":

    houseInfoDict = []

    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }

    cookie = {
        "focus_city_c":"500000",
        "IPLOC":"CN5000",
        "is_from":"direct@@@@@@@@@@@@@@@@",
        "SUV":"1805271110394UXO"
    }
    f = open("d://重庆二手房信息（焦点房产网）).json","w",encoding = "utf-8")
    start_urls = ["https://esf.focus.cn/cq/houses/?page=%d&size=60" % d for d in range(1,18)]
    for url in start_urls:
        try:
            start_html = reqeust(url,header,cookie)
        except:
            continue
        print(url)
        houseIdList = parse_link(start_html )
        for houseId in houseIdList:
            communityInfo = {}
            TransactionAttribute = {}
            url = "https://esf.focus.cn" + houseId
            try:
                html = reqeust(url,header,cookie)
                response = etree.HTML(html)
            except:
                continue
            try:
                #所属省份
                communityInfo['province'] = "重庆市"
                #标题
                communityInfo['title'] = ''.join(response.xpath('//div[@class="secdetail-title"]/span/text()')[0].split())
                #所属小区
                communityInfo['community'] = response.xpath('//div[@class="sechand-info"]/div[4]/p[1]/a/text()')[0].strip()
                #所属位置
                communityInfo['position'] = ''.join(''.join(response.xpath('//div[@class="sechand-info"]/div[4]/p[2]/span[2]/text()')).split())
                #建造年代
                communityInfo['year'] = response.xpath('//div[@class="sechand-detail-info"]//ul[1]/li[3]/span[2]/text()')[0]
                #建筑类型
                communityInfo['house_type'] = response.xpath('//div[@class="sechand-detail-info"]//ul[3]/li[2]/span[2]/text()')[0].strip()
                #房屋户型
                communityInfo['house_style'] = ''.join(response.xpath('//div[@class="sechand-detail-info"]//ul[1]/li[1]/span[2]/text()'))
                #面积
                communityInfo['area'] = response.xpath('//div[@class="sechand-detail-info"]//ul[2]/li[1]/span[2]/text()')[0]
                #室内面积
                #communityInfo['indoor_area'] = response.xpath('//div[@class="base"]/div[2]/ul/li[5]/text()')[0].strip()
                #房屋朝向
                communityInfo['aspect'] = response.xpath('//div[@class="sechand-detail-info"]//ul[2]/li[2]/span[2]/text()')[0]
                #楼层
                communityInfo['floor'] = response.xpath('//div[@class="sechand-detail-info"]//ul[3]/li[1]/span[2]/text()')[0].strip()
                #总价
                communityInfo['all_price'] = ''.join(response.xpath('//div[@class="sechand-info"]/div/h4//text()'))
                #发布时间
                #publishTime = ''.join(''.join(response.xpath('//div[@class="_1iIO-"]/span[1]/text()')).split())
                #communityInfo['publish_time'] = re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',publishTime)[0]
                #单价
                communityInfo['unit_price'] = ''.join(response.xpath('//div[@class="sechand-info"]/div/div/span//text()'))
                #月租
                #communityInfo['monthly_rent'] = response.xpath('//span[@class="total"]/text()')[0]
                #首付
                #communityInfo['first_payment'] = ""
                #付款方式
                #communityInfo['payment_style'] = ''.join(''.join(response.xpath('//div[@class="trl-item_top"]/div[2]//text()')).split())
                #装修程度
                communityInfo['decoration_level'] = response.xpath('//div[@class="sechand-detail-info"]//ul[1]/li[2]/span[2]/text()')[0].strip()
                #描述
                #communityInfo['descrip'] = ''.join(''.join(response.xpath('//ul[@class="fyms_modify"]/li/div/div//text()')).split())
                #地铁
                #communityInfo['subway'] = ''.join(response.xpath('//div[@class="tab-cont-right"]/div[4]/div/div[2]/span/text()')).strip()
                #电梯
                communityInfo['elevator'] = ''.join(response.xpath('//div[@class="sechand-detail-info"]//ul[2]/li[3]/span[2]/text()')).strip()
                #产权信息
                communityInfo['property_right_info'] = ''.join(response.xpath('//div[@class="sechand-detail-info"]//ul[3]/li[3]/span[2]/text()')).strip()
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
                #houseInfoDict.append(communityInfo)
               # houseInfoDict.append((TransactionAttribute))
                print(communityInfo)
                json.dump(communityInfo, f, ensure_ascii=False, indent=4)
            except:
                print("出错啦！",url)


    f.close()
