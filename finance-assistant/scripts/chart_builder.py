"""
Finance Assistant — Chart.js HTML Artifact Builder (v1.0).

Each function returns a complete standalone HTML string suitable for use as a
Claude artifact. Rendered as an interactive chart in Cowork / Claude.ai.
Falls back to scripts/viz.py ASCII charts for plain-text Claude Code terminal.
"""

from __future__ import annotations

import json
from typing import Optional


# ── Shared HTML shell ─────────────────────────────────────────────────────────

_HEAD = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3"></script>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 16px; background: #0f0f1a; color: #e0e0e0;
         font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  .card { background: #16213e; border-radius: 14px; padding: 22px; margin-bottom: 16px;
          box-shadow: 0 4px 24px rgba(0,0,0,0.4); }
  .title { font-size: 18px; font-weight: 700; margin-bottom: 4px; color: #fff; }
  .subtitle { font-size: 13px; color: #888; margin-bottom: 20px; }
  .chart-wrap { position: relative; width: 100%; }
  .row { display: flex; gap: 16px; flex-wrap: wrap; }
  .col { flex: 1; min-width: 260px; }
  .stat-row { display: flex; gap: 24px; flex-wrap: wrap; margin-top: 16px; }
  .stat { background: #0d1b33; border-radius: 10px; padding: 12px 18px; flex: 1; min-width: 120px; }
  .stat-label { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: .06em; }
  .stat-value { font-size: 20px; font-weight: 700; color: #e0e0e0; margin-top: 2px; }
  table.data { width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 13px; }
  table.data th { text-align: left; color: #666; font-weight: 600;
                  border-bottom: 1px solid #1e2d4a; padding: 6px 10px; }
  table.data td { padding: 7px 10px; border-bottom: 1px solid #131f33; }
  table.data tr:last-child td { border-bottom: none; }
  .bar-cell { display: flex; align-items: center; gap: 8px; }
  .mini-bar { height: 6px; border-radius: 3px; background: #0d1b33; flex: 1; overflow: hidden; }
  .mini-bar-fill { height: 100%; border-radius: 3px; }
  .green  { color: #4ade80; } .amber { color: #fbbf24; } .red { color: #f87171; }
  .no-data { text-align: center; padding: 40px; color: #555; font-size: 15px; }
</style>
</head>
<body>"""

_FOOT = "\n</body>\n</html>"


def _html(body: str) -> str:
    return _HEAD + "\n" + body + _FOOT


def _fmt(amount: float, currency: str = "EUR") -> str:
    symbol = "€" if currency == "EUR" else ("$" if currency == "USD" else currency + " ")
    if abs(amount) >= 1_000_000:
        return f"{symbol}{amount / 1_000_000:.1f}M"
    if abs(amount) >= 1_000:
        return f"{symbol}{amount / 1_000:.1f}k"
    return f"{symbol}{amount:,.0f}"


def _pct_color(pct: float) -> str:
    if pct > 100:
        return "#f87171"
    if pct >= 80:
        return "#fbbf24"
    return "#4ade80"


# ── budget_chart ──────────────────────────────────────────────────────────────

def budget_chart(categories: dict, currency: str = "EUR", month: str = None) -> str:
    """
    Doughnut chart: budget usage per category.
    categories = {"Food": {"limit": 400, "actual": 340}, ...}
    Center text: total spent / total budget.
    Color: green <80%, amber 80-100%, red over.
    Below: table with category, spent, limit, % bar.
    """
    if not categories:
        return _html('<div class="card"><div class="no-data">No budget data available.</div></div>')

    labels, data_vals, bg_colors, total_spent, total_limit = [], [], [], 0.0, 0.0
    table_rows = []

    for name, vals in categories.items():
        limit = float(vals.get("limit", 0) or 0)
        actual = float(vals.get("actual", 0) or 0)
        pct = (actual / limit * 100) if limit else 0
        color = _pct_color(pct)
        labels.append(name)
        data_vals.append(round(actual, 2))
        bg_colors.append(color)
        total_spent += actual
        total_limit += limit
        table_rows.append((name, actual, limit, pct, color))

    total_pct = (total_spent / total_limit * 100) if total_limit else 0
    center_color = _pct_color(total_pct)
    subtitle_text = f"Month: {month}" if month else "Budget overview"

    table_html = "".join(
        f"""<tr>
          <td>{n}</td>
          <td style="color:{c}">{_fmt(a, currency)}</td>
          <td style="color:#888">{_fmt(l, currency)}</td>
          <td>
            <div class="bar-cell">
              <div class="mini-bar"><div class="mini-bar-fill"
                style="width:{min(p,100):.0f}%;background:{c}"></div></div>
              <span style="color:{c};min-width:38px">{p:.0f}%</span>
            </div>
          </td>
        </tr>"""
        for n, a, l, p, c in table_rows
    )

    js_labels = json.dumps(labels)
    js_data = json.dumps(data_vals)
    js_colors = json.dumps(bg_colors)

    body = f"""
<div class="card">
  <div class="title">Budget Overview</div>
  <div class="subtitle">{subtitle_text}</div>
  <div style="display:flex;gap:32px;flex-wrap:wrap;align-items:center">
    <div style="width:240px;height:240px;flex-shrink:0;position:relative;margin:0 auto">
      <canvas id="bc"></canvas>
      <div id="center-text" style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
           text-align:center;pointer-events:none">
        <div style="font-size:20px;font-weight:700;color:{center_color}">{_fmt(total_spent, currency)}</div>
        <div style="font-size:11px;color:#888">of {_fmt(total_limit, currency)}</div>
        <div style="font-size:13px;color:{center_color};font-weight:600">{total_pct:.0f}%</div>
      </div>
    </div>
    <div style="flex:1;min-width:280px">
      <table class="data">
        <thead><tr>
          <th>Category</th><th>Spent</th><th>Limit</th><th>Usage</th>
        </tr></thead>
        <tbody>{table_html}</tbody>
      </table>
    </div>
  </div>
</div>
<script>
new Chart(document.getElementById('bc'), {{
  type: 'doughnut',
  data: {{
    labels: {js_labels},
    datasets: [{{ data: {js_data}, backgroundColor: {js_colors},
                 borderColor: '#0f0f1a', borderWidth: 3, hoverOffset: 6 }}]
  }},
  options: {{
    cutout: '72%', responsive: true, maintainAspectRatio: true,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.label}}: {currency == "EUR" and "€" or "$"}${{ctx.parsed.toLocaleString(undefined, {{maximumFractionDigits:0}})}}`
        }}
      }}
    }}
  }}
}});
</script>"""

    return _html(body)


# ── portfolio_chart ───────────────────────────────────────────────────────────

def portfolio_chart(holdings: list, currency: str = "EUR") -> str:
    """
    Left: Pie chart — allocation by asset class.
    Right: Horizontal bar chart — top 10 holdings by value.
    """
    if not holdings:
        return _html('<div class="card"><div class="no-data">No portfolio holdings available.</div></div>')

    total = sum(h.get("value", 0) for h in holdings)
    if total <= 0:
        return _html('<div class="card"><div class="no-data">Portfolio value is zero.</div></div>')

    # Asset class grouping
    classes: dict[str, float] = {}
    for h in holdings:
        cls = h.get("asset_class", "Other")
        classes[cls] = classes.get(cls, 0.0) + h.get("value", 0.0)

    cls_palette = ["#3b82f6", "#06b6d4", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444"]
    sorted_cls = sorted(classes.items(), key=lambda x: x[1], reverse=True)
    cls_labels = [c[0] for c in sorted_cls]
    cls_values = [round(c[1], 2) for c in sorted_cls]
    cls_colors = [cls_palette[i % len(cls_palette)] for i in range(len(cls_labels))]

    # Top 10 holdings
    top10 = sorted(holdings, key=lambda h: h.get("value", 0), reverse=True)[:10]
    h_labels = [h.get("name", "?") for h in top10]
    h_values = [round(h.get("value", 0), 2) for h in top10]
    h_returns = [h.get("return_pct", 0) for h in top10]
    h_colors = ["#4ade80" if r >= 0 else "#f87171" for r in h_returns]

    weighted_return = sum(
        h.get("value", 0) * h.get("return_pct", 0) for h in holdings
    ) / total if total else 0

    js_cls_labels = json.dumps(cls_labels)
    js_cls_values = json.dumps(cls_values)
    js_cls_colors = json.dumps(cls_colors)
    js_h_labels = json.dumps(h_labels)
    js_h_values = json.dumps(h_values)
    js_h_colors = json.dumps(h_colors)

    body = f"""
<div class="card">
  <div class="title">Portfolio Allocation</div>
  <div class="subtitle">Total value: {_fmt(total, currency)} &nbsp;·&nbsp; Weighted return: <span style="color:{'#4ade80' if weighted_return >= 0 else '#f87171'}">{weighted_return:+.1f}%</span></div>
  <div class="row">
    <div class="col">
      <div style="font-size:13px;font-weight:600;color:#aaa;margin-bottom:12px">Asset Class Mix</div>
      <div class="chart-wrap" style="height:220px"><canvas id="pie-chart"></canvas></div>
    </div>
    <div class="col">
      <div style="font-size:13px;font-weight:600;color:#aaa;margin-bottom:12px">Top Holdings</div>
      <div class="chart-wrap" style="height:220px"><canvas id="bar-chart"></canvas></div>
    </div>
  </div>
</div>
<script>
new Chart(document.getElementById('pie-chart'), {{
  type: 'pie',
  data: {{
    labels: {js_cls_labels},
    datasets: [{{ data: {js_cls_values}, backgroundColor: {js_cls_colors},
                 borderColor: '#0f0f1a', borderWidth: 2 }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{
      legend: {{ position: 'bottom', labels: {{ color: '#aaa', font: {{ size: 11 }}, boxWidth: 12 }} }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.label}}: ${{(ctx.parsed / {total} * 100).toFixed(1)}}%`
        }}
      }}
    }}
  }}
}});
new Chart(document.getElementById('bar-chart'), {{
  type: 'bar',
  data: {{
    labels: {js_h_labels},
    datasets: [{{
      label: 'Value',
      data: {js_h_values},
      backgroundColor: {js_h_colors},
      borderRadius: 4
    }}]
  }},
  options: {{
    indexAxis: 'y', responsive: true, maintainAspectRatio: false,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.parsed.x.toLocaleString(undefined, {{maximumFractionDigits:0}})}} {currency}`
        }}
      }}
    }},
    scales: {{
      x: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#1e2d4a' }} }},
      y: {{ ticks: {{ color: '#aaa', font: {{ size: 11 }} }}, grid: {{ display: false }} }}
    }}
  }}
}});
</script>"""

    return _html(body)


# ── net_worth_chart ───────────────────────────────────────────────────────────

def net_worth_chart(snapshots: list, currency: str = "EUR") -> str:
    """
    Line chart of net worth over time.
    Three lines: Net Worth (filled area), Assets (dashed), Liabilities (dashed red).
    """
    if not snapshots:
        return _html('<div class="card"><div class="no-data">No net worth snapshots available.</div></div>')

    sorted_snaps = sorted(snapshots, key=lambda s: s.get("date", ""))
    labels = [s.get("date", "") for s in sorted_snaps]
    nw_data = [round(s.get("net_worth", 0), 2) for s in sorted_snaps]
    asset_data = [round(s.get("assets", 0), 2) for s in sorted_snaps]
    liab_data = [round(s.get("liabilities", 0), 2) for s in sorted_snaps]

    first_nw = nw_data[0] if nw_data else 0
    last_nw = nw_data[-1] if nw_data else 0
    delta = last_nw - first_nw
    delta_pct = (delta / abs(first_nw) * 100) if first_nw else 0
    delta_color = "#4ade80" if delta >= 0 else "#f87171"
    sign = "+" if delta >= 0 else ""

    js_labels = json.dumps(labels)
    js_nw = json.dumps(nw_data)
    js_assets = json.dumps(asset_data)
    js_liabs = json.dumps(liab_data)

    body = f"""
<div class="card">
  <div class="title">Net Worth Timeline</div>
  <div class="subtitle">{len(snapshots)} snapshot{"s" if len(snapshots) != 1 else ""}</div>
  <div class="stat-row">
    <div class="stat">
      <div class="stat-label">Current Net Worth</div>
      <div class="stat-value">{_fmt(last_nw, currency)}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Change</div>
      <div class="stat-value" style="color:{delta_color}">{sign}{_fmt(delta, currency)}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Growth</div>
      <div class="stat-value" style="color:{delta_color}">{sign}{delta_pct:.1f}%</div>
    </div>
  </div>
  <div class="chart-wrap" style="height:280px;margin-top:20px"><canvas id="nw-chart"></canvas></div>
</div>
<script>
new Chart(document.getElementById('nw-chart'), {{
  type: 'line',
  data: {{
    labels: {js_labels},
    datasets: [
      {{
        label: 'Net Worth',
        data: {js_nw},
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59,130,246,0.12)',
        borderWidth: 2.5,
        fill: true,
        tension: 0.35,
        pointRadius: 4,
        pointHoverRadius: 6,
        pointBackgroundColor: '#3b82f6'
      }},
      {{
        label: 'Assets',
        data: {js_assets},
        borderColor: '#4ade80',
        borderWidth: 1.5,
        borderDash: [6,4],
        fill: false,
        tension: 0.35,
        pointRadius: 2,
        pointHoverRadius: 5,
        pointBackgroundColor: '#4ade80'
      }},
      {{
        label: 'Liabilities',
        data: {js_liabs},
        borderColor: '#f87171',
        borderWidth: 1.5,
        borderDash: [6,4],
        fill: false,
        tension: 0.35,
        pointRadius: 2,
        pointHoverRadius: 5,
        pointBackgroundColor: '#f87171'
      }}
    ]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{ labels: {{ color: '#aaa', font: {{ size: 12 }}, boxWidth: 16 }} }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.parsed.y.toLocaleString(undefined, {{maximumFractionDigits:0}})}} {currency}`
        }}
      }}
    }},
    scales: {{
      x: {{ ticks: {{ color: '#666', maxRotation: 45 }}, grid: {{ color: '#1a2540' }} }},
      y: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#1a2540' }} }}
    }}
  }}
}});
</script>"""

    return _html(body)


# ── debt_payoff_chart ─────────────────────────────────────────────────────────

def debt_payoff_chart(avalanche: list, snowball: list, currency: str = "EUR") -> str:
    """
    Line chart: remaining debt for Avalanche vs Snowball strategies.
    Shaded area between lines. Summary stats in legend.
    """
    if not avalanche and not snowball:
        return _html('<div class="card"><div class="no-data">No debt payoff data available.</div></div>')

    def _last(series: list) -> dict:
        return max(series, key=lambda p: p.get("month", 0)) if series else {}

    av_last = _last(avalanche)
    sb_last = _last(snowball)
    av_months = av_last.get("month", 0)
    sb_months = sb_last.get("month", 0)
    av_interest = sum(p.get("interest_paid", 0) for p in avalanche)
    sb_interest = sum(p.get("interest_paid", 0) for p in snowball)

    all_months = sorted(set(p.get("month", 0) for p in avalanche + snowball))
    av_map = {p["month"]: p.get("remaining", 0) for p in avalanche}
    sb_map = {p["month"]: p.get("remaining", 0) for p in snowball}
    av_pts = [av_map.get(m, None) for m in all_months]
    sb_pts = [sb_map.get(m, None) for m in all_months]

    js_months = json.dumps(all_months)
    js_av = json.dumps(av_pts)
    js_sb = json.dumps(sb_pts)
    interest_saved = abs(sb_interest - av_interest)

    body = f"""
<div class="card">
  <div class="title">Debt Payoff Comparison</div>
  <div class="subtitle">Avalanche vs Snowball strategy</div>
  <div class="stat-row">
    <div class="stat">
      <div class="stat-label">Avalanche payoff</div>
      <div class="stat-value" style="color:#3b82f6">{av_months}m</div>
    </div>
    <div class="stat">
      <div class="stat-label">Snowball payoff</div>
      <div class="stat-value" style="color:#f59e0b">{sb_months}m</div>
    </div>
    <div class="stat">
      <div class="stat-label">Avalanche interest</div>
      <div class="stat-value">{_fmt(av_interest, currency)}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Snowball interest</div>
      <div class="stat-value">{_fmt(sb_interest, currency)}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Interest saved (Avalanche)</div>
      <div class="stat-value" style="color:#4ade80">{_fmt(interest_saved, currency)}</div>
    </div>
  </div>
  <div class="chart-wrap" style="height:300px;margin-top:20px"><canvas id="debt-chart"></canvas></div>
</div>
<script>
new Chart(document.getElementById('debt-chart'), {{
  type: 'line',
  data: {{
    labels: {js_months},
    datasets: [
      {{
        label: 'Avalanche',
        data: {js_av},
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59,130,246,0.08)',
        borderWidth: 2.5,
        fill: '+1',
        tension: 0.3,
        pointRadius: 0,
        pointHoverRadius: 5
      }},
      {{
        label: 'Snowball',
        data: {js_sb},
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245,158,11,0.08)',
        borderWidth: 2.5,
        fill: false,
        tension: 0.3,
        pointRadius: 0,
        pointHoverRadius: 5
      }}
    ]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{ labels: {{ color: '#aaa', font: {{ size: 12 }} }} }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.parsed.y !== null ? ctx.parsed.y.toLocaleString(undefined,{{maximumFractionDigits:0}}) + ' {currency}' : '—'}}`
        }}
      }}
    }},
    scales: {{
      x: {{
        title: {{ display: true, text: 'Month', color: '#666' }},
        ticks: {{ color: '#666' }}, grid: {{ color: '#1a2540' }}
      }},
      y: {{
        title: {{ display: true, text: 'Remaining Debt ({currency})', color: '#666' }},
        ticks: {{ color: '#666' }}, grid: {{ color: '#1a2540' }}
      }}
    }}
  }}
}});
</script>"""

    return _html(body)


# ── fire_progress_chart ───────────────────────────────────────────────────────

def fire_progress_chart(current: float, target: float, contributions: list,
                         currency: str = "EUR") -> str:
    """
    Gauge (semi-circle) showing FIRE % + line chart projecting portfolio to target.
    contributions = [{"year": int, "projected_value": float}, ...]
    """
    if target <= 0:
        return _html('<div class="card"><div class="no-data">Invalid FIRE target.</div></div>')

    pct = min(current / target * 100, 100.0)
    gauge_color = _pct_color(pct)

    fire_year = None
    if contributions:
        for c in sorted(contributions, key=lambda x: x.get("year", 0)):
            if c.get("projected_value", 0) >= target:
                fire_year = c.get("year")
                break

    years_label = f"FIRE in {fire_year}" if fire_year else "Keep contributing"

    # Projection chart data
    proj_labels = [str(c.get("year", "")) for c in sorted(contributions, key=lambda x: x.get("year", 0))]
    proj_vals = [round(c.get("projected_value", 0), 2) for c in sorted(contributions, key=lambda x: x.get("year", 0))]
    target_line = [round(target, 2)] * len(proj_labels)

    js_labels = json.dumps(proj_labels)
    js_vals = json.dumps(proj_vals)
    js_target = json.dumps(target_line)

    # Gauge uses a doughnut with half rendered
    gauge_remaining = 100 - pct
    js_gauge = json.dumps([round(pct, 2), round(gauge_remaining, 2)])

    body = f"""
<div class="card">
  <div class="title">FIRE Progress</div>
  <div class="subtitle">{years_label}</div>
  <div class="row" style="align-items:flex-start">
    <div class="col" style="max-width:280px;text-align:center">
      <div style="position:relative;height:160px">
        <canvas id="gauge-chart"></canvas>
        <div style="position:absolute;bottom:8px;left:50%;transform:translateX(-50%);text-align:center">
          <div style="font-size:28px;font-weight:800;color:{gauge_color}">{pct:.0f}%</div>
          <div style="font-size:11px;color:#666">of FIRE target</div>
        </div>
      </div>
      <div class="stat-row" style="margin-top:8px">
        <div class="stat" style="text-align:center">
          <div class="stat-label">Current</div>
          <div class="stat-value" style="font-size:16px">{_fmt(current, currency)}</div>
        </div>
        <div class="stat" style="text-align:center">
          <div class="stat-label">Target</div>
          <div class="stat-value" style="font-size:16px;color:#888">{_fmt(target, currency)}</div>
        </div>
      </div>
    </div>
    <div class="col">
      <div style="font-size:13px;font-weight:600;color:#aaa;margin-bottom:8px">Projected Growth</div>
      <div class="chart-wrap" style="height:220px"><canvas id="proj-chart"></canvas></div>
    </div>
  </div>
</div>
<script>
new Chart(document.getElementById('gauge-chart'), {{
  type: 'doughnut',
  data: {{
    datasets: [{{
      data: {js_gauge},
      backgroundColor: ['{gauge_color}', '#1a2540'],
      borderWidth: 0,
      circumference: 180,
      rotation: -90
    }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    cutout: '75%',
    plugins: {{ legend: {{ display: false }}, tooltip: {{ enabled: false }} }}
  }}
}});
new Chart(document.getElementById('proj-chart'), {{
  type: 'line',
  data: {{
    labels: {js_labels},
    datasets: [
      {{
        label: 'Projected Portfolio',
        data: {js_vals},
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59,130,246,0.1)',
        borderWidth: 2.5,
        fill: true,
        tension: 0.35,
        pointRadius: 3
      }},
      {{
        label: 'FIRE Target',
        data: {js_target},
        borderColor: '#4ade80',
        borderWidth: 1.5,
        borderDash: [8,4],
        fill: false,
        pointRadius: 0,
        pointHoverRadius: 0
      }}
    ]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{ labels: {{ color: '#aaa', font: {{ size: 11 }}, boxWidth: 14 }} }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.parsed.y.toLocaleString(undefined,{{maximumFractionDigits:0}})}} {currency}`
        }}
      }}
    }},
    scales: {{
      x: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#1a2540' }} }},
      y: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#1a2540' }} }}
    }}
  }}
}});
</script>"""

    return _html(body)


# ── spending_trends_chart ─────────────────────────────────────────────────────

def spending_trends_chart(months: list, currency: str = "EUR") -> str:
    """
    Stacked bar chart: monthly spending by category.
    Line overlay: total spending trend.
    months = [{"month": "2025-01", "categories": {"Food": 320, ...}}, ...]
    """
    if not months:
        return _html('<div class="card"><div class="no-data">No spending trend data available.</div></div>')

    sorted_months = sorted(months, key=lambda m: m.get("month", ""))
    month_labels = [m.get("month", "") for m in sorted_months]

    # Collect all categories
    all_cats: set[str] = set()
    for m in sorted_months:
        all_cats.update(m.get("categories", {}).keys())
    all_cats_list = sorted(all_cats)

    cat_palette = [
        "#3b82f6","#06b6d4","#8b5cf6","#f59e0b","#10b981","#ef4444",
        "#ec4899","#84cc16","#f97316","#a78bfa","#34d399","#60a5fa"
    ]
    cat_colors = {c: cat_palette[i % len(cat_palette)] for i, c in enumerate(all_cats_list)}

    datasets = []
    for cat in all_cats_list:
        data = [round(m.get("categories", {}).get(cat, 0), 2) for m in sorted_months]
        datasets.append({
            "type": "bar",
            "label": cat,
            "data": data,
            "backgroundColor": cat_colors[cat],
            "stack": "spending",
            "borderRadius": 3,
            "borderSkipped": False
        })

    # Total line
    totals = [round(sum(m.get("categories", {}).values()), 2) for m in sorted_months]
    datasets.append({
        "type": "line",
        "label": "Total",
        "data": totals,
        "borderColor": "#fff",
        "backgroundColor": "transparent",
        "borderWidth": 2,
        "pointRadius": 4,
        "pointBackgroundColor": "#fff",
        "yAxisID": "y",
        "order": 0,
        "tension": 0.3,
        "stack": None
    })

    js_labels = json.dumps(month_labels)
    js_datasets = json.dumps(datasets)

    body = f"""
<div class="card">
  <div class="title">Spending Trends</div>
  <div class="subtitle">Monthly breakdown by category</div>
  <div class="chart-wrap" style="height:320px"><canvas id="trend-chart"></canvas></div>
</div>
<script>
new Chart(document.getElementById('trend-chart'), {{
  data: {{
    labels: {js_labels},
    datasets: {js_datasets}
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{ labels: {{ color: '#aaa', font: {{ size: 11 }}, boxWidth: 12 }}, position: 'bottom' }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.parsed.y.toLocaleString(undefined,{{maximumFractionDigits:0}})}} {currency}`
        }}
      }}
    }},
    scales: {{
      x: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#1a2540' }}, stacked: true }},
      y: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#1a2540' }}, stacked: true }}
    }}
  }}
}});
</script>"""

    return _html(body)


# ── monthly_comparison_chart ──────────────────────────────────────────────────

def monthly_comparison_chart(current: dict, previous: dict, currency: str = "EUR") -> str:
    """
    Grouped bar chart: current month (blue) vs previous (grey) per category.
    Delta labels above each pair.
    """
    all_cats = sorted(set(list(current.keys()) + list(previous.keys())))
    if not all_cats:
        return _html('<div class="card"><div class="no-data">No comparison data available.</div></div>')

    cur_vals = [round(current.get(c, 0), 2) for c in all_cats]
    prev_vals = [round(previous.get(c, 0), 2) for c in all_cats]
    deltas = [round(current.get(c, 0) - previous.get(c, 0), 2) for c in all_cats]

    total_cur = sum(current.values())
    total_prev = sum(previous.values())
    total_delta = total_cur - total_prev
    delta_color = "#f87171" if total_delta > 0 else "#4ade80"
    sign = "+" if total_delta >= 0 else ""

    js_labels = json.dumps(all_cats)
    js_cur = json.dumps(cur_vals)
    js_prev = json.dumps(prev_vals)
    js_deltas = json.dumps(deltas)
    js_currency = json.dumps(currency)

    body = f"""
<div class="card">
  <div class="title">Month-over-Month Comparison</div>
  <div class="subtitle">Current vs previous month</div>
  <div class="stat-row">
    <div class="stat">
      <div class="stat-label">This Month</div>
      <div class="stat-value">{_fmt(total_cur, currency)}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Last Month</div>
      <div class="stat-value" style="color:#888">{_fmt(total_prev, currency)}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Change</div>
      <div class="stat-value" style="color:{delta_color}">{sign}{_fmt(total_delta, currency)}</div>
    </div>
  </div>
  <div class="chart-wrap" style="height:300px;margin-top:20px"><canvas id="cmp-chart"></canvas></div>
</div>
<script>
(function() {{
  const deltas = {js_deltas};
  const currency = {js_currency};
  const deltaPlugin = {{
    id: 'deltaLabels',
    afterDatasetsDraw(chart) {{
      const ctx = chart.ctx;
      const meta0 = chart.getDatasetMeta(0);
      const meta1 = chart.getDatasetMeta(1);
      ctx.save();
      ctx.font = 'bold 10px sans-serif';
      ctx.textAlign = 'center';
      meta0.data.forEach((bar, i) => {{
        const d = deltas[i];
        const sign = d >= 0 ? '+' : '';
        const color = d > 0 ? '#f87171' : '#4ade80';
        ctx.fillStyle = color;
        const x = (bar.x + meta1.data[i].x) / 2;
        const y = Math.min(bar.y, meta1.data[i].y) - 6;
        ctx.fillText(sign + Math.round(d), x, y);
      }});
      ctx.restore();
    }}
  }};
  new Chart(document.getElementById('cmp-chart'), {{
    type: 'bar',
    plugins: [deltaPlugin],
    data: {{
      labels: {js_labels},
      datasets: [
        {{
          label: 'This Month',
          data: {js_cur},
          backgroundColor: '#3b82f6',
          borderRadius: 4,
          borderSkipped: false
        }},
        {{
          label: 'Last Month',
          data: {js_prev},
          backgroundColor: '#374151',
          borderRadius: 4,
          borderSkipped: false
        }}
      ]
    }},
    options: {{
      responsive: true, maintainAspectRatio: false,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{ labels: {{ color: '#aaa', font: {{ size: 12 }}, boxWidth: 14 }} }},
        tooltip: {{
          callbacks: {{
            label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.parsed.y.toLocaleString(undefined,{{maximumFractionDigits:0}})}} ${{currency}}`
          }}
        }}
      }},
      scales: {{
        x: {{ ticks: {{ color: '#aaa' }}, grid: {{ color: '#1a2540' }} }},
        y: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#1a2540' }} }}
      }}
    }}
  }});
}})();
</script>"""

    return _html(body)


# ── cashflow_forecast_chart ───────────────────────────────────────────────────

def cashflow_forecast_chart(forecast: list, currency: str = "EUR") -> str:
    """
    Line chart: projected account balance over 90 days.
    Red dashed: low-balance threshold. Event markers with tooltips.
    forecast = [{"date": "YYYY-MM-DD", "balance": float, "events": [...]}]
    """
    if not forecast:
        return _html('<div class="card"><div class="no-data">No cash flow forecast data available.</div></div>')

    sorted_fc = sorted(forecast, key=lambda x: x.get("date", ""))
    labels = [x.get("date", "") for x in sorted_fc]
    balances = [round(x.get("balance", 0), 2) for x in sorted_fc]

    min_balance = min(balances) if balances else 0
    max_balance = max(balances) if balances else 0
    low_threshold = max(0, min_balance * 0.2) if min_balance > 0 else max(0, max_balance * 0.1)

    # Point colors: red if below threshold
    point_colors = ["#f87171" if b <= low_threshold else "#3b82f6" for b in balances]

    # Build event annotations
    event_notes = {}
    for entry in sorted_fc:
        evs = entry.get("events", [])
        if evs:
            event_notes[entry.get("date", "")] = evs

    # Build annotation plugins config
    annotations_js = []
    for date_str, evs in event_notes.items():
        if date_str in labels:
            idx = labels.index(date_str)
            label_text = ", ".join(str(e) if isinstance(e, str) else e.get("name", "Event") for e in evs[:2])
            annotations_js.append(f"""
        'event_{idx}': {{
          type: 'point',
          xValue: {idx},
          yValue: {balances[idx]},
          backgroundColor: '#f59e0b',
          radius: 6,
          borderColor: '#fff',
          borderWidth: 1.5
        }}""")

    annotations_js.append(f"""
        'lowThreshold': {{
          type: 'line',
          yMin: {round(low_threshold, 2)},
          yMax: {round(low_threshold, 2)},
          borderColor: '#f87171',
          borderWidth: 1.5,
          borderDash: [6, 4],
          label: {{
            display: true,
            content: 'Low balance threshold',
            color: '#f87171',
            font: {{ size: 10 }},
            position: 'start'
          }}
        }}""")

    annotations_block = "{" + ",".join(annotations_js) + "}"

    js_labels = json.dumps(labels)
    js_balances = json.dumps(balances)
    js_point_colors = json.dumps(point_colors)

    first_bal = balances[0] if balances else 0
    last_bal = balances[-1] if balances else 0
    delta = last_bal - first_bal
    sign = "+" if delta >= 0 else ""
    delta_color = "#4ade80" if delta >= 0 else "#f87171"

    body = f"""
<div class="card">
  <div class="title">Cash Flow Forecast</div>
  <div class="subtitle">Next {len(forecast)} days</div>
  <div class="stat-row">
    <div class="stat">
      <div class="stat-label">Opening Balance</div>
      <div class="stat-value">{_fmt(first_bal, currency)}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Projected Closing</div>
      <div class="stat-value">{_fmt(last_bal, currency)}</div>
    </div>
    <div class="stat">
      <div class="stat-label">Net Change</div>
      <div class="stat-value" style="color:{delta_color}">{sign}{_fmt(delta, currency)}</div>
    </div>
  </div>
  <div class="chart-wrap" style="height:300px;margin-top:20px"><canvas id="cf-chart"></canvas></div>
  <div style="margin-top:12px;font-size:11px;color:#666">
    <span style="color:#f59e0b">● Scheduled events</span>
    &nbsp;&nbsp;
    <span style="color:#f87171">─ ─ Low balance threshold</span>
  </div>
</div>
<script>
new Chart(document.getElementById('cf-chart'), {{
  type: 'line',
  data: {{
    labels: {js_labels},
    datasets: [{{
      label: 'Balance',
      data: {js_balances},
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59,130,246,0.08)',
      fill: true,
      borderWidth: 2,
      tension: 0.3,
      pointRadius: 3,
      pointBackgroundColor: {js_point_colors},
      pointHoverRadius: 6
    }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{
        callbacks: {{
          label: ctx => ` Balance: ${{ctx.parsed.y.toLocaleString(undefined,{{maximumFractionDigits:0}})}} {currency}`
        }}
      }},
      annotation: {{
        annotations: {annotations_block}
      }}
    }},
    scales: {{
      x: {{ ticks: {{ color: '#666', maxTicksLimit: 12, maxRotation: 45 }}, grid: {{ color: '#1a2540' }} }},
      y: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#1a2540' }} }}
    }}
  }}
}});
</script>"""

    return _html(body)
