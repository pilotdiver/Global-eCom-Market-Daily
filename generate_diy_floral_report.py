import json
from pathlib import Path

base = Path('/Users/raymondwaicheungho/Desktop/market-dashboard-template')
html = (base / 'template.html').read_text()
instance = json.loads((base / 'instance-diy-floral-kit.json').read_text())
(base / 'report-diy-floral-kit.html').write_text(
    html.replace('window.__DASHBOARD_DATA__', json.dumps(instance, ensure_ascii=False, indent=2))
)
print('generated report-diy-floral-kit.html')
