/* Shared helpers for Tesla Supply Chain Analysis HTML dashboard */
(function (global) {
  const PAGES = [
    { id: "01", href: "page01_executive_overview.html", label: "01 Overview" },
    { id: "02", href: "page02_production_delivery_performance.html", label: "02 Production" },
    { id: "03", href: "page03_financial_inventory_health.html", label: "03 Financial" },
    { id: "04", href: "page04_quality_recall_risk.html", label: "04 Quality" },
    { id: "05", href: "page05_ev_market_infrastructure.html", label: "05 EV Market" },
    { id: "06", href: "page06_battery_material_risk.html", label: "06 Materials" },
  ];

  function renderNav(activeId) {
    const nav = document.getElementById("siteNav");
    if (!nav) return;
    const links = PAGES.map((p) => {
      const cls = p.id === activeId ? "page active" : "page";
      return `<a class="${cls}" href="${p.href}">${p.label}</a>`;
    }).join("");
    nav.innerHTML = `<div class="inner">
      <a class="brand" href="page01_executive_overview.html">Tesla Supply Chain Analysis</a>
      ${links}
    </div>`;
  }

  function periodSort(id) {
    return Number(id.slice(0, 4)) * 10 + Number(id.slice(-1));
  }

  function fmt(n, digits) {
    if (n === null || n === undefined || Number.isNaN(n)) return "—";
    const d = digits === undefined ? 0 : digits;
    return Number(n).toLocaleString("en-US", {
      minimumFractionDigits: d,
      maximumFractionDigits: d,
    });
  }

  function fmtPct(n, digits) {
    if (n === null || n === undefined || Number.isNaN(n)) return "—";
    const d = digits === undefined ? 1 : digits;
    return (n * 100).toFixed(d) + "%";
  }

  function fmtUSD(n, digits) {
    if (n === null || n === undefined || Number.isNaN(n)) return "—";
    const d = digits === undefined ? 0 : digits;
    return "$" + fmt(n, d) + "M";
  }

  const tipEl = () => document.getElementById("tooltip");

  function showTip(html, x, y) {
    const tip = tipEl();
    if (!tip) return;
    tip.innerHTML = html;
    tip.style.display = "block";
    const pad = 14;
    tip.style.left = Math.min(x + pad, window.innerWidth - 380) + "px";
    tip.style.top = Math.min(y + pad, window.innerHeight - 200) + "px";
  }

  function hideTip() {
    const tip = tipEl();
    if (tip) tip.style.display = "none";
  }

  function citationHtml(opts) {
    const {
      periodId, metricName, metricLabel, valueText,
      reportingPeriod, publicationDate, sourceId, sourceFile, sourceUrl, note,
    } = opts;
    return `<strong>${periodId} · ${metricName} (${metricLabel})</strong>
      Value: ${valueText}<br/>
      Reporting period: ${reportingPeriod || "—"}<br/>
      Published / filed: ${publicationDate || "—"}<br/>
      Source ID: ${sourceId || "—"}<br/>
      <code>${sourceFile || "—"}</code>
      ${sourceUrl ? `<br/><code>${sourceUrl}</code>` : ""}
      ${note ? `<br/><span style="color:#93a1b0">${note}</span>` : ""}`;
  }

  function drawLineChart(canvas, series, options) {
    const opts = options || {};
    const ctx = canvas.getContext("2d");
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth;
    const h = canvas.height;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    const pad = { l: 52, r: 12, t: 12, b: 36 };
    const plotW = w - pad.l - pad.r;
    const plotH = h - pad.t - pad.b;
    const labels = opts.labels || [];
    const n = series[0].values.length;
    let min = Infinity, max = -Infinity;
    series.forEach((s) => s.values.forEach((v) => {
      if (v != null && !Number.isNaN(v)) {
        min = Math.min(min, v);
        max = Math.max(max, v);
      }
    }));
    if (!Number.isFinite(min)) { min = 0; max = 1; }
    if (min === max) { min -= 1; max += 1; }
    const y0 = opts.zeroBaseline ? Math.min(0, min) : min;
    const span = max - y0 || 1;
    const xAt = (i) => pad.l + (n === 1 ? plotW / 2 : (i / (n - 1)) * plotW);
    const yAt = (v) => pad.t + plotH - ((v - y0) / span) * plotH;

    ctx.strokeStyle = "#2c3642";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pad.l, pad.t);
    ctx.lineTo(pad.l, pad.t + plotH);
    ctx.lineTo(pad.l + plotW, pad.t + plotH);
    ctx.stroke();

    if (y0 < 0 && max > 0) {
      ctx.strokeStyle = "#3a4552";
      ctx.beginPath();
      ctx.moveTo(pad.l, yAt(0));
      ctx.lineTo(pad.l + plotW, yAt(0));
      ctx.stroke();
    }

    ctx.fillStyle = "#6b7886";
    ctx.font = "10px IBM Plex Mono, monospace";
    const ticks = 4;
    for (let t = 0; t <= ticks; t++) {
      const v = y0 + (span * t) / ticks;
      const y = yAt(v);
      const label = opts.yFormat ? opts.yFormat(v) : String(Math.round(v));
      ctx.fillText(label, 4, y + 3);
    }
    labels.forEach((lab, i) => {
      if (i % Math.ceil(n / 8) !== 0 && i !== n - 1) return;
      ctx.fillText(lab, xAt(i) - 14, h - 10);
    });

    series.forEach((s) => {
      ctx.strokeStyle = s.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      let started = false;
      s.values.forEach((v, i) => {
        if (v == null || Number.isNaN(v)) { started = false; return; }
        const x = xAt(i), y = yAt(v);
        if (!started) { ctx.moveTo(x, y); started = true; }
        else ctx.lineTo(x, y);
      });
      ctx.stroke();
      s.values.forEach((v, i) => {
        if (v == null || Number.isNaN(v)) return;
        ctx.fillStyle = s.color;
        ctx.beginPath();
        ctx.arc(xAt(i), yAt(v), 3, 0, Math.PI * 2);
        ctx.fill();
      });
    });

    canvas.onmousemove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      let best = 0, bestDist = Infinity;
      for (let i = 0; i < n; i++) {
        const d = Math.abs(mx - xAt(i));
        if (d < bestDist) { bestDist = d; best = i; }
      }
      if (bestDist > 24) { hideTip(); return; }
      if (opts.onHover) opts.onHover(best, e.clientX, e.clientY);
    };
    canvas.onmouseleave = hideTip;
  }

  function drawBarChart(canvas, values, options) {
    const opts = options || {};
    const ctx = canvas.getContext("2d");
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth;
    const h = canvas.height;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    const pad = { l: 52, r: 12, t: 12, b: 36 };
    const plotW = w - pad.l - pad.r;
    const plotH = h - pad.t - pad.b;
    const n = values.length;
    let min = Math.min(0, ...values.filter((v) => v != null));
    let max = Math.max(0, ...values.filter((v) => v != null));
    if (min === max) { min -= 1; max += 1; }
    const span = max - min || 1;
    const yAt = (v) => pad.t + plotH - ((v - min) / span) * plotH;
    const barW = Math.max(4, (plotW / n) * 0.65);
    const colors = opts.colors || values.map((v) => (v >= 0 ? "#6aa8ff" : "#c4923a"));

    ctx.strokeStyle = "#2c3642";
    ctx.beginPath();
    ctx.moveTo(pad.l, pad.t);
    ctx.lineTo(pad.l, pad.t + plotH);
    ctx.lineTo(pad.l + plotW, pad.t + plotH);
    ctx.stroke();
    ctx.strokeStyle = "#3a4552";
    ctx.beginPath();
    ctx.moveTo(pad.l, yAt(0));
    ctx.lineTo(pad.l + plotW, yAt(0));
    ctx.stroke();

    ctx.fillStyle = "#6b7886";
    ctx.font = "10px IBM Plex Mono, monospace";
    (opts.labels || []).forEach((lab, i) => {
      if (i % Math.ceil(n / 8) !== 0 && i !== n - 1) return;
      const x = pad.l + (i + 0.5) * (plotW / n);
      ctx.fillText(lab, x - 14, h - 10);
    });

    values.forEach((v, i) => {
      if (v == null) return;
      const x = pad.l + (i + 0.5) * (plotW / n) - barW / 2;
      const y = yAt(Math.max(v, 0));
      const y2 = yAt(Math.min(v, 0));
      ctx.fillStyle = colors[i] || "#6aa8ff";
      ctx.fillRect(x, y, barW, Math.max(1, y2 - y));
    });

    canvas.onmousemove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const i = Math.min(n - 1, Math.max(0, Math.floor(((mx - pad.l) / plotW) * n)));
      if (mx < pad.l || mx > pad.l + plotW) { hideTip(); return; }
      if (opts.onHover) opts.onHover(i, e.clientX, e.clientY);
    };
    canvas.onmouseleave = hideTip;
  }

  global.Dash = {
    renderNav,
    periodSort,
    fmt,
    fmtPct,
    fmtUSD,
    showTip,
    hideTip,
    citationHtml,
    drawLineChart,
    drawBarChart,
  };
})(window);
