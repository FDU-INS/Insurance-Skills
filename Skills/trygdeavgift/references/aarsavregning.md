# Årsavregning (Annual Reconciliation)

## Overview

Årsavregning is the annual reconciliation process that compares preliminary (forskudd)
avgift paid during the year with the final calculated avgift based on actual income.

## Process Flow

```
┌─────────────────────┐
│ Skattehendelse      │  Kafka from Skatteetaten
│ received            │  (skatteoppgjør ferdig)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Automatisk opprett  │
│ årsavregning        │
│ behandling          │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Saksbehandler       │
│ vurderer grunnlag   │
│ og fastsetter avgift│
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Fatt vedtak         │
│ IVERKSETT_VEDTAK_   │
│ AARSAVREGNING       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Send årsavregnings- │
│ faktura (+ or -)    │
└─────────────────────┘
```

## Data Model

### Årsavregning Entity
Location: `domain/src/main/kotlin/.../avgift/Årsavregning.kt`

```kotlin
@Entity
@Table(name = "aarsavregning")
class Årsavregning(
    @Id var id: Long,
    var år: Int,
    var beregnetAvgiftBeløp: BigDecimal?,
    var harTrygdeavgiftFraAvgiftssystemet: Boolean?,
    var trygdeavgiftFraAvgiftssystemet: BigDecimal?,
    var manueltAvgiftBeløp: BigDecimal?,
    var endeligAvgiftValg: EndeligAvgiftValg?,
    var tidligereBehandlingsresultatId: Long?,
    // ...
)
```

### EndeligAvgiftValg
```kotlin
enum class EndeligAvgiftValg {
    BEREGNET,           // Use calculated amount
    MANUELT,            // Use manually entered amount
    FRA_AVGIFTSSYSTEMET // Use legacy amount from avgiftssystemet
}
```

## Service Layer

### ÅrsavregningService
Location: `service/src/main/kotlin/.../avgift/aarsavregning/ÅrsavregningService.kt`

Key methods:
- `opprettÅrsavregning()` - Create new årsavregning
- `hentTidligereTrygdeavgiftsgrunnlag()` - Get previous grunnlag
- `hentNyttTrygdeavgiftsgrunnlag()` - Get new grunnlag from income
- `replikerMedlemskapsperioder()` - Copy periods for årsavregning

### SkattehendelserConsumer
Location: `service/src/main/kotlin/.../avgift/aarsavregning/SkattehendelserConsumer.kt`

Listens for Kafka messages about completed skatteoppgjør:
- Creates skattehendelse record
- Triggers årsavregning process

## Grunnlag Innhenting (Basis Retrieval)

### Scenarios

| Scenario | Tidligere grunnlag | Endelig trygdeavgift |
|----------|-------------------|---------------------|
| Ingen tidligere årsavregning | From siste vedtak | From siste vedtak + ny inntekt |
| Tidligere årsavregning, ingen ny vurdering | From tidligere årsavregning | From tidligere årsavregning |
| Tidligere årsavregning med ny vurdering (likt medlemskap) | From tidligere årsavregning | From tidligere årsavregning |
| Tidligere årsavregning med ny vurdering (ulikt medlemskap) | From tidligere årsavregning | From ny vurdering (tom trygdeavgift) |

### Logic Flow
```kotlin
fun hentGjeldendeBehandlingsresultaterForÅrsavregning(
    fagsak: Fagsak,
    år: Int
): GjeldendeBehandlingsresultaterForÅrsavregning {
    // Find siste årsavregning for året
    // Find siste vedtak etter eventuell årsavregning
    // Compare medlemskapsperioder
    // Return appropriate grunnlag
}
```

## Saksflyt

### IVERKSETT_VEDTAK_AARSAVREGNING
Flow definition:
```
SEND_FAKTURA_AARSAVREGNING →
VARSLE_PENSJONSOPPTJENING →
AVSLUTT_SAK_OG_BEHANDLING →
SEND_MELDING_OM_VEDTAK
```

### SEND_FAKTURA_AARSAVREGNING Step
Location: `saksflyt/src/main/kotlin/.../steg/arsavregning/SendFakturaÅrsavregning.kt`

Calculates:
```kotlin
tilFakturering = endeligAvgift - tidligereAvgift - trygdeavgiftFraAvgiftssystemet
```

Where:
- `endeligAvgift`: Final calculated avgift for the year
- `tidligereAvgift`: Previously invoiced (forskudd)
- `trygdeavgiftFraAvgiftssystemet`: Amount from legacy system (transition period)

## Totalbeløp Beregning

### TotalbeløpBeregner
Location: `service/src/main/kotlin/.../avgift/aarsavregning/totalbeloep/TotalbeløpBeregner.kt`

Calculates total avgift for a year:
- Sums all trygdeavgiftsperioder for the year
- Applies 25% rule if applicable
- Handles partial year periods

### AntallMdBeregner
Location: `service/src/main/kotlin/.../avgift/aarsavregning/totalbeloep/AntallMdBeregner.kt`

Calculates number of months:
- Handles period spanning year boundaries
- Pro-rata for partial months

## Ikke-Skattepliktige Årsavregning

### Special Handling
Location: `service/src/main/kotlin/.../avgift/aarsavregning/ikkeskattepliktig/`

For members not required to file Norwegian tax return:
- Different trigger mechanism (batch job)
- Different grunnlag retrieval
- May require manual income entry

### Components
- `ÅrsavregningIkkeSkattepliktigeFinner`: Finds eligible cases
- `ÅrsavregningIkkeSkattepliktigeProsessGenerator`: Creates processes
- `ÅrsavregningIkkeSkattepliktigeController`: Admin API

## Debugging

### Find Årsavregning Status
```sql
SELECT aa.*, b.status, b.type, f.saksnummer
FROM aarsavregning aa
JOIN behandlingsresultat br ON aa.behandlingsresultat_id = br.id
JOIN behandling b ON br.behandling_id = b.id
JOIN fagsak f ON b.fagsak_id = f.id
WHERE f.saksnummer = :saksnummer
ORDER BY aa.aar DESC;
```

### Check Skattehendelse
```sql
SELECT * FROM skattehendelse
WHERE fnr = :fnr
AND inntekts_aar = :year;
```

### Verify Grunnlag
```sql
-- Tidligere grunnlag
SELECT t.*, mp.id as mp_id
FROM trygdeavgiftsperiode t
JOIN medlemskapsperiode mp ON t.grunnlag_medlemskapsperiode_id = mp.id
JOIN behandlingsresultat br ON mp.behandlingsresultat_id = br.id
WHERE br.id = (
    SELECT aa.tidligere_behandlingsresultat_id
    FROM aarsavregning aa WHERE aa.id = :aarsavregningId
);

-- Endelig grunnlag
SELECT t.*, mp.id as mp_id
FROM trygdeavgiftsperiode t
JOIN medlemskapsperiode mp ON t.grunnlag_medlemskapsperiode_id = mp.id
JOIN behandlingsresultat br ON mp.behandlingsresultat_id = br.id
WHERE br.id = (
    SELECT aa.behandlingsresultat_id
    FROM aarsavregning aa WHERE aa.id = :aarsavregningId
);
```

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Årsavregning not triggered | Skattehendelse not received | Check Kafka, verify person has avgift |
| Wrong grunnlag | Complex history | Verify behandling chain manually |
| Double årsavregning | Multiple triggers | Check for duplicate skattehendelser |
| Missing tidligere beløp | Avgiftssystemet data | Set harTrygdeavgiftFraAvgiftssystemet |

## Related Confluence Pages

- [Årsavregningen](https://confluence.adeo.no/spaces/TEESSI/pages/514480537)
- [Årsavregning - manuell støtte i flyt](https://confluence.adeo.no/spaces/TEESSI/pages/704517663)
- [Automatisert årsavregningen](https://confluence.adeo.no/spaces/TEESSI/pages/603364839)
- [Akseptansekriteria - trygdeavgift og fakturering](https://confluence.adeo.no/spaces/TEESSI/pages/720918767)
