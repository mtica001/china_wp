# 私立高校择校与规划 Page Block — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-file WordPress Custom HTML block (`private-entrance-block.html`) for the TCK Workshop Chinese page 私立高校择校与规划, covering 3 sections: 私立中学、私立高中、編入考試 — with acceptance-results grids and exam-strategy callouts as the primary new components.

**Architecture:** Single self-contained HTML file; all CSS scoped under `.tck-pe`; no external JS libraries; two new components (`__schools` acceptance grid + `__exambox` exam-strategy card) layered onto the existing design system from `intl-school-page-block.html`. No instructor slider — this page leads with school acceptance results and exam strategy instead of per-subject grades.

**Tech Stack:** HTML5, vanilla CSS (CSS custom properties), vanilla JS (IIFE), Noto Sans SC + Noto Serif SC via Google Fonts. WordPress Custom HTML block (no `<html>/<head>/<body>` wrapper).

---

## Reference & Constraints

- **Design system:** `/Users/mervyn/Claude_Web/intl-school-page-block.html` — copy all CSS patterns (colors, fonts, components) verbatim; use prefix `tck-pe` throughout.
- **Source content (Japanese originals):**
  - 中学受験: https://www.tckwshop.com/course/entranceexam/juniorhigh/
  - 高校受験: https://www.tckwshop.com/course/entranceexam/highschool/
  - 編入試験: https://www.tckwshop.com/course/transferexam/
- **Language rule:** Target is Chinese-speaking families overseas. **Never use 归国生.** Use: 在海外就读的孩子 / 孩子目前在海外 / 从海外回日本 / 打算让孩子入读日本私立校.
- **Voice rule:** Observing teacher tone, no marketing promises. No "保证录取". Use "有一定把握" / "梯队学校参考" where needed.
- **Output file:** `/Users/mervyn/Claude_Web/private-entrance-block.html`

---

## New Components (not in intl-school page)

### `__schools` — Acceptance Results Grid
Displays accepted school names as styled chips, grouped by category label. Replaces the instructor slider as the primary results evidence.

```html
<div class="tck-pe__schools">
  <div class="tck-pe__schools-head">合格実績</div>
  <div class="tck-pe__schools-list">
    <span class="tck-pe__school">広尾学園</span>
    <span class="tck-pe__school tck-pe__school--top">渋谷学園渋谷</span>
    <!-- ... -->
  </div>
</div>
```

CSS:
```css
.tck-pe__schools{margin:18px 0 28px}
.tck-pe__schools-head{font-size:11.5px;font-weight:600;color:var(--gold);letter-spacing:.12em;text-transform:uppercase;margin-bottom:10px}
.tck-pe__schools-list{display:flex;flex-wrap:wrap;gap:8px}
.tck-pe__school{font-size:13px;padding:6px 14px;border-radius:20px;background:#fff;border:1.5px solid var(--border);color:var(--ink);white-space:nowrap}
.tck-pe__school--top{border-color:var(--gold);color:var(--forest);font-weight:600}
```

### `__exambox` — Exam Strategy Card
A 3-slot grid inside a bordered card: 考试科目 / 考试形式 / 建议准备期. One per section.

```html
<div class="tck-pe__exambox">
  <div class="tck-pe__exambox-head">考试科目 &amp; 备考方式</div>
  <div class="tck-pe__exambox-grid">
    <div class="tck-pe__exambox-item">
      <div class="tck-pe__exambox-lbl">考试科目</div>
      <div class="tck-pe__exambox-val">英语作文 · 日语写作 · 数学</div>
    </div>
    <div class="tck-pe__exambox-item">
      <div class="tck-pe__exambox-lbl">考试形式</div>
      <div class="tck-pe__exambox-val">笔试 + 面试 + 提交材料（志望理由書）</div>
    </div>
    <div class="tck-pe__exambox-item">
      <div class="tck-pe__exambox-lbl">建议准备时间</div>
      <div class="tck-pe__exambox-val">3–6个月起，有条件可提前至1年</div>
    </div>
  </div>
</div>
```

CSS:
```css
.tck-pe__exambox{background:var(--sage-lt);border:1px solid var(--border);border-radius:12px;padding:18px 22px;margin:18px 0 26px}
.tck-pe__exambox-head{font-size:12px;font-weight:700;color:var(--sage);letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px}
.tck-pe__exambox-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
.tck-pe__exambox-item{background:#fff;border:1px solid var(--border);border-radius:8px;padding:12px 14px}
.tck-pe__exambox-lbl{font-size:11px;font-weight:600;color:var(--muted);letter-spacing:.06em;margin-bottom:5px}
.tck-pe__exambox-val{font-size:13.5px;color:var(--ink);line-height:1.65}
```

---

## File Structure

| File | Action | Purpose |
|------|--------|---------|
| `private-entrance-block.html` | **Create** | Complete self-contained WordPress block |

---

## Task 1: Scaffold + CSS Foundation

**Files:**
- Create: `private-entrance-block.html`

- [ ] **Step 1: Create the file with head, all CSS, and empty wrapper div**

```html
<!-- TCK 私立高校择校与规划 page block -->
<meta charset="UTF-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;700&family=Noto+Sans+SC:wght@300;400;500&display=swap">

<style>
/* === scope: tck-pe === */
.tck-pe{font-family:'Noto Sans SC',sans-serif;color:#111;line-height:1.7}
.tck-pe *{box-sizing:border-box;margin:0;padding:0}
.tck-pe a{text-decoration:none;color:inherit}
.tck-pe{
  --forest:#2d5016;--sage:#5a8a3c;--sage-lt:#eef5e8;
  --gold:#c9a84c;--gold-lt:#fdf7e6;
  --pink:#e91e63;--pink-dk:#c2185b;
  --cream:#f9f6ef;--ink:#1e2a1e;--muted:#6a7a6a;
  --border:#dde8d0
}

/* ── Intro hero ── */
.tck-pe__intro{text-align:center;padding:52px 0 44px}
.tck-pe__sup{font-size:11.5px;letter-spacing:.2em;color:var(--sage);text-transform:uppercase;display:block;margin-bottom:12px}
.tck-pe__h1{font-family:'Noto Serif SC',serif!important;font-size:clamp(24px,3.8vw,36px)!important;font-weight:700!important;color:var(--forest)!important;line-height:1.35!important;margin:0 0 14px!important;padding:0!important}
.tck-pe__lead{font-size:14.5px;color:var(--muted);max-width:540px;margin:0 auto 40px;line-height:1.85}

/* ── Journey bar ── */
.tck-pe__journey{display:flex;align-items:stretch;justify-content:center;flex-wrap:wrap;gap:0;margin-bottom:4px}
.tck-pe__jstep{display:flex;flex-direction:column;align-items:center;gap:9px;padding:18px 18px 16px;border-radius:14px;text-decoration:none;transition:background .18s,box-shadow .18s;flex:1;max-width:170px;min-width:110px}
.tck-pe__jstep:hover{background:var(--sage-lt);box-shadow:0 2px 12px rgba(45,80,22,.09)}
.tck-pe__jnum{width:36px;height:36px;border-radius:50%;background:var(--forest);color:#fff;font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.tck-pe__jtxt{font-size:13.5px;font-weight:600;color:var(--forest);text-align:center;line-height:1.35}
.tck-pe__jage{font-size:11.5px;color:var(--muted);text-align:center;line-height:1.5;padding:0 4px}
.tck-pe__jlink{font-size:11px;color:var(--sage);letter-spacing:.04em;margin-top:2px}
.tck-pe__jarrow{width:28px;flex-shrink:0;align-self:center;height:1px;background:var(--border);margin:0 4px;position:relative}
.tck-pe__jarrow::after{content:'›';position:absolute;right:-7px;top:-10px;color:var(--border);font-size:20px}

/* ── Section ── */
.tck-pe__section{padding:52px 0;border-top:1px solid var(--border)}
.tck-pe__section:first-of-type{border-top:none}
.tck-pe__sec-head{display:flex;align-items:flex-start;gap:16px;margin-bottom:24px}
.tck-pe__sec-n{font-family:'Noto Serif SC',serif;font-size:52px;font-weight:700;color:var(--border);line-height:.9;flex-shrink:0;user-select:none}
.tck-pe__sec-meta{flex:1;padding-top:4px}
.tck-pe__sec-tag{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--sage);display:block;margin-bottom:5px}
.tck-pe__sec-h2{font-family:'Noto Serif SC',serif;font-size:clamp(19px,2.8vw,26px);font-weight:700;color:var(--forest);line-height:1.3;margin-bottom:3px}
.tck-pe__sec-sub{font-size:13px;color:var(--muted)}

/* ── Body copy ── */
.tck-pe__copy{font-size:14.5px;color:#111;line-height:1.9;margin-bottom:22px}
.tck-pe__copy p{margin-bottom:13px}
.tck-pe__copy p:last-child{margin-bottom:0}
.tck-pe__copy em{font-style:normal;color:var(--forest);font-weight:500}

/* ── Pain chips ── */
.tck-pe__pains{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:18px 0 26px}
.tck-pe__pain{background:var(--cream);border:1px solid var(--border);border-radius:10px;padding:13px 15px;font-size:13px;color:#111;line-height:1.6;display:flex;align-items:flex-start;gap:9px}
.tck-pe__pain-q{flex-shrink:0;margin-top:1px;width:18px;height:18px;border-radius:50%;background:var(--gold);color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center}

/* ── Features list ── */
.tck-pe__feats{list-style:none;display:flex;flex-direction:column;gap:9px;margin:14px 0 24px}
.tck-pe__feats li{display:flex;align-items:flex-start;gap:10px;font-size:14px;color:#111;line-height:1.65}
.tck-pe__feats li strong{color:var(--forest)}
.tck-pe__ck{flex-shrink:0;margin-top:3px;width:17px;height:17px;border-radius:50%;background:var(--sage-lt);display:flex;align-items:center;justify-content:center}
.tck-pe__ck svg{width:9px;height:9px;stroke:var(--sage);stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round}

/* ── Exam strategy box ── */
.tck-pe__exambox{background:var(--sage-lt);border:1px solid var(--border);border-radius:12px;padding:18px 22px;margin:18px 0 26px}
.tck-pe__exambox-head{font-size:12px;font-weight:700;color:var(--sage);letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px}
.tck-pe__exambox-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
.tck-pe__exambox-item{background:#fff;border:1px solid var(--border);border-radius:8px;padding:12px 14px}
.tck-pe__exambox-lbl{font-size:11px;font-weight:600;color:var(--muted);letter-spacing:.06em;margin-bottom:5px;text-transform:uppercase}
.tck-pe__exambox-val{font-size:13.5px;color:var(--ink);line-height:1.65}

/* ── Acceptance results grid ── */
.tck-pe__schools{margin:18px 0 28px}
.tck-pe__schools-head{font-size:11.5px;font-weight:600;color:var(--gold);letter-spacing:.12em;text-transform:uppercase;margin-bottom:10px}
.tck-pe__schools-list{display:flex;flex-wrap:wrap;gap:8px}
.tck-pe__school{font-size:13px;padding:6px 14px;border-radius:20px;background:#fff;border:1.5px solid var(--border);color:var(--ink);white-space:nowrap}
.tck-pe__school--top{border-color:var(--gold);color:var(--forest);font-weight:600}

/* ── Framing callout ── */
.tck-pe__framing{background:var(--cream);border:1px solid var(--border);border-radius:10px;padding:14px 18px;margin:4px 0 20px;font-size:13.5px;color:var(--forest);line-height:1.75}
.tck-pe__framing strong{font-family:'Noto Serif SC',serif;font-size:15px}

/* ── Timing callout ── */
.tck-pe__timing{background:var(--gold-lt);border-left:3px solid var(--gold);border-radius:0 10px 10px 0;padding:16px 20px;margin:8px 0 24px;font-size:13.5px;color:#111;line-height:1.75}
.tck-pe__timing-head{font-weight:600;font-size:14px;color:var(--forest);margin-bottom:6px}

/* ── CTA ── */
.tck-pe__cta-row{display:flex;gap:12px;flex-wrap:wrap;align-items:center;justify-content:center;margin-top:12px}
.tck-pe__btn{display:inline-flex;align-items:center;gap:6px;padding:12px 24px;border-radius:8px;font-family:'Noto Sans SC',sans-serif;font-size:14px;font-weight:500;letter-spacing:.04em;cursor:pointer;border:none;transition:background .2s,transform .15s}
.tck-pe__btn:hover{transform:translateY(-1px)}
.tck-pe .tck-pe__btn--primary{background:var(--pink);color:#fff;font-weight:700}
.tck-pe .tck-pe__btn--primary:hover{background:var(--pink-dk)}
.tck-pe__btn--ghost{background:transparent;color:var(--forest);border:1.5px solid var(--forest)}
.tck-pe__btn--ghost:hover{background:var(--sage-lt)}

/* ── Bottom CTA ── */
.tck-pe__bottom{text-align:center;padding:52px 0 36px;border-top:1px solid var(--border)}
.tck-pe__bottom p{font-size:14.5px;color:var(--muted);margin-bottom:22px;line-height:1.85;max-width:480px;margin-left:auto;margin-right:auto}
.tck-pe__bottom-rule{width:40px;height:2px;background:linear-gradient(90deg,var(--sage),var(--gold));margin:0 auto 28px;border-radius:2px}

/* ── Stats bar ── */
.tck-pe__stats{display:flex;justify-content:center;gap:32px;flex-wrap:wrap;margin-top:32px;padding:20px 28px;background:var(--sage-lt);border:1px solid var(--border);border-radius:12px}
.tck-pe__stat{text-align:center}
.tck-pe__stat strong{font-family:'Noto Serif SC',serif;font-size:28px;font-weight:700;color:var(--forest);display:block;line-height:1}
.tck-pe__stat span{font-size:12px;color:var(--muted);margin-top:5px;display:block}
.tck-pe__stat-div{width:1px;background:var(--border);align-self:stretch;margin:4px 0}

/* ── One-sub note ── */
.tck-pe__onesub{font-size:13px;color:var(--muted);display:flex;align-items:center;gap:8px;margin-top:14px;flex-wrap:wrap}
.tck-pe__onesub-dot{width:6px;height:6px;border-radius:50%;background:var(--sage);flex-shrink:0}
</style>

<div class="tck-pe">
  <!-- sections go here -->
</div>
```

- [ ] **Step 2: Open file with Live Server and confirm fonts load, no CSS errors**

Open `private-entrance-block.html` via VS Code → "Go Live". Verify the page is blank but no console errors.

- [ ] **Step 3: Commit**

```bash
git add private-entrance-block.html
git commit -m "feat: scaffold private-entrance block — CSS foundation + all component styles"
```

---

## Task 2: Intro Section (Hero + Journey Bar + Stats)

**Files:**
- Modify: `private-entrance-block.html` — replace `<!-- sections go here -->` with intro markup

- [ ] **Step 1: Write the intro HTML inside `.tck-pe`**

```html
  <!-- ── 页面标题 ── -->
  <div class="tck-pe__intro">
    <span class="tck-pe__sup">Private School Admission</span>
    <div class="tck-pe__h1">私立高校择校与规划</div>
    <p class="tck-pe__lead">想让孩子进日本的私立名校，光凭运气远不够——从选哪所学校，到备考英语、日语、数学，再到填报手续和面试训练，每一步都需要提前想清楚。TCK从择校那一刻陪你走到拿到录取通知。</p>

    <div class="tck-pe__journey">
      <a href="#sec-jhs" class="tck-pe__jstep">
        <div class="tck-pe__jnum">1</div>
        <div class="tck-pe__jtxt">私立中学</div>
        <div class="tck-pe__jage">小6～中1<br>中学受験</div>
        <span class="tck-pe__jlink">了解详情 →</span>
      </a>
      <div class="tck-pe__jarrow"></div>
      <a href="#sec-hs" class="tck-pe__jstep">
        <div class="tck-pe__jnum">2</div>
        <div class="tck-pe__jtxt">私立高中</div>
        <div class="tck-pe__jage">中3～高1<br>高校受験</div>
        <span class="tck-pe__jlink">了解详情 →</span>
      </a>
      <div class="tck-pe__jarrow"></div>
      <a href="#sec-transfer" class="tck-pe__jstep">
        <div class="tck-pe__jnum">3</div>
        <div class="tck-pe__jtxt">編入考試</div>
        <div class="tck-pe__jage">中学 · 高中<br>転入・編入</div>
        <span class="tck-pe__jlink">了解详情 →</span>
      </a>
    </div>

    <div class="tck-pe__stats">
      <div class="tck-pe__stat">
        <strong>70+</strong>
        <span>国家与地区</span>
      </div>
      <div class="tck-pe__stat-div"></div>
      <div class="tck-pe__stat">
        <strong>500+</strong>
        <span>私立学校备考支援</span>
      </div>
      <div class="tck-pe__stat-div"></div>
      <div class="tck-pe__stat">
        <strong>10年</strong>
        <span>日本私立升学经验</span>
      </div>
    </div>
  </div>
```

- [ ] **Step 2: Preview in Live Server — verify journey bar renders, stats bar shows correctly, 3 steps visible**

- [ ] **Step 3: Commit**

```bash
git add private-entrance-block.html
git commit -m "feat: add private-entrance intro — hero, journey bar, stats"
```

---

## Task 3: Section 01 — 私立中学入学

**Files:**
- Modify: `private-entrance-block.html` — append Section 01 after intro div, inside `.tck-pe`

- [ ] **Step 1: Write Section 01 HTML**

```html
  <!-- ══════════════════════════════════════
       SECTION 1：私立中学入学
  ══════════════════════════════════════ -->
  <div class="tck-pe__section" id="sec-jhs">
    <div class="tck-pe__sec-head">
      <div class="tck-pe__sec-n">01</div>
      <div class="tck-pe__sec-meta">
        <span class="tck-pe__sec-tag">Junior High School Entrance</span>
        <div class="tck-pe__sec-h2">私立中学入学备考</div>
        <div class="tck-pe__sec-sub">从择校到录取，全程陪你想清楚每一步</div>
      </div>
    </div>

    <div class="tck-pe__copy">
      <p>日本的私立中学入学考试（中学受験）通常在小学六年级秋冬举行，竞争激烈的学校有时早在同年1月就会截止。对于孩子目前在海外就读的家庭来说，时间窗口本就紧张，加上英语Essay、日语作文、数学三科都要同时准备，很多家长反映"不知道从哪里开始"。</p>
      <p>各校考试内容差异明显——广尾学园重视英语表达，渋谷系列侧重综合学力，东京学芸大附属国际的日语写作要求较高。<em>选校和备考方向必须同时想，不能割裂来看。</em> TCK的顾问会先帮你理清孩子的语言程度和目标方向，再制定具体的备考计划。</p>
    </div>

    <div class="tck-pe__pains">
      <div class="tck-pe__pain">
        <div class="tck-pe__pain-q">?</div>
        <span>孩子在海外读英语学校，日语写作和汉字完全没底——中学受験还考得上吗？</span>
      </div>
      <div class="tck-pe__pain">
        <div class="tck-pe__pain-q">?</div>
        <span>广尾学园、渋谷学園、三田国際……名字听过，但各校的考试侧重和升学路线到底有什么差别？</span>
      </div>
      <div class="tck-pe__pain">
        <div class="tck-pe__pain-q">?</div>
        <span>志望理由书全是日文，出愿手续看不懂，怕漏交文件或错过截止日期</span>
      </div>
    </div>

    <div class="tck-pe__exambox">
      <div class="tck-pe__exambox-head">考试科目 &amp; 备考方式</div>
      <div class="tck-pe__exambox-grid">
        <div class="tck-pe__exambox-item">
          <div class="tck-pe__exambox-lbl">考试科目</div>
          <div class="tck-pe__exambox-val">英语作文 · 日语写作 · 数学（各校比重不同）</div>
        </div>
        <div class="tck-pe__exambox-item">
          <div class="tck-pe__exambox-lbl">考试形式</div>
          <div class="tck-pe__exambox-val">笔试 + 面试（亲子面接）+ 提交材料（志望理由書）</div>
        </div>
        <div class="tck-pe__exambox-item">
          <div class="tck-pe__exambox-lbl">建议准备期</div>
          <div class="tck-pe__exambox-val">3–6个月起，英语底子好可缩短；日语弱建议提早至1年前</div>
        </div>
      </div>
    </div>

    <ul class="tck-pe__feats">
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>学校评估与择校</strong> — 按孩子的英语/日语程度、学科强项和家庭的升学目标，比较各校考试方向和录取条件</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>英语Essay写作</strong> — 从审题到结构到语言打磨，针对目标校的Essay题型逐题训练</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>日语作文与数学</strong> — 在海外就读的孩子日语往往是短板；按孩子实际程度制定专项补强计划</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>面试训练（亲子面接）</strong> — 模拟校方提问、引导孩子和家长整理志望理由，反复演练到自然流畅</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>出愿手续全程协助</strong> — 志望理由書撰写、文件翻译、截止日期管理，省去在海外处理繁琐日文手续的麻烦</span></li>
    </ul>

    <div class="tck-pe__schools">
      <div class="tck-pe__schools-head">合格実績 · 私立中学</div>
      <div class="tck-pe__schools-list">
        <span class="tck-pe__school tck-pe__school--top">広尾学園</span>
        <span class="tck-pe__school tck-pe__school--top">渋谷学園渋谷</span>
        <span class="tck-pe__school tck-pe__school--top">渋谷学園幕張</span>
        <span class="tck-pe__school tck-pe__school--top">慶應義塾湘南藤沢（SFC）</span>
        <span class="tck-pe__school">市川</span>
        <span class="tck-pe__school">洗足学園</span>
        <span class="tck-pe__school">三田国際学園</span>
        <span class="tck-pe__school">茗渓学園</span>
        <span class="tck-pe__school">啓明学園</span>
        <span class="tck-pe__school">東京学芸大附属国際</span>
        <span class="tck-pe__school">かえつ有明</span>
        <span class="tck-pe__school">同志社国際</span>
      </div>
    </div>

    <div class="tck-pe__cta-row">
      <a href="https://www.tckwshop.com/zh-cn/contact_consultation/" class="tck-pe__btn tck-pe__btn--primary">免费学习咨询 →</a>
      <a href="https://www.tckwshop.com/zh-cn/contact_consultation/" class="tck-pe__btn tck-pe__btn--ghost">学校评估咨询 →</a>
    </div>
  </div>
```

- [ ] **Step 2: Preview — verify exam box grid renders, schools list wraps cleanly, --top chips have gold border**

- [ ] **Step 3: Commit**

```bash
git add private-entrance-block.html
git commit -m "feat: add Section 01 — 私立中学入学 with exambox + schools grid"
```

---

## Task 4: Section 02 — 私立高中入学

**Files:**
- Modify: `private-entrance-block.html` — append Section 02 after Section 01, inside `.tck-pe`

- [ ] **Step 1: Write Section 02 HTML**

```html
  <!-- ══════════════════════════════════════
       SECTION 2：私立高中入学
  ══════════════════════════════════════ -->
  <div class="tck-pe__section" id="sec-hs">
    <div class="tck-pe__sec-head">
      <div class="tck-pe__sec-n">02</div>
      <div class="tck-pe__sec-meta">
        <span class="tck-pe__sec-tag">High School Entrance</span>
        <div class="tck-pe__sec-h2">私立高中入学备考</div>
        <div class="tck-pe__sec-sub">三科并进，也要提前想好大学的路</div>
      </div>
    </div>

    <div class="tck-pe__copy">
      <p>私立高中的入学考试通常覆盖英语、数学、日语三科，部分学校还额外要求英文Essay或小论文。ICU高校、ISAK、广尾学园、同志社国际……各校侧重不同，<em>选错方向备考，事倍功半</em>。更关键的是：进了哪所高中，直接影响三年后能申请哪些大学——高中选校本身就是升学规划的一部分。</p>
      <p>孩子目前在海外就读的家庭还面临一个现实问题：海外国际学校课程和日本私立高中的考试内容几乎没有重叠。英语程度够，但日语作文和日本式数学题型可能完全陌生。TCK的老师熟悉各校考题风格，能帮孩子高效补强真正考到的内容，而不是全科从头来。</p>
    </div>

    <div class="tck-pe__framing">
      <strong>高中不只是"进去"，而是"从哪里出发"。</strong> 选校时就要想清楚三年后的大学方向——走指定校推薦、一般入試还是海外申请，路线不同，高中选哪所差别很大。
    </div>

    <div class="tck-pe__pains">
      <div class="tck-pe__pain">
        <div class="tck-pe__pain-q">?</div>
        <span>ICU高校和ISAK听说都很好，但具体考什么、怎么准备，完全摸不着头脑</span>
      </div>
      <div class="tck-pe__pain">
        <div class="tck-pe__pain-q">?</div>
        <span>孩子日语口语还行，但日语写作和作文从来没练过，笔试怎么应对？</span>
      </div>
      <div class="tck-pe__pain">
        <div class="tck-pe__pain-q">?</div>
        <span>志望理由書要写自己"为什么想进这所学校"，孩子根本不知道怎么组织内容</span>
      </div>
    </div>

    <div class="tck-pe__exambox">
      <div class="tck-pe__exambox-head">考试科目 &amp; 备考方式</div>
      <div class="tck-pe__exambox-grid">
        <div class="tck-pe__exambox-item">
          <div class="tck-pe__exambox-lbl">考试科目</div>
          <div class="tck-pe__exambox-val">英语（Essay含）· 数学 · 日语作文（各校三科权重不同）</div>
        </div>
        <div class="tck-pe__exambox-item">
          <div class="tck-pe__exambox-lbl">考试形式</div>
          <div class="tck-pe__exambox-val">笔试 + 面试 + 志望理由書（部分校加考英语面试）</div>
        </div>
        <div class="tck-pe__exambox-item">
          <div class="tck-pe__exambox-lbl">建议准备期</div>
          <div class="tck-pe__exambox-val">英语底子好约3–4个月；日语弱建议提前6–12个月开始</div>
        </div>
      </div>
    </div>

    <ul class="tck-pe__feats">
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>志望校分析与策略</strong> — 解析目标校的考试题型、录取条件和升学路线，帮你制定主校＋梯队的报考组合</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>英语 Essay 专项</strong> — 从选题、论点、结构到语言，按目标校的Essay评分标准反复打磨</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>数学题型集训</strong> — 日本高中受験的数学题型和思路有其特殊性，针对考试风格专项训练</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>日语作文补强</strong> — 对于在海外就读的孩子，日语写作是高频短板；按孩子实际程度制定追赶计划</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>志望理由書 + 面试训练</strong> — 帮孩子整理志望理由，写出有说服力的申请文书，并做模拟面试到熟练为止</span></li>
    </ul>

    <div class="tck-pe__schools">
      <div class="tck-pe__schools-head">合格実績 · 私立高中</div>
      <div class="tck-pe__schools-list">
        <span class="tck-pe__school tck-pe__school--top">ICU高校</span>
        <span class="tck-pe__school tck-pe__school--top">ISAK（UWC ISAK Japan）</span>
        <span class="tck-pe__school tck-pe__school--top">広尾学園</span>
        <span class="tck-pe__school tck-pe__school--top">慶應義塾湘南藤沢（SFC）</span>
        <span class="tck-pe__school">渋谷学園幕張</span>
        <span class="tck-pe__school">同志社国際</span>
        <span class="tck-pe__school">三田国際学園</span>
        <span class="tck-pe__school">市川</span>
        <span class="tck-pe__school">茗渓学園</span>
        <span class="tck-pe__school">法政大学国際高校</span>
        <span class="tck-pe__school">都立国際高校</span>
        <span class="tck-pe__school">かえつ有明</span>
      </div>
    </div>

    <div class="tck-pe__timing">
      <div class="tck-pe__timing-head">什么时候开始最合适？</div>
      私立高中考试通常在<strong>初三秋冬（11月～1月）</strong>集中举行，竞争激烈的学校更早。英语基础扎实的孩子，初三开学前（暑假）开始准备约3–4个月足够；日语需要补强的情况，建议提前到<strong>初二下学期</strong>开始日语专项训练，不要等到初三才起步。
    </div>

    <div class="tck-pe__cta-row">
      <a href="https://www.tckwshop.com/zh-cn/contact_consultation/" class="tck-pe__btn tck-pe__btn--primary">免费学习咨询 →</a>
    </div>
  </div>
```

- [ ] **Step 2: Preview — verify framing callout, exambox, timing callout all render correctly; schools list shows gold-border --top chips**

- [ ] **Step 3: Commit**

```bash
git add private-entrance-block.html
git commit -m "feat: add Section 02 — 私立高中入学 with exambox + acceptance grid + timing callout"
```

---

## Task 5: Section 03 — 編入考試

**Files:**
- Modify: `private-entrance-block.html` — append Section 03 after Section 02, inside `.tck-pe`

- [ ] **Step 1: Write Section 03 HTML**

```html
  <!-- ══════════════════════════════════════
       SECTION 3：編入考試
  ══════════════════════════════════════ -->
  <div class="tck-pe__section" id="sec-transfer">
    <div class="tck-pe__sec-head">
      <div class="tck-pe__sec-n">03</div>
      <div class="tck-pe__sec-meta">
        <span class="tck-pe__sec-tag">Transfer Exam</span>
        <div class="tck-pe__sec-h2">編入考試备考</div>
        <div class="tck-pe__sec-sub">从海外插班日本私立校——时间紧，但有章可循</div>
      </div>
    </div>

    <div class="tck-pe__copy">
      <p>编入考试（転入・編入試験）是为已就读其他学校、需中途转入的学生设立的特殊考试。对于从海外回到日本、或直接在日本就读并计划转入更好学校的孩子，编入是一条随时可以走的路——但它的难点在于，<em>准备期往往只有一到三个月，而且考试信息几乎不公开</em>。</p>
      <p>岡留智史老师总结过这条路最大的困难："绝大多数家庭都是突然决定回国，然后才开始想学校的事——连报哪所都没定，备考时间已经开始倒计时了。"TCK在编入备考上有丰富的案例积累，从快速择校判断、高效备考策略，到出愿文件全程支援，都可以在时间有限的情况下迅速启动。</p>
    </div>

    <div class="tck-pe__framing">
      <strong>编入不是退路，是另一种主动选择。</strong> 不少家庭是带着明确目标来的——孩子现在在海外读书，计划某一年回日本，提前一年规划编入比临时应对更从容。
    </div>

    <div class="tck-pe__pains">
      <div class="tck-pe__pain">
        <div class="tck-pe__pain-q">?</div>
        <span>回国日期还没定，但想先了解编入考试怎么准备——现在问还来得及吗？</span>
      </div>
      <div class="tck-pe__pain">
        <div class="tck-pe__pain-q">?</div>
        <span>学校官网几乎没有编入考试的详细信息，不知道考什么、难度如何、怎么联络校方</span>
      </div>
      <div class="tck-pe__pain">
        <div class="tck-pe__pain-q">?</div>
        <span>孩子在国际学校就读，日语完全不行——编入真的可以只靠英语吗？</span>
      </div>
    </div>

    <div class="tck-pe__exambox">
      <div class="tck-pe__exambox-head">考试科目 &amp; 备考方式</div>
      <div class="tck-pe__exambox-grid">
        <div class="tck-pe__exambox-item">
          <div class="tck-pe__exambox-lbl">考试科目</div>
          <div class="tck-pe__exambox-val">英语作文 · 日语写作 · 数学（部分学校可仅考英语）</div>
        </div>
        <div class="tck-pe__exambox-item">
          <div class="tck-pe__exambox-lbl">考试形式</div>
          <div class="tck-pe__exambox-val">笔试 + 面试（部分校加个人陈述 / 调查书）</div>
        </div>
        <div class="tck-pe__exambox-item">
          <div class="tck-pe__exambox-lbl">准备期弹性</div>
          <div class="tck-pe__exambox-val">最短1个月起步；有条件提前到3–6个月效果更佳</div>
        </div>
      </div>
    </div>

    <ul class="tck-pe__feats">
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>快速择校判断</strong> — 根据孩子的学年、语言程度和目标方向，迅速帮你锁定有实际胜算的学校组合</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>高效备考计划</strong> — 时间有限时，重点放在哪、怎么分配精力，TCK会给出清晰的优先顺序</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>英语Essay集中突破</strong> — 编入考的英语比一般高中受験更看重表达质量，集中强化Essay写作往往见效最快</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>日语补强（按需）</strong> — 对英语学校背景的孩子，日语往往是弱点；会明确告诉你哪所学校可以不靠日语、哪所不行</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>出愿文件全程支援</strong> — 编入出愿有时需要原学校的推薦書、在籍証明等材料；我们协助你理清流程、避免遗漏</span></li>
      <li><span class="tck-pe__ck"><svg viewBox="0 0 12 12"><polyline points="2,6 5,9 10,3"/></svg></span><span><strong>面试训练</strong> — 编入面试常见问题包括"为什么要转到这所学校"和"现在学校哪里不满足你"，提前准备才不会当场卡壳</span></li>
    </ul>

    <div class="tck-pe__schools">
      <div class="tck-pe__schools-head">合格実績 · 編入（中学）</div>
      <div class="tck-pe__schools-list">
        <span class="tck-pe__school tck-pe__school--top">広尾学園</span>
        <span class="tck-pe__school tck-pe__school--top">渋谷学園渋谷</span>
        <span class="tck-pe__school">市川</span>
        <span class="tck-pe__school">洗足学園</span>
        <span class="tck-pe__school">三田国際学園</span>
        <span class="tck-pe__school">茗渓学園</span>
        <span class="tck-pe__school">啓明学園</span>
        <span class="tck-pe__school">東京学芸大附属国際</span>
        <span class="tck-pe__school">かえつ有明</span>
        <span class="tck-pe__school">同志社国際</span>
        <span class="tck-pe__school">啓明学院</span>
      </div>
    </div>

    <div class="tck-pe__schools" style="margin-top:0">
      <div class="tck-pe__schools-head">合格実績 · 編入（高中）</div>
      <div class="tck-pe__schools-list">
        <span class="tck-pe__school tck-pe__school--top">ICU高校</span>
        <span class="tck-pe__school tck-pe__school--top">広尾学園</span>
        <span class="tck-pe__school">市川</span>
        <span class="tck-pe__school">三田国際学園</span>
        <span class="tck-pe__school">茗渓学園</span>
        <span class="tck-pe__school">同志社国際</span>
        <span class="tck-pe__school">法政国際高校</span>
        <span class="tck-pe__school">かえつ有明</span>
        <span class="tck-pe__school">順天高校</span>
      </div>
    </div>

    <div class="tck-pe__cta-row">
      <a href="https://www.tckwshop.com/zh-cn/contact_consultation/" class="tck-pe__btn tck-pe__btn--primary">免费学习咨询 →</a>
    </div>
    <div class="tck-pe__onesub">
      <div class="tck-pe__onesub-dot"></div>
      一科也可以 &nbsp;·&nbsp; 准备期再短也可以先咨询 &nbsp;·&nbsp; 不确定是否来得及，说出来让我们帮你判断
    </div>
  </div>
```

- [ ] **Step 2: Preview — verify two `__schools` blocks render side by side correctly; framing callout visible; `__onesub` note shows at bottom**

- [ ] **Step 3: Commit**

```bash
git add private-entrance-block.html
git commit -m "feat: add Section 03 — 編入考試 with dual acceptance grids + framing callout"
```

---

## Task 6: Bottom CTA + Final Polish

**Files:**
- Modify: `private-entrance-block.html` — append bottom CTA after Section 03, close `.tck-pe` div

- [ ] **Step 1: Write bottom CTA HTML**

```html
  <!-- ── 底部 CTA ── -->
  <div class="tck-pe__bottom">
    <div class="tck-pe__bottom-rule"></div>
    <p>无论孩子现在在哪个阶段——刚开始想择校，还是回国日期已经定了——都欢迎先来聊聊。<br>TCK会给你一个清晰的下一步，而不是一份漫无边际的建议。</p>
    <a href="https://www.tckwshop.com/zh-cn/contact_consultation/" class="tck-pe__btn tck-pe__btn--primary" style="font-size:15px;padding:14px 32px">免费学习咨询 →</a>
  </div>
```

- [ ] **Step 2: Full-page review checklist in Live Server**
  - Journey bar: all 3 steps visible, arrows between them
  - Section 01: pain chips 3×, exambox 3-slot grid, schools list with gold-border top schools, 2 CTA buttons
  - Section 02: framing callout, pain chips 3×, exambox, schools list, timing callout, CTA
  - Section 03: framing callout, pain chips 3×, exambox, two schools lists (中学/高中), CTA + onesub note
  - Bottom CTA: rule line + paragraph + button
  - Mobile (resize to 375px): exambox grid stacks to 1-col, schools list wraps, journey bar wraps
  - No 归国生 anywhere in the text

- [ ] **Step 3: Final commit**

```bash
git add private-entrance-block.html
git commit -m "feat: complete private-entrance page block — 3 sections, acceptance grids, exam strategy cards"
```

---

## Self-Review

**Spec coverage:**
| Requirement | Task covering it |
|---|---|
| 3 sections: 私立中学 / 私立高中 / 編入 | Tasks 3, 4, 5 |
| 合格実績 per section | Tasks 3, 4, 5 (`__schools` component) |
| 考試/対策方式 per section | Tasks 3, 4, 5 (`__exambox` component) |
| Chinese audience, no 归国生 | All copy in Tasks 2–6 |
| Same visual structure as intl-school page | Task 1 (CSS mirrors intl-school tokens) |
| Journey bar in intro | Task 2 |
| Stats bar | Task 2 |
| Bottom global CTA | Task 6 |

**No placeholders:** All copy, all school names, all CSS values are written out in full.

**Type consistency:** CSS prefix `tck-pe__` used throughout; no ID reuse conflicts (single page, no sliders).
