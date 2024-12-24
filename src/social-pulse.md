---
theme: dashboard
title: Social Pulse
toc: false
---

# Rocket launches 🚀

<!-- Load and transform the data -->

```js
const events = FileAttachment("./data/pulses.json").json();
```

```js
console.log(events);
```

```js
const transformedEvents = Object.entries(events).map(([date, value]) => ({
  Date: new Date(date),
  Value: value
}));

console.log(transformedEvents);
```


```js
Plot.plot({
  padding: 0,
  x: {axis: null},
  y: {tickFormat: Plot.formatWeekday("en", "narrow"), tickSize: 0},
  fy: {tickFormat: ""},
  color: {scheme: "PiYG", legend: true, label: "Value", tickFormat: "+%", domain: [d3.min(events, d => d.Value), d3.max(events, d => d.Value)]},
  marks: [
    Plot.cell(events, {
      x: (d) => d3.utcWeek.count(d3.utcYear(d.Date), d.Date),
      y: (d) => d.Date.getUTCDay(),
      fy: (d) => d.Date.getUTCFullYear(),
      fill: (d) => d.Value,
      title: (d) => d.Value,
      inset: 0.5
    })
  ]
})
```
