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

		grabBrandNamesOfTaboolaAdvertisers()
		grabDomainsOfGoogleAdvertisers()

	except:
		print("Unexpected error:", sys.exc_info()[0])
		print(publisherURL +' not loaded successfully.')
		return False

	else:
		return True




def grabBrandNamesOfTaboolaAdvertisers():
	matches = re.findall(r'(<span class="branding">)([\w \d \s .]*)(<\/span>)', browser.page_source)
	for match in matches:
		print(match[1])


def grabDomainsOfGoogleAdvertisers():
	browser.switch_to_default_content()
	iframes = browser.find_elements_by_tag_name('iframe')
	googleframes = [a for a in iframes if 'google' in a.get_attribute('src')]
	iframeofinterest = googleframes[1]
	browser.switch_to.frame(iframeofinterest)
	links = browser.find_elements_by_tag_name('a')
	linkref = [l.get_attribute('data-original-click-url') for l in links if l.get_attribute('data-original-click-url') is not None]
	# list of strings that are the href for all the google ads on the page
	for oneLink in linkref:
		match = re.search(r'(adurl=)(http|https)(\:\/\/)([\w \d \s .]*)', oneLink)
		if match:
			print(match.group(4))
	browser.switch_to_default_content()


##############
## starts here
##############



### CHANGE TO RELATIVE PATH ##

path_to_chromedriver = os.path.dirname(os.path.abspath('__file__')) +'/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

publisherURL = "http://www.breitbart.com/"

for i in range(0,1):
	grabScreenshotAndAdURLs(publisherURL)
#	print('finished one!')
	seconds = .1 + (random.random() * .1)
	time.sleep(seconds)


# browser.quit()
