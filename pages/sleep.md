---
title: Sleep
sidebar_position: 20
---


```sql sleep
select * from health.sleep_daily_data
```

<Alert status="info">
Last update: <Value data={sleep} column="date" agg="max" />.
</Alert>

The follow charts shows my daily sleeping hours.

<CalendarHeatmap
    data={sleep}
    date=date
    value=total_hours
/>

## Deep Dive by Year

<Dropdown
    name=selected_sleep_years
    data={sleep}
    value=year
    label=year
    title="Select Year(s) to Compare"
    defaultValue={["2024", "2025"]}
    order="year desc"
    multiple=true
/>

```sql selected_sleep_year
select date, year, total_hours, total_hours_7_day_avg from health.sleep_daily_data
where year in ${inputs.selected_sleep_years.value}
```

### 7-Day Moving Average Comparison

Compare sleeping patterns across selected years:

<LineChart
    data={selected_sleep_year}
    x=date
    y=total_hours_7_day_avg
    series=year
    yAxisTitle="7 Day Average of Sleeping Hours"
    downloadableData=false
>
    <ReferenceLine y=7 label="7 Hours" hideValue labelPosition="aboveStart" color=positive/>
</LineChart>

### Distribution Comparison

Histogram of sleeping hours across selected years:

<Histogram
    data={selected_sleep_year}
    x=total_hours
    xAxisTitle="Total Hours"
    series=year
    downloadableData=false
/>

### Statistics by Year

```sql year_stats
select
    year,
    count(*) as days_recorded,
    round(avg(total_hours), 2) as avg_hours,
    round(min(total_hours), 2) as min_hours,
    round(max(total_hours), 2) as max_hours,
    round(stddev(total_hours), 2) as std_dev
from health.sleep_daily_data
where year in ${inputs.selected_sleep_years.value}
group by year
order by year desc
```

<DataTable
    data={year_stats}
    rows=all
/>


---
<LastRefreshed prefix="Data last updated"/>
