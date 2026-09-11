"""Semantic, escaped HTML components for TravelOS roadbooks."""

from html import escape


def e(value):
    return escape(str(value if value is not None else ""), quote=True)


def section_heading(number, label, title):
    return f'<header class="section-heading"><span class="section-no">{e(number)} · {e(label)}</span><h2>{e(title)}</h2></header>'


def render_hero(data):
    meta = data.get("meta", {})
    mode = data.get("trip", {}).get("primary_mode", "city").replace("_", " ")
    facts = (
        ("Destination", meta.get("destination", "—")),
        ("Date", meta.get("start_date", "—")),
        ("Duration", f'{meta.get("days", len(data.get("days", [])))} days'),
        ("Mode", mode),
    )
    fact_html = "".join(f'<div class="fact"><small>{e(label)}</small><strong>{e(value)}</strong></div>' for label, value in facts)
    return f'''<header class="hero" data-section="overview">
      <div class="hero-top"><span>TravelOS / Roadbook 02</span><span>{e(meta.get("language", "zh-CN"))}</span></div>
      <div class="hero-copy"><p class="eyebrow">A field guide for moving well</p><h1>{e(meta.get("title", "旅行路书"))}</h1><p class="subtitle">{e(meta.get("subtitle", "把路线、节奏与临场判断，整理成一份真正能带上路的计划。"))}</p></div>
      <div class="fact-strip">{fact_html}</div>
    </header>'''


def render_route(data):
    stops = []
    for day in data.get("days", []):
        for item in day.get("items", []):
            route = item.get("route_from_previous", {})
            detail = ""
            if route:
                detail = f'{route.get("distance_km", "—")} km · {route.get("duration_min", "—")} min'
            stops.append(f'<li><time>{e(item.get("start", ""))}</time><strong>{e(item.get("name", "未命名地点"))}</strong><span>{e(detail)}</span></li>')
    return f'<section class="section" data-section="route">{section_heading("01", "Route", "一眼看懂移动逻辑")}<ol class="route-ribbon">{"".join(stops) or "<li class=\"empty\">暂无路线节点</li>"}</ol></section>'


def _micro_list(values):
    return f'<ul class="micro-list">{"".join(f"<li>{e(value)}</li>" for value in values)}</ul>' if values else ""


def render_days(data):
    days_html = []
    for day in data.get("days", []):
        items = []
        for item in day.get("items", []):
            route = item.get("route_from_previous", {})
            route_html = f'<span class="route-leg">{e(route.get("mode", "移动"))} · {e(route.get("duration_min", "—"))} min</span>' if route else ""
            items.append(f'''<li class="timeline-item">
              <time class="timeline-time">{e(item.get("start", ""))}<br>{e(item.get("end", ""))}</time><span class="timeline-mark" aria-hidden="true"></span>
              <div class="timeline-copy"><h3>{e(item.get("name", "未命名行程"))}</h3><p>{e(item.get("description", ""))}</p>{route_html}</div>
            </li>''')
        comfort = list(day.get("rest_windows", [])) + list(day.get("rain_alternatives", []))
        days_html.append(f'''<article class="day" id="day-{e(day.get("day", ""))}" data-day="{e(day.get("day", ""))}">
          <div class="day-index">DAY {e(day.get("day", ""))}</div><div><h3 class="day-title">{e(day.get("title", ""))}</h3><p class="day-date">{e(day.get("date", ""))}</p>
          {_micro_list(comfort)}<ol class="timeline">{"".join(items)}</ol></div></article>''')
    return f'<section class="section" id="daily-plan" data-section="daily-plan">{section_heading("02", "Pace", "每天只保留值得的事")}{"".join(days_html)}</section>'


def _cards(records, kind):
    cards = []
    for record in records:
        title = record.get("name") or record.get("area") or record.get("shop") or kind
        description = record.get("reason") or record.get("description") or record.get("detail") or ""
        price = record.get("price", "")
        cards.append(f'<article class="quiet-card"><p class="eyebrow">{e(kind)}</p><h3>{e(title)}</h3><p>{e(description)}</p><p>{e(price)}</p></article>')
    return "".join(cards)


def render_food_stay(data):
    cards = _cards(data.get("foods", []), "Food") + _cards(data.get("hotels", []), "Stay")
    return f'<section class="section" data-section="food-stay">{section_heading("03", "Eat & sleep", "吃好，也住得顺路")}<div class="card-grid">{cards or "<p class=\"empty\">在生成完整路书时补充餐饮与住宿建议。</p>"}</div></section>'


def render_budget(data):
    budget = data.get("budget", {})
    selected = budget.get("selected")
    profile = budget.get("profiles", {}).get(selected, {}) if selected else budget
    categories = profile.get("categories", {})
    rows = "".join(f'<tr><th>{e(name)}</th><td>{e(value)}</td></tr>' for name, value in categories.items())
    total = profile.get("total", sum(value for value in categories.values() if isinstance(value, (int, float))))
    return f'<section class="section" data-section="budget">{section_heading("04", "Budget", "花费透明，临场不慌")}<div class="split-grid"><table class="budget-table"><tbody>{rows or "<tr><th>待估算</th><td>—</td></tr>"}<tr><th>合计</th><td>{e(total)}</td></tr></tbody></table>{render_mode_panel(data)}</div></section>'


def render_mode_panel(data):
    mode = data.get("trip", {}).get("primary_mode", "city")
    labels = {"city": "城市慢游判断", "hiking": "山野安全判断", "road_trip": "公路节奏判断"}
    fields = {
        "city": ("rest_windows", "rain_alternatives"),
        "hiking": ("retreat_points", "stop_conditions", "supplies"),
        "road_trip": ("fuel_or_charge", "parking", "stop_conditions"),
    }
    values = []
    for day in data.get("days", []):
        for field in fields.get(mode, ()):
            value = day.get(field, [])
            if isinstance(value, list):
                values.extend(item.get("trigger", str(item)) if isinstance(item, dict) else str(item) for item in value)
    items = "".join(f"<li>{e(value)}</li>" for value in values[:8]) or "<li>生成完整数据后显示关键判断</li>"
    return f'<aside class="mode-panel" data-mode="{e(mode)}"><p class="eyebrow">Decision layer</p><h3>{e(labels.get(mode, mode))}</h3><ul>{items}</ul></aside>'


def render_sources(data):
    items = []
    for source in data.get("sources", []):
        title = e(source.get("title", source.get("id", "来源")))
        checked = e(source.get("verified_at") or source.get("checked_at") or "待核实")
        url = source.get("url")
        label = f'<a href="{e(url)}" rel="noopener noreferrer">{title}</a>' if url and str(url).startswith(("https://", "http://")) else title
        items.append(f"<li>{label} · {checked}</li>")
    return f'<section class="section" data-section="sources">{section_heading("05", "Sources", "哪些是事实，哪些要复核")}<ol class="source-list">{"".join(items) or "<li>当前示例未附来源；正式路书必须标注动态事实。</li>"}</ol></section>'


def render_body(data):
    return "".join((render_hero(data), render_route(data), render_days(data), render_food_stay(data), render_budget(data), render_sources(data)))
