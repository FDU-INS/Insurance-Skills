# Trygdeavgift Debugging Guide

## Common Investigation Queries

### Find All Trygdeavgiftsperioder for a Person
```sql
SELECT t.*, mp.periode_fra as mp_fra, mp.periode_til as mp_til,
       f.saksnummer, b.id as behandling_id, b.status
FROM trygdeavgiftsperiode t
JOIN medlemskapsperiode mp ON t.grunnlag_medlemskapsperiode_id = mp.id
JOIN behandlingsresultat br ON mp.behandlingsresultat_id = br.id
JOIN behandling b ON br.behandling_id = b.id
JOIN fagsak f ON b.fagsak_id = f.id
WHERE f.bruker_aktor_id = :aktorId
ORDER BY t.periode_fra DESC;
```

### Find Avgift with Skatteforhold Details
```sql
SELECT t.id, t.periode_fra, t.periode_til,
       t.trygdeavgift_beloep_mnd_verdi as mnd_beloep,
       t.trygdesats,
       s.skatteplikttype, s.skattepliktig_til_norge,
       i.avgiftspliktig_mnd_inntekt_verdi as inntekt,
       i.arbeidsgiversavgift_betales_til_skatt
FROM trygdeavgiftsperiode t
JOIN skatteforhold_til_norge s ON t.grunnlag_skatteforhold_id = s.id
JOIN inntektsperiode i ON t.grunnlag_inntektsperiode_id = i.id
WHERE t.id = :trygdeavgiftsperiodeId;
```

### Check Fakturaserie Status
```sql
SELECT br.fakturaserie_referanse, br.id as br_id,
       b.id as behandling_id, b.status as beh_status,
       f.saksnummer, f.betalingsvalg
FROM behandlingsresultat br
JOIN behandling b ON br.behandling_id = b.id
JOIN fagsak f ON b.fagsak_id = f.id
WHERE br.fakturaserie_referanse = :referanse;
```

### Find Årsavregning History
```sql
SELECT aa.id, aa.aar, aa.beregnet_avgift_belop,
       aa.manuelt_avgift_beloep, aa.endelig_avgift_valg,
       aa.har_trygdeavgift_fra_avgiftssystemet,
       aa.trygdeavgift_fra_avgiftssystemet,
       b.id as behandling_id, b.status, b.type
FROM aarsavregning aa
JOIN behandlingsresultat br ON aa.behandlingsresultat_id = br.id
JOIN behandling b ON br.behandling_id = b.id
JOIN fagsak f ON b.fagsak_id = f.id
WHERE f.saksnummer = :saksnummer
ORDER BY aa.aar DESC, b.registrert_dato DESC;
```

### Check Manglende Innbetaling Prosess
```sql
SELECT pi.id, pi.type, pi.status, pi.sist_utforte_steg,
       pi.data, pi.registrert_dato, pi.endret_dato
FROM prosessinstans pi
WHERE pi.type = 'OPPRETT_NY_BEHANDLING_MANGLENDE_INNBETALING'
AND pi.data LIKE '%"fakturaserieReferanse":":referanse"%'
ORDER BY pi.registrert_dato DESC;
```

### Find Skattehendelser
```sql
SELECT sh.id, sh.fnr, sh.skatteoppgjoer_dato, sh.inntekts_aar,
       sh.status, sh.registrert_dato
FROM skattehendelse sh
WHERE sh.fnr = :fnr
ORDER BY sh.registrert_dato DESC;
```

## Common Issues and Solutions

### Issue: Trygdeavgift Not Calculated

**Symptoms:**
- No trygdeavgiftsperioder on behandlingsresultat
- Fakturaseriereferanse is null

**Investigation:**
1. Check that behandlingsresultat has medlemskapsperioder or lovvalgsperioder
2. Verify skatteforhold and inntektsperioder are set
3. Check TrygdeavgiftsberegningService logs for errors
4. Verify melosys-trygdeavgift-beregning service is accessible

```sql
-- Check grunnlag exists
SELECT mp.id, mp.trygdedekning,
       (SELECT COUNT(*) FROM skatteforhold_til_norge s
        WHERE s.medlemskapsperiode_id = mp.id) as skatteforhold_count,
       (SELECT COUNT(*) FROM inntektsperiode i
        WHERE i.medlemskapsperiode_id = mp.id) as inntekt_count
FROM medlemskapsperiode mp
WHERE mp.behandlingsresultat_id = :behandlingsresultatId;
```

### Issue: Wrong Avgift Amount

**Symptoms:**
- Invoice amount doesn't match expected
- 25% rule not applied

**Investigation:**
1. Check satser for the year
2. Verify inntekt amounts
3. Check if 25% rule should apply
4. Verify dekning type

```sql
-- Calculate expected avgift
SELECT t.periode_fra, t.periode_til,
       i.avgiftspliktig_mnd_inntekt_verdi as inntekt,
       t.trygdesats,
       t.trygdeavgift_beloep_mnd_verdi as faktisk_beloep,
       (i.avgiftspliktig_mnd_inntekt_verdi * t.trygdesats / 100) as forventet_beloep
FROM trygdeavgiftsperiode t
JOIN inntektsperiode i ON t.grunnlag_inntektsperiode_id = i.id
WHERE t.grunnlag_medlemskapsperiode_id IN (
    SELECT id FROM medlemskapsperiode
    WHERE behandlingsresultat_id = :behandlingsresultatId
);
```

### Issue: Duplicate Invoicing

**Symptoms:**
- Multiple fakturaseriereferanser for same period
- Customer receives multiple invoices

**Investigation:**
1. Check for duplicate vedtak prosesser
2. Verify kansellering was processed
3. Check prosessinstans history

```sql
-- Find all fakturaserie for case
SELECT br.fakturaserie_referanse, b.id, b.type, b.status,
       b.registrert_dato, b.endret_dato
FROM behandlingsresultat br
JOIN behandling b ON br.behandling_id = b.id
WHERE b.fagsak_id = :fagsakId
AND br.fakturaserie_referanse IS NOT NULL
ORDER BY b.registrert_dato;
```

### Issue: Årsavregning Not Created

**Symptoms:**
- No årsavregning behandling for year
- Skattehendelse received but not processed

**Investigation:**
1. Check skattehendelse status
2. Verify fagsak has trygdeavgift
3. Check for active behandling blocking

```sql
-- Check if skattehendelse exists and status
SELECT sh.*, f.saksnummer
FROM skattehendelse sh
JOIN fagsak f ON sh.fagsak_id = f.id
WHERE f.saksnummer = :saksnummer
AND sh.inntekts_aar = :year;

-- Check for blocking active behandling
SELECT b.id, b.type, b.status
FROM behandling b
WHERE b.fagsak_id = :fagsakId
AND b.status NOT IN ('AVSLUTTET');
```

### Issue: OEBS Integration Failure

**Symptoms:**
- Fakturaserie created but no invoice
- FaktureringskomponentenConsumer errors

**Investigation:**
1. Check faktureringskomponenten logs
2. Verify fakturaserie payload
3. Check OEBS status via faktureringskomponenten API

```kotlin
// Check via FaktureringskomponentenConsumer
faktureringskomponentenConsumer.hentFakturaserie(referanse)
```

## Log Patterns to Search

### Calculation Errors
```
grep "TrygdeavgiftsberegningService" app.log | grep -i "error\|exception"
```

### Fakturering Issues
```
grep "FaktureringskomponentenConsumer" app.log | grep -i "error\|failed"
grep "OPPRETT_FAKTURASERIE" app.log
```

### Årsavregning Processing
```
grep "ÅrsavregningService" app.log
grep "SkattehendelserConsumer" app.log
```

## Key Classes for Debugging

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `TrygdeavgiftsberegningService` | Calculate avgift | `beregnOgLagreTrygdeavgift()` |
| `TrygdeavgiftService` | Query avgift state | `harFakturerbarTrygdeavgift()` |
| `ÅrsavregningService` | Annual reconciliation | `opprettÅrsavregning()` |
| `FaktureringskomponentenConsumer` | OEBS integration | `opprettFakturaserie()` |
| `ManglendeFakturabetalingConsumer` | Handle unpaid | `handleMessage()` |
| `SkattehendelserConsumer` | Tax events | `handleMessage()` |
