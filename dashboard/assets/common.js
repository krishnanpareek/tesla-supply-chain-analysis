/* Shared helpers for Tesla Supply Chain Analysis HTML dashboard */
(function (global) {
  const PAGES = [
    { id: "01", href: "page01_executive_overview.html", label: "01 Overview", theme: "overview" },
    { id: "02", href: "page02_production_delivery_performance.html", label: "02 Production", theme: "ops" },
    { id: "03", href: "page03_financial_inventory_health.html", label: "03 Financial", theme: "fin" },
    { id: "04", href: "page04_quality_recall_risk.html", label: "04 Quality", theme: "quality" },
    { id: "05", href: "page05_ev_market_infrastructure.html", label: "05 EV Market", theme: "ev" },
    { id: "06", href: "page06_battery_material_risk.html", label: "06 Materials", theme: "materials" },
  ];

  const THEME_CLASS = {
    overview: "theme-overview",
    ops: "theme-ops",
    fin: "theme-fin",
    quality: "theme-quality",
    ev: "theme-ev",
    materials: "theme-materials",
  };

  function cssVar(name, fallback) {
    const v = getComputedStyle(document.body).getPropertyValue(name).trim();
    return v || fallback;
  }

  function applyTheme(themeKey) {
    Object.values(THEME_CLASS).forEach((c) => document.body.classList.remove(c));
    document.body.classList.add(THEME_CLASS[themeKey] || THEME_CLASS.overview);
  }

  function renderNav(activeId) {
    const nav = document.getElementById("siteNav");
    const page = PAGES.find((p) => p.id === activeId);
    if (page) applyTheme(page.theme);
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

  function normalizeLabel(label) {
    const s = String(label || "reported").toLowerCase();
    if (s.includes("estimat")) return "estimated";
    if (s.includes("calculat")) return "calculated";
    if (s.includes("model")) return "modeled";
    return "reported";
  }

  function metricClass(label) {
    return "metric-" + normalizeLabel(label);
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

  function setupCanvas(canvas) {
    const ctx = canvas.getContext("2d");
    const dpr = window.devicePixelRatio || 1;
    // Prefer CSS box size — never reuse buffer height (already multiplied by dpr).
    const w = Math.max(1, canvas.clientWidth || Number(canvas.getAttribute("width")) || 600);
    const h = Math.max(
      1,
      canvas.clientHeight || Number(canvas.getAttribute("height")) || 220
    );
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    return { ctx, w, h, pad: { l: 52, r: 14, t: 14, b: 36 } };
  }

  function hatchPattern(ctx, color) {
    const c = document.createElement("canvas");
    c.width = 8;
    c.height = 8;
    const g = c.getContext("2d");
    g.strokeStyle = color;
    g.globalAlpha = 0.55;
    g.lineWidth = 1;
    g.beginPath();
    g.moveTo(0, 8);
    g.lineTo(8, 0);
    g.stroke();
    g.beginPath();
    g.moveTo(-2, 2);
    g.lineTo(2, -2);
    g.stroke();
    g.beginPath();
    g.moveTo(6, 10);
    g.lineTo(10, 6);
    g.stroke();
    return ctx.createPattern(c, "repeat");
  }

  function isEstimated(label) {
    return normalizeLabel(label) === "estimated";
  }

  function drawFrame(ctx, pad, plotW, plotH) {
    ctx.strokeStyle = "#2c3642";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pad.l, pad.t);
    ctx.lineTo(pad.l, pad.t + plotH);
    ctx.lineTo(pad.l + plotW, pad.t + plotH);
    ctx.stroke();
  }

  function drawYTicks(ctx, pad, yAt, y0, span, ticks, yFormat) {
    ctx.fillStyle = "#6b7886";
    ctx.font = "10px IBM Plex Mono, monospace";
    for (let t = 0; t <= ticks; t++) {
      const v = y0 + (span * t) / ticks;
      ctx.fillText(yFormat ? yFormat(v) : String(Math.round(v)), 4, yAt(v) + 3);
    }
  }

  function drawXLabels(ctx, labels, xAt, h, n) {
    ctx.fillStyle = "#6b7886";
    ctx.font = "10px IBM Plex Mono, monospace";
    labels.forEach((lab, i) => {
      if (i % Math.ceil(n / 8) !== 0 && i !== n - 1) return;
      ctx.fillText(lab, xAt(i) - 14, h - 10);
    });
  }

  function drawPoint(ctx, x, y, color, estimated, highlight) {
    const r = highlight ? 5.5 : 3.2;
    if (highlight) {
      ctx.beginPath();
      ctx.fillStyle = color;
      ctx.globalAlpha = 0.25;
      ctx.arc(x, y, r + 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
    }
    if (estimated) {
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.setLineDash([3, 2]);
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "rgba(15,20,25,0.85)";
      ctx.beginPath();
      ctx.arc(x, y, r - 1.2, 0, Math.PI * 2);
      ctx.fill();
    } else {
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function bindHover(canvas, n, xAt, onHover) {
    canvas.onmousemove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      let best = 0;
      let bestDist = Infinity;
      for (let i = 0; i < n; i++) {
        const d = Math.abs(mx - xAt(i));
        if (d < bestDist) {
          bestDist = d;
          best = i;
        }
      }
      if (bestDist > 28) {
        hideTip();
        if (canvas._dashHoverIndex !== null) {
          canvas._dashHoverIndex = null;
          if (canvas._dashRedraw) canvas._dashRedraw(null);
        }
        return;
      }
      if (canvas._dashHoverIndex !== best) {
        canvas._dashHoverIndex = best;
        if (canvas._dashRedraw) canvas._dashRedraw(best);
      }
      if (onHover) onHover(best, e.clientX, e.clientY);
    };
    canvas.onmouseleave = () => {
      hideTip();
      canvas._dashHoverIndex = null;
      if (canvas._dashRedraw) canvas._dashRedraw(null);
    };
  }

  function drawLineChart(canvas, series, options) {
    const opts = options || {};
    const paint = (hoverIdx) => {
      const { ctx, w, h, pad } = setupCanvas(canvas);
      const plotW = w - pad.l - pad.r;
      const plotH = h - pad.t - pad.b;
      const labels = opts.labels || [];
      const n = series[0].values.length;
      let min = Infinity;
      let max = -Infinity;
      series.forEach((s) =>
        s.values.forEach((v) => {
          if (v != null && !Number.isNaN(v)) {
            min = Math.min(min, v);
            max = Math.max(max, v);
          }
        })
      );
      if (!Number.isFinite(min)) {
        min = 0;
        max = 1;
      }
      if (min === max) {
        min -= 1;
        max += 1;
      }
      const y0 = opts.zeroBaseline ? Math.min(0, min) : min;
      const span = max - y0 || 1;
      const xAt = (i) => pad.l + (n === 1 ? plotW / 2 : (i / (n - 1)) * plotW);
      const yAt = (v) => pad.t + plotH - ((v - y0) / span) * plotH;

      drawFrame(ctx, pad, plotW, plotH);
      if (y0 < 0 && max > 0) {
        ctx.strokeStyle = "#3a4552";
        ctx.beginPath();
        ctx.moveTo(pad.l, yAt(0));
        ctx.lineTo(pad.l + plotW, yAt(0));
        ctx.stroke();
      }
      drawYTicks(ctx, pad, yAt, y0, span, 4, opts.yFormat);
      drawXLabels(ctx, labels, xAt, h, n);

      if (hoverIdx != null) {
        ctx.strokeStyle = cssVar("--accent-dim", "#3d6fa8");
        ctx.globalAlpha = 0.45;
        ctx.beginPath();
        ctx.moveTo(xAt(hoverIdx), pad.t);
        ctx.lineTo(xAt(hoverIdx), pad.t + plotH);
        ctx.stroke();
        ctx.globalAlpha = 1;
      }

      series.forEach((s) => {
        const est = isEstimated(s.metricLabel || s.label);
        ctx.strokeStyle = s.color;
        ctx.lineWidth = 2;
        ctx.setLineDash(est ? [6, 4] : []);
        ctx.beginPath();
        let started = false;
        s.values.forEach((v, i) => {
          if (v == null || Number.isNaN(v)) {
            started = false;
            return;
          }
          const x = xAt(i);
          const y = yAt(v);
          if (!started) {
            ctx.moveTo(x, y);
            started = true;
          } else ctx.lineTo(x, y);
        });
        ctx.stroke();
        ctx.setLineDash([]);
        s.values.forEach((v, i) => {
          if (v == null || Number.isNaN(v)) return;
          drawPoint(ctx, xAt(i), yAt(v), s.color, est, hoverIdx === i);
        });
      });

      canvas._dashXAt = xAt;
      canvas._dashN = n;
    };

    canvas._dashRedraw = paint;
    paint(null);
    bindHover(canvas, series[0].values.length, (i) => canvas._dashXAt(i), opts.onHover);
  }

  /** Dual-line chart with shaded gap between produced and delivered. */
  function drawDualLineGap(canvas, produced, delivered, options) {
    const opts = options || {};
    const paint = (hoverIdx) => {
      const { ctx, w, h, pad } = setupCanvas(canvas);
      const plotW = w - pad.l - pad.r;
      const plotH = h - pad.t - pad.b;
      const labels = opts.labels || [];
      const n = produced.length;
      const all = produced.concat(delivered).filter((v) => v != null);
      let min = Math.min(...all);
      let max = Math.max(...all);
      if (min === max) {
        min -= 1;
        max += 1;
      }
      const span = max - min || 1;
      const xAt = (i) => pad.l + (n === 1 ? plotW / 2 : (i / (n - 1)) * plotW);
      const yAt = (v) => pad.t + plotH - ((v - min) / span) * plotH;
      const prodColor = opts.prodColor || cssVar("--prod", "#6aa8ff");
      const delivColor = opts.delivColor || cssVar("--deliv", "#a8cfff");
      const prodEst = isEstimated(opts.prodLabel || "reported");
      const delivEst = isEstimated(opts.delivLabel || "reported");

      drawFrame(ctx, pad, plotW, plotH);
      drawYTicks(ctx, pad, yAt, min, span, 4, opts.yFormat);
      drawXLabels(ctx, labels, xAt, h, n);

      // Shaded gap band
      ctx.beginPath();
      let started = false;
      for (let i = 0; i < n; i++) {
        if (produced[i] == null) continue;
        const x = xAt(i);
        const y = yAt(produced[i]);
        if (!started) {
          ctx.moveTo(x, y);
          started = true;
        } else ctx.lineTo(x, y);
      }
      for (let i = n - 1; i >= 0; i--) {
        if (delivered[i] == null) continue;
        ctx.lineTo(xAt(i), yAt(delivered[i]));
      }
      ctx.closePath();
      ctx.fillStyle = cssVar("--accent-soft", "rgba(106,168,255,0.12)");
      ctx.fill();

      if (hoverIdx != null) {
        ctx.strokeStyle = cssVar("--accent", "#6aa8ff");
        ctx.globalAlpha = 0.35;
        ctx.beginPath();
        ctx.moveTo(xAt(hoverIdx), pad.t);
        ctx.lineTo(xAt(hoverIdx), pad.t + plotH);
        ctx.stroke();
        ctx.globalAlpha = 1;
        if (produced[hoverIdx] != null && delivered[hoverIdx] != null) {
          const y1 = yAt(produced[hoverIdx]);
          const y2 = yAt(delivered[hoverIdx]);
          ctx.fillStyle = cssVar("--accent-glow", "rgba(106,168,255,0.3)");
          ctx.globalAlpha = 0.35;
          ctx.fillRect(xAt(hoverIdx) - 6, Math.min(y1, y2), 12, Math.abs(y2 - y1));
          ctx.globalAlpha = 1;
        }
      }

      function strokeSeries(values, color, estimated) {
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.25;
        ctx.setLineDash(estimated ? [6, 4] : []);
        ctx.beginPath();
        let on = false;
        values.forEach((v, i) => {
          if (v == null) {
            on = false;
            return;
          }
          const x = xAt(i);
          const y = yAt(v);
          if (!on) {
            ctx.moveTo(x, y);
            on = true;
          } else ctx.lineTo(x, y);
        });
        ctx.stroke();
        ctx.setLineDash([]);
        values.forEach((v, i) => {
          if (v == null) return;
          drawPoint(ctx, xAt(i), yAt(v), color, estimated, hoverIdx === i);
        });
      }

      strokeSeries(produced, prodColor, prodEst);
      strokeSeries(delivered, delivColor, delivEst);

      canvas._dashXAt = xAt;
    };

    canvas._dashRedraw = paint;
    paint(null);
    bindHover(canvas, produced.length, (i) => canvas._dashXAt(i), opts.onHover);
  }

  function drawBarChart(canvas, values, options) {
    const opts = options || {};
    const paint = (hoverIdx) => {
      const { ctx, w, h, pad } = setupCanvas(canvas);
      const plotW = w - pad.l - pad.r;
      const plotH = h - pad.t - pad.b;
      const n = values.length;
      let min = Math.min(0, ...values.filter((v) => v != null));
      let max = Math.max(0, ...values.filter((v) => v != null));
      if (min === max) {
        min -= 1;
        max += 1;
      }
      const span = max - min || 1;
      const yAt = (v) => pad.t + plotH - ((v - min) / span) * plotH;
      const barW = Math.max(4, (plotW / n) * 0.65);
      const labels = opts.metricLabels || values.map(() => opts.metricLabel || "reported");
      const colors = opts.colors || values.map((v) => (v >= 0 ? cssVar("--gap-pos", "#6aa8ff") : cssVar("--gap-neg", "#d4a574")));

      drawFrame(ctx, pad, plotW, plotH);
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
        const bh = Math.max(1, y2 - y);
        const color = colors[i] || cssVar("--accent", "#6aa8ff");
        const est = isEstimated(labels[i]);
        if (est) {
          ctx.fillStyle = hatchPattern(ctx, color);
          ctx.fillRect(x, y, barW, bh);
          ctx.strokeStyle = color;
          ctx.setLineDash([4, 3]);
          ctx.strokeRect(x + 0.5, y + 0.5, barW - 1, bh - 1);
          ctx.setLineDash([]);
        } else {
          ctx.fillStyle = color;
          ctx.globalAlpha = hoverIdx === i ? 1 : 0.88;
          ctx.fillRect(x, y, barW, bh);
          ctx.globalAlpha = 1;
        }
        if (hoverIdx === i) {
          ctx.strokeStyle = color;
          ctx.lineWidth = 1.5;
          ctx.shadowColor = cssVar("--accent-glow", "rgba(106,168,255,0.3)");
          ctx.shadowBlur = 12;
          ctx.strokeRect(x, y, barW, bh);
          ctx.shadowBlur = 0;
        }
      });

      canvas._dashBarIndex = (mx) => {
        if (mx < pad.l || mx > pad.l + plotW) return null;
        return Math.min(n - 1, Math.max(0, Math.floor(((mx - pad.l) / plotW) * n)));
      };
    };

    canvas._dashRedraw = paint;
    paint(null);
    canvas.onmousemove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const i = canvas._dashBarIndex(e.clientX - rect.left);
      if (i == null) {
        hideTip();
        if (canvas._dashHoverIndex != null) {
          canvas._dashHoverIndex = null;
          paint(null);
        }
        return;
      }
      if (canvas._dashHoverIndex !== i) {
        canvas._dashHoverIndex = i;
        paint(i);
      }
      if (opts.onHover) opts.onHover(i, e.clientX, e.clientY);
    };
    canvas.onmouseleave = () => {
      hideTip();
      canvas._dashHoverIndex = null;
      paint(null);
    };
  }

  global.Dash = {
    renderNav,
    applyTheme,
    periodSort,
    fmt,
    fmtPct,
    fmtUSD,
    showTip,
    hideTip,
    citationHtml,
    normalizeLabel,
    metricClass,
    drawLineChart,
    drawBarChart,
    drawDualLineGap,
    hatchPattern,
    cssVar,
  };
})(window);
