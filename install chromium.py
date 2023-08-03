# Databricks notebook source
# MAGIC %md
# MAGIC # Create our Init Script
# MAGIC Be aware that the version of chromium needs to have a dependent version of chrome.
# MAGIC
# MAGIC An improvement to this script would be to download the google-chrome-stable (v102 at time of writing) and chromium and put them in DBFS or another ADLS container.
# MAGIC
# MAGIC This script also works against DBR 9.1 LTS, it wasn't working with DBR 10.4 LTS due to libnss issues.

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get update

# COMMAND ----------

# MAGIC %md
# MAGIC ## Change Ubuntu Repository
# MAGIC
# MAGIC This ugly command below uses 'sed' command to insert the Australian country reference in front to the Ubuntu URLs. 
# MAGIC
# MAGIC We did this because there was a problem with the central repo.
# MAGIC
# MAGIC ![Ubuntu Central Error](./Ubuntu_Central_Error.png)
# MAGIC

# COMMAND ----------

# MAGIC %sh
# MAGIC sed -i -e 's/http:\/\//http:\/\/au./g' /etc/apt/sources.list

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get update -y

# COMMAND ----------

# MAGIC %sh
# MAGIC apt -y install /Volumes/demo/binaries/chromium/google-chrome-stable_current_amd64.deb

# COMMAND ----------

# MAGIC %md
# MAGIC ## Find out your Google Chrome version
# MAGIC We run the command below to find out what version of chrome we need - we must align our driver to this.
# MAGIC
# MAGIC Once you have the version, you need to get the URL for the correct version from here: https://chromedriver.chromium.org/downloads
# MAGIC
# MAGIC Ironically, if we had Selenium, we could do this automatically!!

# COMMAND ----------

# MAGIC %sh
# MAGIC /usr/bin/google-chrome --version

# COMMAND ----------

# MAGIC %md
# MAGIC ## Download Chrome Driver
# MAGIC Now that we have the right version

# COMMAND ----------

# MAGIC %md
# MAGIC ## Install Chrome Driver
# MAGIC We can now test that the installation works

# COMMAND ----------

# MAGIC %sh
# MAGIC rm -Rf /chrome
# MAGIC mkdir /chrome
# MAGIC cd /chrome
# MAGIC cp /Volumes/demo/binaries/chromium/chromedriver_linux64.zip /tmp/chromedriver_linux64.zip
# MAGIC unzip /tmp/chromedriver_linux64.zip

# COMMAND ----------

# MAGIC %sh
# MAGIC # Temporarily while on test version of Chrome 115 copy from /chrome/chrome-linux64 to /chrome
# MAGIC cd /chrome
# MAGIC cp -pR ./chromedriver-linux64/* .
# MAGIC rm -Rf ./chromedriver-linux64

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get install -y libglib2.0-0 \
# MAGIC     libnss3 \
# MAGIC     libgconf-2-4 \
# MAGIC     libfontconfig1
