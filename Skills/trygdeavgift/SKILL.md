---
name: trygdeavgift
description: |
  Expert knowledge of trygdeavgift (social insurance charge) domain in melosys-api.
  Use when: (1) Understanding avgift calculation for different member types,
  (2) Debugging årsavregning (annual reconciliation) processing,
  (3) Understanding fakturering flow to OEBS/faktureringskomponenten,
  (4) Investigating avgiftssatser and calculation rules per year,
  (5) Understanding skatteforhold and inntektskilder,
  (6) Debugging trygdeavgiftsperiode generation and storage,
  (7) Understanding the 25% rule and minstebeløp calculations.
---

# Trygdeavgift Domain

Trygdeavgift (social insurance charge) is the domain handling calculation, collection, and reconciliation
of social security contributions for members of Norwegian folketrygden. This includes advance
invoicing (forskuddsfakturering), annual reconciliation (årsavregning), and integration with OEBS.

## Quick Reference

### Domain Model Hierarchy

```
Behandlingsresultat
├── trygdeavgiftType: Trygdeavgift_typer
├── trygdeavgiftFritekst: String?
├── medlemskapsperioder: List<Medlemskapsperiode>
│   └── trygdeavgiftsperioder: Set<Trygdeavgiftsperiode>
├── lovvalgsperioder: List<Lovvalgsperiode>
│   └── trygdeavgiftsperioder: Set<Trygdeavgiftsperiode>
├── helseutgiftDekkesPeriode: HelseutgiftDekkesPeriode?
│   └── trygdeavgiftsperioder: Set<Trygdeavgiftsperiode>
├── årsavregning: Årsavregning?
└── fakturaserieReferanse: String?

Trygdeavgiftsperiode
├── id: Long
├── periodeFra: LocalDate
├── periodeTil: LocalDate?
├── trygdeavgiftsbeløpMd: Penger
├── trygdesats: BigDecimal
├── grunnlagMedlemskapsperiode: Medlemskapsperiode?
├── grunnlagLovvalgsPeriode: Lovvalgsperiode?
├── grunnlagHelseutgiftDekkesPeriode: HelseutgiftDekkesPeriode?
├── grunnlagInntekstperiode: Inntektsperiode
└── grunnlagSkatteforholdTilNorge: SkatteforholdTilNorge

Årsavregning
├── id: Long
├── år: Int
├── beregnetAvgiftBeløp: BigDecimal?
├── harTrygdeavgiftFraAvgiftssystemet: Boolean?
├── trygdeavgiftFraAvgiftssystemet: BigDecimal?
├── manueltAvgiftBeløp: BigDecimal?
├── endeligAvgiftValg: EndeligAvgiftValg?
├── tidligereBehandlingsresultatId: Long?
└── behandlingsresultat: Behandlingsresultat
```

### Key Enums

| Enum | Values | Description |
|------|--------|-------------|
| **Trygdeavgift_typer** | ORDINÆR, FORENKLET_SKATT, EØS_PENSJONIST, etc. | Type of avgift calculation |
| **Avgiftsdekning** | HELSEDEL_UTEN_SYKEPENGER, HELSEDEL_MED_SYKEPENGER, PENSJONSDEL_UTEN_YRKESSKADETRYGD, PENSJONSDEL_MED_YRKESSKADETRYGD | Coverage affecting calculation |
| **Skatteplikttyyper** | BEGRENSET, FULL | Tax liability type |
| **EndeligAvgiftValg** | BEREGNET, MANUELT, FRA_AVGIFTSSYSTEMET | Source of final avgift |
| **Betalingstype** | FAKTURA, KONTONUMMER | Payment method choice |

### Avgift Calculation Flow

```
┌─────────────────────┐
│ Vedtaksfatting      │
│ (fattVedtak)        │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ TrygdeavgiftsService│
│ beregnOgLagre()     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐     ┌─────────────────────┐
│ melosys-trygdeavgift│────►│ Trygdeavgiftsperiode│
│ -beregning          │     │ created & stored    │
└─────────────────────┘     └─────────┬───────────┘
                                      │
                                      ▼
                            ┌─────────────────────┐
                            │ OPPRETT_FAKTURASERIE│
                            │ (saksflyt steg)     │
                            └─────────┬───────────┘
                                      │
                                      ▼
                            ┌─────────────────────┐
                            │ Fakturerings-       │
                            │ komponenten/OEBS    │
                            └─────────────────────┘
```

## Service Layer

### TrygdeavgiftsberegningService
Location: `service/src/main/kotlin/.../avgift/TrygdeavgiftsberegningService.kt`

Key operations:
- `beregnOgLagreTrygdeavgift()` - Calculate and persist avgift periods
- `lagNyeTrygeavgiftsperioder()` - Create new avgift periods
- `beregnTrygdeavgift()` - Call external beregning module
- `sjekkTrygdeavgiftSkalBetalesTilNav()` - Determine if NAV collects avgift

### TrygdeavgiftService
Location: `service/src/main/kotlin/.../avgift/TrygdeavgiftService.kt`

Key operations:
- `harFagsakBehandlingerMedTrygdeavgift()` - Check for avgift on case
- `harFakturerbarTrygdeavgift()` - Check if avgift should be invoiced
- `harTrygdeavgift()` - Check if behandling has avgift

### ÅrsavregningService
Location: `service/src/main/kotlin/.../avgift/aarsavregning/ÅrsavregningService.kt`

Key operations:
- `opprettÅrsavregning()` - Create annual reconciliation
- `hentTidligereTrygdeavgiftsgrunnlag()` - Get previous year's basis
- `hentNyttTrygdeavgiftsgrunnlag()` - Get new basis
- `hentGjeldendeBehandlingsresultaterForÅrsavregning()` - Get results for year

### TrygdeavgiftMottakerService
Location: `service/src/main/kotlin/.../avgift/TrygdeavgiftMottakerService.kt`

Key operations:
- `skalBetalesTilNav()` - Determine if avgift is collected by NAV
- `finnFakturamottaker()` - Find invoice recipient

## Saksflyt Integration

### Fakturering Steps

| ProsessSteg | Description |
|-------------|-------------|
| `OPPRETT_FAKTURASERIE` | Create invoice series in faktureringskomponenten |
| `KANSELLER_FAKTURASERIE` | Cancel existing invoice series |
| `OPPDATER_FAKTURAMOTTAKER` | Update invoice recipient |
| `SEND_FAKTURA_AARSAVREGNING` | Send annual reconciliation invoice |
| `BEREGN_OG_SEND_FAKTURA` | Calculate and send invoice (satsendring) |

### Vedtak Flow with Avgift

```
IVERKSETT_VEDTAK_FTRL:
  LAGRE_MEDLEMSKAPSPERIODE_MEDL →
  OPPRETT_FAKTURASERIE →          # Creates invoice in OEBS
  AVSLUTT_SAK_OG_BEHANDLING →
  SEND_MELDING_OM_VEDTAK →
  RESET_ÅPNE_ÅRSAVREGNINGER

IVERKSETT_VEDTAK_AARSAVREGNING:
  SEND_FAKTURA_AARSAVREGNING →    # Annual reconciliation invoice
  VARSLE_PENSJONSOPPTJENING →
  AVSLUTT_SAK_OG_BEHANDLING →
  SEND_MELDING_OM_VEDTAK
```

## Integration with External Systems

### Faktureringskomponenten
Location: `integrasjon/src/main/kotlin/.../faktureringskomponenten/`

- REST API integration for invoice management
- Creates fakturaserie with periods and amounts
- Handles kansellering of existing series
- Returns fakturaserieReferanse stored on Behandlingsresultat

### OEBS
- Faktureringskomponenten handles integration with OEBS
- OEBS manages actual billing and payment collection
- Manglende innbetaling events sent via Kafka

### Skatteetaten (Sigrun)
- Annual income data retrieved for årsavregning
- Skattehendelser processed via Kafka consumer
- Used for 25% rule calculations

## Debugging Queries

### Find Trygdeavgiftsperioder for Behandling
```sql
SELECT t.*, mp.id as medlemskap_id, lp.id as lovvalg_id
FROM trygdeavgiftsperiode t
LEFT JOIN medlemskapsperiode mp ON t.grunnlag_medlemskapsperiode_id = mp.id
LEFT JOIN lovvalgsperiode lp ON t.grunnlag_lovvalgsperiode_id = lp.id
WHERE mp.behandlingsresultat_id = :behandlingsresultatId
   OR lp.behandlingsresultat_id = :behandlingsresultatId;
```

### Check Fakturaserie Status
```sql
SELECT br.id, br.fakturaserie_referanse, b.status, f.saksnummer
FROM behandlingsresultat br
JOIN behandling b ON br.behandling_id = b.id
JOIN fagsak f ON b.fagsak_id = f.id
WHERE br.fakturaserie_referanse IS NOT NULL
AND f.saksnummer = :saksnummer;
```

### Find Årsavregning for Year
```sql
SELECT aa.*, br.id as behandlingsresultat_id, b.id as behandling_id
FROM aarsavregning aa
JOIN behandlingsresultat br ON aa.behandlingsresultat_id = br.id
JOIN behandling b ON br.behandling_id = b.id
WHERE aa.aar = :year
AND b.fagsak_id = :fagsakId;
```

### Check Manglende Innbetaling
```sql
SELECT pi.*, b.id as behandling_id, f.saksnummer
FROM prosessinstans pi
JOIN behandling b ON pi.behandling_id = b.id
JOIN fagsak f ON b.fagsak_id = f.id
WHERE pi.type = 'OPPRETT_NY_BEHANDLING_MANGLENDE_INNBETALING'
ORDER BY pi.registrert_dato DESC;
```

## Common Issues

| Issue | Symptoms | Investigation |
|-------|----------|---------------|
| Avgift not calculated | Missing trygdeavgiftsperioder | Check TrygdeavgiftsberegningService logs |
| Wrong avgift amount | Unexpected invoice amount | Verify satser, inntekt, dekning |
| Fakturaserie not created | No fakturaserieReferanse | Check OPPRETT_FAKTURASERIE step |
| Årsavregning missing | No reconciliation for year | Check skattehendelser received |
| Double invoicing | Multiple fakturaseriereferanser | Check prosessinstans for duplicate vedtak |
| 25% rule not applied | Avgift too high | Verify TotalbeløpBeregner logic |

## Calculation Rules

### Avgiftssatser (2024)
Rates are defined per year and depend on:
- Avgiftsdekning (helsedel/pensjonsdel, med/uten sykepenger)
- Skattepliktttype (begrenset/full)
- Member type (frivillig/pliktig, yrkesaktiv/pensjonist)

### 25% Rule
- Avgift cannot exceed 25% of total income
- Applies to voluntary members
- Implemented in `TotalbeløpBeregner`

### Minstebeløp
- Minimum amount threshold before invoicing
- Currently set per regulation

## Detailed Documentation

- **[Beregning](references/beregning.md)**: Calculation rules and formulas
- **[Fakturering](references/fakturering.md)**: OEBS integration and invoice flow
- **[Årsavregning](references/aarsavregning.md)**: Annual reconciliation process
- **[Debugging Guide](references/debugging.md)**: SQL queries and troubleshooting
