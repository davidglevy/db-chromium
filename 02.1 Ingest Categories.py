# Databricks notebook source
# MAGIC %sql
# MAGIC USE demo.woolies_scrape;

# COMMAND ----------

from woolies import WooliesClient, WoolworthsCategoryClient
from pyspark.sql.functions import current_timestamp, col
from pyspark.sql.types import DecimalType
from db_better_logging import *


# COMMAND ----------


logger = setup_logging()

PAGE_SIZE = 36 # Default on Woolworths UI

client = WooliesClient()
cookies = client.getCookies()

categoryClient = WoolworthsCategoryClient(cookies)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT category, avg(price) as avg_price, count(*) as product_count
# MAGIC FROM products_bronze
# MAGIC GROUP BY category;

# COMMAND ----------


categories = [
#  {"formatObject": "Cheese", "categoryId": "1_B7EF010", "parentCategory": "dairy-eggs-fridge", "category": "cheese"},
#  {"formatObject": "Milk", "categoryId": "1_223D9D6", "parentCategory": "dairy-eggs-fridge", "category": "milk"},
  #{"formatObject": "Yoghurt", "categoryId": "1_AC76873", "parentCategory": "dairy-eggs-fridge", "category": "yoghurt"},
  #{"formatObject": "Cream, Custard & Desserts", "categoryId": "1_91794DD", "parentCategory": "yoghurt", "category": "cream-custard-desserts"}
  {"formatObject": "Eggs, Butter & Margarine", "categoryId": "1_85274A0", "parentCategory": "dairy-eggs-fridge", "category": "eggs-butter-margarine"},
  {"formatObject": "Dips & Pate", "categoryId": "1_D2B0685", "parentCategory": "dairy-eggs-fridge", "category": "dips-pate"},
  {"formatObject": "Ready to Eat Meals", "categoryId": "1_626AB17", "parentCategory": "dairy-eggs-fridge", "category": "ready-to-eat-meals"},
  {"formatObject": "Fresh Pasta & Sauces", "categoryId": "1_D3D428B", "parentCategory": "dairy-eggs-fridge", "category": "fresh-pasta-sauces"},
  {"formatObject": "Vegetarian & Vegan", "categoryId": "1_00ED79B", "parentCategory": "dairy-eggs-fridge", "category": "vegetarian-vegan"},
  {"formatObject": "International Foods", "categoryId": "1_914C9DE", "parentCategory": "dairy-eggs-fridge", "category": "international-foods"}
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
  #{"formatObject": "", "categoryId": "", "parentCategory": "", "category": ""},
]

"""
{
  "categoryId": "1_914C9DE",
  "pageNumber": 1,
  "pageSize": 24,
  "sortType": "Name",
  "url": "/shop/browse/dairy-eggs-fridge/international-foods",
  "location": "/shop/browse/dairy-eggs-fridge/international-foods",
  "formatObject": "{\"name\":\"International Foods\"}",
  "isSpecial": null,
  "isBundle": false,
  "isMobile": false,
  "filters": [],
  "token": "",
  "gpBoost": 0,
  "isHideUnavailableProducts": null,
  "enableAdReRanking": false,
  "groupEdmVariants": true,
  "categoryVersion": "v2"
}
"""


for category in categories:
  logger.info(f"Processing [{category['category']}]")
  category_name = category["category"]
  products = categoryClient.retrieveProducts(category["formatObject"], category["categoryId"], category["parentCategory"], category_name)

  logger.info(f"We retrieved {len(products)} products from category [{category_name}]")

  logger.info("Creating Spark dataframe from products")
  schema = "stockcode string, barcode string, name string, package_size string, category string, messages array<struct<level string, code string, message string>>, price float, has_cup_price boolean, cup_measure string, cup_price float, raw_text string"
  products_df = (spark
    .createDataFrame(products, schema)
    .withColumn("insert_ts", current_timestamp())
#    .withColumn("cup_price", col("cup_price").cast(DecimalType(5,2)))
  )
  logger.info("Appending refreshed product entries to bronze table")
  products_df.write.mode("append").saveAsTable("products_bronze")

  

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT category, AVG(price) as avg_price, count(*)
# MAGIC FROM products_bronze
# MAGIC GROUP BY category;

# COMMAND ----------

client.close()

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT name, category, price, cup_price, cup_measure
# MAGIC FROM products_bronze
# MAGIC WHERE lower(name) like '%jarlsberg%'
# MAGIC ORDER BY cup_price ASC

# COMMAND ----------


