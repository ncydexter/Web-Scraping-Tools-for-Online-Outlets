'''
This program aims to scrape product information from https://www.apple.com/hk/.
Program written by : Shirry Wan
Program created on : 20.12.2020
Last modified by   : Shirry Wan
Last modified on   : 20.12.2020
'''

import requests
from bs4 import BeautifulSoup
from datetime import date
from urllib import parse

import time
import datetime
import csv
import random
import sys
import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

OutletName = 'Apple'
output_fileName = OutletName
output_path = os.getcwd() + '/../Data/'
outdate = datetime.datetime.now().strftime("%Y%m%d")
outtime = datetime.datetime.now().strftime("%H%M")

sys.stdout = open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_log.txt', 'w', encoding='utf-8-sig')

print("Start of Program Run")
print("********************************************************************************")
print("Outlet Name         : ", OutletName)
print("Current Date        : ", datetime.datetime.now().strftime("%Y.%m.%d"))
print("Current Time        : ", datetime.datetime.now().strftime("%H:%M:%S"))
print("********************************************************************************")

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

with open(OutletName + '_URL.txt', 'r') as f:
	URLs = f.read().splitlines()

chrome_path = 'D:/Python/chromedriver.exe'
caps = DesiredCapabilities().CHROME

option = webdriver.ChromeOptions()
# option.add_argument('--headless')
# option.add_argument('--disable-gpu')
option.add_argument('window-size=1920,1080')
# option.add_argument('window-size=1024,768')
option.add_argument('blink-settings=imagesEnabled=false')
option.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(desired_capabilities=caps, executable_path=chrome_path, options=option)

number = 0

for URL in URLs:

	url_no_trial = 0
	url_max_trial = 15

	while url_no_trial < url_max_trial:
		try:
			driver.implicitly_wait(60)
			driver.get(URL)
			time.sleep(2)
			break
		except TimeoutException:
			url_no_trial += 1
			driver.refresh()
			print(str(url_no_trial), 'Timeout')

	if url_no_trial == url_max_trial:
		print('this product took too much time, skip')
		continue

	try:
		number += 1
		print('\n(' + str(number) + ')')

		max_trial = 100
		no_trial = 0

		while no_trial < max_trial:
			try:
				pageSource = driver.page_source
				soup = BeautifulSoup(pageSource, 'html.parser')
				#
				# html = requests.get(URL)
				# soup = BeautifulSoup(html.text, 'html.parser')
				break
			except:
				no_trial += 1
				time.sleep(random.random() * 10 + 5)
				print(str(no_trial))

		if no_trial == max_trial:
			print(URL)
			print('no_trial == max_trial')
			ProductSpec = [str(number), "", "", "", "", "", "", "", URL]
			RawQuotation = [str(number), "", "", "", "", "", "", "", "", "", URL]

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
		ProductDesc = ""

		try:
			ProductName = soup.find('h1')
			ProductName = ProductName.text.replace('\n', '').replace('自訂你的', '').replace('。', '') \
							.replace('購買', '').replace('全新', '').strip()
			print('ProductName         :', ProductName)
		except:
			ProductName = URL

		if '/buy-mac/' in URL or '/buy-watch/' in URL or '/buy-iphone/' in URL:
			try:
				Nprice = soup.find('span', {'data-autom': 'price'})
				Nprice = Nprice.text.replace('HK$', '').replace('起', '').strip()
			except:
				Nprice = ""

		if '/buy-ipad/' in URL:
			try:
				Nprice = soup.find('div', {'class': 'as-price-currentprice'})
				Nprice = Nprice.text.replace('HK$', '').strip()
			except:
				Nprice = ""

		if '/product/' in URL:
			try:
				Nprice = soup.find('span', {'class': 'current_price'})
				Nprice = Nprice.text.replace('HK$', '').strip()
			except:
				Nprice = ""

		if Nprice != '': print('Nprice              :', Nprice)

		URL = parse.unquote(URL)
		if '?' in URL:
			ProductDesc = URL[URL.rfind('/') + 1:URL.rfind('?')]
		else:
			ProductDesc = URL[URL.rfind('/')+1:]
		ProductDesc = ProductDesc.replace('#', '')

		if '/product/' in URL:
			ProductID = ProductDesc
		else:
			ProductID = ProductName + '+' + ProductDesc

		print('ProductID           :', ProductID)

		if '/product/' in URL:
			try:
				ProductDesc = soup.find('legend', {'class': 'dimensionColor'})
				ProductDesc = ProductDesc.text.strip()
				if ProductDesc != '': print('ProductDesc         :', ProductDesc)
			except:
				ProductDesc = ""

		# -----Other Fields-------------------------
		QuotationNo = str(number)
		CPIBase = '1415'
		OutletID = '=TEXT(32,"000")'
		PopularityMethod = 'Price'
		EffectiveDate = date.today().strftime('%d.%m.%Y')
		ReferenceMonth = date.today().strftime('%Y%m')
		LastInputBy = 'Shirry'

		RecordID = str(number)
		CollectionDate = date.today().strftime('%d.%m.%Y')
		CollectionMethod = 'Python'
		CCY = 'HKD'
		CCYRate = 1

		ProductSpec = [QuotationNo, "", CPIBase, "", "", OutletID, OutletName, ProductID, ProductName, ProductDesc, "",
					   "", "", "", EffectiveDate, ReferenceMonth, "", LastInputBy, ""]

		RawQuotation = [RecordID, "", CollectionDate, CollectionMethod, ReferenceMonth, "", "", "", OutletID, ProductID,
						"", "", "", CCY, CCYRate, Availability, Nprice, "", "", "", "", ""]

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
		ProductSpec = [str(number), "", "", "", "", "", "", "", URL]
		RawQuotation = [str(number), "", "", "", "", "", "", "", "", "", URL]

		with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_ProductSpec.csv', 'a', newline='',
				  encoding='utf-8-sig') as file:
			writer = csv.writer(file)
			writer.writerow(ProductSpec)

		with open(output_path + output_fileName + '_' + outdate + '-' + outtime + '_RawQuotation.csv', 'a', newline='',
				  encoding='utf-8-sig') as file:
			writer = csv.writer(file)
			writer.writerow(RawQuotation)

	time.sleep(2)
driver.close()

print("\n********************************************************************************")
print("Outlet Name         : ", OutletName)
print("Current Date        : ", datetime.datetime.now().strftime("%Y.%m.%d"))
print("Current Time        : ", datetime.datetime.now().strftime("%H:%M:%S"))
print("Time used           :  %.1f minutes" % float((time.time() - start_time) / 60),
	  "or %.0f seconds" % (time.time() - start_time))
print("Total quotations    : ", number)
print("Rate of scraping    :  %.1f minutes/quotation" % float((time.time() - start_time) / 60 / number),
	  "or %.0f seconds/quotation" % float((time.time() - start_time) / number))
print("********************************************************************************")
print("End of Program Run")
print("Successfully Output CSV files")

sys.stdout.close()