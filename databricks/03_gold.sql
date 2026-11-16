-- Databricks notebook source
create or replace table workspace.haze.fact_air_daily as
select  province,
        to_date(ts) as date,
        round(avg(pm2_5),1) as avg_pm25,
        round(max(pm2_5),1) as max_pm25,
        round(avg(pm10),1) as avg_pm10,
        count(*) as reading,
        case when avg(pm2_5) > 37.5 then 1 else 0 end as is_unhealthy
from workspace.haze.silver_air
group by province, to_date(ts);

create or replace table workspace.haze.dim_date as
select  d as date,
        year(d) as year,
        month(d) as month,
        date_format(d, 'MMM') as month_name,
        quarter(d) as quarter,
        date_format(d, 'E') as weekday,
        case when month(d) in (12, 1, 2, 3, 4) then 'Haze season' else 'Other months' end as season
from (select explode(sequence(date'2023-01-01', date'2025-12-31', interval 1 day)) as d);

create or replace table workspace.haze.dim_province as
select * from parquet.`/Volumes/workspace/haze/raw/province/`;

create or replace table workspace.haze.gold_monthly_rank as
with m as (
    select f.province, p.region,
           date_trunc('MONTH', f.date) as month,
           round(avg(f.avg_pm25),1) as avg_pm25,
           sum(f.is_unhealthy) as unhealthy_day
    from workspace.haze.fact_air_daily f
    join workspace.haze.dim_province p on f.province = p.province
    group by f.province, p.region, date_trunc('MONTH', f.date)
)
select *, rank() over (partition by month order by avg_pm25 desc) as rank_in_month from m;

-- COMMAND ----------

SELECT
  (SELECT COUNT(*) FROM workspace.haze.fact_air_daily)    AS fact_rows,
  (SELECT COUNT(*) FROM workspace.haze.dim_date)          AS date_rows,
  (SELECT COUNT(*) FROM workspace.haze.dim_province)      AS province_rows,
  (SELECT COUNT(*) FROM workspace.haze.gold_monthly_rank) AS monthly_rows;

-- COMMAND ----------

select f.province, p.region,
       sum(f.is_unhealthy) as unhealthy_day,
       round(100.0 * sum(f.is_unhealthy) / count(*), 1) as pct_unhealthy
from workspace.haze.fact_air_daily f
join workspace.haze.dim_province p on f.province = p.province
group by f.province, p.region
order by unhealthy_day desc
limit 10;

-- COMMAND ----------

select  d.month_name,
        round(avg(f.avg_pm25),1) as avg_pm25
from workspace.haze.fact_air_daily f
join workspace.haze.dim_date d on f.date = d.date
group by d.month, d.month_name
order by avg_pm25 desc
limit 5;

-- COMMAND ----------

select  d.year, d.quarter,
        round(avg(f.avg_pm25),1) as avg_pm25
from workspace.haze.fact_air_daily f
join workspace.haze.dim_date d on f.date = d.date
group by d.year, d.quarter
order by avg_pm25 desc
limit 5;