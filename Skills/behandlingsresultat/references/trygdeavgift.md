# Trygdeavgift (Social Insurance Charges)

Trygdeavgift represents social insurance charges associated with membership or law choice periods.

## Overview

Trygdeavgiftsperiode entities are attached to:
- `Lovvalgsperiode` (for EU/EEA law choice cases)
- `Medlemskapsperiode` (for FTRL membership cases)
- `HelseutgiftDekkesPeriode` (for EEA pensioner health coverage)

## Trygdeavgiftsperiode Entity

```kotlin
@Entity
class Trygdeavgiftsperiode {
    var fom: LocalDate
    var tom: LocalDate?
    var skattepliktig: Skatteplikttype?  // Tax liability type
    var avgiftsgruppe: Avgiftsgrupper?   // Charge group
    var beregnetAvgift: BigDecimal?      // Calculated charge amount
}
```

## Getting Charge Periods

### From Behandlingsresultat
```kotlin
// All charge periods (from all period types)
val allePerioder = resultat.trygdeavgiftsperioder

// Only from charge-liable periods
val avgiftspliktige = resultat.finnAvgiftspliktigPerioder()
```

### Check Overlap with Tax Year
```kotlin
// Check if any approved period overlaps with year
val overlapper = resultat.harInnvilgetAvgiftspliktigPeriodeSomOverlapperMedÅr(2024)
```

### Calculate Period Bounds
```kotlin
val fom = resultat.utledAvgiftspliktigperioderFom()
val tom = resultat.utledAvgiftspliktigperioderTom()
val skattepliktype = resultat.utledSkatteplikttype()
```

## AvgiftspliktigPeriode Interface

Both `Lovvalgsperiode` and `Medlemskapsperiode` implement this interface:

```kotlin
interface AvgiftspliktigPeriode {
    val trygdeavgiftsperioder: Set<Trygdeavgiftsperiode>
    val innvilgelsesresultat: InnvilgelsesResultat

    fun getFom(): LocalDate
    fun getTom(): LocalDate?
}
```

## Clearing Charge Periods

```kotlin
// Clear from behandlingsresultat
resultat.clearTrygdeavgiftsperioder()

// Clear from health expense period
resultat.clearTrygdeavgiftsperioderHelseutgiftPeriode()
```

## Business Logic

### Which Periods are Charge-Liable?

The logic in `finnAvgiftspliktigPerioder()` depends on case type and result:

```kotlin
fun finnAvgiftspliktigPerioder(): List<AvgiftspliktigPeriode> {
    return when {
        // Lovvalg case with approved period
        fagsak.erLovvalg() && erInnvilgelse() ->
            lovvalgsperioder.filter { it.erInnvilget() }

        // Membership case
        !fagsak.erLovvalg() ->
            medlemskapsperioder.filter { it.erInnvilget() }

        else -> emptyList()
    }
}
```

### Integration with Fakturering

Charge periods are used by `faktureringskomponenten` to create invoices:

```kotlin
// In IVERKSETT_VEDTAK saga
OPPRETT_FAKTURASERIE  // Creates invoice series from trygdeavgiftsperioder
```

## Skatteplikttype

Tax liability types (from kodeverk):
- `SKATTEPLIKTIG_I_NORGE` - Tax liable in Norway
- `IKKE_SKATTEPLIKTIG_I_NORGE` - Not tax liable in Norway
- `BEGRENSET_SKATTEPLIKTIG` - Limited tax liability

## Avgiftsgrupper

Charge groups determine the rate applied:
- Different rates for different situations
- Based on income, coverage type, etc.

## Debugging

### Find charge periods for a behandling
```sql
-- Via lovvalgsperiode
SELECT tp.*
FROM trygdeavgiftsperiode tp
JOIN lovvalgsperiode lp ON lp.id = tp.lovvalgsperiode_id
WHERE lp.behandlingsresultat_id = :behandlingId;

-- Via medlemskapsperiode
SELECT tp.*
FROM trygdeavgiftsperiode tp
JOIN medlemskapsperiode mp ON mp.id = tp.medlemskapsperiode_id
WHERE mp.behandlingsresultat_id = :behandlingId;
```

### Find cases with charge periods in specific year
```sql
SELECT DISTINCT f.saksnummer, br.type
FROM fagsak f
JOIN behandling b ON b.fagsak_saksnummer = f.saksnummer
JOIN behandlingsresultat br ON br.id = b.id
JOIN lovvalgsperiode lp ON lp.behandlingsresultat_id = br.id
JOIN trygdeavgiftsperiode tp ON tp.lovvalgsperiode_id = lp.id
WHERE EXTRACT(YEAR FROM tp.fom) <= 2024
AND (tp.tom IS NULL OR EXTRACT(YEAR FROM tp.tom) >= 2024);
```

### Find missing charge periods
```sql
-- Lovvalgsperioder with INNVILGET but no charge periods
SELECT lp.id, lp.fom, lp.tom, lp.innvilgelsesresultat
FROM lovvalgsperiode lp
LEFT JOIN trygdeavgiftsperiode tp ON tp.lovvalgsperiode_id = lp.id
WHERE lp.innvilgelsesresultat = 'INNVILGET'
AND tp.id IS NULL;
```

## Related Saga Steps

| Step | Description |
|------|-------------|
| `OPPRETT_FAKTURASERIE` | Creates invoice from charge periods |
| `SEND_FAKTURA_AARSAVREGNING` | Annual reconciliation invoice |
| `RESET_ÅPNE_ÅRSAVREGNINGER` | Resets open reconciliations |
