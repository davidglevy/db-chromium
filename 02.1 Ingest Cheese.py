# Databricks notebook source
# MAGIC %pip install selenium

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

# MAGIC %md
# MAGIC # Open Woolworths Website
# MAGIC
# MAGIC We need to setup our REST connection with the same cookies that are present when normally calling the REST endpoint.
# MAGIC
# MAGIC We do this by "grafting" the cookies from the website onto our REST link.

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

driver.find_element(By.LINK_TEXT, "Dairy, Eggs & Fridge").click()
driver.find_element(By.CSS_SELECTOR, ".category-list:nth-child(1) > .item:nth-child(2) > .description").click()
time.sleep(5)

print(driver.title)

# COMMAND ----------

from urllib import request
from urllib.request import Request
from urllib import parse
import uuid
import json
import zlib

class WoolworthsCategoryClient():

  def __init__(self, cookies):
    cookie_parts = []
    
    for cookie in cookies:
      cookie_parts.append(f"{cookie['name']}={cookie['value']}")
    
    self.cookie_header = "; ".join(cookie_parts)    

  def retrieveCategory(self, page: int, formatObject: str, categoryId: str, parentCategory: str, category: str):
    """
      page starts at pageNumber=1, TODO find out how to identify max page
      formatObject used to identify context for which item are shown, for example "Cheese". Likely required to keep traffic appearing as same as other
      categoryId the unique Id for the category; need to understand if it is required, mandatory and how often it changes. Cheese is "1_B7EF010"
      parentCategory the parent grouping for the category, for example the parent of "cheese" is "dairy-eggs-fridge"
      category the actual category, for example "cheese"
    """

    payload = {
      "categoryId": categoryId,
      "pageNumber": page,
      "pageSize": 36,
      "sortType": "Name",
      "url": f"/shop/browse/{parentCategory}/{category}?pageNumber={page}",
      "location": f"/shop/browse/{parentCategory}/{category}?pageNumber={page}",
      "formatObject": "{\"name\":\"" + formatObject + "\"}",
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

    # Create the request object
    data_to_send = json.dumps(payload).encode("UTF-8")
    a_request = Request("https://www.woolworths.com.au/apis/ui/browse/category", data=data_to_send)
    a_request.add_header("Cookie", self.cookie_header)

    # Headers sent from browser, not sure which are mandatory but fails without these.
    a_request.add_header("Accept", "application/json")
    a_request.add_header("Accept-Encoding", "gzip, deflate, br")
    a_request.add_header("Accept-Language", "en-US,en;q=0.9,en-AU;q=0.8,fr;q=0.7")
    a_request.add_header("Content-Length", len(data_to_send))
    a_request.add_header("Content-Type", "application/json")
    a_request.add_header("Origin", "https://www.woolworths.com.au")
    a_request.add_header("Referer", f"https://www.woolworths.com.au/shop/browse/{parentCategory}")
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
    http_result = request.urlopen(a_request)

    result = {
      "status" : http_result.status,
      "message" : http_result.msg
    }

    headers = []
    for header in http_result.headers:
      headers.append({"key": header, "value": http_result.headers[header]})
    result["headers"] = headers

    if (result["status"] == 200):
      print("Result is as expected, getting payload.")
      decompressed_data=zlib.decompress(http_result.read(), 16+zlib.MAX_WBITS)

      result_str = str(decompressed_data, "UTF-8")
      result_dict = json.loads(result_str)
      result['payload'] = result_dict
    else:
      print(f"Received unexpected status [{result['status']}] with message [{result['message']}]")

    return result


# COMMAND ----------

cookies = driver.get_cookies()
client = WoolworthsCategoryClient(cookies)

# COMMAND ----------




# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS demo;
# MAGIC CREATE SCHEMA IF NOT EXISTS demo.woolies_scrape;
# MAGIC USE demo.woolies_scrape;

# COMMAND ----------

# Process cheese
#count_returned = -1

result = client.retrieveCategory(1, "Cheese", "1_B7EF010", "dairy-eggs-fridge", "cheese")
raw_text = json.dumps(result['payload'], indent=4)
print(raw_text)

# With result, we get TotalRecordCount, then divide by PageCount. If > PageCount, we 



# COMMAND ----------

driver.close()
