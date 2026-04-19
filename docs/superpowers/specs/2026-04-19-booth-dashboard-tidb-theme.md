# Booth Dashboard — TiDB Theme Redesign

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle `booth_dashboard/static/style.css` to apply the TiDB brand color palette, Inter + JetBrains Mono typography, and solollm design-token architecture — with zero HTML changes.

**Architecture:** Single CSS file replacement. All existing class names, layout rules, and interactive behavior are preserved exactly. Only color values, font declarations, and border-radius/shadow values change. No JavaScript changes. No HTML changes.

**Tech Stack:** Vanilla CSS custom properties, Google Fonts (Inter 400/500/600/700/800, JetBrains Mono 400/500/700)

---

## Design tokens

```css
/* Backgrounds */
--bg:       #060d1a
--panel:    #0d1629
--panel-2:  #142038
--panel-3:  #1c2d4a

/* Text */
--fg:       #e2e8f4
--muted:    #8a99b8
--dim:      #5a6a8a

/* TiDB accent (red-orange) */
--accent:   #e05a2b
--accent-2: #ff7040

/* Semantic SQL type colors */
--sql-vector: #3b9eff
--sql-fts:    #f59e0b
--sql-hybrid: #10b981

/* Borders */
--border:        #1e2e48
--border-accent: rgba(224, 90, 43, 0.25)

/* Radius */
--radius: 12px

/* Typography */
--font-sans: 'Inter', system-ui, sans-serif
--font-mono: 'JetBrains Mono', ui-monospace, monospace
```

---

## Component restyling map

### Hero
- Background: `linear-gradient(135deg, #0a1628 0%, #060d1a 100%)`
- `.hero-headline`: Inter 800, 44px, letter-spacing -0.02em, `--fg`
- `.hero-tagline`: Inter 500, `--accent`
- `.hero-hook`: border-left 4px `--accent`, background `rgba(224,90,43,0.08)`, border `rgba(224,90,43,0.2)`

### Customer proof strip
- Background: `--panel`, border-bottom: `--border`
- `.proof-name`: `--fg`; `.proof-stat`: `--muted`; `.proof-divider`: `--border`

### Tab bar
- Background: `--panel`, border-bottom: `--border`
- `.tab`: color `--muted`, border `--border`
- `.tab.active`: color `--fg`, border-bottom 2px `--accent`, background `--panel-2`

### SQL cards
- `.sql-card` background: `--panel-2`, border: `--border`
- `.sql-badge-v`: background `rgba(59,158,255,0.15)`, color `--sql-vector`
- `.sql-badge-f`: background `rgba(245,158,11,0.15)`, color `--sql-fts`
- `.sql-badge-h`: background `rgba(16,185,129,0.15)`, color `--sql-hybrid`
- `.sql-block`: font-family `--font-mono`, background `--panel-3`
- `.sql-meta-time` / `.sql-meta-rows`: `--muted`

### Panel sections (panel-hero, panel-title, panel-sub)
- `.panel-title`: Inter 700, 22px, `--fg`, letter-spacing -0.02em
- `.panel-sub`: Inter 400, `--muted`
- `.panel-footer.ok`: background `rgba(16,185,129,0.08)`, border `rgba(16,185,129,0.25)`, color `#10b981`

### Cards (duty-card, failure-mode-card, scenario-card, why-tidb-card, pain-card)
- Background: `--panel`, border: `--border`, radius: `--radius`
- Hover: background `--panel-2`, border-color `--border-accent`
- Icon/number accents: `--accent`

### Stat strip / stat cards
- `.stat-strip` background: `--panel`, border: `--border`
- `.stat-card` background: `--panel-2`
- `.stat-value`: Inter 700, `--fg`
- `.stat-label`: font-family `--font-mono`, `--dim`, uppercase, letter-spacing 0.1em

### Scale ladder
- `.scale-rung`: border-left 3px `--border`; `.highlight-rung`: border-left-color `--accent`
- `.rung-fill`: background `--accent`
- `.rung-count`: Inter 800, `--fg`

### Scale proof tiles (Manus, Pinterest, Dify)
- Background: `--panel-2`, border: `--border`
- `.spt-stat`: Inter 800, 40px, `--fg`
- `.spt-customer`: `--accent`, font-family `--font-mono`

### Outcome strips
- Background: `--panel`, border-top: `--border`
- `.outcome-icon`: kept as emoji
- `.outcome-text`: `--muted`
- `.outcome-divider`: `--border`

### Results / recall chips
- `.recall-chip`: background `--panel-2`, border `--border`
- `.recall-chip.active`: border-color `--accent`, background `rgba(224,90,43,0.08)`
- `.chip-q`: `--fg`; `.chip-hint`: `--muted`, font-family `--font-mono`, smaller

### Chat pane
- `.chat-pane` background: `--panel`
- `.chat-messages` background: `--panel-2`
- `.chat-input`: background `--panel-3`, border `--border`, color `--fg`
- `.chat-send`: background `--accent`, color white
- `.memory-pane`: background `--panel`, border-left `--border`

### Split (before/after)
- `.before-col` boxes: background `--panel-2`, border `--border`
- `.after-col` `.tidb-cluster`: background `--panel-2`, border `--accent` 2px
- `.plane` backgrounds: tinted with `--panel-3`
- Labels: `--accent` for "after", `--muted` for "before"

### Fleet context strip / fleet-band
- Background: `--panel`, borders: `--border`
- `.fci-stat`: Inter 800, `--accent`

### Failure modes grid
- `.failure-mode-card`: background `--panel`, border `--border`
- `.failure-icon`: emoji, kept
- `.failure-signal`: font-family `--font-mono`, `--dim`, font-size 12px

### Domain pills
- Background: `--panel-2`, border: `--border`, color: `--muted`

---

## What does NOT change
- All class names
- All layout rules (flexbox, grid, dimensions, padding)
- All z-index / position / overflow rules
- All responsive breakpoints
- All animation and transition timing
- All JavaScript
- All HTML

---

## Out of scope
- Nav / footer (single-page booth view, none needed)
- Content edits
- Structural HTML changes
- Any JavaScript behavior changes
