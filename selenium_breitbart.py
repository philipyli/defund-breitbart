# Download Selenium webdriver (Chrome for MAC) - https://chromedriver.storage.googleapis.com/index.html?path=2.26/
# http://seleniumhq.github.io/selenium/docs/api/py/index.html

# selenium setup  
# http://seleniumhq.github.io/selenium/docs/api/py/index.html


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import csv
import sys

def grabScreenshotAndAdURLs(publisherURL):
	browser.get(publisherURL)
#	print(browser.page_source)

	try:


	except:
		print("Unexpected error:", sys.exc_info()[0])
		print(publisherURL +' not loaded successfully.')
		return False

	else:

# Write data eg to CSV
		return True



##############
## starts here
##############

path_to_chromedriver = '/Users/pli/Development/defund-breitbart/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

publisherURL = "http://www.breitbart.com/"

for i in range(0,2):
#latlongListFile = open('latlongs.txt')
#latlongList = latlongListFile.read().splitlines()
	grabScreenshotAndAdURLs(publisherURL)
#	print('finished one!')
	seconds = .1 + (random.random() * .1)
	time.sleep(seconds)


# browser.quit()
