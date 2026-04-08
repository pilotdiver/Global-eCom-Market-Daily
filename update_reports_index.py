#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
INDEX = BASE / 'reports-index.json'

# Usage:
# python3 update_reports_index.py path/to/report_meta.json
# report_meta.json should contain a single market report payload matching the schema below.
# This script updates or inserts the report into reports-index.json.

SCHEMA_NOTE = {
  "required": ["marketId", "marketName", "region", "flag", "status", "report"]
}


def load_index():
    if INDEX.exists():
        return json.loads(INDEX.read_text())
    raise SystemExit('reports-index.json not found')


def save_index(data):
    INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    import sys
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 update_reports_index.py report_meta.json')

    payload = json.loads(Path(sys.argv[1]).read_text())
    data = load_index()

    market_id = payload['marketId']
    report = payload['report']

    market = next((m for m in data['markets'] if m['id'] == market_id), None)
    if not market:
        market = {
            'id': market_id,
            'flag': payload['flag'],
            'name': payload['marketName'],
            'region': payload['region'],
            'status': payload.get('status', 'live'),
            'reports': []
        }
        data['markets'].append(market)

    market['flag'] = payload['flag']
    market['name'] = payload['marketName']
    market['region'] = payload['region']
    market['status'] = payload.get('status', 'live')

    existing = next((r for r in market['reports'] if r['id'] == report['id']), None)
    if existing:
        existing.update(report)
    else:
        market['reports'].append(report)

    data['system']['lastUpdated'] = report.get('updatedAt', data['system'].get('lastUpdated'))
    save_index(data)
    print(f'Updated reports-index.json for market={market_id}, report={report["id"]}')


if __name__ == '__main__':
    main()
