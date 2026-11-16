-- Databricks notebook source
create or replace table workspace.haze.bronze_air as
select *, current_timestamp() as ingested_at
from parquet.`/Volumes/workspace/haze/raw/air/`;

create or replace table workspace.haze.bronze_provinces as
select * from parquet.`/Volumes/workspace/haze/raw/province/`;

select count(distinct province) as provinces, count(*) as rows
from workspace.haze.bronze_air;

-- COMMAND ----------

select count(*) as total_rows,
sum(case when pm2_5 is null then 1 else 0 end) as missing_pm25,
sum(case when pm2_5 < 0 or pm2_5 > 500 then 1 else 0 end) as out_of_range,
count(*) - count(distinct province, time) as duplicates
from workspace.haze.bronze_air;

-- COMMAND ----------

