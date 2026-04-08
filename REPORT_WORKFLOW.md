# Report Generation Workflow

## Default workflow for every new report

1. Research the market/topic
2. Generate report instance JSON
3. Generate report HTML from `template.html`
4. Generate/update report registry entry in `reports-index.json`
5. Review homepage preview impact
6. Commit and push to GitHub

## Minimum files per new report

- `instance-<slug>.json`
- `report-<slug>.html`

## Registry update

Preferred method:

```bash
python3 update_reports_index.py path/to/report-meta.json
```

## Report meta payload format

```json
{
  "marketId": "us",
  "marketName": { "zh": "美国", "en": "United States" },
  "region": { "zh": "北美", "en": "North America" },
  "flag": "🇺🇸",
  "status": "live",
  "report": {
    "id": "us-apr-2026",
    "title": { "zh": "4月电商商品爆款分析", "en": "April breakout product analysis" },
    "date": "2026-04",
    "updatedAt": "2026-04-08",
    "file": "report-us-april-breakout-products.html",
    "tags": [
      { "zh": "虫害控制", "en": "Pest control" }
    ],
    "summary": { "zh": "摘要", "en": "Summary" },
    "coverLabel": { "zh": "4月爆款分析", "en": "April Breakout Analysis" },
    "highlight": { "zh": "高确定性季节窗口", "en": "High-certainty seasonal window" },
    "confidence": { "zh": "高", "en": "High" },
    "featured": false
  }
}
```

## Publish workflow

```bash
git add .
git commit -m "Add <report-name> dashboard"
git push
```

## Rule

Do not publish `.workbuddy/`, secrets, SSH files, or local machine artifacts.
