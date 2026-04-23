---
name: generate-newsletter-insurance
description: Generate an insurance-specific newsletter for Anchor Point Insurance Co. (brand=LIFEINSUR)
---

## Purpose
Generates a branded newsletter for Anchor Point Insurance Co. (brand=LIFEINSUR). This is a specialization of the generate-newsletter skill, pre-configured for the insurance vertical — it fetches life insurance and financial planning news, uses the Anchor Point brand palette (warm charcoal #44403E, terracotta #AD7C59, warm beige #FCF9F6), and omits property listings (which are CRE-11TRUST only).

## Inputs
- **date** (optional): Edition date as YYYY-MM-DD. Default: today.
- **dry-run** (optional): Generate content but do NOT push to Strapi. Useful for previewing.
- **news-query** (optional): Override the default NewsAPI query. Default: `LIFEINSUR_NEWSAPI_QUERY` env var or `"life insurance financial planning south florida"`.

## Steps
1. Call `lib/newsletter/generate-insurance.ts::generateInsuranceNewsletter(options?)` to orchestrate
2. **Load LIFEINSUR brand config** — palette, sender email (from `brand-config` in Strapi or hardcoded defaults), display name "Anchor Point Insurance Co."
3. **Fetch news** — `fetchNews(query)` hits NewsAPI for 5 latest articles matching insurance/financial planning topics
4. **Generate AI content** — `generateAiContent(null, news)` sends news to Groq (no properties for LIFEINSUR). Returns market overview and news summaries.
5. **Build HTML** — `buildHtml()` assembles responsive email-safe HTML with Anchor Point brand colors and insurance-specific sections
6. **Build Strapi payload** — `buildStrapiPayload()` with brand=`LIFEINSUR`, slug includes timestamp for uniqueness
7. **Push to Strapi** — `strapiPost('/api/newsletters', data)` creates a draft newsletter (skipped in dry-run mode)
8. Log execution via `lib/board/index.ts::logActivity()`

## Output
```
Brand: LIFEINSUR (Anchor Point Insurance Co.)
News articles fetched: 5
AI content generated: market_overview (342 words), 5 news summaries
HTML length: 12,847 chars
Strapi draft created: documentId=abc123-def456
```

## CLI Usage
```bash
# Generate insurance newsletter for today
optimal generate-newsletter-insurance

# Specific date
optimal generate-newsletter-insurance --date 2026-03-01

# Preview without pushing to Strapi
optimal generate-newsletter-insurance --dry-run

# Custom news query
optimal generate-newsletter-insurance --news-query "florida insurance market rates"
```

## Environment
Requires: `GROQ_API_KEY`, `NEWSAPI_KEY`, `STRAPI_URL`, `STRAPI_API_TOKEN`
Optional: `GROQ_MODEL` (default: llama-3.3-70b-versatile), `LIFEINSUR_NEWSAPI_QUERY`

## Gotchas
- **No properties**: Unlike CRE-11TRUST, LIFEINSUR newsletters do not include property listings. The `--excel` parameter is not available.
- **Slug uniqueness**: Slugs include a timestamp (YYYYMMDDTHHMMSS) to avoid conflicts on same-day reruns.
- **Brand palette**: Primary #44403E (warm charcoal), Accent #AD7C59 (terracotta), BG #FCF9F6 (warm beige).
- **Preview site**: Published newsletters render at https://newsletter.op-hub.com/lifeinsur

## Status
Implementation status: Not yet implemented. Spec only. Lib function `lib/newsletter/generate-insurance.ts` to be ported from `generate-newsletter-lifeinsur.py` in the newsletter-automation repo.
