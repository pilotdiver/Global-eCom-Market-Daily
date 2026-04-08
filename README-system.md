# 全球电商情报系统 — 系统说明

> Global E-Commerce Intelligence System · v1.0.0

---

## 系统架构

```
market-dashboard-template/
├── index.html                    ← 情报系统主控台（多市场总览）
├── template.html                 ← 受保护的报告模板（勿直接编辑内容）
├── schema.json                   ← 数据结构规范
├── market-config.json            ← 全局市场注册表
│
├── instance-au-march.json        ← 澳洲3月数据实例
├── report-au-march-best-sellers.html  ← 生成的报告（template + 实例数据）
│
└── README-system.md              ← 本文档
```

---

## 核心原则

| 原则 | 说明 |
|------|------|
| **模板不动** | `template.html` 是受保护的渲染引擎，只注入数据，不改结构 |
| **数据分离** | 所有业务内容通过 JSON 实例文件管理 |
| **历史归档** | 每份报告在 JSON 中包含 `history` 字段，支持同市场跨月切换 |
| **主控台导航** | `index.html` 是所有报告的入口，统一管理市场与历史档案 |

---

## 生成新报告（3步流程）

### 第1步：复制并填写数据实例

```bash
cp instance-au-march.json instance-us-april.json
# 编辑 instance-us-april.json，填写所有字段
```

### 第2步：在实例 JSON 中加入 history 字段

```json
"history": {
  "market": { "zh": "美国", "en": "United States" },
  "reports": [
    {
      "title": { "zh": "4月畅销商品", "en": "April Best Sellers" },
      "date": "2026-04",
      "file": "report-us-april.html",
      "current": true
    },
    {
      "title": { "zh": "3月畅销商品", "en": "March Best Sellers" },
      "date": "2026-03",
      "file": "report-us-march.html",
      "current": false
    }
  ]
}
```

### 第3步：运行生成命令

```bash
node -e "
const fs = require('fs');
const t = fs.readFileSync('template.html', 'utf8');
const d = JSON.parse(fs.readFileSync('instance-us-april.json', 'utf8'));
const s = '<script>window.__DASHBOARD_DATA__=' + JSON.stringify(d) + ';</scri' + 'pt>';
fs.writeFileSync('report-us-april.html', t.replace('</head>', s + '</head>'));
console.log('Done');
"
```

### 第4步：注册到 market-config.json

在 `market-config.json` 对应市场的 `reports` 数组中添加新报告条目。

---

## 数据字段说明（schema.json）

所有动态字段均支持双语：
```json
{ "zh": "中文内容", "en": "English content" }
```

主要数据模块：

| 模块 | 字段名 | 说明 |
|------|--------|------|
| 基础信息 | `meta`, `sidebar`, `navigation` | 标题、侧边栏、导航 |
| 摘要 | `hero`, `summaryMetrics` | 核心结论与指标卡片 |
| 内容 | `sections.overview` | 总览、强度图、执行评分 |
| 内容 | `sections.signals` | 关键信号（需求 & 场景） |
| 内容 | `sections.opportunities` | 机会方向卡片 |
| 内容 | `sections.pricing` | 价格带表格 |
| 内容 | `sections.players` | 头部玩家与链接 |
| 内容 | `sections.nextMoves` | 下一步行动 |
| 内容 | `sections.risks` | 风险与最终判断 |
| 内容 | `sections.references` | 证据来源 |
| 导航 | `history` | 同市场历史报告（侧边栏归档） |

---

## 市场状态说明

| 状态 | 含义 |
|------|------|
| `live` | 已有报告，主控台展示完整报告库 |
| `soon` | 即将上线，主控台显示占位卡片 |
| `planned` | 规划中，主控台列出但标注灰色 |

---

## 未来规划

- [ ] **Phase 2**：报告生成 CLI 工具（自动化流程）
- [ ] **Phase 3**：多市场对比分析页面
- [ ] **Phase 4**：Web 应用（后台管理 + 数据录入表单）
- [ ] **Phase 5**：爬虫/API 数据源接入层

---

© Raymond Ho 2026 · 全球电商情报系统
