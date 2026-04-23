# FTRL Debugging Guide

## Common Investigation Queries

### Find All Medlemskapsperioder for Person
```sql
SELECT mp.*, f.saksnummer, b.status as beh_status
FROM medlemskapsperiode mp
JOIN behandlingsresultat br ON mp.behandlingsresultat_id = br.id
JOIN behandling b ON br.behandling_id = b.id
JOIN fagsak f ON b.fagsak_id = f.id
WHERE f.bruker_aktor_id = :aktorId
AND f.type = 'FTRL'
ORDER BY mp.fom DESC;
```

### Check Bestemmelse with Full Details
```sql
SELECT mp.id, mp.fom, mp.tom,
       mp.bestemmelse, mp.trygdedekning,
       mp.medlemskapstype, mp.arbeidsland,
       mp.innvilgelsesresultat, mp.medl_periode_id
FROM medlemskapsperiode mp
WHERE mp.behandlingsresultat_id = :behandlingsresultatId;
```

### Find Skatteforhold for Medlemskapsperiode
```sql
SELECT sf.*, mp.id as mp_id
FROM skatteforhold_til_norge sf
WHERE sf.medlemskapsperiode_id = :medlemskapsperiodeId;
```

### Find Inntektsperioder
```sql
SELECT ip.*, mp.id as mp_id
FROM inntektsperiode ip
WHERE ip.medlemskapsperiode_id = :medlemskapsperiodeId;
```

### Check Trygdeavgiftsperioder
```sql
SELECT t.*, mp.id as mp_id
FROM trygdeavgiftsperiode t
WHERE t.grunnlag_medlemskapsperiode_id = :medlemskapsperiodeId;
```

### Find FTRL Vedtak Process
```sql
SELECT pi.id, pi.type, pi.status, pi.sist_utforte_steg,
       pi.registrert_dato, pi.endret_dato
FROM prosessinstans pi
WHERE pi.behandling_id = :behandlingId
AND pi.type = 'IVERKSETT_VEDTAK_FTRL'
ORDER BY pi.registrert_dato DESC;
```

### Check MEDL Registration Status
```sql
SELECT mp.id, mp.fom, mp.tom, mp.bestemmelse,
       mp.medl_periode_id, mp.innvilgelsesresultat
FROM medlemskapsperiode mp
JOIN behandlingsresultat br ON mp.behandlingsresultat_id = br.id
JOIN behandling b ON br.behandling_id = b.id
WHERE b.fagsak_id = :fagsakId
AND mp.innvilgelsesresultat = 'INNVILGET';
```

## Common Issues and Solutions

### Issue: Wrong Bestemmelse Selected

**Symptoms:**
- Incorrect paragraph in vedtak letter
- Validation errors on bestemmelse

**Investigation:**
1. Check behandlingstema matches bestemmelse type
2. Verify vilkårsvurdering results
3. Check avklarte fakta for relevant answers

```sql
-- Check avklarte fakta
SELECT af.type, af.verdi, af.registrert_dato
FROM avklarte_fakta af
WHERE af.behandling_id = :behandlingId
ORDER BY af.registrert_dato DESC;

-- Check vilkårsresultat
SELECT vr.vilkaar, vr.oppfylt, vr.begrunnelse
FROM vilkaarsresultat vr
WHERE vr.behandling_id = :behandlingId;
```

### Issue: Invalid Trygdedekning

**Symptoms:**
- Validation error when selecting dekning
- Cannot save medlemskapsperiode

**Investigation:**
1. Check LovligeKombinasjonerTrygdedekningBestemmelse
2. Verify bestemmelse allows the dekning
3. Check if behandlingstema restricts options

```kotlin
// Valid combinations example:
// §2-8.1.d (pensjonist) -> only HELSEDEL
// §2-8.1.a (utsendt) -> FULL_DEKNING
```

### Issue: Period Overlap

**Symptoms:**
- Cannot create new medlemskapsperiode
- Validation error about overlapping

**Investigation:**
1. Check existing periods for same fagsak
2. Look for periods with same fom/tom
3. Verify previous behandling avsluttet

```sql
-- Find overlapping periods
SELECT mp1.id, mp1.fom, mp1.tom, mp1.bestemmelse,
       b1.id as beh_id, b1.status
FROM medlemskapsperiode mp1
JOIN behandlingsresultat br1 ON mp1.behandlingsresultat_id = br1.id
JOIN behandling b1 ON br1.behandling_id = b1.id
WHERE b1.fagsak_id = :fagsakId
AND mp1.innvilgelsesresultat = 'INNVILGET'
ORDER BY mp1.fom;
```

### Issue: Missing MEDL Registration

**Symptoms:**
- medl_periode_id is NULL
- Period not visible in MEDL

**Investigation:**
1. Check prosessinstans for LAGRE_MEDLEMSKAPSPERIODE_MEDL
2. Verify MEDL consumer logs
3. Check if all required fields set

```sql
-- Check vedtak process status
SELECT pi.sist_utforte_steg, pi.status, pi.feilmelding
FROM prosessinstans pi
WHERE pi.behandling_id = :behandlingId
AND pi.type = 'IVERKSETT_VEDTAK_FTRL';

-- Check medlemskapsperiode completeness
SELECT mp.id, mp.bestemmelse, mp.trygdedekning,
       mp.medlemskapstype, mp.innvilgelsesresultat, mp.fom, mp.tom
FROM medlemskapsperiode mp
WHERE mp.behandlingsresultat_id = :brId;
```

### Issue: Avgift Not Calculated

**Symptoms:**
- No trygdeavgiftsperiode created
- Faktura not generated

**Investigation:**
1. Check skatteforhold set on medlemskapsperiode
2. Verify inntektsperioder exist
3. Check TrygdeavgiftsberegningService logs

```sql
-- Check grunnlag for avgift
SELECT mp.id,
       (SELECT COUNT(*) FROM skatteforhold_til_norge s
        WHERE s.medlemskapsperiode_id = mp.id) as skatteforhold_count,
       (SELECT COUNT(*) FROM inntektsperiode i
        WHERE i.medlemskapsperiode_id = mp.id) as inntekt_count,
       (SELECT COUNT(*) FROM trygdeavgiftsperiode t
        WHERE t.grunnlag_medlemskapsperiode_id = mp.id) as avgift_count
FROM medlemskapsperiode mp
WHERE mp.behandlingsresultat_id = :brId;
```

### Issue: Ny Vurdering Problems

**Symptoms:**
- Cannot update existing period
- Opphør not working correctly

**Investigation:**
1. Check previous behandling is AVSLUTTET
2. Verify kopiert perioder logic
3. Check erstattMedlemskapsperioder service

```sql
-- Find all behandlinger for sak
SELECT b.id, b.type, b.status, b.registrert_dato
FROM behandling b
WHERE b.fagsak_id = :fagsakId
ORDER BY b.registrert_dato;

-- Check ny vurdering bakgrunn
SELECT af.verdi as bakgrunn
FROM avklarte_fakta af
WHERE af.behandling_id = :behandlingId
AND af.type = 'NY_VURDERING_BAKGRUNN';
```

## Log Patterns to Search

### FTRL Processing
```
grep "MedlemskapsperiodeService" app.log
grep "FtrlVedtakService" app.log
```

### Bestemmelse Selection
```
grep "FtrlBestemmelser" app.log
grep "VilkårForBestemmelse" app.log
```

### MEDL Integration
```
grep "LagreMedlemskapsperiodeMedl" app.log
grep "MedlConsumer" app.log
```

### Avgift Issues
```
grep "TrygdeavgiftsberegningService" app.log
grep "OpprettFakturaserie" app.log
```

## Key Classes for Debugging

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `MedlemskapsperiodeService` | Period management | `opprettMedlemskapsperiode()` |
| `FtrlBestemmelser` | Valid bestemmelser | Configuration class |
| `VilkårForBestemmelse*` | Vilkår evaluation | `hentVilkår()` |
| `FtrlVedtakService` | FTRL vedtak | `fattVedtak()` |
| `LagreMedlemskapsperiodeMedl` | MEDL registration | `utfør()` |
| `OpprettForslagMedlemskapsperiodeService` | Period suggestion | `opprettForslag()` |
| `UtledMedlemskapsperioder` | Period derivation | `utled()` |

## Validation Rules

### Bestemmelse-Dekning Combinations
```kotlin
// Examples of valid combinations:
§2-8.1.a → FULL_DEKNING
§2-8.1.b → FULL_DEKNING
§2-8.1.c → FULL_DEKNING
§2-8.1.d → HELSEDEL only (pensjonist)
§2-8.2   → FULL_DEKNING
§2-1     → FULL_DEKNING
§2-13    → UTEN_DEKNING (unntak)
```

### Period Validation
- fom must be before or equal to tom
- tom can be null (åpen slutt)
- No overlap with other innvilget periods on same fagsak
- Bestemmelse must match behandlingstema
