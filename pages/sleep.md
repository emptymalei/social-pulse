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

<LineChart
    data={sleep}
    x=date
    y=total_hours_7_day_avg
    yAxisTitle="7 Day Average of Sleeping Hours"
/>

<Dropdown
    name=selected_sleep_year
    data={sleep}
    value=year
    defaultValue="2024"
    title="Select a Year"
/>



```sql selected_sleep_year
select * from health.sleep_daily_data
where year = '${inputs.selected_sleep_year.value}'
```

Histogram of sleeping hours for <Value data={selected_sleep_year} column="year" agg="max" />.

<Histogram
    data={selected_sleep_year}
    x=total_hours
    xAxisTitle="Total Hours",
/>


---
<LastRefreshed prefix="Data last updated"/>
