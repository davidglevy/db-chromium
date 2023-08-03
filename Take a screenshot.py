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

driver.find_element(By.CSS_SELECTOR, ".browseMenuDesktop > .wx-header__drawer-button-label").click()
driver.find_element(By.CSS_SELECTOR, ".item:nth-child(8) > .description").click()
driver.find_element(By.CSS_SELECTOR, ".category:nth-child(5) > .description").click()
    #element = self.driver.find_element(By.LINK_TEXT, "Fridge Snacks. Shop now.")

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
driver.stop_client()

# COMMAND ----------

# MAGIC %md
# MAGIC # Test the Screenshot

# COMMAND ----------

# MAGIC %pip install opencv-python

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
