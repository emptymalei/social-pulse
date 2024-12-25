---
title: Social Pulse
sidebar_position: 10
---


Am I still alive? Life is not only measured by biological metrics. It is also measured by our online activities. This dashboard shows my online activities. If I am ever online, a bar will show up in the chart. If this dashboard is showing null activities, it probably means I am dead, at least online.

In the background, we have GitHub Actions running regularly on GitHub and update the social activities. The updated data is then fed into this dashboard.

## Was I Online?

The follow calendar heatmap indicates all my online activities. Color indicates that I was online on that day. Missing values means I was most likely offline.

```sql pulses_all
select * from pulses.pulses
```

<CalendarHeatmap
    data={pulses_all}
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
