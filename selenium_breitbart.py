# This was some scraping code I wrote sometime ago to scrape with Selenium 
# This needs to be readapted for DefundBreitbart
# Selenium for Mac driver at
# https://chromedriver.storage.googleapis.com/index.html?path=2.26/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import csv
import sys

def getPropertyEstimate(url):
	print("url = ")
	print(url)
	browser.get(url)

	try:
		element = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="UserJumpButton1Text"]/img')))
		txtStreetAddress = browser.find_element_by_xpath('//*[@id="plcMain_rptrProperties_ctl01_Address"]/a').get_attribute('title')
		txtStreetAddress = txtStreetAddress[23:]
		print("txtStreetAddress = ")
		print(txtStreetAddress)
		tdOrigValue = browser.find_element_by_xpath('//*[@id="tdOrigValue"]').text.strip()
		lblValue = browser.find_element_by_xpath('//*[@id="lblValue"]').text.strip()		
		lastSoldDate = browser.find_element_by_xpath('//*[@id="plcMain_rptrProperties_ctl01_SoldDate"]').text.strip()
		lastSoldPrice = browser.find_element_by_xpath('//*[@id="tdSalePriceVal"]').text.strip()
		propertyType = browser.find_element_by_xpath('//*[@id="plcMain_rptrProperties_ctl01_PropertyType"]').text.strip()
		yearBuilt = browser.find_element_by_xpath('//*[@id="plcMain_rptrProperties_ctl01_YearBuilt"]').text.strip()
		livingSquareFeet = browser.find_element_by_xpath('//*[@id="plcMain_rptrProperties_ctl01_LivingSquareFeet"]').text.strip()
		totalSquareFeet = browser.find_element_by_xpath('//*[@id="plcMain_rptrProperties_ctl01_TotalSquareFeet"]').text.strip()
		latlong = browser.find_element_by_xpath('//*[@id="plcMain_rptrProperties_ctl01_Address"]/a').get_attribute('onclick')
		latlong = latlong[21:-16]
		pageContentElement = browser.find_element_by_xpath('//*[@id="divContent01"]')
		pageContentHTML = pageContentElement.get_attribute('innerHTML')

	except:
		print("Unexpected error:", sys.exc_info()[0])
		print(url +' not loaded successfully.')
		return False

	else:
		with open(txtStreetAddress+'.html', 'a') as htmlSnippetFile:
			htmlSnippetFile.write(pageContentHTML.encode('utf8'))
		with open('output.csv', 'a') as csvFile:
			myWriter = csv.writer(csvFile)
			data = [url, txtStreetAddress, tdOrigValue, lblValue, lastSoldDate, lastSoldPrice, propertyType, yearBuilt, livingSquareFeet, totalSquareFeet, latlong]
			print(data)
			myWriter.writerow(data)
		return True


##############
## starts here
##############

path_to_chromedriver = '/Users/pli/Desktop/selenium_scrape/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)


propertyListFile = open('propertyURLs.txt')
propertyList = propertyListFile.read().splitlines()
for propertyURL in propertyList:
	getPropertyEstimate(propertyURL)
	print('finished one!')
	seconds = 3 + (random.random() * 3)
	time.sleep(seconds)

print('done!')
# browser.quit()
