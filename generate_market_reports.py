import json
from pathlib import Path
import subprocess

base = Path('/Users/raymondwaicheungho/Desktop/market-dashboard-template')
template = (base / 'template.html').read_text()
markets = [
    ('instance-us-press-on-nails.json', 'report-us-press-on-nails.html', 'report-meta-us-press-on-nails.json'),
    ('instance-au-press-on-nails.json', 'report-au-press-on-nails.html', 'report-meta-au-press-on-nails.json'),
    ('instance-sea-press-on-nails.json', 'report-sea-press-on-nails.html', 'report-meta-sea-press-on-nails.json'),
    ('instance-europe-press-on-nails.json', 'report-europe-press-on-nails.html', 'report-meta-europe-press-on-nails.json')
]

for instance_name, report_name, meta_name in markets:
    data = json.loads((base / instance_name).read_text())
    (base / report_name).write_text(template.replace('window.__DASHBOARD_DATA__', json.dumps(data, ensure_ascii=False, indent=2)))
    subprocess.run(['python3', 'update_reports_index.py', meta_name], cwd=base, check=True)
    print(f'generated {report_name}')
