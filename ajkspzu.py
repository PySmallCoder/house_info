# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree
import json

def reqeust(url,header,cookie):
    r = requests.get(url,headers=header,cookies=cookie,timeout=30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

def parse_link(html):
    urls = re.findall(r'https://chongqing.anjuke.com/prop/view/A[0-9]{10}',html)
    return urls

if __name__ =="__main__":

    houseInfoDict = []

    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }

    cookie = {
        "58tj_uuid": "969984f6-d5b1-4b63-b7cb-5f557af8e82f;",
        "als": "0;",
        'aQQ_ajkguid': 'C6ADE390-8535-77D9-2282-F87A3868C952;',
        'ctid': '20;',
        '_ga': 'GA1.2.2074477191.1526995874;',
        '_gid': 'GA1.2.616896479.1526995874;',
        'isp': 'true;',
        'Hm_lvt_c5899c8768ebee272710c9c5f365a6d8': '1526999312;',
        'lp_lt_ut': 'c882a30b5f4b13d8af07a2ba520142e6;',
        'browse_comm_ids': '616716%7C874320%7C873088%7C823678%7C368442;',
        'propertys': 'kelnby-p94xq5_jz2267-p94w8s_kcn0rg-p94ua5_k7kemp-p94u19_k7qs8y-p94tzl_k7fdq7-p94ts2_;',
        'lps': 'http%3A%2F%2Fchongqing.anjuke.com%2Fsale%2Fp1%2F%7C;',
        'twe': '2;',
        'sessid': '9A47033C-9405-B888-0C38-34EF711A3211;',
        '__xsptplusUT_8': '1;',
        'new_session': '1;',
        'new_uv': '4;',
        '__xsptplus8': '8.5.1527035612.1527035612.1%232%7Cwww.baidu.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%23Yv_o6_zTj0-ivJhvzpSMOkJ7VM7NinKZ%23;',
        '_gat': '1'
    }
    start_urls = ["https://cq.zu.anjuke.com/fangyuan/p%d/" % d for d in range(1,50)]
    for url in start_urls:
        start_html = reqeust(url,header,cookie)
        urls = parse_link(start_html )
        for url in urls:
            communityInfo = {}
            html = reqeust(url,header,cookie)
            response = etree.HTML(html)
            #所属省份
            communityInfo['province'] = "重庆市"
            #所属小区
            communityInfo['community'] = response.xpath('//div[@class="houseInfo-wrap"]/div/div/dl[1]/dd/a/text()')[0].strip()
            position_list = response.xpath('//p[@class="loc-text"]//text()')
            #所属位置
            communityInfo['position'] = position_list[0]+position_list[2]+position_list[3][9:]
            #建造年代
            communityInfo['year'] = response.xpath('//div[@class="houseInfo-wrap"]/div/div[1]/dl[3]/dd/text()')[0].strip()
            #房屋类型
            communityInfo['house_type'] = response.xpath('//div[@class="houseInfo-wrap"]/div/div[1]/dl[4]/dd/text()')[0].strip()
            #房屋户型
            communityInfo['house_style'] = ''.join(response.xpath('//div[@class="houseInfo-wrap"]/div/div[2]/dl[1]/dd/text()')[0].split())
            #面积
            communityInfo['area'] = response.xpath('//div[@class="houseInfo-wrap"]/div/div[2]/dl[2]/dd/text()')[0].strip()
            #房屋朝向
            communityInfo['aspect'] = response.xpath('//div[@class="houseInfo-wrap"]/div/div[2]/dl[3]/dd/text()')[0].strip()
            #楼层
            communityInfo['floor'] = response.xpath('//div[@class="houseInfo-wrap"]/div/div[2]/dl[4]/dd/text()')[0].strip()
            #单价
            communityInfo['unit_price'] = response.xpath('//div[@class="houseInfo-wrap"]/div/div[3]/dl[1]/dd/text()')[0].strip()
            #首付
            communityInfo['first_payment'] = response.xpath('//div[@class="houseInfo-wrap"]/div/div[3]/dl[2]/dd/text()')[0].strip()
            #装修程度
            communityInfo['decoration_level'] = response.xpath('//div[@class="houseInfo-wrap"]/div/div[3]/dl[4]/dd/text()')[0].strip()
            houseInfoDict.append(communityInfo)
            print(communityInfo)

with open("d://房产//fangchan.json","w",encoding = "utf-8") as f:
    json.dump(houseInfoDict,f,ensure_ascii=False,indent=4)
    print("文件写入完成")
