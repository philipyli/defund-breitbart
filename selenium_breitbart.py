# Download Selenium webdriver (Chrome for MAC) - https://chromedriver.storage.googleapis.com/index.html?path=2.26/
# http://seleniumhq.github.io/selenium/docs/api/py/index.html

# selenium setup
# http://seleniumhq.github.io/selenium/docs/api/py/index.html


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
import time
import random
import csv
import sys
import os
import base64
import csv

def fullpage_screenshot(driver, file):
        print("Starting chrome full page screenshot workaround ...")

        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []


        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(500, rectangle[1]))
                print("Scrolled To ({0},{1})".format(500, rectangle[1]))
                #time.sleep(0.4)

            file_name = "part_{0}.png".format(part)
            print("Capturing {0} ...".format(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        print("Finishing chrome full page screenshot workaround...")
        return True

def grabScreenshotAndAdURLs(publisherURL):

	try:
		print("start try")
		#	print(browser.page_source)
		viewport_height = browser.execute_script("return window.innerHeight")

		banner_height = viewport_height / 4

		fullpage_screenshot(browser, 'screenshot.png')
		print("finish full screenshot")
		# get divs potentially containing iframe
		#div_elems = browser.find_elements_by_xpath('//div[contains(@class, "Hmobi")]')
		image_names = []
		all_links = []
		div_elems = browser.find_elements_by_xpath('//div[contains(@id, "google_ads_iframe")]')
		for index, div_elem in enumerate(div_elems):
			# get the most nested div that contains iframe, and save its location
			#div_elem.find_element_by_xpath('//div[contains(@id, "google_ads_iframe")]')
			location = div_elem.location


			frame_size = div_elem.size

			#open screenshot and get size
			im = Image.open('screenshot' + '.png') # uses PIL library to open image in memory
			image_width, image_height = im.size
			if location['y'] < banner_height: # banner image
				# get parameters for cropping image
				left = max(0, location['x'] - 200)
				right =  min(image_width, location['x'] + frame_size['width'] + 200)
				top = 0
				bottom = location['y'] + frame_size['height'] + 100
			else: # body page image
				left = 0
				right = image_width
				top = max(0, location['y'] - 10)
				bottom = min(image_height, location['y'] + frame_size['height'] + 10)
			# crop image
			im = im.crop((left, top, right, bottom)) # defines crop points
			image_name = 'pic' + str(index) + '.png'
			im.save(image_name)
			image_names.append(image_name)
			#open new picture, and base64 encode it into a string
			print("finish creating image: " + image_name)
			# get content on corresponding iframe
			googleframe = div_elem.find_element_by_tag_name('iframe')
			browser.switch_to.frame(googleframe)
			links = browser.find_elements_by_tag_name('a')
			linkref = [l.get_attribute('data-original-click-url') for l in links if l.get_attribute('data-original-click-url') is not None]
			all_links.append(linkref)
			browser.switch_to_default_content()
		print("construct csv")
		# write links and image files into 2-column csv called eggs.csv
		with open('eggs.csv', 'w', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',',
							quotechar='"', quoting=csv.QUOTE_ALL)
			for i in range(0,len(image_names)):
				print("making row" + str(i))
				with open(image_names[i], "rb") as image_file:
					encoded_string = base64.b64encode(image_file.read())
				if len(all_links[i]) == 0:
					continue
				spamwriter.writerow([all_links[i][0], encoded_string])


	except Exception as e:
		print("Unexpected error:", sys.exc_info()[0])
		print(str(e))
		print(publisherURL +' not loaded successfully.')
		return False

	else:

		# Write data eg to CSV
		return True



##############
## starts here
##############

path_to_chromedriver = os.path.dirname(os.path.abspath('__file__'))+ '/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

publisherURL = "http://www.breitbart.com/"
browser.get(publisherURL)

for i in range(0,1):
#latlongListFile = open('latlongs.txt')
#latlongList = latlongListFile.read().splitlines()
	grabScreenshotAndAdURLs(publisherURL)
#	print('finished one!')
	seconds = .1 + (random.random() * .1)
	time.sleep(seconds)


# browser.quit()

