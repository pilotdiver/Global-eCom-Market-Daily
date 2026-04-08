# Protected Dashboard Master Files

These files are the protected master layer and should NOT be casually edited during daily report generation:

- template.html
- schema.json
- README-template.md

## Daily operation rule

For normal report generation:
1. Keep `template.html` unchanged
2. Inject business content through JSON only
3. Generate instance files separately, for example:
   - report-au-2026-03.html
   - report-us-tiktok-summer.html

## Dynamic data rule

All business content is dynamic data, including:
- market
- platform
- theme
- date
- judgments
- metrics
- signals
- opportunities
- pricing
- players
- references

## Rendering rule

At runtime, inject a report JSON into:
- `window.__DASHBOARD_DATA__`

Then let the built-in JS render the dashboard.
