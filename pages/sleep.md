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


<DateRange
    name=sleep_range_filtering_a_query
    data={sleep}
    dates=date
    defaultValue={'Last 12 Months'}
/>

```sql filtered_sleep
select
    date, total_hours_7_day_avg
from health.sleep_daily_data
where date between '${inputs.sleep_range_filtering_a_query.start}' and '${inputs.sleep_range_filtering_a_query.end}'
```

<LineChart
    data={filtered_sleep}
    x=date
    y=total_hours_7_day_avg
    yAxisTitle="7 Day Average of Sleeping Hours"
>
    <ReferenceLine y=7 label="7 Hours" hideValue labelPosition="aboveStart" color=positive/>
</LineChart>

Histogram of sleeping hours for the above selected date range.

<Histogram
    data={filtered_sleep}
    x=total_hours_7_day_avg
    xAxisTitle="Total Hours",
/>


---
<LastRefreshed prefix="Data last updated"/>
