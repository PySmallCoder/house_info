# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree
import json

def reqeust(url,header,cookie):
    r = requests.get(url,headers=header,cookies=cookie,timeout=60)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

def parse_link(html):
    response = etree.HTML(html)
    urls = response.xpath('//div[@class="list-item"]/@link')
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
        "58tj_uuid": "969984f6-d5b1-4b63-b7cb-5f557af8e82f;",
        "als": "0;",
        'aQQ_ajkguid': 'C6ADE390-8535-77D9-2282-F87A3868C952;',
        'ctid': '20;',
        '_ga': 'GA1.2.2074477191.1526995874;',
        '_gid': 'GA1.2.616896479.1526995874;',
        'isp': 'true;',
        'propertys' : 'j4knsv - p96bg9_;',
        'Hm_lvt_c5899c8768ebee272710c9c5f365a6d8': '1526999312,1527119732;',
        'lp_lt_ut': '5f26869df0f2d462d3bf70fe1c40ca67;',
        'browse_comm_ids': '616716%7C874320%7C873088%7C823678%7C368442;',
        'propertys': 'kelnby-p94xq5_jz2267-p94w8s_kcn0rg-p94ua5_k7kemp-p94u19_k7qs8y-p94tzl_k7fdq7-p94ts2_;',
        'lps': 'http%3A%2F%2Fwww.anjuke.com%2F%3Fpi%3DPZ-baidu-pc-all-biaoti%7Chttps%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%26rsv_spt%3D1%26rsv_iqid%3D0xf6fa1cae00020a29%26issp%3D1%26f%3D8%26rsv_bp%3D0%26rsv_idx%3D2%26ie%3Dutf-8%26tn%3D98012088_5_dg%26ch%3D12%26rsv_enter%3D1%26rsv_sug3%3D4%26rsv_sug1%3D2%26rsv_sug7%3D100;',
        'twe': '2;',
        'sessid': 'A18D1680-2D53-FEB5-49EE-F3F047E8AB7A;',
        '__xsptplusUT_8': '1;',
        'new_uv': '12;',
        'new_session':'0',
        '__xsptplus8': '8.14.1527136110.1527136119.2%232%7Cwww.baidu.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%23VE3CzvpYg_iUnuNNiQnYkPQ7Msze9R7H%23;',
        '_gat': '1'
    }
    xzlzu_urls = ["https://cq.xzl.anjuke.com/zu/p%d/" % d for d in range(1,90)]
    xzlshou_urls = ['https://cq.xzl.anjuke.com/shou/p%d/' % d for d in range(1,90)]
    start_urls = xzlshou_urls + xzlzu_urls
    for url in start_urls:
        start_html = reqeust(url,header,cookie)
        urls = parse_link(start_html )
        print(urls)
        for url in urls:
            communityInfo = {}
            html = reqeust(url,header,cookie)
            response = etree.HTML(html)
            try:
                #所属省份
                communityInfo['province'] = "重庆市"
                #日租金
                communityInfo['data_rent'] = ''.join(response.xpath('//div[@id="fy_info"]//ul[@class="litem"]/li[1]/span[2]/text()'))
                #月租金
                communityInfo['month_rent'] = ''.join(response.xpath('//div[@id="fy_info"]//ul[@class="litem"]/li[2]/span[2]/text()'))
                #楼盘名
                communityInfo['house_name'] = response.xpath('//div[@id="fy_info"]//ul[@class="litem"]/li[4]/span[2]//text()')
                #地址
                communityInfo['address'] = ''.join(response.xpath('//div[@id="fy_info"]//ul[@class="litem"]/li[5]/span[2]//text()'))
                #地铁
                communityInfo['subway'] = ''.join(response.xpath('//div[@id="fy_info"]//ul[@class="litem"]/li[6]/span[2]//text()'))
                #面积
                communityInfo['area'] = ''.join(response.xpath('//div[@id="fy_info"]//ul[@class="ritem"]/li[1]/span[2]//text()'))
                #楼层
                communityInfo['floor'] = ''.join(response.xpath('//div[@id="fy_info"]//ul[@class="ritem"]/li[2]/span[2]//text()'))
                #工位数
                communityInfo['work_number'] = ''.join(response.xpath('//div[@id="fy_info"]//ul[@class="ritem"]/li[3]/span[2]//text()'))
                #物业费
                communityInfo['property_fee'] = ''.join(response.xpath('//div[@id="fy_info"]//ul[@class="ritem"]/li[4]/span[2]//text()')).strip()
                #类型
                communityInfo['type'] = ''.join(response.xpath('//div[@class="item-mod"]//ul[1]/li[1]/span[2]//text()'))
                #总楼层
                communityInfo['all_floor'] = ''.join(response.xpath('//div[@class="item-mod"]//ul[1]/li[2]/span[2]//text()'))
                #空调类型
                communityInfo['air_conditioner'] = ''.join(response.xpath('//div[@class="item-mod"]//ul[1]/li[5]/span[2]//text()'))
                #车位
                communityInfo['truck_space'] = ''.join(response.xpath('//div[@class="item-mod"]//ul[1]/li[6]/span[2]//text()'))
                #单层面积
                communityInfo['floor_area'] = ''.join(response.xpath('//div[@class="item-mod"]//ul[2]/li[1]/span[2]//text()'))
                #物业公司
                communityInfo['property_company'] = ''.join(response.xpath('//div[@class="item-mod"]//ul[2]/li[3]/span[2]//text()'))
                #电梯,
                communityInfo['elevator'] = ''.join(response.xpath('//div[@class="item-mod"]//ul[2]/li[5]/span[2]//text()'))
                houseInfoDict.append(communityInfo)
                print(communityInfo)
            except:
                print(response.url)

with open("d://房产//写字楼信息.json","w",encoding = "utf-8") as f:
    json.dump(houseInfoDict,f,ensure_ascii=False,indent=4)
    print("文件写入完成")
