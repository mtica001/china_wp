# School Search Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `school-search.html` — a self-contained, Chinese-only Japanese language school search page using Alpine.js v3, with sidebar filters and full-width result cards, embeddable in WordPress as a Custom HTML block.

**Architecture:** Single HTML file with Alpine.js loaded from CDN. All 103 schools baked into a `const SCHOOLS` array in a `<script>` block. Alpine's `x-data="schoolSearch()"` drives reactive filtering, sorting, and rendering. No build step, no server requests beyond the Alpine CDN.

**Tech Stack:** HTML5, Alpine.js v3 (CDN), CSS custom properties, inline `<style>`, data from `data/schools.json`.

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `data/scrape_schools.py` | Modify | Fix prefecture regex bug (京都 → 京都府) |
| `data/schools.json` | Regenerate | Re-run scraper after fix |
| `school-search.html` | Create | Entire deliverable — HTML + CSS + JS |

---

## Task 1: Fix scraper prefecture bug and regenerate data

**Files:**
- Modify: `data/scrape_schools.py`
- Regenerate: `data/schools.json`

The regex `r'^(.+?[都道府県])'` on `京都府京都市...` non-greedily matches `京都` (stops at `都`) instead of `京都府`. Fix by using a greedy alternation that prefers 2-character suffixes.

- [ ] **Step 1: Fix the prefecture regex in scrape_schools.py**

Find this line in `parse_school()`:
```python
pref_match = re.match(r'^(.+?[都道府県])', location_hint)
prefecture = pref_match.group(1) if pref_match else location_hint
```

Replace with:
```python
pref_match = re.match(r'^(.+?(?:都|道|府|県))', location_hint)
prefecture = pref_match.group(1) if pref_match else location_hint
# Normalize bare 京都 → 京都府
if prefecture == '京都':
    prefecture = '京都府'
```

Also fix the same pattern in the `except` block at the bottom of `main()`:
```python
pref_m = re.match(r'^(.+?(?:都|道|府|県))', loc)
prefecture = pref_m.group(1) if pref_m else loc
if prefecture == '京都':
    prefecture = '京都府'
```

- [ ] **Step 2: Re-run scraper**

```bash
cd /Users/mervyn/Claude_Web
python3 data/scrape_schools.py
```

Expected: `Done. 103 schools → /Users/mervyn/Claude_Web/data/schools.json`

- [ ] **Step 3: Verify fix**

```bash
python3 -c "
import json
with open('data/schools.json') as f:
    s = json.load(f)
bad = [x for x in s if x.get('prefecture') == '京都']
print('京都 (unfixed):', bad)
fixed = [x for x in s if x.get('prefecture') == '京都府']
print('京都府 count:', len(fixed))
from collections import Counter
print(Counter(x['region'] for x in s))
"
```

Expected: `京都 (unfixed): []` and `近畿` count increases to 20.

- [ ] **Step 4: Commit**

```bash
git add data/scrape_schools.py data/schools.json
git commit -m "fix: normalize 京都 prefecture and regenerate schools.json"
```

---

## Task 2: HTML skeleton with Alpine.js and baked-in data

**Files:**
- Create: `school-search.html`

- [ ] **Step 1: Generate the SCHOOLS constant from schools.json**

```bash
python3 -c "
import json
with open('data/schools.json') as f:
    schools = json.load(f)
print(f'const SCHOOLS = {json.dumps(schools, ensure_ascii=False)};')
" > /tmp/schools_const.js
wc -c /tmp/schools_const.js
```

Expected: ~350–450 KB file.

- [ ] **Step 2: Create school-search.html skeleton**

Create `school-search.html`:

```html
<!DOCTYPE html>
<html lang="zh-Hans">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>日本语学校搜索</title>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <style>
    /* CSS added in Task 7 */
  </style>
</head>
<body x-data="schoolSearch()">

  <header class="page-header">
    <h1>日本语学校搜索</h1>
    <span class="result-count" x-text="`显示 ${totalCount} 所学校`"></span>
  </header>

  <div class="layout">
    <aside class="sidebar">
      <!-- filters added in Task 4 -->
      <p>筛选面板（即将添加）</p>
    </aside>
    <main class="results">
      <!-- results added in Task 6 -->
      <p x-text="`已加载 ${schools.length} 所学校`"></p>
    </main>
  </div>

  <script>
  // DATA PLACEHOLDER — replaced in Step 3
  const SCHOOLS = [];

  function schoolSearch() {
    return {
      schools: [],
      init() {
        this.schools = SCHOOLS.map(s => ({ ...s, tags: deriveTags(s) }));
      },
      get totalCount() {
        return this.schools.length;
      },
    };
  }

  function deriveTags(s) {
    return [];  // implemented in Task 3
  }
  </script>
</body>
</html>
```

- [ ] **Step 3: Bake schools.json into the file**

Replace the `const SCHOOLS = [];` line with the full data:

```bash
python3 - <<'EOF'
import json

with open('data/schools.json') as f:
    schools = json.load(f)

schools_js = f"const SCHOOLS = {json.dumps(schools, ensure_ascii=False)};"

with open('school-search.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('const SCHOOLS = [];', schools_js)

with open('school-search.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Done. File size: {len(content)//1024} KB")
EOF
```

Expected: `Done. File size: ~430 KB`

- [ ] **Step 4: Verify in browser**

Open `school-search.html` in a browser. Expected: page loads, shows "已加载 103 所学校".

- [ ] **Step 5: Commit**

```bash
git add school-search.html
git commit -m "feat: scaffold school-search.html with Alpine.js and baked data"
```

---

## Task 3: Tag derivation

**Files:**
- Modify: `school-search.html` — `deriveTags()` function

- [ ] **Step 1: Implement deriveTags() in the `<script>` block**

Replace `function deriveTags(s) { return []; }` with:

```javascript
function deriveTags(s) {
  const tags = [];
  const p = s.placement || {};
  const j = s.jlpt || {};

  // Goal tags (blue)
  if ((p['大学院'] || 0) > 0)               tags.push({ key: 'grad',     label: '升大学院',   type: 'goal' });
  if ((p['大学'] || 0) > 0)                 tags.push({ key: 'univ',     label: '升大学',     type: 'goal' });
  if ((p['専修学校(専門課程)'] || 0) > 0)   tags.push({ key: 'senmon',   label: '升专门学校', type: 'goal' });
  if ((p['その他'] || 0) > 0)               tags.push({ key: 'work',     label: '就职',       type: 'goal' });
  if ((j.N1 && j.N1.examined > 0) ||
      (j.N2 && j.N2.examined > 0))          tags.push({ key: 'jlpt',     label: 'JLPT対策',   type: 'goal' });

  // Service tags (green)
  const topNation = (s.nationalities || [])[0];
  if (topNation && topNation.country === '中国') tags.push({ key: 'chinese', label: '中文对应', type: 'service' });
  if (s.has_accommodation)                       tags.push({ key: 'dorm',    label: '有宿舍',   type: 'service' });
  if ((s.start_months || []).includes('4'))      tags.push({ key: 'apr',     label: '4月入学',  type: 'service' });
  if ((s.start_months || []).includes('10'))     tags.push({ key: 'oct',     label: '10月入学', type: 'service' });

  return tags;
}
```

- [ ] **Step 2: Verify tags in browser console**

Open `school-search.html`, open DevTools console and run:
```javascript
schoolSearch().init.toString()  // sanity check
```
Then temporarily add to the `init()` method: `console.log(this.schools[0].tags)` and reload. Expected: array of tag objects for 文化外国語専門学校 with keys like `univ`, `senmon`, `jlpt`, `apr`, `oct`.

Remove the console.log after verifying.

- [ ] **Step 3: Commit**

```bash
git add school-search.html
git commit -m "feat: implement tag derivation for 9 keyword categories"
```

---

## Task 4: Filter state and filter panel HTML

**Files:**
- Modify: `school-search.html` — `schoolSearch()` function + sidebar HTML

- [ ] **Step 1: Add filter state to schoolSearch()**

Replace the `schoolSearch()` function body with:

```javascript
function schoolSearch() {
  return {
    schools: [],

    // Filter state
    filterRegion: '',
    filterPrefecture: '',
    tuitionMin: 0,
    tuitionMax: 2000000,
    teachersMin: 0,
    filterTags: [],
    sortBy: 'default',

    // Constants
    TUITION_FLOOR: 0,
    TUITION_CEIL: 2000000,
    TEACHERS_MAX: 50,

    REGION_ORDER: ['関東', '中部', '近畿', '中国・四国', '九州・沖縄', 'その他'],

    ALL_TAGS: [
      { key: 'grad',    label: '升大学院',   type: 'goal' },
      { key: 'univ',    label: '升大学',     type: 'goal' },
      { key: 'senmon',  label: '升专门学校', type: 'goal' },
      { key: 'work',    label: '就职',       type: 'goal' },
      { key: 'jlpt',    label: 'JLPT対策',   type: 'goal' },
      { key: 'chinese', label: '中文对应',   type: 'service' },
      { key: 'dorm',    label: '有宿舍',     type: 'service' },
      { key: 'apr',     label: '4月入学',    type: 'service' },
      { key: 'oct',     label: '10月入学',   type: 'service' },
    ],

    init() {
      this.schools = SCHOOLS.map(s => ({ ...s, tags: deriveTags(s) }));
    },

    // Cascading prefecture options
    get regions() {
      return [...new Set(this.schools.map(s => s.region))]
        .sort((a, b) => this.REGION_ORDER.indexOf(a) - this.REGION_ORDER.indexOf(b));
    },

    get prefectures() {
      if (!this.filterRegion) return [];
      return [...new Set(
        this.schools
          .filter(s => s.region === this.filterRegion)
          .map(s => s.prefecture)
      )].sort();
    },

    onRegionChange() {
      this.filterPrefecture = '';
    },

    toggleTag(key) {
      const idx = this.filterTags.indexOf(key);
      if (idx === -1) this.filterTags.push(key);
      else this.filterTags.splice(idx, 1);
    },

    isTagActive(key) {
      return this.filterTags.includes(key);
    },

    resetFilters() {
      this.filterRegion = '';
      this.filterPrefecture = '';
      this.tuitionMin = this.TUITION_FLOOR;
      this.tuitionMax = this.TUITION_CEIL;
      this.teachersMin = 0;
      this.filterTags = [];
      this.sortBy = 'default';
    },

    // Core filter: applies to all schools except tuition slider
    matchesBaseFilters(s) {
      if (this.filterRegion && s.region !== this.filterRegion) return false;
      if (this.filterPrefecture && s.prefecture !== this.filterPrefecture) return false;
      if (this.teachersMin > 0 && (s.full_time_teachers || 0) < this.teachersMin) return false;
      if (this.filterTags.length > 0) {
        const schoolTagKeys = s.tags.map(t => t.key);
        if (!this.filterTags.every(k => schoolTagKeys.includes(k))) return false;
      }
      return true;
    },

    // Schools with known tuition that pass all filters including slider
    get primaryResults() {
      const results = this.schools.filter(s => {
        if (s.tuition_min === null) return false;
        if (!this.matchesBaseFilters(s)) return false;
        // Overlap check: school range overlaps slider range
        if (s.tuition_max < this.tuitionMin) return false;
        if (s.tuition_min > this.tuitionMax) return false;
        return true;
      });
      return this.sortResults(results);
    },

    // Schools with unknown tuition — tuition slider does not apply
    get unknownResults() {
      return this.schools.filter(s => {
        if (s.tuition_min !== null) return false;
        return this.matchesBaseFilters(s);
      });
    },

    get totalCount() {
      return this.primaryResults.length + this.unknownResults.length;
    },

    sortResults(list) {
      const copy = [...list];
      if (this.sortBy === 'tuition_asc') {
        return copy.sort((a, b) => (a.tuition_min || 0) - (b.tuition_min || 0));
      }
      if (this.sortBy === 'tuition_desc') {
        return copy.sort((a, b) => (b.tuition_max || 0) - (a.tuition_max || 0));
      }
      if (this.sortBy === 'capacity_desc') {
        return copy.sort((a, b) => (b.capacity || 0) - (a.capacity || 0));
      }
      // Default: sort by REGION_ORDER, then prefecture alphabetically
      return copy.sort((a, b) => {
        const ri = this.REGION_ORDER.indexOf(a.region) - this.REGION_ORDER.indexOf(b.region);
        if (ri !== 0) return ri;
        return (a.prefecture || '').localeCompare(b.prefecture || '', 'ja');
      });
    },

    formatTuition(yen) {
      if (yen === null || yen === undefined) return '未公开';
      return `¥${(yen / 10000).toFixed(0)}万`;
    },

    formatMonths(months) {
      if (!months || months.length === 0) return '未公开';
      return months.slice().sort((a, b) => Number(a) - Number(b)).map(m => `${m}月`).join('・');
    },
  };
}
```

- [ ] **Step 2: Replace sidebar HTML**

Replace `<p>筛选面板（即将添加）</p>` in the `<aside class="sidebar">` with:

```html
<div class="filter-panel">
  <div class="filter-header">
    <span class="filter-title">筛选条件</span>
    <button class="reset-btn" @click="resetFilters()">重置</button>
  </div>

  <!-- Region -->
  <div class="filter-group">
    <label class="filter-label">📍 地区</label>
    <select x-model="filterRegion" @change="onRegionChange()" class="filter-select">
      <option value="">全部地区</option>
      <template x-for="region in regions" :key="region">
        <option :value="region" x-text="region"></option>
      </template>
    </select>
  </div>

  <!-- Prefecture (cascades) -->
  <div class="filter-group" x-show="filterRegion !== ''">
    <label class="filter-label">🏙️ 都道府県</label>
    <select x-model="filterPrefecture" class="filter-select">
      <option value="">全部</option>
      <template x-for="pref in prefectures" :key="pref">
        <option :value="pref" x-text="pref"></option>
      </template>
    </select>
  </div>

  <!-- Tuition dual range slider -->
  <div class="filter-group">
    <label class="filter-label">💰 年学费</label>
    <div class="range-display">
      <span x-text="formatTuition(tuitionMin)"></span>
      <span> ～ </span>
      <span x-text="formatTuition(tuitionMax)"></span>
    </div>
    <div class="dual-range">
      <input type="range" class="range-min"
        :min="TUITION_FLOOR" :max="TUITION_CEIL" step="50000"
        x-model.number="tuitionMin"
        @input="if(tuitionMin > tuitionMax) tuitionMax = tuitionMin">
      <input type="range" class="range-max"
        :min="TUITION_FLOOR" :max="TUITION_CEIL" step="50000"
        x-model.number="tuitionMax"
        @input="if(tuitionMax < tuitionMin) tuitionMin = tuitionMax">
    </div>
  </div>

  <!-- Teachers min slider -->
  <div class="filter-group">
    <label class="filter-label">👨‍🏫 专任教师（最少）</label>
    <div class="range-display">
      <span x-text="teachersMin > 0 ? `${teachersMin} 名以上` : '不限'"></span>
    </div>
    <input type="range" class="filter-range"
      min="0" :max="TEACHERS_MAX" step="1"
      x-model.number="teachersMin">
  </div>

  <!-- Keyword tags -->
  <div class="filter-group">
    <label class="filter-label">🏷️ 关键词</label>
    <div class="tag-group">
      <template x-for="tag in ALL_TAGS.filter(t => t.type === 'goal')" :key="tag.key">
        <button class="tag-chip goal"
          :class="{ active: isTagActive(tag.key) }"
          @click="toggleTag(tag.key)"
          x-text="tag.label">
        </button>
      </template>
    </div>
    <div class="tag-group" style="margin-top: 6px;">
      <template x-for="tag in ALL_TAGS.filter(t => t.type === 'service')" :key="tag.key">
        <button class="tag-chip service"
          :class="{ active: isTagActive(tag.key) }"
          @click="toggleTag(tag.key)"
          x-text="tag.label">
        </button>
      </template>
    </div>
  </div>
</div>
```

- [ ] **Step 3: Verify in browser**

Open `school-search.html`. Expected:
- Sidebar shows all filters
- Region dropdown lists 6 regions
- Prefecture dropdown appears only after selecting a region
- Tuition display updates when sliders move
- Tag chips toggle active state on click
- Reset button clears all selections

- [ ] **Step 4: Commit**

```bash
git add school-search.html
git commit -m "feat: add filter panel with region, tuition slider, teachers, and keyword tags"
```

---

## Task 5: Card template

**Files:**
- Modify: `school-search.html` — card HTML template (added as a `<template>` used in Task 6)

Add this `<template id="school-card-tpl">` inside `<body>` (outside the layout, as a reusable snippet). In practice with Alpine.js `x-for`, this is inlined directly in the results section in Task 6. Write it here as the definitive card structure:

- [ ] **Step 1: Define card HTML (will be placed inline in x-for in Task 6)**

The card structure is:

```html
<div class="school-card" :class="{ 'no-tuition': school.tuition_min === null }">
  <div class="card-top">
    <div class="card-name" x-text="school.name"></div>
    <div class="card-location">
      📍 <span x-text="school.prefecture"></span>
      <span x-text="school.city !== school.prefecture ? school.city.replace(school.prefecture, '') : ''"></span>
    </div>
  </div>

  <div class="card-stats">
    <span class="stat">
      👥 招生上限
      <strong x-text="school.capacity ? school.capacity + '名' : '未公开'"></strong>
    </span>
    <span class="stat">
      👨‍🏫 专任教师
      <strong x-text="school.full_time_teachers ? school.full_time_teachers + '名' : '未公开'"></strong>
    </span>
    <span class="stat">
      📅 入学月
      <strong x-text="formatMonths(school.start_months)"></strong>
    </span>
  </div>

  <div class="card-tuition">
    <template x-if="school.tuition_min !== null">
      <span>
        💰 年学费
        <strong x-text="`${formatTuition(school.tuition_min)} ～ ${formatTuition(school.tuition_max)}`"></strong>
        <span class="tuition-note">（含报名费・入学金）</span>
      </span>
    </template>
    <template x-if="school.tuition_min === null">
      <span class="no-tuition-badge">学费未公开</span>
    </template>
  </div>

  <div class="card-tags" x-show="school.tags.length > 0">
    <template x-for="tag in school.tags" :key="tag.key">
      <span class="tag-chip-display" :class="tag.type" x-text="tag.label"></span>
    </template>
  </div>

  <div class="card-footer">
    <span class="data-source">数据来源：日本語教育振興協会</span>
    <div class="card-links">
      <a :href="school.nisshinkyo_url"
         target="_blank" rel="noopener noreferrer"
         class="btn btn-secondary">
        📋 查看日振协资料
      </a>
      <template x-if="school.website">
        <a :href="school.website"
           target="_blank" rel="noopener noreferrer"
           class="btn btn-primary">
          🌐 前往学校官网 →
        </a>
      </template>
      <template x-if="!school.website">
        <span class="no-website">官网未登录</span>
      </template>
    </div>
  </div>
</div>
```

(This will be placed inside `x-for` in Task 6 — do not add it standalone yet.)

---

## Task 6: Results section

**Files:**
- Modify: `school-search.html` — replace `<main class="results">` content

- [ ] **Step 1: Replace results main content**

Replace `<p x-text="..."></p>` inside `<main class="results">` with:

```html
<!-- Sort bar -->
<div class="sort-bar">
  <span class="result-summary" x-text="`共 ${totalCount} 所学校`"></span>
  <div class="sort-control">
    <label>排序：</label>
    <select x-model="sortBy" class="sort-select">
      <option value="default">综合（按地区）</option>
      <option value="tuition_asc">学费从低到高</option>
      <option value="tuition_desc">学费从高到低</option>
      <option value="capacity_desc">招生人数从多到少</option>
    </select>
  </div>
</div>

<!-- Primary results -->
<div class="card-list">
  <template x-for="school in primaryResults" :key="school.id">
    <!-- PASTE CARD HTML FROM TASK 5 HERE -->
    <div class="school-card" :class="{ 'no-tuition': school.tuition_min === null }">
      <div class="card-top">
        <div class="card-name" x-text="school.name"></div>
        <div class="card-location">
          📍 <span x-text="school.prefecture"></span>
          <span x-text="school.city !== school.prefecture ? school.city.replace(school.prefecture, '') : ''"></span>
        </div>
      </div>
      <div class="card-stats">
        <span class="stat">👥 招生上限 <strong x-text="school.capacity ? school.capacity + '名' : '未公开'"></strong></span>
        <span class="stat">👨‍🏫 专任教师 <strong x-text="school.full_time_teachers ? school.full_time_teachers + '名' : '未公开'"></strong></span>
        <span class="stat">📅 入学月 <strong x-text="formatMonths(school.start_months)"></strong></span>
      </div>
      <div class="card-tuition">
        <template x-if="school.tuition_min !== null">
          <span>💰 年学费 <strong x-text="`${formatTuition(school.tuition_min)} ～ ${formatTuition(school.tuition_max)}`"></strong> <span class="tuition-note">（含报名费・入学金）</span></span>
        </template>
        <template x-if="school.tuition_min === null">
          <span class="no-tuition-badge">学费未公开</span>
        </template>
      </div>
      <div class="card-tags" x-show="school.tags.length > 0">
        <template x-for="tag in school.tags" :key="tag.key">
          <span class="tag-chip-display" :class="tag.type" x-text="tag.label"></span>
        </template>
      </div>
      <div class="card-footer">
        <span class="data-source">数据来源：日本語教育振興協会</span>
        <div class="card-links">
          <a :href="school.nisshinkyo_url" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">📋 查看日振协资料</a>
          <template x-if="school.website">
            <a :href="school.website" target="_blank" rel="noopener noreferrer" class="btn btn-primary">🌐 前往学校官网 →</a>
          </template>
          <template x-if="!school.website">
            <span class="no-website">官网未登录</span>
          </template>
        </div>
      </div>
    </div>
  </template>
</div>

<!-- Tuition-unknown section -->
<template x-if="unknownResults.length > 0">
  <div class="unknown-section">
    <div class="unknown-header">
      其他学校（学费未公开）：<span x-text="unknownResults.length"></span> 所
    </div>
    <div class="card-list">
      <template x-for="school in unknownResults" :key="school.id">
        <div class="school-card no-tuition">
          <div class="card-top">
            <div class="card-name" x-text="school.name"></div>
            <div class="card-location">📍 <span x-text="school.prefecture"></span></div>
          </div>
          <div class="card-stats">
            <span class="stat">👥 招生上限 <strong x-text="school.capacity ? school.capacity + '名' : '未公开'"></strong></span>
            <span class="stat">👨‍🏫 专任教师 <strong x-text="school.full_time_teachers ? school.full_time_teachers + '名' : '未公开'"></strong></span>
            <span class="stat">📅 入学月 <strong x-text="formatMonths(school.start_months)"></strong></span>
          </div>
          <div class="card-tuition">
            <span class="no-tuition-badge">学费未公开</span>
          </div>
          <div class="card-tags" x-show="school.tags.length > 0">
            <template x-for="tag in school.tags" :key="tag.key">
              <span class="tag-chip-display" :class="tag.type" x-text="tag.label"></span>
            </template>
          </div>
          <div class="card-footer">
            <span class="data-source">数据来源：日本語教育振興協会</span>
            <div class="card-links">
              <a :href="school.nisshinkyo_url" target="_blank" rel="noopener noreferrer" class="btn btn-secondary">📋 查看日振协资料</a>
              <template x-if="school.website">
                <a :href="school.website" target="_blank" rel="noopener noreferrer" class="btn btn-primary">🌐 前往学校官网 →</a>
              </template>
              <template x-if="!school.website">
                <span class="no-website">官网未登录</span>
              </template>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<!-- Empty state -->
<template x-if="primaryResults.length === 0 && unknownResults.length === 0">
  <div class="empty-state">
    <p>没有符合条件的学校，请调整筛选条件。</p>
    <button @click="resetFilters()" class="reset-btn-lg">清除所有筛选</button>
  </div>
</template>
```

- [ ] **Step 2: Verify in browser**

Open `school-search.html`. Expected:
- 95 primary cards visible on load
- 8 tuition-unknown cards in the "其他学校" section below
- Sort dropdown reorders cards
- Selecting a region reduces the card count
- All filter combinations work without JS errors

- [ ] **Step 3: Commit**

```bash
git add school-search.html
git commit -m "feat: add results section with cards, unknown-tuition separation, empty state"
```

---

## Task 7: CSS — layout and card styling

**Files:**
- Modify: `school-search.html` — `<style>` block

- [ ] **Step 1: Add complete CSS to the `<style>` block**

Replace the empty `<style>` block with:

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --accent: #c0392b;
  --accent-light: #f8f0f0;
  --goal-bg: #ebf3ff;
  --goal-color: #1a6cc8;
  --service-bg: #eafaf1;
  --service-color: #1a7a40;
  --card-border: #e0e0e0;
  --card-shadow: 0 1px 4px rgba(0,0,0,0.08);
  --sidebar-width: 260px;
  --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
}

body { font-family: var(--font); font-size: 14px; color: #333; background: #f5f5f5; }

/* Header */
.page-header {
  background: var(--accent);
  color: white;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.page-header h1 { font-size: 18px; font-weight: 700; }
.result-count { font-size: 13px; opacity: 0.9; }

/* Layout */
.layout {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  gap: 0;
  align-items: flex-start;
}

/* Sidebar */
.sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
  background: white;
  border-right: 1px solid var(--card-border);
  min-height: calc(100vh - 50px);
  position: sticky;
  top: 0;
  max-height: 100vh;
  overflow-y: auto;
}

.filter-panel { padding: 16px; }
.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.filter-title { font-weight: 700; font-size: 14px; }
.reset-btn {
  font-size: 12px;
  color: var(--accent);
  background: none;
  border: 1px solid var(--accent);
  border-radius: 4px;
  padding: 2px 8px;
  cursor: pointer;
}
.reset-btn:hover { background: var(--accent-light); }

.filter-group { margin-bottom: 18px; }
.filter-label { display: block; font-size: 12px; font-weight: 600; color: #555; margin-bottom: 6px; }
.filter-select {
  width: 100%;
  padding: 7px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 13px;
  background: white;
}

/* Dual range slider */
.range-display { font-size: 13px; color: #333; margin-bottom: 6px; }
.dual-range { position: relative; height: 28px; }
.dual-range input[type=range] {
  position: absolute;
  width: 100%;
  pointer-events: none;
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  height: 4px;
  top: 50%;
  transform: translateY(-50%);
}
.dual-range input[type=range]::-webkit-slider-thumb {
  pointer-events: all;
  -webkit-appearance: none;
  width: 18px; height: 18px;
  border-radius: 50%;
  background: var(--accent);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}
.dual-range input[type=range]::-webkit-slider-runnable-track {
  background: #ddd;
  height: 4px;
  border-radius: 2px;
}
.filter-range { width: 100%; -webkit-appearance: none; appearance: none; height: 4px; background: #ddd; border-radius: 2px; outline: none; cursor: pointer; }
.filter-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px; height: 18px;
  border-radius: 50%;
  background: var(--accent);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

/* Tag chips (filter panel) */
.tag-group { display: flex; flex-wrap: wrap; gap: 5px; }
.tag-chip {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 12px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.15s;
}
.tag-chip.goal { background: var(--goal-bg); color: var(--goal-color); border-color: #c5d8f5; }
.tag-chip.service { background: var(--service-bg); color: var(--service-color); border-color: #b8e8cc; }
.tag-chip.goal.active { background: var(--goal-color); color: white; }
.tag-chip.service.active { background: var(--service-color); color: white; }

/* Main results */
.results {
  flex: 1;
  padding: 16px;
  min-width: 0;
}

.sort-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--accent);
}
.result-summary { font-weight: 600; font-size: 13px; }
.sort-control { display: flex; align-items: center; gap: 6px; font-size: 13px; }
.sort-select { padding: 4px 8px; border: 1px solid #ccc; border-radius: 4px; font-size: 13px; }

/* Cards */
.card-list { display: flex; flex-direction: column; gap: 10px; }

.school-card {
  background: white;
  border: 1px solid var(--card-border);
  border-radius: 8px;
  padding: 14px 16px;
  box-shadow: var(--card-shadow);
}
.school-card.no-tuition { background: #fafafa; }

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}
.card-name {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.card-location { font-size: 12px; color: #666; white-space: nowrap; margin-left: 12px; flex-shrink: 0; }

.card-stats {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 13px;
  color: #555;
  margin-bottom: 6px;
}
.stat strong { color: #222; }

.card-tuition {
  font-size: 13px;
  color: #555;
  margin-bottom: 8px;
}
.card-tuition strong { color: #222; font-size: 14px; }
.tuition-note { font-size: 11px; color: #888; }
.no-tuition-badge {
  display: inline-block;
  background: #f0f0f0;
  color: #888;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
}

.card-tags { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; }
.tag-chip-display {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
}
.tag-chip-display.goal { background: var(--goal-bg); color: var(--goal-color); }
.tag-chip-display.service { background: var(--service-bg); color: var(--service-color); }

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}
.data-source { font-size: 11px; color: #999; }
.card-links { display: flex; gap: 8px; flex-wrap: wrap; }

.btn {
  font-size: 12px;
  padding: 5px 12px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 600;
  white-space: nowrap;
  display: inline-block;
}
.btn-secondary { background: white; color: #555; border: 1px solid #ccc; }
.btn-secondary:hover { background: #f5f5f5; }
.btn-primary { background: var(--accent); color: white; border: 1px solid var(--accent); }
.btn-primary:hover { background: #a93226; }
.no-website { font-size: 11px; color: #bbb; }

/* Unknown section */
.unknown-section { margin-top: 24px; }
.unknown-header {
  font-size: 13px;
  font-weight: 600;
  color: #888;
  padding: 8px 0;
  border-top: 1px dashed #ccc;
  margin-bottom: 10px;
}

/* Empty state */
.empty-state { text-align: center; padding: 60px 20px; color: #888; }
.empty-state p { font-size: 15px; margin-bottom: 16px; }
.reset-btn-lg {
  padding: 8px 20px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

/* Mobile filter toggle (hidden on desktop) */
.mobile-filter-toggle { display: none; }
```

- [ ] **Step 2: Verify in browser**

Open `school-search.html`. Expected:
- Two-column layout with red header
- Cards have white background, subtle shadow, red action button
- Goal tags appear in blue, service tags in green
- "查看日振协资料" and "前往学校官网 →" buttons visible on each card

- [ ] **Step 3: Commit**

```bash
git add school-search.html
git commit -m "feat: add full CSS layout, card styling, filter panel styles"
```

---

## Task 8: Responsive CSS and mobile filter toggle

**Files:**
- Modify: `school-search.html` — add to `<style>` block + mobile toggle button to HTML

- [ ] **Step 1: Add responsive CSS after the existing styles (inside `<style>`)**

```css
/* Tablet: 600–900px */
@media (max-width: 900px) {
  .layout { flex-direction: column; }
  .sidebar {
    width: 100%;
    position: static;
    max-height: none;
    border-right: none;
    border-bottom: 1px solid var(--card-border);
  }
  .filter-panel { padding: 12px 16px; }
}

/* Mobile: <600px */
@media (max-width: 600px) {
  .sidebar { display: none; }
  .sidebar.open { display: block; }
  .mobile-filter-toggle {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    background: white;
    border-bottom: 1px solid var(--card-border);
    font-size: 14px;
    cursor: pointer;
    border: none;
    width: 100%;
  }
  .results { padding: 10px; }
  .card-stats { gap: 8px; }
  .sort-bar { flex-direction: column; align-items: flex-start; gap: 6px; }
}
```

- [ ] **Step 2: Add mobile filter toggle button to HTML**

Add this immediately before `<div class="layout">`:

```html
<button class="mobile-filter-toggle"
  @click="$refs.sidebar.classList.toggle('open')">
  <span>筛选条件</span>
  <span>▼</span>
</button>
```

Add `x-ref="sidebar"` to the `<aside class="sidebar">` element:

```html
<aside class="sidebar" x-ref="sidebar">
```

- [ ] **Step 3: Verify responsiveness**

Open DevTools, switch to 375px width (iPhone). Expected:
- Sidebar is hidden, "筛选条件 ▼" button appears at top
- Clicking button reveals sidebar
- Cards are full-width with no overflow

- [ ] **Step 4: Commit**

```bash
git add school-search.html
git commit -m "feat: responsive layout — tablet filter bar, mobile filter toggle"
```

---

## Task 9: Edge cases and final polish

**Files:**
- Modify: `school-search.html`

- [ ] **Step 1: Normalize half-width katakana in nationality display**

In the `schoolSearch()` function, add a helper inside `init()` that normalizes katakana in nationality country names. Add after `this.schools = SCHOOLS.map(...)`:

```javascript
// Normalize half-width katakana to full-width in nationality display
const hwToFw = str => str.replace(/[｡-ﾟ]/g, c =>
  String.fromCharCode(c.charCodeAt(0) - 0xFF61 + 0x30A1));
this.schools = this.schools.map(s => ({
  ...s,
  nationalities: (s.nationalities || []).map(n => ({
    ...n,
    country: hwToFw(n.country)
  }))
}));
```

- [ ] **Step 2: Verify katakana normalization**

Open browser console, run:
```javascript
document.querySelector('[x-data]').__x.$data.schools
  .find(s => s.nationalities.some(n => /[｡-ﾟ]/.test(n.country)))
```

Expected: `undefined` (no half-width katakana remains).

- [ ] **Step 3: Add final meta tags for WordPress embedding**

In `<head>`, ensure these exist:
```html
<meta name="robots" content="noindex">
<meta name="referrer" content="no-referrer-when-downgrade">
```

The `noindex` prevents this data-heavy page from being indexed by search engines separately from the WordPress page that embeds it.

- [ ] **Step 4: Final browser smoke test**

Open `school-search.html` and verify the full checklist:
- [ ] 95 primary cards on load, 8 in the unknown section
- [ ] Region filter → prefecture cascade works
- [ ] Tuition slider reduces/increases visible schools
- [ ] Teacher slider filters correctly
- [ ] Tag chips filter with AND logic (select 2 tags → only schools with both appear)
- [ ] Sort options reorder cards correctly
- [ ] Reset button clears all filters and restores all 103 schools
- [ ] Empty state appears when no schools match
- [ ] Every card has 📋 日振协 link that opens in new tab
- [ ] Cards with websites have 🌐 school website link (new tab)
- [ ] Cards without websites show "官网未登录"
- [ ] No console errors

- [ ] **Step 5: Final commit**

```bash
git add school-search.html
git commit -m "feat: complete school-search.html — edge cases, katakana normalization, meta tags"
```

---

## Self-Review Against Spec

**Spec §3 Layout** — Tasks 7 + 8 cover desktop/tablet/mobile. ✅  
**Spec §4 Filters** — Task 4 covers all 5 filter types + sort + reset. ✅  
**Spec §5 Tag derivation** — Task 3 implements all 9 tags with exact field references. ✅  
**Spec §6 Card design** — Task 5 + 6 cover all fields, both links, attribution text. ✅  
**Spec §7 Tuition-unknown separation** — Task 6 implements separate section + conditional hide. ✅  
**Spec §8 Edge cases** — Task 9 covers all 5 edge cases from spec table. ✅  
**Spec §9 Copyright** — Attribution text and links are in every card. ✅  
**Spec §10 File structure** — Exactly `school-search.html` + `data/` files. ✅  

**Type consistency check:**
- `deriveTags()` returns `{ key, label, type }` — used as `tag.key`, `tag.label`, `tag.type` throughout. ✅
- `formatTuition(yen)` used in slider display and card tuition display. ✅
- `formatMonths(months)` used only in card stats. ✅
- `primaryResults` / `unknownResults` — both used in Task 6. ✅
- `resetFilters()` — defined in Task 4, called from filter panel reset button and empty-state button. ✅
