#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将森波拉行程规划 Markdown 转为主题化 HTML"""

import re
from pathlib import Path

import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension

BASE = Path(__file__).parent
MD_FILE = BASE / "森波拉行程规划.md"
HTML_FILE = BASE / "森波拉行程规划.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>森波拉松鼠酒店 · 13人大家庭作战手册</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --forest-dark: #1b4332;
      --forest: #2d6a4f;
      --forest-light: #52b788;
      --leaf: #95d5b2;
      --sky: #4cc9f0;
      --sky-light: #a8e6ff;
      --sun: #ffb703;
      --sun-light: #ffd166;
      --coral: #ff6b6b;
      --cream: #fefae0;
      --cream-dark: #f5ebe0;
      --white: #ffffff;
      --text: #2d3436;
      --text-soft: #5c6b6a;
      --shadow: rgba(27, 67, 50, 0.12);
      --radius: 18px;
      --radius-sm: 12px;
    }

    * { box-sizing: border-box; }

    html { scroll-behavior: smooth; }

    body {
      margin: 0;
      font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
      font-size: 15px;
      line-height: 1.75;
      color: var(--text);
      background:
        radial-gradient(circle at 8% 12%, rgba(149, 213, 178, 0.45) 0%, transparent 42%),
        radial-gradient(circle at 92% 8%, rgba(168, 230, 255, 0.5) 0%, transparent 38%),
        radial-gradient(circle at 50% 100%, rgba(255, 209, 102, 0.25) 0%, transparent 50%),
        linear-gradient(160deg, #e8f5e9 0%, var(--cream) 45%, #e3f2fd 100%);
      min-height: 100vh;
    }

    /* 场景容器：主体 + 两侧动物 */
    .scene {
      position: relative;
      margin: 0 auto;
      max-width: 1180px;
      min-height: 100vh;
    }

    .animal-lane {
      position: absolute;
      top: 0;
      width: 150px;
      height: 100%;
      z-index: 1;
      pointer-events: none;
    }

    .animal-lane-left { left: 0; }
    .animal-lane-right { right: 0; }

    .peek-animal {
      position: absolute;
      width: 96px;
    }

    .peek-animal--wide { width: 112px; }
    .peek-animal--tall { width: 88px; }

    .peek-animal-body {
      display: block;
      line-height: 0;
    }

    .peek-animal-body svg {
      display: block;
      width: 100%;
      height: auto;
      filter: drop-shadow(2px 5px 10px rgba(27, 67, 50, 0.22));
    }

    .peek-animal-left .peek-animal-body { margin-left: -32px; }
    .peek-animal-right .peek-animal-body {
      margin-right: -32px;
      float: right;
    }

    .peek-animal-inner {
      display: block;
      transform-origin: 62% 92%;
    }

    .peek-animal-right .peek-animal-inner {
      transform-origin: 38% 92%;
    }

    .anim-bobble-1 { animation: animal-bobble 2.8s ease-in-out infinite; }
    .anim-bobble-2 { animation: animal-bobble 3.5s ease-in-out infinite 0.45s; }
    .anim-bobble-3 { animation: animal-wiggle 2.4s ease-in-out infinite 0.2s; }
    .anim-bobble-4 { animation: animal-wiggle 3.1s ease-in-out infinite 0.75s; }
    .anim-bobble-5 { animation: animal-bobble 3.8s ease-in-out infinite 1.1s; }
    .anim-bobble-6 { animation: animal-wiggle 2.6s ease-in-out infinite 0.35s; }

    .anim-flip.anim-bobble-1 { animation: animal-bobble-flip 2.8s ease-in-out infinite; }
    .anim-flip.anim-bobble-2 { animation: animal-bobble-flip 3.5s ease-in-out infinite 0.45s; }
    .anim-flip.anim-bobble-3 { animation: animal-wiggle-flip 2.4s ease-in-out infinite 0.2s; }
    .anim-flip.anim-bobble-4 { animation: animal-wiggle-flip 3.1s ease-in-out infinite 0.75s; }
    .anim-flip.anim-bobble-5 { animation: animal-bobble-flip 3.8s ease-in-out infinite 1.1s; }
    .anim-flip.anim-bobble-6 { animation: animal-wiggle-flip 2.6s ease-in-out infinite 0.35s; }

    @keyframes animal-bobble {
      0%, 100% { transform: rotate(-11deg) translateY(0); }
      25% { transform: rotate(9deg) translateY(-4px); }
      50% { transform: rotate(-7deg) translateY(2px); }
      75% { transform: rotate(10deg) translateY(-3px); }
    }

    @keyframes animal-wiggle {
      0%, 100% { transform: rotate(8deg); }
      33% { transform: rotate(-10deg); }
      66% { transform: rotate(6deg); }
    }

    @keyframes animal-bobble-flip {
      0%, 100% { transform: scaleX(-1) rotate(-11deg) translateY(0); }
      25% { transform: scaleX(-1) rotate(9deg) translateY(-4px); }
      50% { transform: scaleX(-1) rotate(-7deg) translateY(2px); }
      75% { transform: scaleX(-1) rotate(10deg) translateY(-3px); }
    }

    @keyframes animal-wiggle-flip {
      0%, 100% { transform: scaleX(-1) rotate(8deg); }
      33% { transform: scaleX(-1) rotate(-10deg); }
      66% { transform: scaleX(-1) rotate(6deg); }
    }

    @media (max-width: 1080px) {
      .animal-lane { display: none; }
    }

    @media (prefers-reduced-motion: reduce) {
      .peek-animal-inner {
        animation: none !important;
      }
    }

    .page-wrap {
      max-width: 920px;
      margin: 0 auto;
      padding: 28px 20px 48px;
      position: relative;
      z-index: 2;
    }

  /* 顶部横幅 */
    .hero {
      position: relative;
      text-align: center;
      padding: 36px 28px 32px;
      margin-bottom: 28px;
      background: linear-gradient(135deg, var(--forest) 0%, #40916c 55%, var(--forest-light) 100%);
      border-radius: 28px;
      color: var(--white);
      box-shadow: 0 12px 32px var(--shadow);
      overflow: hidden;
    }

    .hero::before,
    .hero::after {
      content: "";
      position: absolute;
      border-radius: 50%;
      opacity: 0.15;
      background: var(--white);
    }

    .hero::before {
      width: 180px;
      height: 180px;
      top: -60px;
      right: -40px;
    }

    .hero::after {
      width: 120px;
      height: 120px;
      bottom: -40px;
      left: -30px;
    }

    .hero-deco {
      font-size: 28px;
      letter-spacing: 8px;
      margin-bottom: 8px;
      opacity: 0.95;
    }

    .hero h1 {
      font-family: "ZCOOL KuaiLe", cursive;
      font-size: 2rem;
      font-weight: 400;
      margin: 0 0 14px;
      line-height: 1.35;
      text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }

    .hero-meta {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      margin-top: 16px;
    }

    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      background: rgba(255, 255, 255, 0.22);
      border: 2px solid rgba(255, 255, 255, 0.35);
      border-radius: 999px;
      font-size: 0.92rem;
      backdrop-filter: blur(4px);
    }

    .hero-badge.birthday {
      background: linear-gradient(90deg, #ff9a9e, #fecfef);
      border-color: rgba(255, 255, 255, 0.6);
      color: #5c2d0e;
      font-weight: 700;
    }

  /* 正文卡片 */
    .content-card {
      background: rgba(255, 255, 255, 0.88);
      border-radius: var(--radius);
      padding: 28px 32px;
      box-shadow: 0 8px 28px var(--shadow);
      border: 3px solid rgba(149, 213, 178, 0.45);
    }

    .content-card > h2:first-child { margin-top: 0; }

    h2 {
      font-family: "ZCOOL KuaiLe", cursive;
      font-size: 1.45rem;
      font-weight: 400;
      color: var(--forest-dark);
      margin: 36px 0 16px;
      padding: 10px 16px;
      background: linear-gradient(90deg, rgba(149, 213, 178, 0.55) 0%, transparent 100%);
      border-left: 5px solid var(--forest-light);
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    }

    h2:first-of-type { margin-top: 8px; }

    h2.day-title {
      background: linear-gradient(90deg, rgba(76, 201, 240, 0.45) 0%, transparent 100%);
      border-left-color: var(--sky);
    }

    h3 {
      font-family: "ZCOOL KuaiLe", cursive;
      font-size: 1.12rem;
      font-weight: 400;
      color: var(--forest);
      margin: 22px 0 10px;
      padding-left: 12px;
      border-left: 4px dotted var(--sun);
    }

    p { margin: 0.6em 0; }

    strong { color: var(--forest-dark); }

    hr {
      border: none;
      height: 3px;
      margin: 32px 0;
      background: repeating-linear-gradient(
        90deg,
        var(--leaf) 0,
        var(--leaf) 12px,
        transparent 12px,
        transparent 20px
      );
      opacity: 0.7;
    }

  /* 引用块 */
    blockquote {
      margin: 16px 0;
      padding: 14px 18px;
      border: none;
      border-radius: var(--radius-sm);
      background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
      border-left: 5px solid var(--sun);
      color: #6b4e16;
      box-shadow: 0 4px 12px rgba(255, 183, 3, 0.15);
    }

    blockquote p { margin: 0; }

    blockquote strong { color: #8b5a00; }

  /* 列表 */
    ul, ol {
      margin: 10px 0;
      padding-left: 0;
      list-style: none;
    }

    ul li, ol li {
      position: relative;
      padding: 6px 0 6px 28px;
      margin-bottom: 4px;
    }

    ul li::before {
      content: "🌿";
      position: absolute;
      left: 0;
      top: 6px;
      font-size: 0.85rem;
    }

    ol {
      counter-reset: tip-counter;
    }

    ol li {
      counter-increment: tip-counter;
      padding-left: 36px;
    }

    ol li::before {
      content: counter(tip-counter);
      position: absolute;
      left: 0;
      top: 8px;
      width: 24px;
      height: 24px;
      line-height: 24px;
      text-align: center;
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--white);
      background: var(--forest-light);
      border-radius: 50%;
    }

    ul li ul li::before { content: "✨"; }

  /* 表格 */
    table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      margin: 16px 0 20px;
      font-size: 0.92rem;
      border-radius: var(--radius-sm);
      overflow: hidden;
      box-shadow: 0 4px 16px var(--shadow);
    }

    thead th {
      background: linear-gradient(180deg, var(--forest) 0%, #40916c 100%);
      color: var(--white);
      font-weight: 600;
      padding: 12px 14px;
      text-align: left;
      border: none;
    }

    tbody td {
      padding: 11px 14px;
      border-bottom: 1px solid rgba(149, 213, 178, 0.35);
      background: var(--white);
      vertical-align: top;
    }

    tbody tr:nth-child(even) td {
      background: rgba(232, 245, 233, 0.55);
    }

    tbody tr:last-child td { border-bottom: none; }

    tbody tr:hover td {
      background: rgba(168, 230, 255, 0.25);
    }

  /* 时间线代码块 */
    pre {
      margin: 16px 0;
      padding: 20px 22px;
      background: linear-gradient(145deg, #1b4332 0%, #2d6a4f 100%);
      color: #d8f3dc;
      border-radius: var(--radius-sm);
      font-family: "Noto Sans SC", monospace;
      font-size: 0.88rem;
      line-height: 1.65;
      white-space: pre-wrap;
      word-break: break-word;
      box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);
      border: 3px solid var(--leaf);
    }

    code {
      font-family: "Noto Sans SC", monospace;
      font-size: 0.9em;
    }

    p > code, td > code, li > code {
      background: rgba(149, 213, 178, 0.35);
      padding: 2px 8px;
      border-radius: 6px;
      color: var(--forest-dark);
    }

  /* 页脚 */
    .footer-note {
      margin-top: 28px;
      text-align: center;
      padding: 20px;
      font-family: "ZCOOL KuaiLe", cursive;
      font-size: 1.05rem;
      color: var(--forest);
      background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(254, 250, 224, 0.95));
      border-radius: var(--radius);
      border: 2px dashed var(--leaf);
    }

  /* 打印 / PDF */
    @media print {
      body {
        background: white;
        font-size: 11pt;
      }

      .scene {
        max-width: none;
      }

      .animal-lane {
        width: 110px;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }

      .peek-animal { width: 78px; }
      .peek-animal--wide { width: 90px; }

      .peek-animal-inner {
        animation: none !important;
      }

      .page-wrap {
        max-width: none;
        padding: 0;
      }

      .hero {
        break-inside: avoid;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }

      .content-card {
        box-shadow: none;
        border: 1px solid #ccc;
        padding: 16px 20px;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }

      h2 {
        break-after: avoid;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }

      table, blockquote, pre {
        break-inside: avoid;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }

      thead th, tbody tr:nth-child(even) td, pre, .hero {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
    }

    @page {
      margin: 14mm 12mm;
      size: A4;
    }
  </style>
</head>
<body>
  <div class="scene">
    <aside class="animal-lane animal-lane-left" aria-hidden="true">
      <!-- 松鼠 -->
      <div class="peek-animal peek-animal-left peek-animal--wide" style="top: 6%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-bobble-1">
            <svg viewBox="0 0 110 130" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M18 78 Q4 58 12 36 Q22 48 28 68 Q14 72 18 78Z" fill="#b33a0a"/>
              <ellipse cx="58" cy="82" rx="30" ry="34" fill="#e67e22"/>
              <ellipse cx="58" cy="88" rx="16" ry="20" fill="#fdebd0"/>
              <circle cx="66" cy="46" r="24" fill="#e67e22"/>
              <ellipse cx="50" cy="30" rx="9" ry="13" fill="#e67e22"/>
              <ellipse cx="78" cy="30" rx="9" ry="13" fill="#e67e22"/>
              <circle cx="58" cy="44" r="5" fill="#1a1a1a"/><circle cx="72" cy="44" r="5" fill="#1a1a1a"/>
              <circle cx="59" cy="43" r="2" fill="#fff"/><circle cx="73" cy="43" r="2" fill="#fff"/>
              <ellipse cx="66" cy="54" rx="4" ry="3" fill="#5c3d2e"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 梅花鹿 -->
      <div class="peek-animal peek-animal-left peek-animal--tall" style="top: 20%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-bobble-3">
            <svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="52" cy="88" rx="22" ry="18" fill="#c9a66b"/>
              <rect x="42" y="70" width="8" height="22" rx="3" fill="#a67c52"/>
              <rect x="58" y="70" width="8" height="22" rx="3" fill="#a67c52"/>
              <ellipse cx="52" cy="58" rx="18" ry="20" fill="#d4a574"/>
              <ellipse cx="52" cy="64" rx="10" ry="12" fill="#f5e6c8"/>
              <path d="M38 42 L32 18 M44 40 L40 14 M56 40 L60 14 M64 42 L70 18" stroke="#8b6914" stroke-width="3" stroke-linecap="round"/>
              <circle cx="46" cy="52" r="4" fill="#1a1a1a"/><circle cx="58" cy="52" r="4" fill="#1a1a1a"/>
              <ellipse cx="52" cy="60" rx="5" ry="3" fill="#8b6914"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 羊驼 -->
      <div class="peek-animal peek-animal-left" style="top: 36%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-bobble-2">
            <svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="48" cy="108" rx="20" ry="14" fill="#e8dcc8"/>
              <rect x="38" y="88" width="7" height="18" rx="2" fill="#d4c4a8"/>
              <rect x="52" y="88" width="7" height="18" rx="2" fill="#d4c4a8"/>
              <ellipse cx="48" cy="72" rx="22" ry="26" fill="#f5f0e6"/>
              <ellipse cx="48" cy="42" rx="16" ry="18" fill="#f5f0e6"/>
              <ellipse cx="48" cy="30" rx="12" ry="14" fill="#f5f0e6"/>
              <circle cx="42" cy="38" r="4" fill="#1a1a1a"/><circle cx="54" cy="38" r="4" fill="#1a1a1a"/>
              <ellipse cx="48" cy="46" rx="4" ry="3" fill="#c9b8a0"/>
              <path d="M30 50 Q20 45 18 55 Q25 58 32 54" fill="#f5f0e6"/>
              <path d="M66 50 Q76 45 78 55 Q71 58 64 54" fill="#f5f0e6"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 土拨鼠 -->
      <div class="peek-animal peek-animal-left" style="top: 54%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-bobble-4">
            <svg viewBox="0 0 100 90" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="50" cy="62" rx="32" ry="26" fill="#8b7355"/>
              <ellipse cx="50" cy="68" rx="18" ry="14" fill="#c9b896"/>
              <circle cx="50" cy="38" r="26" fill="#8b7355"/>
              <circle cx="42" cy="34" r="5" fill="#1a1a1a"/><circle cx="58" cy="34" r="5" fill="#1a1a1a"/>
              <circle cx="43" cy="33" r="2" fill="#fff"/><circle cx="59" cy="33" r="2" fill="#fff"/>
              <ellipse cx="50" cy="44" rx="6" ry="4" fill="#6b5344"/>
              <ellipse cx="28" cy="42" rx="8" ry="6" fill="#8b7355"/>
              <ellipse cx="72" cy="42" rx="8" ry="6" fill="#8b7355"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 狐獴 -->
      <div class="peek-animal peek-animal-left peek-animal--tall" style="top: 70%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-bobble-5">
            <svg viewBox="0 0 90 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="45" cy="98" rx="14" ry="10" fill="#c9a66b"/>
              <rect x="36" y="72" width="7" height="28" rx="2" fill="#a67c52"/>
              <rect x="50" y="72" width="7" height="28" rx="2" fill="#a67c52"/>
              <ellipse cx="45" cy="58" rx="16" ry="22" fill="#d4a574"/>
              <ellipse cx="45" cy="64" rx="9" ry="12" fill="#f5e6c8"/>
              <ellipse cx="45" cy="32" rx="14" ry="16" fill="#d4a574"/>
              <circle cx="39" cy="30" r="4" fill="#1a1a1a"/><circle cx="51" cy="30" r="4" fill="#1a1a1a"/>
              <ellipse cx="45" cy="38" rx="4" ry="3" fill="#8b6914"/>
              <path d="M32 22 L28 8 M52 22 L56 8" stroke="#d4a574" stroke-width="3" stroke-linecap="round"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 松鼠（小） -->
      <div class="peek-animal peek-animal-left" style="top: 86%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-bobble-6">
            <svg viewBox="0 0 90 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M14 62 Q4 48 10 32 Q18 42 22 56Z" fill="#b33a0a"/>
              <ellipse cx="48" cy="68" rx="24" ry="26" fill="#e67e22"/>
              <circle cx="54" cy="38" r="18" fill="#e67e22"/>
              <circle cx="48" cy="36" r="4" fill="#1a1a1a"/><circle cx="60" cy="36" r="4" fill="#1a1a1a"/>
              <ellipse cx="54" cy="44" rx="3" ry="2" fill="#5c3d2e"/>
            </svg>
          </span>
        </div>
      </div>
    </aside>

    <div class="page-wrap">
      <header class="hero">
        <div class="hero-deco">🌲 🐿️ 🦕 🌊 🛝</div>
        <h1>森波拉松鼠酒店<br>13人大家庭 2天1夜作战手册</h1>
        <div class="hero-meta">
          <span class="hero-badge birthday">🎂 Excel 小朋友生日特别版</span>
          <span class="hero-badge">📅 2026年6月26日 出发</span>
          <span class="hero-badge">📍 清远佛冈森波拉度假森林</span>
        </div>
      </header>

      <main class="content-card">
{body}
      </main>

      <div class="footer-note">
        🏁 祝 Excel 小朋友生日快乐！恐龙、水花、滑梯，全是快乐回忆！🦕🌊🛝
      </div>
    </div>

    <aside class="animal-lane animal-lane-right" aria-hidden="true">
      <!-- 恐龙 -->
      <div class="peek-animal peek-animal-right peek-animal--wide" style="top: 5%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-flip anim-bobble-1">
            <svg viewBox="0 0 120 130" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="58" cy="95" rx="28" ry="22" fill="#52b788"/>
              <ellipse cx="58" cy="100" rx="14" ry="10" fill="#95d5b2"/>
              <path d="M30 88 L18 95 L22 82 Z" fill="#40916c"/>
              <ellipse cx="62" cy="58" rx="30" ry="32" fill="#52b788"/>
              <ellipse cx="88" cy="48" rx="22" ry="20" fill="#52b788"/>
              <circle cx="78" cy="42" r="6" fill="#1a1a1a"/><circle cx="94" cy="42" r="6" fill="#1a1a1a"/>
              <circle cx="79" cy="41" r="2" fill="#fff"/><circle cx="95" cy="41" r="2" fill="#fff"/>
              <path d="M108 52 L118 58 L108 62 Z" fill="#40916c"/>
              <path d="M42 30 L38 12 L48 22 Z" fill="#40916c"/>
              <path d="M52 28 L50 10 L58 20 Z" fill="#40916c"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 梅花鹿 -->
      <div class="peek-animal peek-animal-right peek-animal--tall" style="top: 19%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-flip anim-bobble-3">
            <svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="48" cy="88" rx="22" ry="18" fill="#c9a66b"/>
              <rect x="38" y="70" width="8" height="22" rx="3" fill="#a67c52"/>
              <rect x="58" y="70" width="8" height="22" rx="3" fill="#a67c52"/>
              <ellipse cx="48" cy="58" rx="18" ry="20" fill="#d4a574"/>
              <path d="M34 42 L28 18 M42 40 L36 14 M54 40 L58 14 M62 42 L68 18" stroke="#8b6914" stroke-width="3" stroke-linecap="round"/>
              <circle cx="42" cy="52" r="4" fill="#1a1a1a"/><circle cx="54" cy="52" r="4" fill="#1a1a1a"/>
              <ellipse cx="48" cy="60" rx="5" ry="3" fill="#8b6914"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 狐獴 -->
      <div class="peek-animal peek-animal-right" style="top: 35%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-flip anim-bobble-2">
            <svg viewBox="0 0 90 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="45" cy="98" rx="14" ry="10" fill="#c9a66b"/>
              <rect x="36" y="72" width="7" height="28" rx="2" fill="#a67c52"/>
              <rect x="50" y="72" width="7" height="28" rx="2" fill="#a67c52"/>
              <ellipse cx="45" cy="58" rx="16" ry="22" fill="#d4a574"/>
              <ellipse cx="45" cy="32" rx="14" ry="16" fill="#d4a574"/>
              <circle cx="39" cy="30" r="4" fill="#1a1a1a"/><circle cx="51" cy="30" r="4" fill="#1a1a1a"/>
              <path d="M32 22 L28 8 M52 22 L56 8" stroke="#d4a574" stroke-width="3" stroke-linecap="round"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 恐龙（小） -->
      <div class="peek-animal peek-animal-right" style="top: 52%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-flip anim-bobble-4">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="50" cy="72" rx="24" ry="18" fill="#40916c"/>
              <ellipse cx="52" cy="44" rx="22" ry="24" fill="#52b788"/>
              <ellipse cx="72" cy="36" rx="16" ry="14" fill="#52b788"/>
              <circle cx="66" cy="32" r="5" fill="#1a1a1a"/><circle cx="78" cy="32" r="5" fill="#1a1a1a"/>
              <path d="M86 40 L96 44 L86 48 Z" fill="#2d6a4f"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 羊驼 -->
      <div class="peek-animal peek-animal-right peek-animal--tall" style="top: 68%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-flip anim-bobble-5">
            <svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="52" cy="108" rx="20" ry="14" fill="#e8dcc8"/>
              <rect x="42" y="88" width="7" height="18" rx="2" fill="#d4c4a8"/>
              <rect x="56" y="88" width="7" height="18" rx="2" fill="#d4c4a8"/>
              <ellipse cx="52" cy="72" rx="22" ry="26" fill="#f5f0e6"/>
              <ellipse cx="52" cy="42" rx="16" ry="18" fill="#f5f0e6"/>
              <ellipse cx="52" cy="30" rx="12" ry="14" fill="#f5f0e6"/>
              <circle cx="46" cy="38" r="4" fill="#1a1a1a"/><circle cx="58" cy="38" r="4" fill="#1a1a1a"/>
              <path d="M34 50 Q24 45 22 55 Q29 58 36 54" fill="#f5f0e6"/>
              <path d="M70 50 Q80 45 82 55 Q75 58 68 54" fill="#f5f0e6"/>
            </svg>
          </span>
        </div>
      </div>
      <!-- 土拨鼠 -->
      <div class="peek-animal peek-animal-right" style="top: 84%;">
        <div class="peek-animal-body">
          <span class="peek-animal-inner anim-flip anim-bobble-6">
            <svg viewBox="0 0 100 90" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <ellipse cx="50" cy="62" rx="32" ry="26" fill="#8b7355"/>
              <circle cx="50" cy="38" r="26" fill="#8b7355"/>
              <circle cx="42" cy="34" r="5" fill="#1a1a1a"/><circle cx="58" cy="34" r="5" fill="#1a1a1a"/>
              <ellipse cx="50" cy="44" rx="6" ry="4" fill="#6b5344"/>
              <ellipse cx="28" cy="42" rx="8" ry="6" fill="#8b7355"/>
              <ellipse cx="72" cy="42" rx="8" ry="6" fill="#8b7355"/>
            </svg>
          </span>
        </div>
      </div>
    </aside>
  </div>
</body>
</html>
"""


def post_process_html(html: str) -> str:
    """微调生成的 HTML 结构"""
    # 移除 markdown 生成的第一个 h1（已在 hero 中展示）
    html = re.sub(r"<h1>.*?</h1>\s*", "", html, count=1, flags=re.DOTALL)

    # 移除开头元信息引用块（已在 hero 展示）
    html = re.sub(r"<blockquote>\s*<p><strong>Excel.*?</blockquote>\s*", "", html, count=1, flags=re.DOTALL)

    # 移除末尾祝福引用块（已在 footer 展示）
    html = re.sub(r"<hr />\s*<blockquote>\s*<p>🏁.*?</blockquote>\s*$", "", html, count=1, flags=re.DOTALL)

    # Day 标题加特殊标记
    html = re.sub(
        r"<h2>🗓️ (Day \d[^<]*)</h2>",
        r'<h2 class="day-title">🗓️ \1</h2>',
        html,
    )

    return html.strip()


def main():
    md_text = MD_FILE.read_text(encoding="utf-8")

    body = markdown.markdown(
        md_text,
        extensions=[
            TableExtension(),
            FencedCodeExtension(),
        ],
    )
    body = post_process_html(body)

    full_html = HTML_TEMPLATE.replace("{body}", body)
    HTML_FILE.write_text(full_html, encoding="utf-8")
    print(f"已生成: {HTML_FILE}")


if __name__ == "__main__":
    main()
