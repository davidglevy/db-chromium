# Databricks notebook source
# MAGIC %md
# MAGIC ## Send a Request to Woolworths
# MAGIC
# MAGIC Unfortunately the Woolworths site 

# COMMAND ----------

import requests

url = 'https://www.woolworths.com.au/apis/ui/browse/category'
request = {
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


x = requests.post(url, json = request)

print(x.text)
