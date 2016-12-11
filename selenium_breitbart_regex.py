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
import os
import re


def grabScreenshotAndAdURLs(publisherURL):
	browser.get(publisherURL)

	try:
#		print(browser.page_source)

		# Get the actual page dimensions using javascript
		pageWidth  = browser.execute_script("return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
		pageHeight = browser.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
		browser.set_window_size(pageWidth + 100, pageHeight + 100)

		# set screensize to maximum offered by site... but not to exceed client's physical screensize
		browser.get_screenshot_as_file('publisherScreenshot.png') 

		grabDomainsOfGoogleAdvertisers()
		grabBrandNamesOfTaboolaAdvertisers(browser.page_source)


#<span class="static-text top-right"></span>
#		//*[@id="internal_trc_"]/div[1]/a[1]/span/span[2]

	except:
		print("Unexpected error:", sys.exc_info()[0])
		print(publisherURL +' not loaded successfully.')
		return False

	else:

		# Write data eg to CSV
		return True


## ADD REGEXs TO GRAB BRAND NAMES AND DOMAINS ##


def grabDomainsOfGoogleAdvertisers():

#	div_elems = browser.find_elements_by_xpath('//div[contains(@id, "google_ads_iframe")]')

#	for div_elem in enumerate(div_elems):
#	WebDriverWait wait = new WebDriverWait(driver, 30000)
#	wait.until(ExpectedConditions.visibilityOfElementLocated((By.name("google_ads_iframe"))))

#	ff = webdriver.Firefox()
#	ff.get("http://somedomain/url_that_delays_loading")
	try:
		div_elems = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "adurl")))
	except:
		print("Unexpected error:", sys.exc_info()[0])
		print(' not loaded successfully.')
		return False

	else:
		print('blah')
#		return True

	print(div_elems)

#	for div_elem in div_elems:
#		browser.switch_to.frame(frame_reference=div_elem)
#		print(browser.page_source)


#		print(div_elem.get_attribute('outerHTML'))

#	matches = re.findall(r'(adurl=)(http|https)(\:\/\/)([\w \d \s .]*)', pageSource)
#	for match in matches:
#		print(match[3]) 


def grabBrandNamesOfTaboolaAdvertisers(pageSource):
	matches = re.findall(r'(<span class="branding">)([\w \d \s .]*)(<\/span>)', pageSource)
	for match in matches:                      
		print(match[1]) 




##############
## starts here
##############



### CHANGE TO RELATIVE PATH ##

path_to_chromedriver = os.path.dirname(os.path.abspath(__file__)) +'/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

publisherURL = "http://www.breitbart.com/"

for i in range(0,1):
	grabScreenshotAndAdURLs(publisherURL)
#	print('finished one!')
	seconds = .1 + (random.random() * .1)
	time.sleep(seconds)


# browser.quit()
