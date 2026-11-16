-- Databricks notebook source
create schema if not exists workspace.haze;
create volume if not exists workspace.haze.raw;

-- COMMAND ----------

list '/Volumes/workspace/haze/raw';