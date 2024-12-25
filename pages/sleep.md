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


<CalendarHeatmap
    data={sleep}
    date=date
    value=total_hours
/>


<Dropdown
    name=selected_sleep_year
    data={sleep}
    value=year
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
