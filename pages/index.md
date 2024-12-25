---
title: LM's Dashboard
neverShowQueries: true
---

# Social Pulse

Am I still alive? Life is not only measured by biological metrics. It is also measured by our online activities. This dashboard shows my online activities. If I am ever online, a bar will show up in the chart. If this dashboard is showing null activities, it probably means I am dead, at least online.

In the background, we have GitHub Actions running regularly on GitHub and update the social activities. The updated data is then fed into this dashboard.

## Everything Combined



```sql pulses
select * from pulses.pulses
```

<CalendarHeatmap
    data={pulses}
    date=Date
    value=Value
/>

## Social Media Activities


```sql pulses_social
select * from pulses.social_media
```

<CalendarHeatmap
    data={pulses_social}
    date=Date
    value=Value
/>

## Tech Activities

```sql pulses_tech
select * from pulses.tech
```

<CalendarHeatmap
    data={pulses_tech}
    date=Date
    value=Value
/>



```sql categories
  select
      category
  from needful_things.orders
  group by category
```

<Dropdown data={categories} name=category value=category>
    <DropdownOption value="%" valueLabel="All Categories"/>
</Dropdown>

<Dropdown name=year>
    <DropdownOption value=% valueLabel="All Years"/>
    <DropdownOption value=2019/>
    <DropdownOption value=2020/>
    <DropdownOption value=2021/>
</Dropdown>

```sql orders_by_category
  select
      date_trunc('month', order_datetime) as month,
      sum(sales) as sales_usd,
      category
  from needful_things.orders
  where category like '${inputs.category.value}'
  and date_part('year', order_datetime) like '${inputs.year.value}'
  group by all
  order by sales_usd desc
```

<BarChart
    data={orders_by_category}
    title="Sales by Month, {inputs.category.label}"
    x=month
    y=sales_usd
    series=category
/>
