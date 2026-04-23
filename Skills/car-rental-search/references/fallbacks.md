# Fallbacks — Service Category

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli && flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: Service Not Found

```bash
flyai keyword-search --query "{alternative_phrasing}"
→ Use domain knowledge as fallback + tag "⚠️ Reference only"
```

## Case 2: Irrelevant Results

```
→ Refine query with more specific keywords
→ Inform user if service not available via flyai
```

## Case 3: Parameter Conflict

```bash
flyai keyword-search --query "{simplified query}"
```

## Case 4: API Timeout

```
Retry once → Simplify → Report honestly.
```
