# Playbooks — car-rental-search

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: City Rental

**Trigger:** "rent a car in {city}"

```bash
flyai keyword-search --query "租车 {city}"
```

**Output emphasis:** Car rental in city.

---

## Playbook B: Airport Rental

**Trigger:** "car rental at airport"

```bash
flyai keyword-search --query "机场租车 {city}"
```

**Output emphasis:** Airport pickup car rental.

---

## Playbook C: SUV Rental

**Trigger:** "rent SUV"

```bash
flyai keyword-search --query "SUV租车 {city}"
```

**Output emphasis:** SUV for road trips.

---

