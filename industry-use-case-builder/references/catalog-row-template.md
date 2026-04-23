# Use Case Catalog Row Template

## Row format

Each row in the use case catalog table follows this exact format:

```
| <img src="assets/use-case-icons/{industry}/icon-{kebab-name}.png" alt="{Alt Text}" width="40"> | [{Use Case Title}]({industry}/{industry}-overview.md#{heading-anchor}) | {One-sentence description} | [!BADGE {Maturity}]{type={Type}} | [{Pattern Name}](/help/blueprints/use-case-patterns/{category}/{pattern-file}.md) |
```

### Row without icon (use when icon is not yet available)

```
| | [{Use Case Title}]({industry}/{industry}-overview.md#{heading-anchor}) | {One-sentence description} | [!BADGE {Maturity}]{type={Type}} | [{Pattern Name}](/help/blueprints/use-case-patterns/{category}/{pattern-file}.md) |
```

## Field reference

| Field | Format | Example |
| --- | --- | --- |
| industry | kebab-case directory name | retail, financial-services, travel-hospitality |
| kebab-name | kebab-case use case name for icon | abandoned-cart, lead-nurturing |
| Alt Text | Title case, short | Abandoned Cart, Lead Nurturing |
| heading-anchor | kebab-case of the ## heading in overview | abandoned-cart-email-recovery |
| Maturity + Type | Badge syntax | `[!BADGE Foundational]{type=Neutral}`, `[!BADGE Emerging]{type=Informative}`, `[!BADGE Advanced]{type=Caution}` |

## Industry tab markers in catalog

The catalog file uses this tab structure:

- `>[!TAB Retail]`
- `>[!TAB Automotive]`
- `>[!TAB Financial Services]`
- `>[!TAB Healthcare]`
- `>[!TAB Insurance]`
- `>[!TAB Media & Entertainment]`
- `>[!TAB Telecommunications]`
- `>[!TAB Travel & Hospitality]`
- `>[!TAB B2B]`

## Ordering within tabs

Rows are ordered by maturity level:

1. **Foundational** rows first (type=Neutral)
2. **Emerging** rows second (type=Informative)
3. **Advanced** rows last (type=Caution)

Within the same maturity level, add new rows at the end of that group.
