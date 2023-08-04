# Databricks notebook source
# MAGIC %pip install selenium opencv-python

# COMMAND ----------

# MAGIC %sh
# MAGIC #pkill chromedriver
# MAGIC ps -ef | grep chrome

# COMMAND ----------

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# COMMAND ----------

# Instantiate an Options object
# and add the "--headless" argument
opts = Options()
opts.add_argument("--headless")
opts.add_argument("--enable-logging")
opts.add_argument("--verbose")
opts.add_argument("--log-path=/chrome/chrome.log")
opts.add_argument("--webdriver.chrome.bin=/usr/bin/google-chrome")
opts.add_argument("--user-data-dir=/root/chrome")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--disable-notifications")

opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")
opts.add_argument("--window-size=2560,1440")

chrome_driver = "/chrome/chromedriver"

# If necessary set the path to you browser’s location
# Instantiate a webdriver
service = Service(chrome_driver)
driver = webdriver.Chrome(service=service, options=opts)


# COMMAND ----------

from db_better_logging import *
setup_logging()


# COMMAND ----------


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import time


wait_for_element = 10
driver.get("https://www.woolworths.com.au")
time.sleep(5)
print(driver.title)

#print("Going to wait for button to load")
#try:
#  WebDriverWait(driver, wait_for_element).until(EC.presence_of_element_located((By.XPATH, '//div[@class="wx-header__drawer-button-label"]')))
#  print("Wait complete, button loaded")
#except TimeoutException as e:
#  print("Wait Timed out")
#  print(e)

print("Clicking browse menu")
driver.find_element(By.XPATH, '//button[@class="wx-header__drawer-button browseMenuDesktop"]').click()
time.sleep(5)

print("Clicking [Dairy, Eggs & Fridge]")
wait = WebDriverWait(driver, 20)

try:
    showmore_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".iconAct-Menu")))
    showmore_link.click()
except ElementClickInterceptedException:
    print("Could not click first button")
    #driver.execute_script("arguments[0].click()", showmore_link)

#driver.find_element(By.CSS_SELECTOR, ".iconAct-Menu").click()
driver.find_element(By.LINK_TEXT, "Dairy, Eggs & Fridge").click()
driver.find_element(By.CSS_SELECTOR, ".category-list:nth-child(1) > .item:nth-child(2) > .description").click()

#driver.find_element(By.XPATH, '//div[text()="Dairy, Eggs & Fridge"]').click()
time.sleep(5)

print(driver.title)


#driver.get("https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge")

#page = 1
#while page != -1:
#  print(f"getting page {page}")
#  driver.get(f"https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge?pageNumber={page}&sortBy=Name")
#  driver.save_screenshot(f"woolworths-dairy-eggs-fridge-{page}.png")
#  break

# COMMAND ----------

from urllib import request
from urllib.request import Request
from urllib import parse
import uuid
import json

payload = {
  "categoryId": "1_B7EF010",
  "pageNumber": 2,
  "pageSize": 36,
  "sortType": "Name",
  "url": "/shop/browse/dairy-eggs-fridge/cheese?pageNumber=2",
  "location": "/shop/browse/dairy-eggs-fridge/cheese?pageNumber=2",
  "formatObject": "{\"name\":\"Cheese\"}",
  "isSpecial": None,
  "isBundle": False,
  "isMobile": False,
  "filters": [],
  "token": "",
  "gpBoost": 0,
  "isHideUnavailableProducts": None,
  "enableAdReRanking": False,
  "groupEdmVariants": True,
  "categoryVersion": "v2"
}

a_request = Request("https://www.woolworths.com.au/apis/ui/browse/category", data=json.dumps(payload).encode("UTF-8"))

cookies = driver.get_cookies()
print(cookies[0])
cookie_parts = []
for cookie in cookies:
  cookie_parts.append(f"{cookie['name']}={cookie['value']}")
cookie_header = "; ".join(cookie_parts)
a_request.add_header("Cookie", cookie_header)


# Headers sent from browser, not sure which are mandatory but fails without these.

# pseudo-header fields as per https://www.rfc-editor.org/rfc/rfc7230#section-3.1
#a_request.add_header(":authority:", "www.woolworths.com.au")
#a_request.add_header(":method:", "POST")
#a_request.add_header(":path:", "/apis/ui/browse/category")
#a_request.add_header(":scheme:", "https")
a_request.add_header("Accept", "application/json")
#a_request.add_header("Accept-Encoding", "gzip, deflate, br")
a_request.add_header("Accept-Language", "en-US,en;q=0.9,en-AU;q=0.8,fr;q=0.7")
#a_request.add_header("Content-Length", str(len(data)))
a_request.add_header("Cache-Control", "no-cache")
a_request.add_header("Content-Type", "application/json")
a_request.add_header("Origin", "https://www.woolworths.com.au")
a_request.add_header("Referer", "https://www.woolworths.com.au/shop/browse/dairy-eggs-fridge")
# Create a request ID as per that found on category Browser request
a_request.add_header("Request-Id", "|" + str(uuid.uuid4().hex) + "." + str(uuid.uuid4().hex)[0:16])
a_request.add_header("Sec-Ch-Ua", 'Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"')
a_request.add_header("Sec-Ch-Ua-Mobile", "?0")
a_request.add_header("Sec-Ch-Ua-Platform", "macOS")
#a_request.add_header("Sec-Fetch-Dest", None)
a_request.add_header("Sec-Fetch-Mode", "cors")
a_request.add_header("Sec-Fetch-Site", "same-origin")
a_request.add_header("Traceparent", "00-" + str(uuid.uuid4().hex) + "-" + str(uuid.uuid4().hex)[0:16] + "-01")
a_request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")


result = request.urlopen(a_request)

# COMMAND ----------

print(result.status)
print(result.msg)

# COMMAND ----------

for header in result.headers:
  print(header + "=" + result.headers[header])


# COMMAND ----------

result_str = str(result.read(), "UTF-8")
result_dict = json.loads(result_str)
#print(result_dict)

# COMMAND ----------

print(json.dumps(result_dict, indent=4))

# COMMAND ----------

page = 1
driver.save_screenshot(f"woolworths-dairy-eggs-fridge-{page}.png")

# COMMAND ----------

# MAGIC %sh
# MAGIC pwd

# COMMAND ----------

import os
path = os.getcwd()
dbutils.fs.mv(f"file:///{path}/woolworths-dairy-eggs-fridge-{page}.png", f"/FileStore/woolworths-dairy-eggs-fridge-{page}.png")


# COMMAND ----------

driver.close()

# COMMAND ----------

# MAGIC %md
# MAGIC # Test the Screenshot

# COMMAND ----------

import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
%matplotlib inline
from IPython.display import Image
plt.rcParams['image.cmap'] = 'gray'

# COMMAND ----------

# Read the image.
logo = f'/dbfs/FileStore/woolworths-dairy-eggs-fridge-{page}.png'
logo_img = cv2.imread(logo, cv2.IMREAD_COLOR)

# Print the size of the image.
print("Image size is ", logo_img.shape)

# COMMAND ----------

# Swap the Red and Blue color channels.
logo_img = logo_img[:, :, ::-1]

# Display the image.
plt.figure(figsize = (10, 10))
plt.imshow(logo_img);
