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

# MAGIC %sh
# MAGIC apt install -y chromium-browser

# COMMAND ----------

# MAGIC %sh
# MAGIC # Do this once
# MAGIC wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# MAGIC cp ./google-chrome-stable_current_amd64.deb /Volumes/demo/binaries/chromium
# MAGIC
# MAGIC #apt -y install ./google-chrome-stable_current_amd64.deb

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

# MAGIC %sh
# MAGIC ls | grep chrome
# MAGIC #rm /Volumes/demo/binaries/chromium/chromedriver_linux64.zip
# MAGIC echo "Second ls"
# MAGIC ls /Volumes/demo/binaries/chromium | grep chrome

# COMMAND ----------

# MAGIC %sh
# MAGIC #wget https://chromedriver.storage.googleapis.com/115.0.5790.17/chromedriver_linux64.zip
# MAGIC
# MAGIC # 115 wasn't out when I re-ran the script so needed this "testing" stable release
# MAGIC rm chromedriver_linux64.zip
# MAGIC wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.170/linux64/chromedriver-linux64.zip -O chromedriver_linux64.zip
# MAGIC rm /Volumes/demo/binaries/chromium/chromedriver_linux64.zip
# MAGIC cp chromedriver_linux64.zip /Volumes/demo/binaries/chromium/chromedriver_linux64.zip

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test the Installation
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
# MAGIC # Temporarily copy from /chrome/chrome-linux64 to /chrome
# MAGIC cd /chrome
# MAGIC cp -pR ./chromedriver-linux64/* .
# MAGIC rm -Rf ./chromedriver-linux64

# COMMAND ----------

# MAGIC %sh
# MAGIC apt-get install -y libglib2.0-0 \
# MAGIC     libnss3 \
# MAGIC     libgconf-2-4 \
# MAGIC     libfontconfig1

# COMMAND ----------

dbutils.fs.put("/databricks/scripts/install-chrome.sh", """
#!/bin/bash

apt-get update

mkdir /chrome
cd /chrome

#
wget https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt -y install ./google-chrome-stable_current_amd64.deb

apt-get install -y libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1

echo "it worked" > /tmp/test_init.log
""", True)

# COMMAND ----------

# MAGIC %md
# MAGIC # Run the Init Script
# MAGIC
# MAGIC We can run the init script here if we want to test it for the attached server.

# COMMAND ----------

# MAGIC %sh /dbfs/databricks/scripts/install-chrome.sh
# MAGIC

# COMMAND ----------

# MAGIC %sh
# MAGIC cat /tmp/test_init.log 
