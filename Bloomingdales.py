'''
This program aims to scrape product information from https://www.bloomingdales.com/.
Program written by : Shirry Wan
Program created on : 17.06.2020
Last modified by   : Shirry Wan
Last modified on   : 18.12.2020
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

OutletName = 'Bloomingdales'
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

number = 0
headers = {'User-agent': 'Mozilla/5.0'}

for URL in URLs:

	try:
		number += 1
		print('\n(' + str(number) + ')')

		max_trial = 100
		no_trial = 0

		while no_trial < max_trial:
			try:
				html = requests.get(URL, headers=headers)
				soup = BeautifulSoup(html.text, 'html.parser')
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

		try:
			ProductName = soup.find('div', {'data-auto': 'product-name'})
			ProductName = ProductName.text.strip()
			print('ProductName         :', ProductName)
		except (IndexError, AttributeError):
			ProductName = ""

		try:
			ProductColor = soup.find('span', {'class': 'color-display-name'})
			ProductColor = ProductColor.text
			print('ProductColor        :', ProductColor)
		except (IndexError, AttributeError):
			ProductColor = ""

		try:
			lenOfNprice = len(soup.findAll('span', {'class': 'prev-price'}))
			Nprice = soup.findAll('span', {'class': 'prev-price'})[lenOfNprice-1]
			Nprice = Nprice.text.replace('Reg.', '').replace('Orig.', '').replace('HKD', '').strip()
			print('Nprice              :', Nprice)
		except (IndexError, AttributeError):
			Nprice = ""

		try:
			Sprice = soup.find('div', {'class': 'final-price'}).find('span')
			Sprice = Sprice.text.replace('Sale', '').replace('Now', '').replace('HKD', '').strip()
			print('Sprice              :', Sprice)
		except (IndexError, AttributeError):
			Sprice = ""

		if Nprice == "" and Sprice != "":
			Nprice = Sprice
			Sprice = ""

		try:
			SpriceDiscount = soup.find('div', {'class': 'final-price'}).find_all('span')[1]
			SpriceDiscount = SpriceDiscount.text.replace('(', '').replace(')', '').strip()
			if SpriceDiscount != "": print('SpriceDiscount      :', SpriceDiscount)
		except (IndexError, AttributeError):
			SpriceDiscount = ""

		try:
			ProductDiscount = soup.find('button', {'class': 'h5 offer-overlay-button offer-badge'})
			ProductDiscount = ProductDiscount.text.replace('details', '').strip()
			print('ProductDiscount     :', ProductDiscount)
		except (IndexError, AttributeError):
			ProductDiscount = ""

		try:
			UnavailableText = soup.find('div', {'class': 'unavailable-image-message small'})
			UnavailableText = UnavailableText.text.replace('This item is', '').replace('.', '').strip()
			Availability = -1
			print('UnavailableText     :', UnavailableText)
		except (IndexError, AttributeError):
			UnavailableText = ""

		try:
			ProductDescriptionBullets = soup.find('ul', {'data-auto': 'product-description-bullets'}).find_all('li')
			ProductID = ProductDescriptionBullets[len(ProductDescriptionBullets) - 1].text.replace('Web ID: ', '')
			print('ProductID           :', ProductID)
		except (IndexError, AttributeError):
			ProductID = ""

		# -----Other Fields-------------------------
		QuotationNo = str(number)
		CPIBase = '1415'
		OutletID = '=TEXT(14,"000")'
		PopularityMethod = 'BestSellers'
		EffectiveDate = date.today().strftime('%d.%m.%Y')
		ReferenceMonth = date.today().strftime('%Y%m')
		LastInputBy = 'Shirry'

		RecordID = str(number)
		CollectionDate = date.today().strftime('%d.%m.%Y')
		CollectionMethod = 'Python'
		CCY = 'HKD'
		CCYRate = 1

		ProductSpec = [QuotationNo, "", CPIBase, "", "", OutletID, OutletName, ProductID, ProductName, ProductColor, "",
					   "", "", "", EffectiveDate, ReferenceMonth, "", LastInputBy, ""]

		RawQuotation = [RecordID, "", CollectionDate, CollectionMethod, ReferenceMonth, "", "", "", OutletID, ProductID,
						"", "", "", CCY, CCYRate, Availability, Nprice, UnavailableText, Sprice, SpriceDiscount, "",
						ProductDiscount]

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