# McKinsey PPT Style Guide

## Design Philosophy

McKinsey & Company consulting style emphasizes clarity, professionalism, and conclusion-first communication. This guide documents the design principles extracted from client corporate reports.

## Color Scheme Extraction

Colors extracted from **四川分公司2026年车险规划报告**:

| Color      | Hex Code  | Usage                                  | Frequency      |
| ---------- | --------- | -------------------------------------- | -------------- |
| Deep Red   | `#a02724` | Primary color, core messages, key data | 60 occurrences |
| Bright Red | `#c00000` | Warnings, risk alerts                  | 12 occurrences |
| Black      | `#000000` | Titles, important text                 | 14 occurrences |
| White      | `#FFFFFF` | Background                             | 7 occurrences  |

**Typography:** Microsoft YaHei (微软雅黑) - 1016 occurrences
**Aspect Ratio:** 16:9 modern widescreen (13.333 x 7.5 inches)

## Core Design Principles

### 1. Conclusion-First Titles (So What?)

**Principle:** Every slide title must answer "So what?" for the executive audience.

❌ **Wrong (Descriptive):**

- "Profitability Analysis"
- "New Energy Vehicle Business Status"
- "Business Data"

✅ **Right (Conclusive):**

- "Profitability remains healthy with 83.9% combined ratio below industry benchmark"
- "NEV profitability is concerning: 108.5% loss ratio, 41.4pp higher than traditional vehicles"
- "Business scale expanded 5.9%, but cost control needs attention"

**Why:** McKinsey reports follow the "Pyramid Principle" - conclusions at the top enable decision-makers to grasp key information at a glance.

### 2. Minimalist Design + Generous White Space

**Principle:** Less is More

**McKinsey Style:**

- One core message per slide
- Generous white space (0.8 inch margins)
- No excessive decoration (no logo stacking, no fancy borders)
- Only a thin red line at top for brand identity

**Comparison with Traditional Style:**

| Element         | Traditional PPT           | McKinsey Style         |
| --------------- | ------------------------- | ---------------------- |
| Decorative bars | Thick color blocks (0.3") | Thin line (0.015")     |
| Logo            | Multiple locations        | Cover page only, small |
| Header/Footer   | Lengthy text              | Page number only       |
| Background      | Gradients/textures        | Pure white             |

### 3. Left-Aligned + Structured Layout

**Principle:** Professional business style

**Layout Specification:**

```
┌─────────────────────────────────┐
│ Top red line (0.015")            │
├─────────────────────────────────┤
│ Title (left-aligned, 24pt, conclusive) │
├──────────────┬──────────────────┤
│              │                  │
│ Left content │  Right content   │
│ • Point 1    │                  │
│ • Point 2    │   [Chart area]   │
│ • Point 3    │                  │
│              │                  │
├──────────────┴──────────────────┤
│ Bottom recommendation (italic, 12pt) │
│                    Page # (right) │
└─────────────────────────────────┘
```

**Contrast:**

- Traditional PPT: Center-aligned, symmetric layout
- McKinsey style: Left-aligned, left-right columns, clear visual flow

### 4. Professional Data Visualization

**Principle:** Let numbers speak, avoid decoration

**Large Number Display (McKinsey signature approach):**

```
        83.9%          ← 48pt, bold, red
    Combined Ratio    ← 14pt, gray caption

    • Loss Ratio: 71.3%    ← 14pt, bullet points
    • Expense Ratio: 12.6%
```

**Chart Standards:**

- Maximum 3 colors
- No 3D effects
- No shadows
- Clear data labels
- Clean axes

## Generated PPT Structure Comparison

### Original (Hua'an Insurance Style)

| Page | Title Example                                                | Style                          |
| ---- | ------------------------------------------------------------ | ------------------------------ |
| 1    | Hua'an Insurance Sichuan Branch Auto Insurance Weekly Report | Centered, blue-gold decoration |
| 2    | Executive Summary                                            | Emoji icons                    |
| 3    | Profitability: Combined Ratio 83.9% - Operating Well         | Mixed style                    |
| 4    | NEV Business: Premium Share 3.86%                            | Descriptive                    |
| 5    | Risk Management: Average Claims Frequency 20.1%              | Descriptive                    |

### McKinsey Version (Current)

| Page | Title Example                                                                               | Style                       |
| ---- | ------------------------------------------------------------------------------------------- | --------------------------- |
| 1    | Hua'an Insurance Sichuan Branch Auto Insurance Weekly Report                                | Left-aligned, thin red line |
| 2    | Weekly premium ¥770M, combined ratio 83.9% meets target                                     | **Conclusive**              |
| 3    | Profitability remains healthy, 83.9% combined ratio below industry benchmark                | **Conclusive**              |
| 4    | NEV profitability is concerning: 108.5% loss ratio, 41.4pp higher than traditional vehicles | **Conclusive**              |
| 5    | Risk control effective: 20.1% claims frequency within reasonable range                      | **Conclusive**              |
| 6    | Business scale expanded 5.9%, cost control needs attention                                  | **Conclusive** (WoW)        |

## Business Value of McKinsey Style

### 1. Decision Efficiency Improvement

**Traditional PPT:**

- Board members read page by page, extract conclusions themselves
- Average time per slide: 2-3 minutes
- Meeting duration: 30-45 minutes

**McKinsey Style:**

- Conclusions in titles, board members scan quickly
- Average time per slide: 30-60 seconds
- Meeting duration: 15-20 minutes

**Efficiency Gain:** **50% time savings**

### 2. Information Transmission Accuracy

**Title = Conclusion** → Avoids information misinterpretation

Traditional title: "NEV Business Analysis"

- Board asks: "So how is NEV doing?"
- Requires repeated explanation

McKinsey title: "NEV profitability is concerning: 108.5% loss ratio, 41.4pp higher than traditional vehicles"

- Board sees the problem in the title
- Directly discusses solutions

### 3. Professionalism and Authority

**McKinsey** = World's top consulting firm

- Using their style → Enhances professional image
- Suitable for: Board meetings, executive meetings, investor roadshows
- Conveys message: "Our analysis is professional and rigorous"

## Implementation Guide (Configuration)

To implement these design principles, please refer to the `config.json` file. The following mapping ensures the style is correctly applied:

### 1. Color Implementation

Set the color codes in `config.json` to match the **Deep Red** scheme:

```json
"PPT样式": {
  "风格预设": "mckinsey",
  "主色调": "#a02724",  // Deep Red
  "辅助色": "#000000",  // Black
  "预警色": "#c00000"   // Bright Red
}
```

### 2. Title Logic Implementation

Configure the **Smart Copywriting Rules** in `config.json` to generate conclusive titles automatically:

```json
"智能文案规则": {
  "综合成本率": [
    {
      "条件": "> 100",
      "标题模板": "盈利能力恶化警告：综合成本率突破 {value}%"
    }
  ]
}
```

> **Note**: For detailed configuration instructions, please refer to the `config-guide.md` document.

---

**Design Basis:** Client Sichuan Branch 2026 Auto Insurance Planning Report color scheme
**Design Style:** McKinsey & Company Consulting Style
