-- Databricks notebook source
create or replace table workspace.haze.silver_air as
select province, ts, pm2_5, pm10 from
(select province, to_timestamp(time) as ts,
        pm2_5, pm10,
        row_number() over (partition by province, time order by ingested_at desc) as rn
 from workspace.haze.bronze_air)
where rn = 1 and pm2_5 between 0 and 500 ;

alter table workspace.haze.silver_air
add constraint valid_pm25 check (pm2_5 between 0 and 500);

select (select count(*) from workspace.haze.bronze_air) as bronze_rows,
       (select count(*) from workspace.haze.silver_air) as silver_rows;