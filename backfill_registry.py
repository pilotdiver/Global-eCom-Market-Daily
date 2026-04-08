import json
from pathlib import Path
import subprocess

base = Path('/Users/raymondwaicheungho/Desktop/market-dashboard-template')
for meta in sorted(base.glob('report-meta-*.json')):
    subprocess.run(['python3', 'update_reports_index.py', meta.name], cwd=base, check=True)
    print(f'processed {meta.name}')
