# Travel Roadbook

一个面向真实出行的旅行攻略路书 Skill。它保留原项目的结构化校验、路线估算和多格式导出，同时新增个人偏好适配、城市慢游/山岳徒步/自驾长线模式、公开分享脱敏，以及全新的 TravelOS 离线 HTML。

## 特性

- 城市慢游：片区聚类、错峰、休息窗口、雨天备选、固定住宿基地优先
- 山岳徒步：爬升、补给、撤退点、最晚通过时间和停止条件
- 自驾长线：净驾驶时长、司机休息、补能、停车、备用道路和停止条件
- 可选本地画像：只读取明确提供的目录，仅输出派生信号，不复制原始笔记
- Personal / Share 双版本：分享版在渲染前递归脱敏并阻断本地路径
- 单文件离线 HTML：桌面、手机和打印适配，支持清单、时间顺延与预算编辑
- 同时导出 Markdown、ICS、GeoJSON、规范化 JSON 和质量报告

## 快速使用

安装为 Codex Skill 后，直接请求：

> 帮我做一份杭州 3 天路书，从合肥出发，休闲美食风格，少排队，全程尽量住同一家酒店。

结构化构建：

```bash
python3 scripts/build_roadbook.py examples/hangzhou-city-3d.json \
  --output generated/hangzhou-roadbook \
  --scope share
```

可选读取本地旅行框架：

```bash
python3 scripts/build_roadbook.py trip.json \
  --output generated/my-trip \
  --knowledge-root /path/to/travel-framework \
  --scope personal
```

输出为 `.html`、`.md`、`.ics`、`.geojson`、`.normalized.json` 和 `.quality.json`。

## 隐私

真实知识库、个人画像、姓名、私人事件、订单数据和 API Key 不应提交到公开仓库。需要公开发布时使用 `--scope share`，并在发布前检查所有格式；精确轨迹也可能属于隐私。

## 兼容性

旧版 `1.0` 输入和 `scripts/build_guide.py` 保留。新路书使用 schema `2.0` 与 `scripts/build_roadbook.py`。高德 API 是可选增强，没有 Key 时继续使用明确标注的离线估算。

## 测试

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
npm install
npm run test:browser
```

浏览器测试复用本机 Chrome，不会把截图写入仓库。
