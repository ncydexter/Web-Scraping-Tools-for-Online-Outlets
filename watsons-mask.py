from bs4 import BeautifulSoup
from datetime import date

import time
import datetime
import csv
import random
import sys

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

output_fileName = 'watsons-mask'
output_path = 'R:/CPI_SD/Online Pricing/Regular Price Collection/Watsons/Data/watsons-mask/'
outdate = datetime.datetime.now().strftime("%Y%m%d")
outtime = datetime.datetime.now().strftime("%H%M")
start_time = time.time()

sys.stdout=open(output_path + output_fileName +'-log-' + outdate + '-' + outtime + '.txt','w', encoding='utf-8-sig')

print("\n************************************************************************")
print("Watsons Masks")
print("Current Date: ", datetime.datetime.now().strftime("%Y%m%d"))
print("Current Time: ", datetime.datetime.now().strftime("%H%M"))
print("Start of Program Run")
print("************************************************************************\n")

chrome_path = 'D:\\Python\\chromedriver.exe'
caps = DesiredCapabilities().CHROME

option = webdriver.ChromeOptions()
# option.add_argument('--headless')
# option.add_argument('--disable-gpu')
option.add_argument('window-size=1920,1080')
# option.add_argument('blink-settings=imagesEnabled=false')
option.add_experimental_option('excludeSwitches', ['enable-logging'])

ProductsInfoList = []
ProductsInfoTitle = ['RecordNo', 'Outlet', 'ProductID', 'ProductBrand', 'ProductName', 'Nprice', 'Sprice',
                     'MemberRemarks', 'Remarks', 'ReviewCount', 'Rating', 'CollectionDate', 'CollectionTime',
                     'Availability']
ProductsInfoList.append(ProductsInfoTitle)

ProductURL = 'https://www.watsons.com.hk/Products-2-0/Medicine/Surgical-Masks-/c/050304'
# ProductURL = 'https://www.watsons.com.hk/search?text=%E5%8F%A3%E7%BD%A9'

url_no_trial = 0
url_max_trial = 15
while url_no_trial < url_max_trial:
    try:
        driver = webdriver.Chrome(desired_capabilities=caps, executable_path=chrome_path, options=option)
        driver.implicitly_wait(120)
        driver.get(ProductURL)
        break
    except TimeoutException:
        url_no_trial += 1
        driver.refresh()
        print(str(url_no_trial), 'Timeout')
if url_no_trial == url_max_trial: print('timeout, url_no_trial == url_max_trial')

no_trial = 0
max_trial = 100
while no_trial < max_trial:
    try:
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        break
    except:
        no_trial += 1
        time.sleep(random.random() * 10 + 5)
        print(str(no_trial))
if no_trial == max_trial: print('timeout, no_trial == max_trial')

try:
    ProductTotalNumber = soup.find('div', {'class': 'item hidden-xs hidden-sm'})
    ProductTotalNumber = ProductTotalNumber.text.replace('產品結果', '').strip()
    print('ProductTotalNumber       :', ProductTotalNumber)
except:
    ProductTotalNumber = str(999999)
    print('ProductTotalNumber       :', ProductTotalNumber)

driver.close()

ProductURLwithTotalNo = ProductURL + '?resultsForPage=' + ProductTotalNumber
# ProductURLwithTotalNo = ProductURL + '&resultsForPage=' + ProductTotalNumber
print(ProductURLwithTotalNo)

url_no_trial = 0
url_max_trial = 15
while url_no_trial < url_max_trial:
    try:
        driver = webdriver.Chrome(desired_capabilities=caps, executable_path=chrome_path, options=option)
        driver.implicitly_wait(120)
        driver.get(ProductURLwithTotalNo)
        break
    except TimeoutException:
        url_no_trial += 1
        driver.refresh()
        print(str(url_no_trial), 'Timeout')
if url_no_trial == url_max_trial: print('timeout, url_no_trial == url_max_trial (with ProductTotalNumber)')

no_trial = 0
max_trial = 100
while no_trial < max_trial:
    try:
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        break
    except:
        no_trial += 1
        time.sleep(random.random() * 10 + 5)
        print(str(no_trial))
if no_trial == max_trial: print('timeout, no_trial == max_trial (with ProductTotalNumber)')

productItems = soup.findAll('div', {'class': 'productItemContainer'})

i = 0
for productItem in productItems:
    i += 1
    try:
        ProductBrand = productItem.find('div', {'class': 'h1'}).find('span')
        ProductBrand = ProductBrand.text
    except:
        ProductBrand = None

    try:
        ProductName = productItem.find('div', {'class': 'h1'})
        ProductName = ProductName.text.strip().replace(ProductBrand, '').strip()
    except:
        ProductName = None

    try:
        Nprice = productItem.find('div', {'class': 'h3'})
        Nprice = Nprice.text.replace('RRP', '').replace('HK', '').strip()
    except:
        Nprice = None

    try:
        Sprice = productItem.find('div', {'class': 'h2'})
        Sprice = Sprice.text.replace('HK', '').strip()
    except:
        Sprice = None

    if Nprice == '':
        Nprice = Sprice
        # Sprice = ''

    try:
        MemberPrice = productItem.find('div', {'class': 'h2 mbPrice'})
        MemberPrice = MemberPrice.text.strip()
        if MemberPrice != '': MemberRemarks = '會員價'
    except:
        MemberRemarks = None
    try:
        Remarks = productItem.find('div', {'class': 'PWPbtn'})
        Remarks = Remarks.text.strip()
    except:
        Remarks = None

    try:
        ReviewCount = productItem.find('div', {'class': 'h4'})
        ReviewCount = ReviewCount.text.replace('(', '').replace(')', '').strip()
    except:
        ReviewCount = None

    try:
        Ratings = productItem.find('div', {'class': 'h4'}).findAll('i', {'class': 'icon-star01'})
        Rating = len(Ratings)
        if Rating == 0: Rating = ''
    except:
        Rating = None

    try:
        ProductID = productItem.find('div',
                     {'class': 'hidden gtmProductImpressions gtmProductClicks'}).get('data-gtm-product-impressions-id')
        ProductID = ProductID.replace('bp','BP')
    except:
        ProductID = None

    Availability = 1
    if '售罄' in Remarks: Availability = 0

    CollectionDate = datetime.datetime.now().strftime('%d.%m.%Y')
    CollectionTime = datetime.datetime.now().strftime('%H:%M')

    ProductsInfo = [i, 'Wastons', ProductID, ProductBrand, ProductName, Nprice, Sprice, MemberRemarks, Remarks,
                    ReviewCount, Rating, CollectionDate, CollectionTime, Availability]
    ProductsInfoList.append(ProductsInfo)

driver.close()

print("\n************************************************************************")
print("Current Date: ", datetime.datetime.now().strftime("%Y%m%d"))
print("Current Time: ", datetime.datetime.now().strftime("%H%M"))
print("Time used   :  %.4f minutes" % float((time.time() - start_time) / 60))
print("End of Program Run")
print("************************************************************************")

with open(output_path + output_fileName + '-' + outdate + '-' + outtime + '.csv', 'w', newline='',
          encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    for ProdInfo in ProductsInfoList: writer.writerow(ProdInfo)

print("Successfully Output CSV file")

sys.stdout.close()