'''
This program aims to scrape product information from https://www.hktvmall.com/.
Program written by : Shirry Wan
Program created on : 17.06.2020
Last modified by   : Shirry Wan
Last modified on   : 12.01.2021
'''

import requests
from bs4 import BeautifulSoup
from datetime import date

import time
import datetime
import csv
import random
import sys
import os
import pandas as pd

user_agent_list = pd.read_csv("R:/CPI_SD/Online Pricing/User Agent/user_agent_20210217.csv")
user_agent_list = user_agent_list.values.tolist()

user_agent = random.choice(user_agent_list)

headers = {
    'User-Agent': user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

proxy_list = pd.read_csv("R:/CPI_SD/Online Pricing/Scraper Specification/proxy_20210217.csv")
proxy_list = proxy_list.values.tolist()

proxy = random.choice(proxy_list)

proxies = {
    "http": proxy,
	"https": proxy
}
OutletName = 'HKTVmall'
output_fileName = OutletName
output_path = os.getcwd() + '/../Data/Regular/'
outdate = datetime.datetime.now().strftime('%Y%m%d')
outtime = datetime.datetime.now().strftime('%H%M')

sys.stdout = open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_log.txt', 'w', encoding='utf-8-sig')

print('Start of Program Run')
print('********************************************************************************')
print('Outlet Name         : ', OutletName)
print('Current Date        : ', datetime.datetime.now().strftime('%Y.%m.%d'))
print('Current Time        : ', datetime.datetime.now().strftime('%H:%M:%S'))
print('********************************************************************************')

ProductSpec = ['QuotationNo', 'QuotationID', 'CPIBase', 'Set', 'CPICode', 'OutletID', 'OutletName', 'ProductID',
               'ProductName', 'ProductDesc', 'ProductGroup', 'PopularityRank', 'PopularityMethod', 'PopularityCounter',
               'EffectiveDate', 'ReferenceMonth', 'ExpiredDate', 'LastInputBy', 'Remarks', 'ChangeLog']
RawQuotation = ['RecordNo', 'QuotationID', 'CollectionDate', 'CollectionMethod', 'ReferenceMonth', 'BatchNo', 'Set',
				'CPICode', 'OutletID', 'ProductID', 'ProductName', 'ProductDesc', 'PopularityRank', 'CCY', 'CCYRate',
				'Availability', 'NP_LCY', 'NPR_LCY', 'SPA_LCY', 'SPAR_LCY', 'SPB_LCY', 'SPBR_LCY', 'SPC_LCY',
				'SPCR_LCY', 'SPD_LCY', 'SPDR_LCY', 'SPE_LCY', 'SPER_LCY', 'OutletRemarks', 'EditedNP_LCY',
				'EditedSP_LCY', 'EditedNP_HKE', 'EditedSP_HKE', 'EditingRemarks', 'RecordInputBy', 'SampleCheck',
				'SampleCheckBy', 'SampleCheckRemarks']

try:
    with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_ProductSpec.csv', 'w', newline='',
              encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(ProductSpec)

    with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_RawQuotation.csv', 'w', newline='',
              encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(RawQuotation)

except Exception as e:
    print('Please CLOSE related csv before run the program!')
    exit()

start_time = time.time()

with open(OutletName + '_Code.txt', 'r') as f:
    codes = f.read().splitlines()

url_string = 'https://www.hktvmall.com/p/'
URLs = [url_string + code for code in codes]

number = 0

for URL in URLs:

    try:

        number += 1
        print('\n(' + str(number) + ')', datetime.datetime.now().strftime('%Y.%m.%d,%H:%M:%S'))

        max_trial = 100
        no_trial = 0

        while no_trial < max_trial:
            try:
                html = requests.get(URL, headers=headers)
                soup = BeautifulSoup(html.text, 'html.parser')
                break
            except:
                no_trial += 1
                time.sleep(random.random() * 100 + random.random() * random.random() * 5 + 8)
                print(str(no_trial))

        if no_trial == max_trial:
            print(URL)
            print('no_trial == max_trial')
            ProductSpec = [str(number), '', '', '', '', '', '', '', URL]
            RawQuotation = [str(number), '', '', '', '', '', '', '', '', '', URL]

            with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_ProductSpec.csv', 'a',
                      newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(ProductSpec)

            with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_RawQuotation.csv', 'a',
                      newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(RawQuotation)

            continue

        Availability = 1
        NpriceOrg = ''
        overallRemarks = ''

        try:
            ProductName = soup.find('h1', {'class': 'last'})
            ProductName = ProductName.text
            print('ProductName    :', ProductName)
        except (IndexError, AttributeError):
            ProductName = URL

        try:
            Categories = soup.find('div', {'class': 'cat clearfix'})
            Categories = Categories.text.replace('\n', '  ').strip()
            Categories = Categories.replace('  ', ',')
            Categories = ''.join(filter(lambda x: not x.isdigit(), Categories))
            print('Categories     :', Categories)
        except (IndexError, AttributeError):
            Categories = ''

        try:
            Nprice = soup.find('div', {'class': 'promotional'})
            Nprice = Nprice.text
            NpriceOrg = Nprice.strip()
            Nprice = Nprice.replace('多買多平', '').replace('原價', '')
            Nprice = Nprice.replace('│', '').replace('|', '').replace('｜', '').replace('︱', '').replace('丨', '') \
                .replace('!', '').replace('﹗', '').replace('！', '').replace('*', '').replace('_', '') \
                .replace(':', '').replace('：', '').replace('。', '').replace('--', '').replace('-', '') \
                .replace('，', '   ').replace(',', '   ').replace('(', '').replace(')', '').replace(';', '') \
                .replace('、', '').replace('↓', '').replace('|', '').replace('~', '') \
                .replace('【', '').replace('】', '').replace('[', '').replace(']', '')                \
                .replace('平均最低$29.5/條', '').replace('平均最低$31.5/條', '').replace('特價$68', '') \
                .replace('買3包$75', '').replace('平均$25/包', '').replace('買3Set$57', '').replace('平均$9.5/包', '') \
                .replace('買2Set$46', '').replace('平均$11.5/包', '').replace('買2包', '').replace('每包$26', '') \
                .replace('54.8/2件', '').replace('58/2件', '').replace('59.9/2件', '').replace('62/2包', '') \
                .replace('63/2件', '').replace('64/2件', '') \
                .replace('69.9/3件', '').replace('72/2件', '').replace('76/2件', '').replace('80/6件', '') \
                .replace('89.9/2件', '').replace('99/2件', '').replace('99/3件', '') \
                .replace('99.9/2件', '').replace('109/2件', '').replace('119/2件', '') \
                .replace('129/3件', '').replace('149/2件', '').replace('189/2件', '').replace('219/2件', '') \
                .replace('買2件$51.9', '').replace('買2件$56', '').replace('買3件$79.8', '').replace('買2件$89', '') \
                .replace('買2件$90', '').replace('買2件$98', '').replace('買2件$99', '') \
                .replace('買4件$104', '').replace('買2件$108', '').replace('買4件$108', '') \
                .replace('買2件$112', '').replace('買2件$116', '').replace('買2件$118', '') \
                .replace('買2件$119', '').replace('買2件$120', '').replace('買4件$120', '') \
                .replace('買2件$126', '').replace('買2件$132', '').replace('買4件$136', '').replace('買2件$138', '') \
                .replace('買2件$142', '').replace('買4件$148', '').replace('買6件$155.6', '').replace('買4件$160', '') \
                .replace('買2件$169', '') \
                .replace('買2件$170', '').replace('買2件$172', '') \
                .replace('買4件$184', '').replace('買2件$188', '').replace('買4件$188', '').replace('買2件$189', '') \
                .replace('買2件$192', '').replace('買2件$198', '') \
                .replace('買2件$244', '').replace('買2件$282', '').replace('買2件$360', '').replace('買2件$378', '') \
                .replace('買2件$469', '').replace('買2件$492', '').replace('買2件$520', '').replace('買2件$578', '') \
                .replace('買2件$662', '') \
                .replace('特價$30', '').replace('特價$46', '').replace('特價$72', '') \
                .replace('特價$76/2件', '').replace('特價$118', '') \
                .replace('/包大劈價$62/2包', '') \
                .replace('平均$2.9/罐', '').replace('平均$4.5一罐', '') \
                .replace('低至$55', '').replace('低至$188', '') \
                .replace('低至3折', '').replace('低至7折', '') \
                .replace('至少69折', '').replace('最少7折', '').replace('單件88折', '') \
                .replace('閃購價$30', '').replace('大劈價$108', '').replace('買2包 每包$26', '') \
                .replace('買2Set 平均每杯$8', '').replace('買3Set$57平均$9.5/包', '') \
                .replace('買2Set$46平均$11.5/包', '').replace('買2Set$57平均$9.5/包', '') \
                .replace('限時優惠$99', '').replace('全店最少8折', '') \
                .replace('10套一箱$288', '').replace('4套一箱$275', '') \
                .replace('2021 無限', '').replace('2021全店', '') \
                .replace('12月', '').replace('N1', '') \
                .replace('RSP', '').replace('SRP', '').replace('優惠', '').replace('超低', '') \
                .replace('半價', '').replace('折扣', '').replace('10大熱銷', '').replace('10大養生', '') \
                .replace('大特價', '').replace('特價', '') \
                .replace('包送貨', '').replace('父親節', '').replace('母親節', '') \
                .replace('夏日', '').replace('假日', '').replace('假期', '').replace('全年', '').replace('最暢銷', '') \
                .replace('全店狂減', '').replace('有限的時間和庫存', '').replace('送手機支架', '').replace('HKTV', '') \
                .replace('感謝祭瘋狂減', '').replace('2支/6支平更多', '').replace('今日', '') \
                .replace('迎聖誕', '').replace('賀新年', '').replace('大特價', '') \
                .replace('限定減', '').replace('限定', '').replace('限時', '').replace('最抵', '').replace('感謝', '') \
                .replace('信譽優良店', '').replace('網上', '').replace('BB Fair Promotion', '').replace('朋友', '') \
                .replace('玩具節瘋狂減', '').replace('開學', '').replace('激賞', '').replace('網上玩具節', '') \
                .replace('價', '').replace('清貨', '').replace('日常', '').replace('現在', '').replace('開業', '') \
                .replace('獨家', '').replace('無休店', '').replace('買兩箱更平', '').replace('貼合幼兒腕握力成長', '') \
                .replace('德國製造', '').replace('再享', '').replace('快閃', '').replace('約', '').replace('至少', '') \
                .replace('額外', '').replace('激減', '').replace('Summer Special', '').replace('récolte', '') \
                .replace('人氣廚電推介', '').replace('7月份', '').replace('暑期', '').replace('大減', '') \
                .replace('大手', '').replace('比利時國慶', '').replace('年中', '').replace('勁減', '').replace('祭', '') \
                .replace('全店', '').replace('仲要超好味道', '').replace('BB展', '').replace('現只售', '') \
                .replace('BB fair', '').replace('新貨特賣', '').replace('推廣', '').replace('套裝', '') \
                .replace('特惠', '').replace('含测试 Video', '').replace('香港STC認證', '').replace('超荀', '') \
                .replace('抗疫', '').replace('期間', '').replace('動起來', '') \
                .replace('HKD', '').replace('HK', '').replace('CNY', '') \
                .replace('額滿即止', '').replace('在家自學', '').replace('至小', '').replace('鮮有', '') \
                .replace('至抵', '').replace('買一送一', '').replace('含測試', '').replace('Video', '') \
                .replace('送沐浴旅行裝乙支', '').replace('四層防護', '').replace('灰色別注版', '') \
                .replace('PFE', '').replace('BFE', '').replace('VFE', '').replace('99%', '') \
                .replace('AQ', '').replace('防疫', '').replace('專家', '').replace('持續殺菌', '').replace('保護層', '') \
                .replace('買3件$168', '').replace('買2件$160', '').replace('平均低至$45.8', '').replace('星期四', '') \
                .replace('高溫蒸氣除菌', '').replace('億世家', '').replace('盤點', '').replace('開倉', '') \
                .replace('24小時內快速出貨', '').replace('熱賣', '').replace('激筍', '').replace('純正', '') \
                .replace('每週瘋狂減', '').replace('1週', '').replace('本週', '').replace('週', '').replace('每日', '') \
                .replace('送兩款贈品', '').replace('線上書展', '').replace('新貨', '').replace('上市', '') \
                .replace('大搶購', '').replace('搶購', '').replace('新店', '').replace('開張', '').replace('一店', '') \
                .replace('VIP日', '').replace('VIP', '').replace('黑色', '').replace('星期五', '').replace('商店', '') \
                .replace('美肌', '').replace('黑五', '').replace('discount', '').replace('Day', '').replace('香港', '') \
                .replace('全港', '').replace('免運費', '').replace('快速', '').replace('出貨', '').replace('一周', '') \
                .replace('先進高速旋轉', '').replace('型號', '').replace('秋銷', '').replace('大劈', '') \
                .replace('請參閱', '').replace('簡介', '').replace('家庭必備', '').replace('買2件其中1件免費', '') \
                .replace('低至2折', '').replace('低至88折', '').replace('低至5折', '').replace('2 件再', '') \
                .replace('電子節', '').replace('電子熱店', '').replace('電器節', '').replace('小家庭必備', '') \
                .replace('日本製造', '').replace('學習好幫手', '').replace('簡單易用', '') \
                .replace('精選2件', '').replace('精選', '').replace('商品', '').replace('激搶', '').replace('優恵', '') \
                .replace('居家', '').replace('美酒', '').replace('多客讚賞本店No.1梅酒', '').replace('甘口清香', '') \
                .replace('SONY 原裝正貨', '').replace('ssmsung 原裝正貨', '').replace('當造新鮮蔬菜', '') \
                .replace('荔枝清香', '').replace('新品', '').replace('只限5部售完即止', '').replace('齊心', '') \
                .replace('200枝限量', '').replace('原廠保養', '').replace('香港加油', '').replace('全城', '') \
                .replace('期有限', '').replace('有機米', '').replace('健康', '').replace('香港老字號', '') \
                .replace('韓國食品節', '').replace('抗疫', '').replace('樺源食品', '').replace('收穫當日即製', '') \
                .replace('最新上市', '').replace('肉汁香甜', '').replace('新產品', '').replace('人人是', '') \
                .replace('咁多客人讚', '').replace('梗係好產品', '').replace('清甜口感', '').replace('健康純正', '') \
                .replace('日式の料理', '').replace('輕鬆自煮', '').replace('經常缺貨產品', '').replace('小食系列', '') \
                .replace('台灣直送', '').replace('韓國節', '').replace('新包裝牛油果味UP', '').replace('200支限量', '') \
                .replace('香醇濃郁', '').replace('品味之選', '').replace('只限5部', '').replace('售完即止', '') \
                .replace('冬日', '').replace('送三支Exit7 30ml酒精搓手液', '').replace('泰國制', '').replace('倉貨', '') \
                .replace('澳洲食品節', '').replace('優質の選擇', '').replace('加拿大節', '') \
                .replace('入冬', '').replace('美食', '').replace('巡禮', '').replace('氣炸鍋', '').replace('食品', '') \
                .replace('威士忌', '').replace('梅酒', '').replace('年底', '').replace('狂歡節', '').replace('瘋狂', '') \
                .replace('冬季', '').replace('最後一擊', '').replace('迪士尼', '').replace('超級', '') \
                .replace('品牌日', '').replace('全部', '').replace('季末減', '').replace('Clearance', '') \
                .replace('一年', '').replace('1年', '').replace('3年', '').replace('保養', '') \
                .replace('節慶', '').replace('人氣曾拌麵', '').replace('台灣拌麵', '').replace('香港製造', '') \
                .replace('新西蘭及荷蘭奶源', '').replace('低糖', '').replace('可口可樂', '').replace('高級工藝', '') \
                .replace('靚爆木盒', '').replace('製造日期2020', '').replace('信譽', '').replace('優良', '') \
                .replace('港式奶茶', '').replace('茶葉', '').replace('維他', '').replace('檸檬茶', '') \
                .replace('最新', '').replace('青檸', '').replace('蜜糖', '').replace('菊花茶', '').replace('行貨', '') \
                .replace('養生之選', '').replace('高鈣', '').replace('降膽固醇', '').replace('0膽固醇', '') \
                .replace('非基因', '').replace('改造', '').replace('大豆', '').replace('心臟', '').replace('優質', '') \
                .replace('新增', '').replace('節奏', '').replace('遊戲', '').replace('慢跑', '').replace('模式', '') \
                .replace('特快', '').replace('螢幕保護貼', '').replace('正版', '').replace('正貨', '') \
                .replace('商標許可', '').replace('史上最強的', '').replace('音樂', '').replace('電玩', '') \
                .replace('集合啦', '').replace('動物森友會', '').replace('作品', '').replace('', '').replace('', '') \
                .replace('信心保證', '').replace('冷泡', '').replace('無糖', '').replace('錫蘭', '').replace('鍚蘭', '') \
                .replace('打邊爐', '').replace('推介', '').replace('火鍋', '').replace('好拍檔', '').replace('今周', '') \
                .replace('唔使等', '').replace('集運', '').replace('清熱', '').replace('滋潤', '').replace('附送', '') \
                .replace('特典', '').replace('行李箱', '').replace('貼紙', '').replace('cap帽', '').replace('搶閘', '') \
                .replace('Black', '').replace('Friday', '').replace('聖誕', '').replace('Xmas', '').replace('市集', '') \
                .replace('瘦身', '').replace('咖啡', '').replace('台灣', '').replace('早餐', '').replace('必選', '') \
                .replace('凍頂', '').replace('烏龍', '').replace('年終', '').replace('PUMA', '').replace('官方', '') \
                .replace('旗艦店', '').replace('直營店', '').replace('線上', '').replace('書展', '').replace('日本', '') \
                .replace('暖笠笠', '').replace('面膜', '').replace('精華', '').replace('智慧', '').replace('', '') \
                .replace('慳水慳電', '').replace('升級陶瓷內膽', '').replace('授權書', '').replace('指定店', '') \
                .replace('狂減', '').replace('400次', '').replace('必備', '').replace('產品', '').replace('免費', '') \
                .replace('升級', '').replace('VC20', '').replace('Plus', '').replace('護目', '').replace('首選', '') \
                .replace('國際', '').replace('藍牙', '').replace('耳機', '').replace('TOSHIBA', '').replace('東芝', '') \
                .replace('電視', '').replace('專門店', '').replace('24小時', '').replace('TCL', '').replace('五款', '') \
                .replace('屏幕', '').replace('掛牆架', '').replace('禮物', '').replace('任君', '').replace('選擇', '') \
                .replace('小巧', '').replace('機身', '').replace('WiFi', '').replace('打印', '').replace('限量', '') \
                .replace('$100超市券', '').replace('$500超市券', '').replace('Free', '').replace('HDMI', '') \
                .replace('Cable', '').replace('WD', '').replace('款式', '').replace('最', '').replace('熱銷', '') \
                .replace('防毒', '').replace('軟件', '').replace('特別', '').replace('清倉', '').replace('上架', '') \
                .replace('小編', '').replace('重點', '').replace('滿2套', '').replace('本集', '').replace('另有', '') \
                .replace('任意', '').replace('5星', '').replace('之選', '').replace('大熱', '').replace('全場', '') \
                .replace('皇牌', '').replace('新年', '').replace('新春', '').replace('真實', '').replace('好評', '') \
                .replace('好用', '').replace('年前', '').replace('老字號', '').replace('產自', '').replace('歐洲', '') \
                .replace('9包裝', '').replace('16包裝', '').replace('鈣思寶', '').replace('9+3裝', '') \
                .replace('2件以上', '').replace('發財', '').replace('製造', '').replace('經典', '').replace('口味', '') \
                .replace('家庭裝', '').replace('直營', '').replace('經典', '').replace('果汁', '') \
                .replace('100%', '').replace('循環', '').replace('再造', '').replace('膠樽', '').replace('嘉士伯', '') \
                .replace('直送', '').replace('送達', '').replace('有折', '').replace('上折', '').replace('代用', '') \
                .replace('原裝', '').replace('3個月', '').replace('', '').replace('', '').replace('', '').replace('', '').replace('', '').replace('', '') \
                .replace('奶', '').replace('茶', '').replace('送', '').replace('到', '').replace('版', '') \
                .replace('加', '').replace('內', '').replace('年', '').replace('筍', '').replace('奶', '') \
                .replace('買', '').replace('起', '').replace('現', '').replace('度', '').replace('/', '') \
                .replace('禮', '').replace('節', '').replace('大', '').replace('更', '') \
                .replace('75折', '').replace('74折', '').replace('72折', '').replace('49折', '').replace('55折', '') \
                .replace('35折', '').replace('68折', '').replace('38折', '') \
                .replace('63折', '').replace('88折', '').replace('95折', '').replace('89折', '').replace('45折', '') \
                .replace('85 折', '').replace('9 折', '').replace('39折', '').replace('56折', '').replace('39折', '') \
                .replace('85折', '').replace('5折', '').replace('7折', '').replace('9折', '').replace('6折', '') \
                .replace('77 折', '').replace('8折', '').replace('3 折', '').replace('4折', '').replace('2折', '') \
                .replace('九折', '')
            Nprice = Nprice.replace('$', '').replace('   ', '').strip()
            print('NpriceOrg b4   :', NpriceOrg)
            NpriceCheck = NpriceOrg.replace('$', '').replace(',', '').strip()
            if Nprice == NpriceCheck: NpriceOrg = ''
            print('Nprice         :', Nprice)
            print('NpriceOrg      :', NpriceOrg)
        except (IndexError, AttributeError):
            Nprice = ''
            NpriceOrg = ''

        try:
            Sprice = soup.find('div', {'class': 'price'})
            Sprice = Sprice.text
            Sprice = Sprice.replace('$', '').replace('價格動向','').replace('Price Trend','').strip()
            print('Sprice         :', Sprice)
        except (IndexError, AttributeError):
            Sprice = ''

        if Nprice == '':
            Nprice = Sprice
            Sprice = ''

        try:
            D1price = \
            soup.find('div', {'class': 'bulk_list'}).findAll('span', {'class': 'bulk_message'})[0].findAll('strong')[1]
            D1price = D1price.text.replace('$', '').strip()
            print('D1   Price     :', D1price)
        except (IndexError, AttributeError):
            D1price = ''

        try:
            D1priceR = \
            soup.find('div', {'class': 'bulk_list'}).findAll('span', {'class': 'bulk_message'})[0].findAll('strong')[0]
            D1priceR = D1priceR.text.replace('平均', '').strip()
            print('D1 Remarks     :', D1priceR)
        except (IndexError, AttributeError):
            D1priceR = ''

        try:
            D2price = \
            soup.find('div', {'class': 'bulk_list'}).findAll('span', {'class': 'bulk_message'})[1].findAll('strong')[1]
            D2price = D2price.text.replace('$', '').strip()
            print('D2   Price     :', D2price)
        except (IndexError, AttributeError):
            D2price = ''

        try:
            D2priceR = \
            soup.find('div', {'class': 'bulk_list'}).findAll('span', {'class': 'bulk_message'})[1].findAll('strong')[0]
            D2priceR = D2priceR.text.replace('平均', '').strip()
            print('D2 Remarks     :', D2priceR)
        except (IndexError, AttributeError):
            D2priceR = ''

        try:
            D3price = \
            soup.find('div', {'class': 'bulk_list'}).findAll('span', {'class': 'bulk_message'})[2].findAll('strong')[1]
            D3price = D3price.text.replace('$', '').strip()
            print('D3   Price     :', D3price)
        except (IndexError, AttributeError):
            D3price = ''

        try:
            D3priceR = \
            soup.find('div', {'class': 'bulk_list'}).findAll('span', {'class': 'bulk_message'})[2].findAll('strong')[0]
            D3priceR = D3priceR.text.replace('平均', '').strip()
            print('D3 Remarks     :', D3priceR)
        except (IndexError, AttributeError):
            D3priceR = ''

        try:
            PackingSpec = soup.find('div', {'class': 'productDetailPanelTableWrapper'}).find('tr', {
                'class': 'productPackingSpec'}).findAll('td')[1]
            PackingSpec = PackingSpec.text.strip()
            print('PackingSpec    :', PackingSpec)
        except (IndexError, AttributeError):
            PackingSpec = ''

        try:
            salesNo = soup.find('div', {'class': 'salesNumber-container'}).find('span')
            salesNo = salesNo.text.replace('已售出', '').replace('+', '').strip()
            print('SalesCount     :', salesNo)
        except (IndexError, AttributeError):
            salesNo = ''

        try:
            reviewsNo = soup.find('div', {'class': 'reviews-number'}).find('span', {'class': 'comment'})
            reviewsNo = reviewsNo.text
            reviewsNo = reviewsNo.replace('(', '').replace(')', '').replace('則用家評論', '')
            reviewsNo = reviewsNo.strip()
            print('Reviews No     :', reviewsNo)
        except (IndexError, AttributeError):
            reviewsNo = ''

        try:
            stockRemarks = soup.find('div', {'class': 'stockLevelMsg1'})
            stockRemarks = stockRemarks.text
            stockRemarks = stockRemarks.replace('此商品', '').replace('！', '')
            print('stockRemarks   :', stockRemarks)
            if '缺貨' in stockRemarks:
                Availability = 0
        except (IndexError, AttributeError):
            stockRemarks = ''

        try:
            errorRemarks = soup.find('div', {'class': 'globalMessages'}).find('span', {'class': 'error'})
            errorRemarks = errorRemarks.text
            errorRemarks = errorRemarks.replace('This product is offline or being updated now', '')
            errorRemarks = errorRemarks.replace('/', '').replace('此', '').replace('或正在更新', '')
            errorRemarks = errorRemarks.strip()
            print('errorRemarks   :', errorRemarks)
            Availability = -1
        except (IndexError, AttributeError):
            errorRemarks = ''

        overallRemarks = stockRemarks + errorRemarks

        if '售罄' in overallRemarks:
            Availability = -1
            Nprice == ''
            Sprice == ''
            print('overallRemarks :', overallRemarks)

        if Nprice == '' and Sprice == '' and overallRemarks == '':
            Availability = -1
            overallRemarks = '網上沒有顯示'
            print('overallRemarks :', overallRemarks)

        ProductID = URL[URL.find('/p/') + 3:]
        print('ProductID      :', ProductID)

        # -----Other Fields-------------------------
        QuotationNo = str(number)
        CPIBase = '1415'
        OutletID = '=TEXT(1,"000")'
        PopularityMethod = 'Sales'
        EffectiveDate = date.today().strftime('%d.%m.%Y')
        ReferenceMonth = date.today().strftime('%Y%m')
        LastInputBy = 'Shirry'

        RecordID = str(number)
        CollectionDate = date.today().strftime('%d.%m.%Y')
        CollectionMethod = 'Python'
        CCY = 'HKD'
        CCYRate = 1

        ProductSpec = [QuotationNo, '', CPIBase, '', '', OutletID, OutletName, ProductID, ProductName, PackingSpec,
                       Categories, '', PopularityMethod, salesNo, EffectiveDate, ReferenceMonth, '', LastInputBy, '']

        RawQuotation = [RecordID, '', CollectionDate, CollectionMethod, ReferenceMonth, '', '', '', OutletID, ProductID,
                        '', '', '', CCY, CCYRate, Availability, Nprice, NpriceOrg, Sprice, overallRemarks, D1price,
                        D1priceR, D2price, D2priceR, D3price, D3priceR]

        with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_ProductSpec.csv', 'a', newline='',
                  encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(ProductSpec)

        with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_RawQuotation.csv', 'a', newline='',
                  encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(RawQuotation)

        time.sleep(random.random() * 2)

    except:
        print(URL)
        print('time out')
        ProductSpec = [str(number), '', '', '', '', '', '', '', URL]
        RawQuotation = [str(number), '', '', '', '', '', '', '', '', '', URL]

        with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_ProductSpec.csv', 'a', newline='',
                  encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(ProductSpec)

        with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_RawQuotation.csv', 'a', newline='',
                  encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(RawQuotation)

print('\n********************************************************************************')
print('Outlet Name         : ', OutletName)
print('Current Date        : ', datetime.datetime.now().strftime('%Y.%m.%d'))
print('Current Time        : ', datetime.datetime.now().strftime('%H:%M:%S'))
print('Time used           :  %.1f minutes' % float((time.time() - start_time) / 60),
      'or %.0f seconds' % (time.time() - start_time))
print('Total quotations    : ', number)
print('Rate of scraping    :  %.1f minutes/quotation' % float((time.time() - start_time) / 60 / number),
      'or %.0f seconds/quotation' % float((time.time() - start_time) / number))
print('********************************************************************************')
print('End of Program Run')
print('Successfully Output CSV files')

sys.stdout.close()