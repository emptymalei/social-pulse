---
title: Open Source
sidebar_position: 30
---


```sql github_stats
select date, domain, sum(stargazers_count) as stargazers_count,
sum(watchers_count) as watchers_count
from opensource.github__stats
group by date, domain
```

<Alert status="info">
Last update: <Value data={github_stats} column="date" agg="max" />.
</Alert>

<AreaChart
    data={github_stats}
    x=date
    y=stargazers_count
    series=domain
    title="Stargazers"
/>




```sql github_top_by_date
select full_name, sum(stargazers_count) as stargazers_count
from opensource.github__stats
WHERE date = (select max(date) from opensource.github__stats)
group by date, full_name
ORDER BY
    stargazers_count DESC
LIMIT 10
```

As of <Value data={github_stats} column="date" agg="max" />, the top 10 repositories by stargazers are:

<DataTable data={github_top_by_date}/>



<LastRefreshed prefix="Data last updated"/>
