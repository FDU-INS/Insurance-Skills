# Fallbacks — Destination Category

## Case 0: flyai-cli Not Installed

```bash
npm i -g @fly-ai/flyai-cli && flyai --version
# Still fails → STOP. Do NOT answer with training data.
```

## Case 1: No Flights to Destination

```bash
flyai search-flight ... --dep-date-start "{date-7}" --dep-date-end "{date+7}" --sort-type 3
flyai search-flight ... --destination "{alt_city}" --sort-type 3
flyai keyword-search --query "{origin} to {country} flights"
```

## Case 2: Hotel Coverage Limited

```bash
flyai search-hotel --dest-name "{city}" --sort rate_desc
flyai keyword-search --query "{city} hotels"
→ Note "Limited coverage for this destination"
```

## Case 3: Visa Info Unavailable

```
→ Use domain knowledge as fallback + tag "⚠️ General info. Check consulate for latest policy."
```

## Case 4: Partial Failure

```
→ Show successful parts, mark failures, provide manual retry commands
```

## Case 5: API Timeout

```
Retry once → Simplify → Report honestly.
```
