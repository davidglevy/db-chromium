-- Databricks notebook source
CREATE CATALOG IF NOT EXISTS demo;
CREATE SCHEMA IF NOT EXISTS demo.woolies_scrape;
USE demo.woolies_scrape;

-- COMMAND ----------

CREATE OR REPLACE TABLE products_bronze (
  stockcode string,
  barcode string,
  name string,
  package_size string,
  category string,
  messages array < 
    struct < 
      level string,
      code string,
      message string
    > 
  >,
  price float,
  has_cup_price boolean,
  cup_measure string,
  cup_price float,
  raw_text string,
  insert_ts timestamp
);
