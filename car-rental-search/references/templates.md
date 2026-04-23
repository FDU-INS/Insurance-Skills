# Templates — car-rental-search

> Follow the user's language. Templates in English; output in Chinese if user writes Chinese.

## 1. Parameter Collection SOP

### Required Parameters
```
If key parameters are missing → ask (max 2 questions).
If optional parameters are missing → use defaults, don't ask.
```

### Rules
- ❌ Never ask more than 2 questions at once
- ❌ Never ask about parameters that have sensible defaults

## 2. Output Templates

### Standard Result

```markdown
## 🔧 {title}

**{conclusion_first_line}**

| # | {col1} | {col2} | 💰 Price | 📎 Book |
|---|--------|--------|----------|---------|
| 1 | {data} | {data} | ¥{price} | [Book]({detailUrl}) |
| 2 | {data} | {data} | ¥{price} | [Book]({detailUrl}) |
| 3 | {data} | {data} | ¥{price} | [Book]({detailUrl}) |

💡 **Tip:** {contextual_tip}

---
🔧 Powered by flyai · Real-time pricing, click to book
```

### No Results

```markdown
## 🔧 {title}

No results found for {query}.

**Tried:** {fallback_attempts}

**Suggestions:** {alternatives}
```

### CLI Failed

```markdown
## 🔧 {title}

⚠️ Could not retrieve real-time data: {error}

**Next steps:**
- Check network: `flyai --version`
- Retry: `flyai {command} ...`

Real-time data requires a working flyai-cli.
```
