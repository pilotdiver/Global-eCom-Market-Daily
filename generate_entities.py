import json
from pathlib import Path

base = Path('/Users/raymondwaicheungho/Desktop/market-dashboard-template')
index = json.loads((base / 'reports-index.json').read_text())
out = base / 'entities'
out.mkdir(exist_ok=True)

for entity in index.get('registry', {}).get('entities', []):
    reports = [r for r in index['registry']['reports'] if r['reportId'] in entity.get('reports', [])]
    title = entity['title']
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title.get('zh','Opportunity Profile')} · 全球电商情报系统</title>
  <style>
    body{{margin:0;padding:32px;background:#08111f;color:#ecf3ff;font-family:Inter,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6}}
    .wrap{{max-width:1100px;margin:0 auto;display:grid;gap:20px}}
    .panel{{background:rgba(18,28,48,.92);border:1px solid rgba(148,167,198,.16);border-radius:22px;padding:24px}}
    h1,h2{{margin:0 0 12px}} .muted{{color:#94a7c6;font-size:14px}} .pill{{display:inline-flex;padding:6px 10px;border-radius:999px;background:rgba(53,208,255,.12);border:1px solid rgba(53,208,255,.18);margin-right:8px;font-size:12px}} a{{color:#35d0ff;text-decoration:none}} .list{{display:grid;gap:12px}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="panel">
      <div class="muted">Opportunity Profile</div>
      <h1>{title.get('zh','')} / {title.get('en','')}</h1>
      <div class="muted">Top priority score: {entity.get('topPriorityScore','-')} · Lead report: {entity.get('leadReportId','-')}</div>
      <p>{entity.get('summary',{}).get('zh','')}</p>
      <div>
        <span class="pill">{entity.get('priorityTier','')}</span>
        <span class="pill">Reports {len(entity.get('reports',[]))}</span>
        <span class="pill">Markets {len(entity.get('markets',[]))}</span>
      </div>
    </div>
    <div class="panel">
      <h2>Linked Reports</h2>
      <div class="list">
        {''.join([f'<div><a href="../{r["latestFile"]}">{r["title"].get("zh","")} / {r["title"].get("en","")}</a><div class="muted">{r["marketName"].get("zh","")} · Score {r.get("priorityScore","-")} · Confidence {round((r.get("confidence",0))*100)}%</div></div>' for r in reports])}
      </div>
    </div>
    <div class="panel">
      <h2>Platform Fit</h2>
      <div class="muted">Amazon: {round(entity.get('platformFit',{}).get('amazon',0)*100)}% · TikTok: {round(entity.get('platformFit',{}).get('tiktok',0)*100)}% · Shopify: {round(entity.get('platformFit',{}).get('shopify',0)*100)}%</div>
    </div>
    <div class="panel"><a href="../index.html">← 返回系统首页</a></div>
  </div>
</body>
</html>'''
    (out / f"{entity['entityId']}.html").write_text(html)
    entity['profileFile'] = f"entities/{entity['entityId']}.html"

(base / 'reports-index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n')
print('generated entity profile pages')
