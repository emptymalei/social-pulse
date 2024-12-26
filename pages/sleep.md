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
    name=selected_sleep_year
    data={sleep}
    value=year
    title="Select a Year"
    defaultValue="2024"
/>

```sql selected_sleep_year
select date, year, total_hours, total_hours_7_day_avg from health.sleep_daily_data
where year = '${inputs.selected_sleep_year.value}'
```

Moving average of sleeping hours for <Value data={selected_sleep_year} column="year" agg="max" />:

<LineChart
    data={selected_sleep_year}
    x=date
    y=total_hours_7_day_avg
    yAxisTitle="7 Day Average of Sleeping Hours"
    downloadableData=false
>
    <ReferenceLine y=7 label="7 Hours" hideValue labelPosition="aboveStart" color=positive/>
</LineChart>


Histogram of sleeping hours for <Value data={selected_sleep_year} column="year" agg="max" />:


<Histogram
    data={selected_sleep_year}
    x=total_hours
    xAxisTitle="Total Hours"
    downloadableData=false
/>


---
<LastRefreshed prefix="Data last updated"/>
