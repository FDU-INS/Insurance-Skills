---
name: ftrl
description: |
  Expert knowledge of Folketrygdloven (National Insurance Act) processing in melosys-api.
  Use when: (1) Understanding FTRL bestemmelser (§2-5 to §2-13),
  (2) Debugging yrkesaktiv/ikke-yrkesaktiv/pensjonist processing flows,
  (3) Understanding trygdedekning options and combinations,
  (4) Investigating vilkår for each bestemmelse,
  (5) Understanding medlemskapsperiode generation logic,
  (6) Debugging frivillig vs pliktig membership determination.
---

# Folketrygdloven (FTRL) Domain

Folketrygdloven (National Insurance Act) Chapter 2 governs membership in the Norwegian social
insurance scheme for persons outside treaty/EU contexts. This domain handles §2-1 through §2-13,
managing pliktig (mandatory) and frivillig (voluntary) membership applications.

## Quick Reference

### Domain Model Hierarchy

```
Behandlingsresultat
├── medlemskapsperioder: List<Medlemskapsperiode>
│   ├── fom/tom: LocalDate
│   ├── bestemmelse: Medlemskapsbestemmelser
│   ├── medlemskapstype: Medlemskapstyper (PLIKTIG/FRIVILLIG)
│   ├── trygdedekning: Trygdedekning
│   ├── arbeidsland: String?
│   ├── innvilgelsesresultat: Innvilgelsesresultater
│   ├── skatteforholdTilNorge: Set<SkatteforholdTilNorge>
│   ├── inntektsperioder: Set<Inntektsperiode>
│   └── trygdeavgiftsperioder: Set<Trygdeavgiftsperiode>
└── trygdeavgiftType: Trygdeavgift_typer?
```

### FTRL Bestemmelser (Paragraphs)

| Paragraph | Type | Description |
|-----------|------|-------------|
| **§2-1** | Pliktig | Bosatt i Norge - grunnregel |
| **§2-2** | Pliktig | Arbeidstaker i Norge |
| **§2-5.a-g** | Pliktig | Offentlig ansatte (statsforvaltning, forsvaret, etc.) |
| **§2-5.h** | Pliktig | Student med lån/stipend |
| **§2-6** | Pliktig | Sjømenn på norskregistrerte skip |
| **§2-7.1** | Frivillig | Opphold i Norge (ikke bosatt) |
| **§2-7.4** | Frivillig | Familiemedlemmer §2-7 |
| **§2-7a** | Frivillig | Sjømenn bosatt i Norge, utenlandsk skip |
| **§2-8.1.a** | Frivillig | Utsendt arbeidstaker |
| **§2-8.1.b** | Frivillig | Student utenlands |
| **§2-8.1.c** | Frivillig | Offentlig oppdrag/stipend |
| **§2-8.1.d** | Frivillig | Pensjonist/uføretrygdet |
| **§2-8.2** | Frivillig | Andre yrkesaktive (rimelighetsvurdering) |
| **§2-8.4** | Frivillig | Familiemedlemmer §2-8 |
| **§2-13** | Unntak | Unntak fra medlemskap |

### Behandlingstema

| Tema | Description | Bestemmelser |
|------|-------------|--------------|
| **YRKESAKTIV** | Working persons | §2-1, §2-2, §2-5, §2-6, §2-7.1, §2-7a, §2-8.1.a, §2-8.2 |
| **IKKE_YRKESAKTIV** | Non-working persons | §2-1, §2-5.h, §2-7.1, §2-7.4, §2-8.1.b, §2-8.1.c, §2-8.4 |
| **PENSJONIST** | Pensioners/disabled | §2-8.1.d |

### Trygdedekning (Coverage)

| Code | Description | Use Case |
|------|-------------|----------|
| `FULL_DEKNING` | Full coverage in folketrygden | Standard for pliktig |
| `HELSEDEL` | Health coverage only | Pensjonister utenlands |
| `UTEN_DEKNING` | No coverage | Avslag/unntak |
| `FTRL_2_9_FØRSTE_LEDD_A_HELSE` | §2-9 health only | Special cases |

### Medlemskapstype

| Type | Description |
|------|-------------|
| `PLIKTIG` | Mandatory membership - automatic by law |
| `FRIVILLIG` | Voluntary membership - by application |

## Service Layer

### FtrlBestemmelser
Location: `service/src/main/kotlin/.../ftrl/bestemmelse/FtrlBestemmelser.kt`

Defines valid FTRL bestemmelser and their properties.

### YrkesaktivBestemmelser / IkkeYrkesaktivBestemmelser / PensjonistBestemmelser
Location: `service/src/main/kotlin/.../ftrl/bestemmelse/`

Separate files defining valid bestemmelser for each behandlingstema.

### MedlemskapsperiodeService
Location: `service/src/main/kotlin/.../ftrl/medlemskapsperiode/MedlemskapsperiodeService.kt`

Key operations:
- `hentMedlemskapsperioder()` - Get periods for behandling
- `opprettMedlemskapsperiode()` - Create new period
- `oppdaterMedlemskapsperiode()` - Update existing period
- `erstattMedlemskapsperioder()` - Replace periods (ny vurdering)

### OpprettForslagMedlemskapsperiodeService
Location: `service/src/main/kotlin/.../ftrl/medlemskapsperiode/OpprettForslagMedlemskapsperiodeService.kt`

Creates suggested membership periods based on søknadsperiode and rules.

### UtledMedlemskapsperioder
Location: `service/src/main/kotlin/.../ftrl/medlemskapsperiode/UtledMedlemskapsperioder.kt`

Logic for deriving membership periods from input data.

### GyldigeTrygdedekningerService
Location: `service/src/main/kotlin/.../ftrl/GyldigeTrygdedekningerService.kt`

Returns valid trygdedekning options for given context.

### LovligeKombinasjonerTrygdedekningBestemmelse
Location: `service/src/main/kotlin/.../ftrl/bestemmelse/LovligeKombinasjonerTrygdedekningBestemmelse.kt`

Defines valid combinations of trygdedekning and bestemmelse.

## Vilkår System

### Vilkår Structure
Location: `service/src/main/kotlin/.../ftrl/bestemmelse/vilkaar/`

```
VilkårForBestemmelse (interface)
├── VilkårForBestemmelseYrkesaktiv
├── VilkårForBestemmelseIkkeYrkesaktiv
└── VilkårForBestemmelsePensjonist
```

Each bestemmelse has associated vilkår (conditions) that must be evaluated.

### AvklarteFaktaForBestemmelse
Location: `service/src/main/kotlin/.../ftrl/bestemmelse/avklartefakta/`

Defines which avklarte fakta are required for each bestemmelse.

## Processing Flows

### Yrkesaktiv Flow (§2-8)
```
┌─────────────────────┐
│ Søknad mottas       │
│ (behandlingstema:   │
│  YRKESAKTIV)        │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Velg bestemmelse    │
│ (§2-8.1.a, §2-8.2)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Avklar vilkår       │
│ (arbeidsgiver,      │
│  arbeidsland, etc.) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Opprett medlemskaps-│
│ periode med avgift  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Fatt vedtak         │
│ IVERKSETT_VEDTAK_   │
│ FTRL                │
└─────────────────────┘
```

### Pensjonist Flow (§2-8.1.d)
```
┌─────────────────────┐
│ Søknad mottas       │
│ (behandlingstema:   │
│  PENSJONIST)        │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Bestemmelse:        │
│ §2-8.1.d automatisk │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Trygdedekning:      │
│ HELSEDEL            │
│ (kun helsedel)      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Betalingsvalg:      │
│ FAKTURA/KONTONUMMER │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Fatt vedtak         │
└─────────────────────┘
```

## Saksflyt Integration

### IVERKSETT_VEDTAK_FTRL
```
LAGRE_MEDLEMSKAPSPERIODE_MEDL →
OPPRETT_FAKTURASERIE →
AVSLUTT_SAK_OG_BEHANDLING →
SEND_MELDING_OM_VEDTAK →
RESET_ÅPNE_ÅRSAVREGNINGER
```

## Debugging Queries

### Find Medlemskapsperiode by Behandling
```sql
SELECT mp.*, br.id as br_id, b.status
FROM medlemskapsperiode mp
JOIN behandlingsresultat br ON mp.behandlingsresultat_id = br.id
JOIN behandling b ON br.behandling_id = b.id
WHERE b.id = :behandlingId;
```

### Check Bestemmelse and Dekning
```sql
SELECT mp.id, mp.fom, mp.tom,
       mp.bestemmelse, mp.trygdedekning,
       mp.medlemskapstype, mp.arbeidsland,
       mp.innvilgelsesresultat
FROM medlemskapsperiode mp
WHERE mp.behandlingsresultat_id = :behandlingsresultatId;
```

### Find FTRL Cases for Person
```sql
SELECT f.saksnummer, f.type, b.id, b.status, b.tema
FROM fagsak f
JOIN behandling b ON b.fagsak_id = f.id
WHERE f.bruker_aktor_id = :aktorId
AND f.type = 'FTRL'
ORDER BY b.registrert_dato DESC;
```

### Check MEDL Registration
```sql
SELECT mp.medl_periode_id, mp.bestemmelse, mp.fom, mp.tom
FROM medlemskapsperiode mp
WHERE mp.behandlingsresultat_id = :brId
AND mp.medl_periode_id IS NOT NULL;
```

## Common Issues

| Issue | Symptoms | Investigation |
|-------|----------|---------------|
| Wrong bestemmelse | Incorrect paragraph in vedtak | Check vilkårsvurdering flow |
| Invalid dekning | Validation error | Check LovligeKombinasjonerTrygdedekningBestemmelse |
| Period overlap | Cannot save medlemskapsperiode | Check existing periods for fagsak |
| Missing MEDL | medl_periode_id is NULL | Check LAGRE_MEDLEMSKAPSPERIODE_MEDL step |
| Avgift calculation fail | No trygdeavgiftsperiode | Verify skatteforhold and inntekt set |

## Bestemmelse Details

### §2-8 First Paragraph (Frivillig Yrkesaktiv)

**a) Utsendt arbeidstaker**
- Norwegian employer sends to work abroad
- Employer has substantial activity in Norway
- Previously subject to Norwegian legislation

**b) Student utenlands**
- Studying abroad with Norwegian loan/stipend
- Enrolled at recognized institution

**c) Offentlig oppdrag/stipend**
- Government assignment abroad
- Research stipend from Norwegian sources

**d) Pensjonist/uføretrygdet**
- Receiving pension from folketrygden
- Only helsedel coverage available

### §2-8 Second Paragraph
- Other workers where "særlige grunner" make it reasonable
- Discretionary evaluation (rimelighetsvurdering)

### §2-13 Unntak
- Exception from mandatory membership
- Used when person should not be member despite §2-1/§2-2

## Detailed Documentation

- **[Bestemmelser](references/bestemmelser.md)**: All FTRL paragraphs and conditions
- **[Trygdedekning](references/trygdedekning.md)**: Coverage types and combinations
- **[Flows](references/flows.md)**: Processing flows per arbeidssituasjon
- **[Debugging Guide](references/debugging.md)**: SQL queries and troubleshooting
