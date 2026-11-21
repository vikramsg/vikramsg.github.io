---
title: "Optimization Diagrams (JS Test)"
date: 2026-11-21
---

<div id="diag-gradient" class="opt-diagram"></div>

<div id="diag-constraints" class="opt-diagram"></div>

<div id="diag-ga" class="opt-diagram"></div>

<style>
.opt-diagram {
  margin: 1.5rem 0;
  background: #ffffff;
  border: 1px solid #e5e2da;
  border-radius: 12px;
  padding: 14px;
}
.opt-diagram svg {
  display: block;
  width: 100%;
  height: auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif;
}
</style>
<script>
(function () {
  const NS = "http://www.w3.org/2000/svg";
  function el(tag, attrs, parent) {
    const node = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, v);
    if (parent) parent.appendChild(node);
    return node;
  }

  // 1. Gradient Optimization — Hill Climbing
  const gradHost = document.getElementById("diag-gradient");
  if (gradHost) {
    gradHost.innerHTML = `
      <svg viewBox="0 0 720 330" role="img" aria-label="Gradient optimization hill climbing">
        <defs>
          <linearGradient id="hillFill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.22" />
            <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.02" />
          </linearGradient>
          <marker id="arrowBlue" viewBox="0 0 10 10" refX="7.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
            <path d="M 1 1.5 L 8.5 5 L 1 8.5 z" fill="#1d4ed8" />
          </marker>
          <marker id="arrowAxis" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#94a3b8" />
          </marker>
        </defs>
        <line x1="72" y1="270" x2="670" y2="270" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrowAxis)" />
        <line x1="72" y1="270" x2="72" y2="34" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arrowAxis)" />
        <text x="668" y="294" text-anchor="end" font-size="12.5" fill="#475569" font-weight="500">Parameter (x)</text>
        <text x="26" y="152" text-anchor="middle" font-size="12.5" fill="#475569" font-weight="500" transform="rotate(-90 26 152)">Objective / Score</text>
        <path d="M 88 264 C 145 262, 185 250, 225 224 C 268 196, 305 144, 345 104 C 378 72, 405 64, 430 64 C 455 64, 482 72, 515 104 C 555 144, 592 196, 635 224 L 635 270 L 88 270 Z" fill="url(#hillFill)" />
        <path d="M 88 264 C 145 262, 185 250, 225 224 C 268 196, 305 144, 345 104 C 378 72, 405 64, 430 64 C 455 64, 482 72, 515 104 C 555 144, 592 196, 635 224" fill="none" stroke="#2563eb" stroke-width="3" stroke-linecap="round" />
        <line x1="212" y1="234" x2="292" y2="164" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5 4" />
        <text x="116" y="182" font-size="12" fill="#b45309" font-weight="600">local slope (+\u2207f)</text>
        <line x1="218" y1="184" x2="242" y2="196" stroke="#d97706" stroke-width="1.2" />
        <path d="M 186 244 Q 208 214 244 202" fill="none" stroke="#1d4ed8" stroke-width="2" marker-end="url(#arrowBlue)" />
        <path d="M 259 194 Q 280 156 312 135" fill="none" stroke="#1d4ed8" stroke-width="2" marker-end="url(#arrowBlue)" />
        <path d="M 326 123 Q 345 92 374 82" fill="none" stroke="#1d4ed8" stroke-width="2" marker-end="url(#arrowBlue)" />
        <path d="M 389 75 Q 406 58 421 63" fill="none" stroke="#1d4ed8" stroke-width="2" marker-end="url(#arrowBlue)" />
        <circle cx="180" cy="248" r="6" fill="#ffffff" stroke="#1d4ed8" stroke-width="2.5" />
        <circle cx="252" cy="199" r="6" fill="#ffffff" stroke="#1d4ed8" stroke-width="2.5" />
        <circle cx="319" cy="129" r="6" fill="#ffffff" stroke="#1d4ed8" stroke-width="2.5" />
        <circle cx="382" cy="78" r="6" fill="#ffffff" stroke="#1d4ed8" stroke-width="2.5" />
        <circle cx="430" cy="64" r="12" fill="#16a34a" fill-opacity="0.16" />
        <circle cx="430" cy="64" r="6.5" fill="#16a34a" stroke="#ffffff" stroke-width="2" />
        <text x="176" y="290" text-anchor="middle" font-size="12" fill="#334155" font-weight="600">Start</text>
        <line x1="180" y1="256" x2="180" y2="275" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="2 2" />
        <text x="430" y="38" text-anchor="middle" font-size="12.5" fill="#15803d" font-weight="700">Peak (Optimum)</text>
        <text x="430" y="52" text-anchor="middle" font-size="11" fill="#64748b">slope = 0</text>
      </svg>`;
  }

  // 2. Discrete Constraint Solvers
  const conHost = document.getElementById("diag-constraints");
  if (conHost) {
    conHost.innerHTML = `
      <svg viewBox="0 0 720 370" role="img" aria-label="Discrete constraint solvers feasible region">
        <defs>
          <pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="8" stroke="#cbd5e1" stroke-width="1.5" stroke-opacity="0.55" />
          </pattern>
          <marker id="arrowAxis2" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 2 L 8 5 L 1 8 z" fill="#94a3b8" />
          </marker>
        </defs>
        <rect x="92" y="42" width="408" height="266" rx="4" fill="url(#hatch)" />
        <polygon points="172,298 172,160 292,160 472,298" fill="#dbeafe" fill-opacity="0.88" stroke="#2563eb" stroke-width="2" />
        <line x1="172" y1="44" x2="172" y2="306" stroke="#dc2626" stroke-width="2" stroke-dasharray="6 4" />
        <text x="164" y="102" text-anchor="end" font-size="11.5" fill="#b91c1c" font-weight="600">x\u2081 \u2265 1</text>
        <line x1="94" y1="160" x2="494" y2="160" stroke="#d97706" stroke-width="2" stroke-dasharray="6 4" />
        <text x="492" y="152" text-anchor="end" font-size="11.5" fill="#b45309" font-weight="600">x\u2082 \u2264 3</text>
        <line x1="146" y1="48" x2="494" y2="315" stroke="#7c3aed" stroke-width="2.2" />
        <text x="380" y="196" font-size="11.5" fill="#6d28d9" font-weight="600" transform="rotate(37.5 380 196)">x\u2081 + x\u2082 \u2264 6</text>
        <line x1="92" y1="298" x2="508" y2="298" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrowAxis2)" />
        <line x1="112" y1="316" x2="112" y2="34" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrowAxis2)" />
        <g id="con-points"></g>
        <circle cx="292" cy="160" r="13" fill="#16a34a" fill-opacity="0.2" />
        <circle cx="292" cy="160" r="6.5" fill="#16a34a" stroke="#ffffff" stroke-width="2" />
        <text x="308" y="142" text-anchor="start" font-size="12" fill="#15803d" font-weight="700">Optimal (3, 3)</text>
        <text x="262" y="236" text-anchor="middle" font-size="11.5" fill="#1e40af" font-weight="600" opacity="0.85">Feasible Region</text>
        <g transform="translate(534, 86)">
          <rect x="0" y="0" width="166" height="162" rx="10" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1" />
          <text x="14" y="24" font-size="11.5" fill="#334155" font-weight="700">LEGEND</text>
          <circle cx="22" cy="50" r="5.5" fill="#16a34a" stroke="#ffffff" stroke-width="1.5" />
          <text x="36" y="54" font-size="11.5" fill="#1e293b" font-weight="600">Optimal solution</text>
          <circle cx="22" cy="78" r="5" fill="#2563eb" stroke="#ffffff" stroke-width="1.2" />
          <text x="36" y="82" font-size="11.5" fill="#334155">Legal discrete point</text>
          <circle cx="22" cy="106" r="3.5" fill="#94a3b8" />
          <text x="36" y="110" font-size="11.5" fill="#64748b">Forbidden (pruned)</text>
          <line x1="14" y1="134" x2="30" y2="134" stroke="#7c3aed" stroke-width="2.2" />
          <text x="36" y="138" font-size="11.5" fill="#334155">Hard constraint</text>
        </g>
      </svg>`;
    const pts = conHost.querySelector("#con-points");
    for (let x1 = 0; x1 <= 6; x1++) {
      const cx = 112 + x1 * 60;
      el("text", { x: cx, y: 320, "text-anchor": "middle", "font-size": 11, fill: "#64748b" }, pts).textContent = x1;
      for (let x2 = 0; x2 <= 5; x2++) {
        const cy = 298 - x2 * 46;
        if (x1 === 0) {
          el("text", { x: 84, y: cy + 4, "text-anchor": "end", "font-size": 11, fill: "#64748b" }, pts).textContent = x2;
        }
        if (x1 === 3 && x2 === 3) continue;
        const feasible = x1 >= 1 && x2 <= 3 && x1 + x2 <= 6;
        el("circle", feasible
          ? { cx, cy, r: 5, fill: "#2563eb", stroke: "#ffffff", "stroke-width": 1.4 }
          : { cx, cy, r: 3.5, fill: "#94a3b8", "fill-opacity": 0.65 }, pts);
      }
    }
    el("text", { x: 504, y: 320, "text-anchor": "middle", "font-size": 11, "font-weight": 600, fill: "#334155" }, pts).textContent = "x\u2081";
    el("text", { x: 84, y: 42, "text-anchor": "end", "font-size": 11, "font-weight": 600, fill: "#334155" }, pts).textContent = "x\u2082";
  }

  // 3. Genetic Algorithms — 2D Colored Box + Detached X & Y Ranges
  const gaHost = document.getElementById("diag-ga");
  if (gaHost) {
    gaHost.innerHTML = `
      <svg viewBox="0 0 720 400" role="img" aria-label="Genetic algorithm 2D colored design space">
        <defs>
          <marker id="hopArrow1" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
            <path d="M 1 1.5 L 8 5 L 1 8.5 z" fill="#ffffff" />
          </marker>
          <marker id="hopArrowDark" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto">
            <path d="M 1 1.5 L 8 5 L 1 8.5 z" fill="#0f172a" />
          </marker>
          <linearGradient id="qtyScale" x1="0" y1="1" x2="0" y2="0">
            <stop offset="0%" stop-color="#1e293b" />
            <stop offset="25%" stop-color="#2563eb" />
            <stop offset="50%" stop-color="#14b8a6" />
            <stop offset="75%" stop-color="#f59e0b" />
            <stop offset="100%" stop-color="#ef4444" />
          </linearGradient>
          <clipPath id="boxClip"><rect x="128" y="42" width="420" height="252" rx="6" /></clipPath>
        </defs>
        <g id="range-y">
          <text x="32" y="168" text-anchor="middle" font-size="12.5" font-weight="700" fill="#334155" transform="rotate(-90 32 168)">Range of Y</text>
          <rect x="64" y="42" width="12" height="252" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.3" />
          <g id="y-ticks" stroke="#94a3b8" stroke-width="1.2"></g>
          <text x="70" y="34" text-anchor="middle" font-size="10.5" fill="#64748b" font-weight="600">y<tspan dy="2" font-size="8.5">max</tspan></text>
          <text x="70" y="310" text-anchor="middle" font-size="10.5" fill="#64748b" font-weight="600">y<tspan dy="2" font-size="8.5">min</tspan></text>
          <circle cx="70" cy="204" r="5" fill="#0f172a" stroke="#ffffff" stroke-width="1.8" />
          <circle cx="70" cy="96" r="5" fill="#7c3aed" stroke="#ffffff" stroke-width="1.8" />
        </g>
        <g id="range-x">
          <rect x="128" y="330" width="420" height="12" rx="6" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.3" />
          <g id="x-ticks" stroke="#94a3b8" stroke-width="1.2"></g>
          <text x="128" y="360" text-anchor="start" font-size="10.5" fill="#64748b" font-weight="600">x<tspan dy="2" font-size="8.5">min</tspan></text>
          <text x="338" y="370" text-anchor="middle" font-size="12.5" font-weight="700" fill="#334155">Range of X</text>
          <text x="548" y="360" text-anchor="end" font-size="10.5" fill="#64748b" font-weight="600">x<tspan dy="2" font-size="8.5">max</tspan></text>
          <circle cx="233" cy="336" r="5" fill="#0f172a" stroke="#ffffff" stroke-width="1.8" />
          <circle cx="443" cy="336" r="5" fill="#7c3aed" stroke="#ffffff" stroke-width="1.8" />
        </g>
        <g id="heatmap-cells" clip-path="url(#boxClip)"></g>
        <rect x="128" y="42" width="420" height="252" rx="6" fill="none" stroke="#1e293b" stroke-width="2" />
        <g stroke-dasharray="4 3" fill="none" stroke-width="1.8" opacity="0.92">
          <path d="M 233 194 L 233 140" stroke="#0f172a" marker-end="url(#hopArrowDark)" />
          <path d="M 243 204 L 307 204" stroke="#0f172a" marker-end="url(#hopArrowDark)" />
          <path d="M 443 106 L 443 160" stroke="#ffffff" marker-end="url(#hopArrow1)" />
          <path d="M 433 96 L 369 96" stroke="#ffffff" marker-end="url(#hopArrow1)" />
        </g>
        <circle cx="233" cy="132" r="4" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-dasharray="2 2" />
        <circle cx="317" cy="204" r="4" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-dasharray="2 2" />
        <circle cx="443" cy="168" r="4" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-dasharray="2 2" />
        <circle cx="359" cy="96" r="4" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-dasharray="2 2" />
        <circle cx="233" cy="204" r="10.5" fill="#ffffff" fill-opacity="0.95" />
        <circle cx="233" cy="204" r="7" fill="#0f172a" />
        <circle cx="443" cy="96" r="10.5" fill="#ffffff" fill-opacity="0.95" />
        <circle cx="443" cy="96" r="7" fill="#7c3aed" />
        <g transform="translate(584, 52)">
          <text x="0" y="0" font-size="11.5" fill="#334155" font-weight="700">Quantity</text>
          <rect x="4" y="14" width="18" height="168" rx="4" fill="url(#qtyScale)" stroke="#cbd5e1" stroke-width="1" />
          <text x="30" y="25" font-size="11" fill="#475569" font-weight="600">High</text>
          <text x="30" y="102" font-size="11" fill="#64748b">Mid</text>
          <text x="30" y="180" font-size="11" fill="#475569" font-weight="600">Low</text>
          <line x1="0" y1="200" x2="112" y2="200" stroke="#e2e8f0" stroke-width="1" />
          <circle cx="12" cy="218" r="5" fill="#0f172a" />
          <text x="24" y="222" font-size="11" fill="#334155">Candidate 1</text>
          <circle cx="12" cy="238" r="5" fill="#7c3aed" />
          <text x="24" y="242" font-size="11" fill="#334155">Candidate 2</text>
        </g>
      </svg>`;
    const yTicks = gaHost.querySelector("#y-ticks");
    for (let i = 1; i < 7; i++) el("line", { x1: 65, y1: 42 + i * 36, x2: 75, y2: 42 + i * 36 }, yTicks);
    const xTicks = gaHost.querySelector("#x-ticks");
    for (let i = 1; i < 10; i++) el("line", { x1: 128 + i * 42, y1: 331, x2: 128 + i * 42, y2: 341 }, xTicks);

    const grid = [
      [0.14, 0.22, 0.62, 0.18, 0.12, 0.45, 0.72, 0.88, 0.35, 0.16],
      [0.20, 0.55, 0.30, 0.15, 0.68, 0.28, 0.91, 0.97, 0.64, 0.22],
      [0.08, 0.40, 0.78, 0.48, 0.22, 0.10, 0.34, 0.70, 0.25, 0.50],
      [0.32, 0.15, 0.65, 0.82, 0.30, 0.52, 0.18, 0.42, 0.84, 0.38],
      [0.44, 0.74, 0.86, 0.24, 0.12, 0.66, 0.58, 0.15, 0.60, 0.28],
      [0.18, 0.52, 0.60, 0.16, 0.40, 0.76, 0.22, 0.30, 0.14, 0.72],
      [0.10, 0.26, 0.35, 0.50, 0.28, 0.18, 0.46, 0.62, 0.36, 0.12],
    ];
    const stops = [
      [0.00, [30, 41, 59]],
      [0.25, [37, 99, 235]],
      [0.50, [20, 184, 166]],
      [0.75, [245, 158, 11]],
      [1.00, [239, 68, 68]],
    ];
    function colorFor(v) {
      for (let i = 0; i < stops.length - 1; i++) {
        const [t0, c0] = stops[i], [t1, c1] = stops[i + 1];
        if (v >= t0 && v <= t1) {
          const f = (v - t0) / (t1 - t0);
          return `rgb(${Math.round(c0[0]+f*(c1[0]-c0[0]))},${Math.round(c0[1]+f*(c1[1]-c0[1]))},${Math.round(c0[2]+f*(c1[2]-c0[2]))})`;
        }
      }
      return "rgb(239,68,68)";
    }
    const cells = gaHost.querySelector("#heatmap-cells");
    grid.forEach((row, r) => row.forEach((val, c) => {
      el("rect", {
        x: 128 + c * 42, y: 42 + r * 36, width: 42, height: 36,
        fill: colorFor(val), stroke: "#ffffff", "stroke-opacity": 0.28, "stroke-width": 1
      }, cells);
    }));
  }
})();
</script>
