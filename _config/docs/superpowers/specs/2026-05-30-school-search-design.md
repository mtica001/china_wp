# Japanese Language School Search — Design Spec
**Date:** 2026-05-30  
**Status:** Approved  

---

## 1. Overview

A Chinese-only filterable school search page embedded in a company WordPress site as a static HTML file. Data source is the 日本語教育振興協会 (日振協 / nisshinkyo.org) accredited school registry. All 103 schools have been pre-scraped into `data/schools.json`.

**Copyright strategy:** Extract only objective factual fields (address, capacity, tuition, stats). No promotional text, photos, or logos copied. Each card links back to the nisshinkyo source page and the school's own website.

---

## 2. Tech Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Reactivity | Alpine.js v3 (CDN, defer) | 15 KB, reactive filters in ~50 lines, no build step |
| Styling | Custom CSS (inline in `<style>`) | No Tailwind CDN needed, full control |
| Data | JSON baked into `<script>` const | Single self-contained file, no server requests |
| WordPress integration | Custom HTML block | Paste file content, or upload and link as page template |

**Output:** One file — `school-search.html` (~200 KB with data)

---

## 3. Layout

### Desktop (>900px)
Two-column: 260px sticky sidebar (filters) + fluid main area (cards).

```
┌──────────────────────────────────────────────────────────┐
│  日本语学校搜索                       [显示 95 所学校]     │
├──────────────┬───────────────────────────────────────────┤
│ 筛选条件      │  排序: [综合 ▾]   显示 95 所学校           │
│ (sticky)     ├───────────────────────────────────────────┤
│              │  [full-width card row]                    │
│              │  [full-width card row]                    │
│              │  ...                                      │
│              ├── 其他学校（学费未公开）：8 所 ──────────── │
│              │  [full-width card row, grey tint]         │
└──────────────┴───────────────────────────────────────────┘
```

### Tablet (600–900px)
Horizontal filter bar at top, full-width cards below.

### Mobile (<600px)
Filter bar hidden behind "筛选 ▾" toggle button. Full-width cards.

---

## 4. Filter Panel

| Filter | UI Control | Field | Logic |
|--------|-----------|-------|-------|
| 地区（大区） | Dropdown | `region` | Exact match |
| 都道府県 | Dropdown (cascades from region selection) | `prefecture` | Exact match |
| 年学费 | Dual-handle range slider | `tuition_min` / `tuition_max` | School included if tuition range **overlaps** slider range |
| 专任教师数 | Single slider (min) | `full_time_teachers` | `>= slider value` |
| 关键词标签 | Multi-select toggle chips | derived (see §5) | AND logic — school must match all selected tags |

**Sort options:** 综合（默认，按地区排列：关东→中部→近畿→中国四国→九州冲绳）/ 学费从低到高 / 学费从高到低 / 招生人数从多到少

**Reset button:** Clears all filters and returns to full 103-school view.

---

## 5. Keyword Tag Derivation

Tags are computed from data fields at page load. No manual tagging required.

| Tag (Chinese) | Derived from |
|--------------|-------------|
| 升大学院 | `placement.大学院 > 0` |
| 升大学 | `placement.大学 > 0` |
| 升专门学校 | `placement["専修学校(専門課程)"] > 0` |
| 就职 | `placement["その他"] > 0` |
| JLPT対策 | `jlpt.N1.examined > 0 OR jlpt.N2.examined > 0` |
| 中文对应 | `nationalities[0].country === "中国"` (top nationality is Chinese) |
| 有宿舍 | `has_accommodation === true` |
| 4月入学 | `start_months` includes `"4"` |
| 10月入学 | `start_months` includes `"10"` |

Goal tags (升大学院, 升大学, 升专门学校, 就职, JLPT対策) styled in **blue**.  
Service tags (中文对应, 有宿舍, 4月入学, 10月入学) styled in **green**.

---

## 6. Result Card Design

Full-width horizontal card, stacked row-by-row.

```
┌──────────────────────────────────────────────────────────┐
│ 文化外国語専門学校                      📍 东京都 渋谷区   │
│                                                          │
│ 👥 招生上限 280名   👨‍🏫 专任教师 15名   📅 4月・10月入学    │
│ 💰 年学费 ¥110万 〜 ¥158万（含报名费・入学金）             │
│                                                          │
│ [升大学] [升专门学校] [JLPT対策] [有宿舍]                 │
│                                                          │
│ 数据来源：日本語教育振興協会                              │
│ [📋 查看日振协资料]              [🌐 前往学校官网 →]       │
└──────────────────────────────────────────────────────────┘
```

**Both links open in new tab (`target="_blank" rel="noopener"`).**  
**No iframes.** Direct external links only.

### Card field details

| Field | Source | Fallback |
|-------|--------|---------|
| School name | `school.name` | — |
| Location | `school.prefecture` + `school.city` | `school.city` |
| Capacity | `school.capacity` | "未公开" |
| Full-time teachers | `school.full_time_teachers` | "未公开" |
| Start months | `school.start_months` joined with "・" | "未公开" |
| Tuition range | `school.tuition_min` ~ `school.tuition_max` | "学费未公开" badge |
| Tags | Derived per §5 | (none shown if no tags) |
| Nisshinkyo link | `school.nisshinkyo_url` | Always present |
| School website | `school.website` | "官网未登录" (button hidden) |

---

## 7. Tuition-Unknown School Separation

Schools where `tuition_min` is null (~8 schools) are **rendered in a separate section** below the main results:

- Section header: `其他学校（学费未公开）：X 所`
- Cards in this section have a subtle grey background tint
- The tuition range slider does **not** filter this section
- All other filters (region, teachers, keyword tags) apply normally
- Section is hidden if no tuition-unknown schools match the current filters

---

## 8. Edge Cases

| Case | Handling |
|------|---------|
| No results | Empty state: "没有符合条件的学校，请调整筛选条件" |
| No school website | Hide 学校官网 button; show "官网未登录" in grey text |
| Long school name | Clamp to 2 lines with ellipsis |
| Half-width katakana in nationality data (e.g. `ｲﾝﾄﾞ`) | Normalize to full-width on display |
| Tuition-unknown + tuition slider active | Tuition-unknown schools shown in lower section regardless of slider |

---

## 9. Data Source & Copyright Compliance

- All data extracted from public pages at `nisshinkyo.org/search/college.php?id=X`
- Only objective factual fields are stored — no promotional text, photos, or logos
- Each card includes visible attribution: "数据来源：日本語教育振興協会"
- Each card links directly to the source page: `[查看日振协资料]`
- School website link provided separately: `[前往学校官网 →]`
- No iframe embedding of nisshinkyo pages

---

## 10. File Structure

```
Claude_Web/
├── data/
│   ├── scrape_schools.py      ← scraper (re-run to refresh data)
│   └── schools.json           ← 103 schools, all fields parsed
├── docs/superpowers/specs/
│   └── 2026-05-30-school-search-design.md  ← this file
└── school-search.html         ← OUTPUT: the deliverable
```

---

## 11. Out of Scope

- Server-side search or database
- User accounts or saved searches
- School photos or maps
- Automatic data refresh (manual re-scrape + re-upload to update)
- SEO optimisation (JS-rendered content)
