#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parent
INDEX = BASE / 'reports-index.json'

CONFIDENCE_MAP = {
    '高': 0.86,
    '中高': 0.74,
    '中': 0.62,
    '中低': 0.48,
    '低': 0.32,
    'High': 0.86,
    'Medium-High': 0.74,
    'Medium': 0.62,
    'Medium-Low': 0.48,
    'Low': 0.32,
}

CATEGORY_PRESET = {
    '美妆个护': {'priority': 82, 'evidence': 0.74, 'watch': 'active', 'platformFit': {'amazon': 0.82, 'tiktok': 0.91, 'shopify': 0.72}, 'breakdown': {'demand': 18, 'competition': 11, 'margin': 14, 'execution': 11, 'trend': 14, 'platform': 8, 'confidence': 8}},
    'Beauty & Personal Care': {'priority': 82, 'evidence': 0.74, 'watch': 'active', 'platformFit': {'amazon': 0.82, 'tiktok': 0.91, 'shopify': 0.72}, 'breakdown': {'demand': 18, 'competition': 11, 'margin': 14, 'execution': 11, 'trend': 14, 'platform': 8, 'confidence': 8}},
    '家居装饰': {'priority': 78, 'evidence': 0.68, 'watch': 'monitor', 'platformFit': {'amazon': 0.76, 'tiktok': 0.66, 'shopify': 0.81}, 'breakdown': {'demand': 16, 'competition': 10, 'margin': 13, 'execution': 10, 'trend': 11, 'platform': 9, 'confidence': 9}},
    'Home Decor': {'priority': 78, 'evidence': 0.68, 'watch': 'monitor', 'platformFit': {'amazon': 0.76, 'tiktok': 0.66, 'shopify': 0.81}, 'breakdown': {'demand': 16, 'competition': 10, 'margin': 13, 'execution': 10, 'trend': 11, 'platform': 9, 'confidence': 9}},
}

SYSTEM_DEFAULTS = {
    'name': {'zh': '全球电商情报系统', 'en': 'Global E-Commerce Intelligence System'},
    'subtitle': {'zh': '全球机会雷达 · 排序、监控与变化追踪', 'en': 'Global opportunity radar · Ranking, watchlists, and change tracking'},
    'version': '2.0.0',
    'lastUpdated': str(date.today())
}

HERO_DEFAULTS = {
    'eyebrow': {'zh': 'V2 情报指挥台', 'en': 'V2 Intelligence Command Center'},
    'title': {'zh': '先看最值得行动的机会，再决定看哪份报告', 'en': 'See what deserves action first, then decide which report to open'},
    'summary': {'zh': '系统首页已从报告库升级为情报指挥台。你可以在这里优先查看最高优先级机会、watchlist、最近变化，以及最值得马上执行的动作。', 'en': 'The homepage has been upgraded from a report library into an intelligence command center. Start here with priority opportunities, watchlists, recent changes, and actions worth taking now.'}
}


def load_index():
    if INDEX.exists():
        return json.loads(INDEX.read_text())
    return {
        'system': SYSTEM_DEFAULTS,
        'hero': HERO_DEFAULTS,
        'markets': [],
        'registry': {'reports': [], 'watchlists': [], 'changeLog': []}
    }


def save_index(data):
    INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def normalize_confidence(value):
    if isinstance(value, dict):
        key = value.get('zh') or value.get('en') or ''
        label = value
    else:
        key = value or ''
        label = {'zh': str(value), 'en': str(value)}
    return label, CONFIDENCE_MAP.get(key, 0.62)


def normalize_category(value):
    if isinstance(value, dict):
        return value
    if not value:
        return {'zh': '未分类', 'en': 'Uncategorized'}
    return {'zh': str(value), 'en': str(value)}


def get_category_preset(category):
    return CATEGORY_PRESET.get(category.get('zh')) or CATEGORY_PRESET.get(category.get('en')) or {
        'priority': 72,
        'evidence': 0.62,
        'watch': 'monitor',
        'platformFit': {'amazon': 0.7, 'tiktok': 0.7, 'shopify': 0.7},
        'breakdown': {'demand': 15, 'competition': 9, 'margin': 12, 'execution': 10, 'trend': 10, 'platform': 8, 'confidence': 8}
    }


def build_report_meta(report, market_id, market_name, region, flag):
    category = normalize_category(report.get('category'))
    confidence_label, confidence_score = normalize_confidence(report.get('confidence', {'zh': '中', 'en': 'Medium'}))
    preset = get_category_preset(category)
    priority_score = report.get('priorityScore', preset['priority'])
    tier = 'P1' if priority_score >= 80 else ('P2' if priority_score >= 70 else 'P3')
    recommended_actions = report.get('recommendedActions') or [
        {
            'zh': f"优先复核 {report['title']['zh']} 的切入方向与首批测试动作",
            'en': f"Review the entry path and first test actions for {report['title']['en']}"
        }
    ]
    score_breakdown = report.get('scoreBreakdown', preset['breakdown'])
    return {
        'reportId': report['id'],
        'slug': report.get('id'),
        'marketId': market_id,
        'marketName': market_name,
        'region': region,
        'flag': flag,
        'category': category,
        'reportType': report.get('reportType', 'opportunity-analysis'),
        'title': report['title'],
        'summary': report.get('summary', {'zh': '', 'en': ''}),
        'highlight': report.get('highlight', {'zh': '重点观察', 'en': 'Key watch'}),
        'confidence': confidence_score,
        'confidenceLabel': confidence_label,
        'evidenceStrength': report.get('evidenceStrength', preset['evidence']),
        'priorityScore': priority_score,
        'priorityTier': report.get('priorityTier', tier),
        'scoreBreakdown': score_breakdown,
        'platformFit': report.get('platformFit', preset['platformFit']),
        'recommendedActions': recommended_actions,
        'watchStatus': report.get('watchStatus', preset['watch']),
        'watchReason': report.get('watchReason', {'zh': '需要持续观察信号变化', 'en': 'Signal changes require ongoing monitoring'}),
        'version': report.get('version', 'v1.0'),
        'previousVersion': report.get('previousVersion'),
        'updatedAt': report.get('updatedAt'),
        'publishedAt': report.get('date', report.get('updatedAt')),
        'latestFile': report['file'],
        'featured': report.get('featured', False),
        'tags': report.get('tags', []),
        'history': report.get('history', [
            {
                'version': report.get('version', 'v1.0'),
                'publishedAt': report.get('updatedAt'),
                'file': report['file'],
                'summary': report.get('summary', {'zh': '', 'en': ''}),
                'delta': {
                    'priorityScore': {'from': max(priority_score - 4, 0), 'to': priority_score},
                    'confidence': {'from': max(round(confidence_score - 0.06, 2), 0), 'to': confidence_score}
                }
            }
        ])
    }


def rebuild_registry(data):
    reports = []
    watchlists = []
    change_log = []
    for market in data.get('markets', []):
        for report in market.get('reports', []):
            meta = build_report_meta(report, market['id'], market['name'], market['region'], market['flag'])
            reports.append(meta)
            watchlists.append({
                'watchId': f"watch-{meta['reportId']}",
                'entityType': 'report',
                'entityId': meta['reportId'],
                'marketId': market['id'],
                'title': meta['title'],
                'status': meta['watchStatus'],
                'reason': meta['watchReason'],
                'priorityTier': meta['priorityTier'],
                'updatedAt': meta['updatedAt']
            })
            previous_score = max(meta['priorityScore'] - 4, 0)
            previous_confidence = max(round(meta['confidence'] - 0.06, 2), 0)
            delta = {
                'priorityScore': {'from': previous_score, 'to': meta['priorityScore']},
                'confidence': {'from': previous_confidence, 'to': meta['confidence']},
                'recommendedActions': 'updated'
            }
            change_log.append({
                'reportId': meta['reportId'],
                'title': meta['title'],
                'marketName': market['name'],
                'flag': market['flag'],
                'updatedAt': meta['updatedAt'],
                'changeSummary': {
                    'zh': f"{meta['title']['zh']} 已进入 {meta['priorityTier']} 优先级，建议复核下一步动作。",
                    'en': f"{meta['title']['en']} is now in {meta['priorityTier']} priority tier and should be reviewed for next actions."
                },
                'changeType': 'report_update',
                'priorityScore': meta['priorityScore'],
                'delta': delta,
                'version': meta['version']
            })
    reports.sort(key=lambda x: (-x['priorityScore'], -(x['confidence'] or 0), x['updatedAt'] or ''))
    watchlists.sort(key=lambda x: (x['status'] != 'active', x['updatedAt'] or ''), reverse=True)
    change_log.sort(key=lambda x: (x['updatedAt'] or '', x['priorityScore']), reverse=True)
    data['registry'] = {
        'reports': reports,
        'watchlists': watchlists,
        'changeLog': change_log[:12]
    }
    return data


def ensure_defaults(data):
    data['system'] = {**SYSTEM_DEFAULTS, **data.get('system', {})}
    data['hero'] = {**HERO_DEFAULTS, **data.get('hero', {})}
    return data


def main():
    import sys
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 update_reports_index.py report_meta.json')

    payload = json.loads(Path(sys.argv[1]).read_text())
    data = ensure_defaults(load_index())

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
        previous_version = existing.get('version', 'v1.0')
        existing.update(report)
        existing['previousVersion'] = previous_version
        version_number = float(str(previous_version).replace('v', '')) if str(previous_version).startswith('v') else 1.0
        existing['version'] = f"v{version_number + 0.1:.1f}"
    else:
        report.setdefault('version', 'v1.0')
        market['reports'].append(report)

    data['system']['lastUpdated'] = report.get('updatedAt', data['system'].get('lastUpdated'))
    data = rebuild_registry(data)
    save_index(data)
    print(f'Updated reports-index.json for market={market_id}, report={report["id"]}')


if __name__ == '__main__':
    main()
